

def get_company_desc() -> str:
    pass


def extract_keyword(desc: str) -> list[str]:
    pass


def validate_keywords(keywords: list[str]) -> bool:
    pass


def generate_queries(keywords: list[str]) -> list[str]:
    # TODO validate queries
    pass


if __name__ == "__main__":
    # TODO: get company name
    # TODO: get company description

    name = "Motion Society"

    description = get_company_desc(name)
    keywords = extract_keyword(description)

    if validate_keywords(keywords):
        pass

    queries = generate_queries(description, keywords)

    for query in queries:
        call_query()
        pass


