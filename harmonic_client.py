import asyncio
import aiohttp


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


if __name__ == "__main__":
    async def main():
        website_domain = "atomico.com"  # Replace with the actual website domain
        api_key = "vF0yJYxvL6DwG9y0nUDXDXei7uGuKsz5"  # Replace with your actual API key
        company_info = await get_company_info_by_domain(website_domain, api_key)

        if company_info:
            print("Company Information:")
            print(company_info)
        else:
            print("Failed to fetch company information.")

        asyncio.run(main())
