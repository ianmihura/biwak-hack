import json

from executors.SqlExecutor import SqlExecutor
from harmonic_client import HarmonicClient
from openai_client import OpenAIClient


search_similar_companies_api = """
API Name: Get similar companies
Function: Pass in a company ID, and get back a list of similar companies. You can use either the int ID, or the full URN.
ID example: GET https://api.harmonic.ai/search/similar_companies/123456
URN example: GET https://api.harmonic.ai/search/similar_companies/urn:harmonic:company:123456
Query Params: size:integer
Limitations: Size has a limit of 1000 companies.
Rest example: GET https://api.harmonic.ai/search/similar_companies/<id or urn>
Response: {
  "count": 3,
  "results": [
    "urn:harmonic:company:123456",
    "urn:harmonic:company:123457",
    "urn:harmonic:company:123458"
  ]
}
"""

get_companies_by_id_api = """
API Name: Get companies by ID.
Function: Pass in a list of company IDs or URNs, and get back a full picture of those companies.
Note:
If a company ID is -1, that we means we don't yet have a canonical company record for that company.
The API will not return data for these companies.
Note: The data in latest company snapshot might not match the current state of the company for up to 14 days. This is because we take snapshot of a company every 14 days but we might update the live state of company before that.
Note: The 'funding_rounds' field is a paid add-on - contact us at support@harmonic.ai if you're interested in exploring the product!
Query Params: {ids: array[integer], urns: array[string]}
Limitations: Endpoint has a limit of 50 companies.
Rest: example: GET https://api.harmonic.ai/companies
Response: [
  {
      "entity_urn": "urn:harmonic:company:123456",
      "id": 123456,
      "initialized_date": "2020-10-27T08:07:20.940106",
      "website": {...},
      "customer_type": "B2C",
      "logo_url": "string",
      "name": "string",
      "legal_name": "string",
      "description": "string",
      "external_description": "string",
      "founding_date": {...},
      "headcount": 0,
      "ownership_status": "PRIVATE",
      "company_type": "UNKNOWN",
      "stage": "SEED",
      "location": {...},
      "contact": {...},
      "socials": {...},
      "funding": {...},
      "people": [...], // returns first 60. See "Pagination > Nested People"
      "tags": [...],
      "tags_v2": [...],
      "funding_attribute_null_status": "EXISTS_BUT_UNDISCLOSED",
      "highlights": [...],
      "snapshots": [...],
      "traction_metrics": [...],
      "website_domain_aliases": [...],
      "name_aliases":[...],
      "employee_highlights": [...],
      "funding_rounds": [...],
      "investor_urn": "urn:harmonic:investor:203005",
      "related_companies": {...}
  },
]
"""

get_companies_by_id_batch_api = """
API Name: Batch get companies by ID
Function: Pass in a list of company IDs or URNs, and get back a full picture of those companies.
Note:
If a company ID is -1, that we means we don't yet have a canonical company record for that company.
The API will not return data for these companies.
Note: The data in latest company snapshot might not match the current state of the company for up to 14 days. 
This is because we take snapshot of a company every 14 days but we might update the live state of company before that.

Body Params: {ids: array[integer], urns: array[string]}
Limitations.
Endpoint has a limit of 500 companies.

Rest example: POST https://api.harmonic.ai/companies/batchGet
Response: 
[
  {
      "entity_urn": "urn:harmonic:company:123456",
      "id": 123456,
      "initialized_date": "2020-10-27T08:07:20.940106",
      "website": {...},
      "customer_type": "B2C",
      "logo_url": "string",
      "name": "string",
      "legal_name": "string",
      "description": "string",
      "external_description": "string",
      "founding_date": {...},
      "headcount": 0,
      "ownership_status": "PRIVATE",
      "company_type": "UNKNOWN",
      "stage": "SEED",
      "location": {...},
      "contact": {...},
      "socials": {...},
      "funding": {...},
      "people": [...], // returns first 60. See "Pagination > Nested People"
      "tags": [...],
      "tags_v2": [...],
      "funding_attribute_null_status": "EXISTS_BUT_UNDISCLOSED",
      "highlights": [...],
      "snapshots": [...],
      "traction_metrics": [...],
      "website_domain_aliases": [...],
      "name_aliases":[...],
      "employee_highlights": [...],
      "funding_rounds": [...],
      "investor_urn": "urn:harmonic:investor:203005",
      "related_companies": {...}
  },
]
"""

harmonic_api_doc = f"{search_similar_companies_api}, {get_companies_by_id_batch_api}"

class BossExecutor:
    def __init__(self):
        self.sql_client = SqlExecutor()
        self.harmonic_client = HarmonicClient()


    async def execute_step_with_input(self, executor, query, dependencies):
        # TODO: make sure this can handle query which comes out from the previous step
        # double check this, because we need to define which part of the query should dependency replace
        if dependencies:
            query = dependencies
        if executor == "SqlExecutor":
            return await self.sql_client.execute(query)
        elif executor == "HarmonicClient":
            # query is a dictionary, with keys: method, url, body
            return await self.harmonic_client.execute(query)
        else:
            raise ValueError(f"Unknown executor: {executor}")


    async def execute_steps_with_chaining(self, executions):
        all_res = {}
        for execution in executions:
            executor, query, dependency = execution
            res = await self.execute_step_with_input(executor, query, all_res[dependency] if dependency else None)
            # TODO: create an endpoint to send to frontend to get the result
            all_res[execution] = res
        return list(all_res.values())[-1]


    def generate_executions(self, question: str):
        # TODO: THIS needs to come out from Bader's LLM, the data will look like this
        # TODO: check how to write it so each execution can have multiple dependencies
        # for each execution tuple, it will contain: executor, query, and dependencies, meaning
        # the query is the result of the previous execution
        # execution1 = ("SqlExecutor", "SELECT * FROM table WHERE condition", None)
        execution2 = ("HarmonicClient", {
            "method": "GET",
            "url": "https://api.harmonic.ai/search/similar_companies/10327314",
            "body": {"size": 20}
        }, None)
        execution3 = ("HarmonicClient", {
            "method": "GET",
            "url": "https://api.harmonic.com/api2",
            "body": {}
        }, execution2)
        executions = [execution2, execution3]
        return executions

    async def smart_generate_executions(self, question: str,
                                        openAI_question_asker: OpenAIClient, openAI_code_writer: OpenAIClient,
                                        harmonic_client: HarmonicClient):
        system_prompt = ("You are an orchestrator of a programme. You will be given a question and need to answer that."
                         "In order to answer it, you will be given some Harmonic API docs,"
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
        steps = openAI_question_asker.query_chat(inputs)
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
                                                            results_from_dependency_steps or [], openAI_code_writer)
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
                         " complete a task using Harmonic APIs."
                         " you will be given some Harmonic API docs,"
                         " please find what APIs to use to achieve the task. "
                         "Please return the results in a dictionary with the following 3 keys, with no explanations: "
                         "url (string, use real value, not placeholder), method (string, POST or GET),"
                         " body (string, the POST body should be constructed using dependencies data and pre-information,"
                         " strictly not the values from the API docs example)."
                         "If this cannot be done, return `Error!!!` with explanations instead.")
        user_prompt = f"""Task: {task}. Pre_information: {pre_info},  dependencies data: {dependency_data}, 
        Harmonic API docs: {harmonic_api_doc}"""
        inputs = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        res = client.query_chat(inputs)
        return res
