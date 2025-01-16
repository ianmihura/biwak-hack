import asyncio
import json
from typing import Optional

import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

COMPANY_FIELDS = ["name", "description", "headcount", "customer_type", "stage", "id", "tags_v2", "funding"]

class HarmonicClient:
    def __init__(self):
        api_key = os.getenv("HARMONIC_API_KEY")
        self.api_key = api_key

    async def execute(self, instructions: dict) -> any:
        # Theoretically, this URL needs to be produced by LLM
        method = instructions.get("method")
        url = instructions.get("url")
        body = instructions.get("body")

        # method = "POST"
        # # ID IS A PROBLEM, becuase LLM query generator needs to produce that
        # url = f"https://api.harmonic.ai/search/similar_companies/{id}?size=20"
        # body = ""
        headers = {'apikey': self.api_key}

        async with aiohttp.ClientSession() as session:
            try:
                if method == "GET":
                    async with session.get(url, headers=headers) as response:
                        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
                        if response is not None:
                            return await response.json()
                elif method == "POST":
                    if isinstance(body, str):
                        try:
                            body = json.loads(body)
                        except json.JSONDecodeError as e:
                            print("Body is not a valid JSON string: ", body)
                    async with session.post(url, headers=headers, json=body) as response:
                        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
                        res = await response.json()
                        return res
            except aiohttp.ClientError as e:
                print(f"Error running query {url} with {method} method: {e}")
                return None

    async def get_similar_sites(self, id, size=10):
        url = f"https://api.harmonic.ai/search/similar_companies/{id}?size={size}"
        headers = {'apikey': self.api_key}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()

            except aiohttp.ClientError as e:
                print(f"Error fetching similar companies: {e}")
                return None


    async def get_company_info_by_domain(self, website_domain) -> Optional[dict]:
        # Theoretically, this URL needs to be produced by LLM
        url = f"https://api.harmonic.ai/companies?website_domain={website_domain}"
        headers = {'apikey': self.api_key}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
                    company_obj = await response.json()
                    filtered_obj = {field: company_obj[field] for field in COMPANY_FIELDS if field in company_obj}
                    return filtered_obj
            except aiohttp.ClientError as e:
                print(f"Error getting company description: {e}")
                return None

    async def get_companies_by_key_words(self, key_words: list[str]):
        # Theoretically, this URL needs to be produced by LLM
        url = f"https://api.harmonic.ai/search/companies_by_keywords"
        headers = {'apikey': self.api_key}
        body = {"contains_any_of_keywords": ",".join(key_words), "include_ids_only": False}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=body) as response:
                    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
                    return await response.json()
            except aiohttp.ClientError as e:
                print(f"Error getting company description: {e}")
                return None


    async def get_companies_info_by_ids(self, ids):
        url = "https://api.harmonic.ai/companies/batchGet"
        body = {"ids": ids}
        headers = {'apikey': self.api_key}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=body, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                print(f"Error getting company data: {e}")
                return None

#
# if __name__ == "__main__":
#     async def main():
#         website_domain = "atomico.com"  # Replace with the actual website domain
#         api_key = os.getenv("HARMONIC_API_KEY")
#         id = 2261160
#
#         similar_companies_data = await get_similar_sites(id, api_key)
#
#         if similar_companies_data:
#             print("Similar Companies:")
#             for urn in similar_companies_data.get('results', []):
#                 print(urn)
#         else:
#             print("No similar companies data found.")
#
#     asyncio.run(main())
