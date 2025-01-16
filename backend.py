# highlights.category, highlights.text
# location.location
# tags[..].display_value || tags_v2[..].display_value
# funding
# external_description
import asyncio
import os

from executors.BossExecutor import BossExecutor
# customer_type
# tags_v2
# location
# headcount
# funding

from harmonic_client import HarmonicClient
from mock import mock
from openai_client import OpenAIClient


async def start_backend(question: str) -> dict:
    # This is a mock question
    # This engine is based upon the rest of the project to extract the company and find id.
    question = "Find competitors for company with id of 10327314" # Perplexity

    openAI_question_asker = OpenAIClient()
    openAI_code_writer = OpenAIClient()
    harmonic_client = HarmonicClient()

    boss_executor = BossExecutor()
    results = await boss_executor.smart_generate_executions(question, openAI_question_asker, openAI_code_writer, harmonic_client)
    if results:
        companies = [{"name": res.get("name"), "description": res.get("description")} for res in results]
        print("results:", companies)

if __name__ == "__main__":
    async def main():
        await start_backend("")  # Pass company_name as an argument

    asyncio.run(main())