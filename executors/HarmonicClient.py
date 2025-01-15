import os

import aiohttp


class HarmonicClient:
    def __init__(self):
        api_key = os.getenv("HARMONIC_API_KEY")
        self.api_key = api_key

    async def run_query(self, instructions) -> any:
        # Theoretically, this URL needs to be produced by LLM
        method = instructions.method
        url = instructions.url
        body = instructions.body

        method = "POST"
        # ID IS A PROBLEM, becuase LLM query generator needs to produce that
        url = f"https://api.harmonic.ai/search/similar_companies/{id}?size=20"
        body = ""
        headers = {'apikey': self.api_key}

        async with aiohttp.ClientSession() as session:
            try:
                if method == "GET":
                    async with session.get(url, headers=headers) as response:
                        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
                        return await response.json()
                elif method == "POST":
                    async with session.post(url, headers=headers) as response:
                        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
                        res = await response.json()
                        return res
            except aiohttp.ClientError as e:
                print(f"Error running query {url} with {method} method: {e}")
                return None