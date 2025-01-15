import asyncio
import openai

from dotenv import load_dotenv
import os

load_dotenv()

class OpenAIClient:
    def __init__(self, model: str = "gpt-4"):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        openai.api_key = OPENAI_API_KEY
        self.model = model

    def query_chat(self, messages: list, max_tokens: int = 150, temperature: float = 0.7):
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            # Extract the content of the response
            return completion["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"An error occurred: {e}"


async def get_company_key_words(company_name: str, company_domain: str, company_description: str):
    client = OpenAIClient()

    system_prompt = """
    You are a VC analyst trying to find direct competitors for a provided company, in their niche area. \n
    You will be given a company's domain, name and description. Please return 4 key words that can be used to identify 
    the niche specialty of the company. Return the results in an array of strings.
    """
    user_prompt = f"""
    Company: "{company_name}" \n
    Domain: "{company_domain}" \n
    Description: "{company_description}" """
    inputs = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    res = client.query_chat(inputs)
    print(res)
    return res


async def validate_db_with_openai(company_info: dict, db: dict):
    client = OpenAIClient()

    system_prompt = """
    """
    user_prompt = f"""
    Company Info: {company_info}
    """
    inputs = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    res = client.query_chat(inputs)
    print(res)
    return res


if __name__ == "__main__":

    async def main():

        company_name = "Motion Society"
        domain = "motionsociety.com"
        description = "Motion Society helps content creators reaching their full potential and develops their brands in all social medias. Motion Society currently brings together a diversified and strong community of creators spanning from a lot of different worlds. Our team is fully dedicated to make them blossom on Facebook, Instagram, Snapchat, TikTok, Pinterest and YouTube."
        key_words = await get_company_key_words(company_name, domain, description)

        # Query the client
        print(key_words)

    asyncio.run(main())
