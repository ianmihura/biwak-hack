# highlights.category, highlights.text
# location.location
# tags[..].display_value || tags_v2[..].display_value
# funding
# external_description
import os

# customer_type
# tags_v2
# location
# headcount
# funding

from harmonic_client import HarmonicClient
from mock import mock
from openai_client import OpenAIClient


async def start_backend(company_domain: str) -> dict:
    harmonic_client = HarmonicClient(os.getenv("HARMONIC_API_KEY"))
    openai_client = OpenAIClient()

    # This will be the blue-print for the final implementation. For now, we are mocking the generated query.
    possible_client, possible_query = openai_client.generate_queries("Find competitors for company with domain: " + company_domain)
    possible_client = "Harmonic"
    if possible_client == "Harmonic":
        answers = await harmonic_client.run_query(possible_query)
        if answers:
            return answers
        else

    target_company_dict = await harmonic_client.get_company_info_by_domain(company_domain)
    description = target_company_dict.get("description")

    # TODO: set filters to company_info
    keywords = openai_client.query_chat()
    # keywords = extract_keyword(description)

    if validate_keywords(keywords):
        # manually validated by user
        pass

    result = run_query(company_info, keywords)  # and validate
    return result or mock


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
