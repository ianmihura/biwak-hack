

def start_backend():
    # TODO: get company name
    # TODO: get company company_info

    name = "Motion Society"

    company_info = get_company_desc(name)
    # TODO: set filters to company_info
    keywords = extract_keyword(company_info)

    if validate_keywords(keywords):
        # manually validated by user
        pass

    result = run_query(company_info, keywords)  # and validate

    return result


def get_company_desc() -> str:
    pass


def extract_keyword(company_info: dict) -> list[str]:
    pass


def validate_keywords(keywords: list[str]) -> bool:
    pass


def run_query(company_info: dict, keywords: list[str]) -> dict:
    # Mayb be recursively called
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
    pass


def call_query(query: str) -> dict:
    pass


def aggr_query_results(db: dict, result: dict) -> dict:
    pass


def validate_db(company_info: dict, db: dict) -> bool:
    # HARD
    # filter with company_info.filters
    pass
