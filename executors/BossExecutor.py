from executors.SqlExecutor import SqlExecutor
from harmonic_client import HarmonicClient

class BossExecutor:
    def __init__(self):
        self.sql_client = SqlExecutor()
        self.harmonic_client = HarmonicClient()


    def execute_step_with_input(self, executor, query, dependencies):
        # TODO: make sure this can handle query which comes out from the previous step
        # double check this, because we need to define which part of the query should dependency replace
        if dependencies:
            query = dependencies
        if executor == "SqlExecutor":
            return self.sql_client.execute(query)
        elif executor == "HarmonicClient":
            # query is a dictionary, with keys: method, url, body
            return self.harmonic_client.execute(query)
        else:
            raise ValueError(f"Unknown executor: {executor}")


    def execute_steps_with_chaining(self, executions):
        all_res = {}
        for execution in executions:
            executor, query, dependency = execution
            res = self.execute_step_with_input(executor, query, all_res[dependency])
            # TODO: create an endpoint to send to frontend to get the result
            all_res[execution] = res
        return list(all_res.values())[-1]


    def generate_executions(self, question: str):
        # TODO: THIS needs to come out from Bader's LLM, the data will look like this
        # TODO: check how to write it so each execution can have multiple dependencies
        # for each execution tuple, it will contain: executor, query, and dependencies, meaning
        # the query is the result of the previous execution
        execution1 = ("SqlExecutor", "SELECT * FROM table WHERE condition", None)
        execution2 = ("HarmonicClient", {
            "method": "GET",
            "url": "https://api.harmonic.com/api1",
            "body": {}
        }, None)
        execution3 = ("HarmonicClient", {
            "method": "GET",
            "url": "https://api.harmonic.com/api2",
            "body": {}
        }, execution2)
        executions = [execution1, execution2, execution3]
        return executions
