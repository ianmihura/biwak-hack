import json

from executors.SqlExecutor import SqlExecutor
from harmonic_client import HarmonicClient
from openai_client import OpenAIClient

file_path = "./harmonic_api_doc.txt"
with open(file_path, "r", encoding="utf-8") as file:
    harmonic_api_doc = file.read()


class BossExecutor:
    def __init__(self):
        self.sql_client = SqlExecutor()
        self.harmonic_client = HarmonicClient()

    async def execute_step_with_input(self, executor, query, dependencies):
        if dependencies:
            query = dependencies
        if executor == "SqlExecutor":
            return await self.sql_client.execute(query)
        elif executor == "HarmonicClient":
            # query is a dictionary, with keys: method, url, body
            return await self.harmonic_client.execute(query)
        else:
            raise ValueError(f"Unknown executor: {executor}")

    async def smart_generate_executions(self, question: str,
                                        flow_orchestrator: OpenAIClient, query_generator: OpenAIClient,
                                        harmonic_client: HarmonicClient):
        system_prompt = ("You are an orchestrator of a programme. You will be given a question and need to answer that."
                         "In order to answer it, you will be given some API docs,"
                         " and you need to find the logical steps to use relevant APIs in order to get the"
                         "results . Please return the results in an array of dictionaries. "
                         "each dictionaries should have the following 6 keys: step_number: (int),"
                         "step_description (string, describing what it is doing, and what data input is required, "
                         "use real value if value is available.),"
                         " rest_api_method (string, POST or GET), url (string), pre_condition (string, pre-conditions "
                         "for the step to be executed), dependencies (list of int, previous step numbers of dependencies."
                         " If nothing is required, return an empty list)."
                         " Return the results in an array of dictionaries, without explanations")
        user_prompt = f"Question: {question}. Harmonic API docs: {harmonic_api_doc}"
        inputs = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        steps = flow_orchestrator.query_chat(inputs)
        if steps:
            steps = json.loads(steps)
        steps_aggregated_res = {}
        res = None
        for step in steps:
            # we can validate each step using a validator
            print(f"step {step['step_number']} being executed: {step['step_description']}")
            results_from_dependency_steps = []
            if len(step["dependencies"]) > 0:
                results_from_dependency_steps = [steps_aggregated_res.get(pre) for pre in step["dependencies"]]
            apis_to_call = await self.openAI_code_generator(step["step_description"], step["pre_condition"],
                                                            results_from_dependency_steps or [], query_generator)
            if apis_to_call.startswith("Error!!!"):
                print("Error in generating APIs for ", step["step_number"], apis_to_call)
                break
            else:
                apis_to_call = json.loads(apis_to_call)
                print("apis to call", apis_to_call)
                res = await harmonic_client.execute(apis_to_call)
                steps_aggregated_res[step["step_number"]] = res
                print("results from step ", step["step_number"], str(res) if len(str(res)) < 1000 else str(res)[:1000])

        return res

    async def openAI_code_generator(self, task: str, pre_info: str, dependency_data: list[int], client: OpenAIClient):
        system_prompt = ("You are a helpful analyst. Your job is to provide a dictionary of data to help a programmer"
                         " complete a task using APIs."
                         " you will be given some API docs,"
                         " please find what APIs to use to achieve the task. "
                         "Please return the results in a dictionary with the following 3 keys, with no explanations: "
                         "url (string, use real value, not placeholder), method (string, POST or GET),"
                         " body (string, the POST body should be constructed using dependencies data and pre-information,"
                         " strictly not the values from the API docs example)."
                         "If this cannot be done, return `Error!!!` with explanations instead.")
        user_prompt = f"""Task: {task}. Pre_information: {pre_info},  dependencies data: {dependency_data}, 
        API docs: {harmonic_api_doc}"""
        inputs = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        res = client.query_chat(inputs)
        return res
