import asyncio
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()


async def get_company_info_by_domain(website_domain, api_key):
    url = f"https://api.harmonic.ai/companies?website_domain={website_domain}"
    headers = {'apikey': api_key}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers) as response:
                response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error getting company description: {e}")
            return None

async def get_companies_by_key_words(api_key, key_words: list[str]):
    url = f"https://api.harmonic.ai/search/companies_by_keywords"
    headers = {'apikey': api_key}
    body = {"contains_any_of_keywords": ",".join(key_words), "include_ids_only": False}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=body) as response:
                response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error getting company description: {e}")
            return None


async def get_companies_info_by_ids(ids, api_key):
    url = "https://api.harmonic.ai/companies/batchGet"
    body = {
        "ids": ids
    }
    headers = {'apikey': api_key}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=body, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error getting company data: {e}")
            return None


if __name__ == "__main__":
    async def main():
        website_domain = "atomico.com"  # Replace with the actual website domain
        api_key = os.getenv("HARMONIC_API_KEY")
        ids = [3639957, 2261160]
        companies = await get_companies_info_by_ids(ids, api_key)

        if companies:
            for company in companies:
                headcount = company.get('headcount', 0)
                print(f"Company {company['id']} has {headcount} employees.")

    asyncio.run(main())
