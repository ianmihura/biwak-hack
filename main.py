

def main():
    # TODO: get company name
    # TODO: get company description

    name = "Motion Society"

    description = get_company_desc(name)
    keywords = extract_keyword(description)

    if validate_keywords(keywords):
        pass

    result = run_query(description, keywords)

    return result


def get_company_desc() -> str:
    pass


def extract_keyword(desc: str) -> list[str]:
    pass


def validate_keywords(keywords: list[str]) -> bool:
    pass


def run_query(description: str, keywords: list[str]) -> dict:
    # Mayb be recursively called
    queries = generate_queries(description, keywords)
    db = {}

    for query in queries:
        result = call_query(query)
        shortlist()
        db = aggr_query_results(db, result)
    
    is_valid = validate_db(db)

    if is_valid:
        return db
    else:
        return run_query(description, keywords)


def generate_queries(description: str, keywords: list[str]) -> list[str]:
    # TODO validate queries with description
    pass


def call_query(query: str) -> dict:
    pass


def aggr_query_results(db: dict, result: dict) -> dict:
    # using global full_db
    pass


def shortlist():
    pass


if __name__ == "__main__":
    main()
    
