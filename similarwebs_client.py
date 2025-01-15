import asyncio
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

import requests

async def get_similar_sites(website_domain, api_key):
    url = f"https://api.similarweb.com/v4/website/{website_domain}/similar-sites/similarsites?api_key={api_key}&format=json&limit=40"
    headers = {"accept": "application/json"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error getting company description: {e}")
            return None

if __name__ == "__main__":
    async def main():
        website_domain = "atomico.com"  # Replace with the actual website domain
        api_key = "5145365ab2a741a794892d13ec3ce7ea"

        similar_sites_data = await get_similar_sites(website_domain, api_key)

        if similar_sites_data:
            print(f"Top similar sites for {website_domain}:")
            for site in similar_sites_data.get('similar_sites', []):
                print(f"Website: {site.get('url')}, Similarity Score: {site.get('score')}")

    asyncio.run(main())