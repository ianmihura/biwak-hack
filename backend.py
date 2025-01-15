# highlights.category, highlights.text
# location.location
# tags[..].display_value || tags_v2[..].display_value
# funding
# external_description
import os

from executors.BossExecutor import BossExecutor
# customer_type
# tags_v2
# location
# headcount
# funding

from harmonic_client import HarmonicClient
from mock import mock
from openai_client import OpenAIClient


async def start_backend(question: str) -> dict:
    # This is a mock question
    question = "Find competitors for company Career26.com"
    boss_executor = BossExecutor()
    executions = boss_executor.generate_executions(question)
    final_result = boss_executor.execute_steps_with_chaining(executions)
    return final_result

def get_company_info(company_domain: str) -> str:
    pass


def extract_keyword(company_info: dict) -> list[str]:
    pass


def validate_keywords(keywords: list[str]) -> bool:
    pass


def run_query(company_info: dict, keywords: list[str]) -> dict:
    # Can be recursively called
    queries = generate_queries(company_info, keywords)
    db = {}

    for query in queries:
        result = call_query(query)
        # maybe validate at this step?
        db = aggr_query_results(db, result)

    is_valid = validate_db(company_info, db)

    if is_valid:
        return db
    else:
        return run_query(company_info, keywords)


def generate_queries(company_info: dict, keywords: list[str]) -> list[str]:
    # TODO validate queries with company_info
    # KINDA HARD - we can mock
    return []


def call_query(query: str) -> dict:
    pass


def aggr_query_results(db: dict, result: dict) -> dict:
    pass


def validate_db(company_info: dict, db: dict) -> bool:

    # HARD
    # filter with company_info.filters
    return True
