from functools import reduce
import openai
import api_config

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


    async def get_company_key_words(self, company_name: str, company_domain: str, company_description: str):
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
        res = self.query_chat(inputs)
        print(res)
        return res


    async def get_url_with_openai(self, user_input: str) -> str:
        endpoints_descriptions = reduce(lambda x: ": " + x["description"], api_config.config)
        system_prompt = f"""
        You have to choose an endpoint to answer to the user input.
        The list of endpoints are: {endpoints_descriptions}
        """
        inputs = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        res = self.query_chat(inputs)
        print(res)
        return res
