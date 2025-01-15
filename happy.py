import asyncio
import re
from openai_client import OpenAIClient
from harmonic_client import HarmonicClient, COMPANY_FIELDS
from functools import reduce


# company_name = "Motion Society"
# domain = "motionsociety.com"
# description = "Motion Society helps content creators reaching their full potential and develops their brands in all social medias. Motion Society currently brings together a diversified and strong community of creators spanning from a lot of different worlds. Our team is fully dedicated to make them blossom on Facebook, Instagram, Snapchat, TikTok, Pinterest and YouTube."

async def main() -> dict:
    # TODO: make sure we have a domain in the search
    user_input = "Get me the competitors of motionsociety.com"
    domain = re.findall(r'\b\w+\.\w+\b', user_input)[0]
    
    # TODO: include more clients -> allow the user to implement their own clients
    client = HarmonicClient()

    # TODO: make sure we need to do this (if we have a domain)
    company_info = await client.get_company_info_by_domain(domain)

    # TODO[hard]: choose endoint call according to user_input
    similar_sites = await client.get_similar_sites(company_info["id"])
    ids = reduce(lambda a, v: a + [v.split(":")[-1]], similar_sites["results"], [])
    similar_companies = await client.get_companies_info_by_ids(ids)

    # TODO: can vectore search be better?
    client = OpenAIClient()
    system_prompt = f"""
    You are a vector search engine that measures the distance a company
    description and whatever the user will prompt next.
    Give the answer in a normalized accuracy from 0 to 1.
    The first company description is: {user_input}. {company_info}.
    """

    for entry in similar_companies:
        filtered_entry = {field: entry[field] for field in COMPANY_FIELDS if field in entry}
        inputs = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(filtered_entry)}
        ]
        res = client.query_chat(inputs)

        # hallucination: sometimes the AI will give you more info than you asked for
        if len(res) > 10:
            # TODO: maybe the user wants this always?
            entry["accuracy_descr"] = res
            res = re.findall("\d+\.\d+", res)
            entry["accuracy"] = res
        else:
            entry["accuracy"] = res
    
    print(similar_companies)
    return similar_companies

if __name__ == "__main__":
    asyncio.run(main())
