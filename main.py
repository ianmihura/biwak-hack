import asyncio
import re
from openai_client import OpenAIClient
from harmonic_client import HarmonicClient, COMPANY_FIELDS
from functools import reduce


async def enrich_user_query(user_input = "Get me the competitors of motionsociety.com") -> str:
    # TODO: make sure we have a domain in the search
    domain = re.findall(r'\b\w+\.\w+\b', user_input)[0]

    # TODO: include more clients -> allow the user to implement their own clients
    client = HarmonicClient()

    # TODO: make sure we need to do this (if we have a domain)
    company_info = await client.get_company_info_by_domain(domain)
    company_info["tags_v2"] = reduce(lambda a, v: a + [v["display_value"]], company_info["tags_v2"], [])
    company_info["funding"] = company_info["funding"]["funding_stage"]
    return company_info


async def execute_queries(enriched_user_input, company_id) -> dict:
    # return [{'name': 'Captiv8', 'description': 'Captiv8 offers an influencer marketing platform that leverages artificial intelligence and predictive analytics to identify and engage social media creators, enhancing the effectiveness of marketing campaigns. The platform utilizes first-party creator data to optimize return on investment and streamline marketing operations.', 'headcount': 185, 'stage': 'SEED', 'id': 1372198, 'tags_v2': ['Business (B2B)', 'Communications and information technology', 'Service', 'Data Analytics', 'Artificial intelligence'], 'funding': 'SEED', 'accuracy': '0.85'}, {'name': 'Spotter', 'description': 'Spotter provides a platform that leverages artificial intelligence to offer financial tools specifically designed for YouTube content creators, facilitating their growth and success. The platform includes a video catalog that enhances watch-time metrics and optimizes advertising strategies for brands.', 'headcount': 237, 'stage': 'SERIES_D', 'id': 56727483, 'tags_v2': ['Consumer products and services', 'Business services', 'Communications and information technology', 'Consumer (B2C)', 'Business (B2B)', 'Education and research', 'Service', 'Software', 'Hardware'], 'funding': 'SERIES_D', 'accuracy': '0.72'}, {'name': 'Aive', 'description': 'Aive is a generative AI video platform designed for large-scale video automation, offering simplified video creation, reduced post-production costs, and improved productivity through automation and collaboration. The platform enables users to enhance video post-production, distribution, and creative collaboration with features such as data-driven video creation, workflow automation, and dynamic cookieless distribution.', 'headcount': 59, 'stage': 'SEED', 'id': 20264588, 'tags_v2': ['Artificial intelligence', 'Service', 'Communications and information technology', 'Business (B2B)', 'Data Analytics'], 'funding': 'SEED', 'accuracy': '0.82'}, {'name': 'Jellysmack', 'description': 'Jellysmack provides a service that leverages AI technology and first-party data to enhance content optimization for creators, facilitating increased revenue and audience engagement across multiple social media platforms. Their methodology includes multi-platform distribution and strategic brand partnerships to maximize reach and effectiveness.', 'headcount': 803, 'stage': 'SERIES_D', 'id': 486126, 'tags_v2': ['Data Analytics', 'Communications and information technology', 'Artificial intelligence', 'Service', 'Consumer (B2C)', 'Consumer products and services'], 'funding': 'SERIES_D', 'accuracy_descr': 'The similarity between Motion Society and Jellysmack is approximately 0.88. This high score indicates a strong similarity between the two companies, given their shared focus on content optimization for social media platforms and the use of advanced technologies.', 'accuracy': ['0.88']}, {'name': 'Electrify Video Partners', 'description': 'Electrify Video Partners specializes in acquiring and enhancing established YouTube channels through strategic investments and tailored business growth strategies aimed at increasing audience engagement and revenue. The company utilizes investment methodologies and resources to support creators in effectively expanding their brands.', 'headcount': 50, 'stage': 'SERIES_C', 'id': 9894929, 'tags_v2': ['Consumer (B2C)', 'Communications and information technology', 'Service'], 'funding': 'SERIES_C', 'accuracy': '0.75'}, {'name': 'onomy', 'description': 'Onomy offers a platform that provides free educational content aimed at adults, focusing on personal development, career advancement, and personal finance through formats like podcasts and web series. The service employs bite-sized content to enhance accessibility and relevance for young adults.', 'headcount': 9, 'stage': 'SEED', 'id': 1489866, 'tags_v2': ['Data Analytics', 'Consumer (B2C)', 'Service', 'Consumer products and services'], 'funding': 'SEED', 'accuracy': '0.4'}, {'name': 'Olyn', 'description': 'Olyn offers a pay-per-view hosting platform that allows creators to distribute media content directly to consumers, utilizing advanced streaming technologies for high-resolution video and multi-language support. The platform incorporates security features such as API keys and tokenization to safeguard content during distribution.', 'headcount': 20, 'stage': 'PRE_SEED', 'id': 21501749, 'tags_v2': ['Consumer products and services', 'Business services', 'Business (B2B)', 'Service', 'Consumer (B2C)', 'Software'], 'funding': 'PRE_SEED', 'accuracy': '0.71'}, {'name': 'Linius', 'description': 'The primary offering is a Video Virtualization Engine™ that enables users to create customized video compilations by selecting specific moments from extensive video libraries, leveraging AI and machine learning for efficient content discovery. It includes robust APIs and interactive tools designed to enhance community engagement and improve viewer experiences.', 'headcount': 21, 'stage': 'SERIES_A', 'id': 703761, 'tags_v2': ['Business services', 'Business (B2B)', 'Blockchain', 'Communications and information technology', 'Artificial intelligence', 'Data Analytics', 'Service'], 'funding': 'SERIES_A', 'accuracy_descr': 'An error occurred: Rate limit reached for gpt-4 in organization org-oRz5Ro6gqG7Ai0TxGFV2BCXL on tokens per min (TPM): Limit 10000, Used 8188, Requested 2121. Please try again in 1.854s. Visit https://platform.openai.com/account/rate-limits to learn more.', 'accuracy': ['1.854']}, {'name': 'Matchmade', 'description': 'Matchmade offers an automated platform for influencer marketing that utilizes machine learning and big data to connect brands with creators based on audience demographics. The service tracks over 16 million YouTube channels and synchronizes 2.5 million videos every hour, streamlining the contracting and payment processes for marketing campaigns.', 'headcount': 11, 'stage': 'SERIES_A', 'id': 1371863, 'tags_v2': ['Business (B2B)', 'Consumer (B2C)', 'Artificial intelligence', 'Communications and information technology', 'Data Analytics', 'Service'], 'funding': 'SERIES_A', 'accuracy_descr': 'An error occurred: Rate limit reached for gpt-4 in organization org-oRz5Ro6gqG7Ai0TxGFV2BCXL on tokens per min (TPM): Limit 10000, Used 8137, Requested 2114. Please try again in 1.506s. Visit https://platform.openai.com/account/rate-limits to learn more.', 'accuracy': ['1.506']}, {'name': 'ByUs Media', 'description': 'ByUs Media specializes in producing athlete-focused video content and digital marketing strategies, particularly for name, image, and likeness (NIL) initiatives. Their offerings include creative strategy and branded content, such as mini-documentaries and short-form videos tailored for the sports and lifestyle sectors.', 'headcount': 5, 'stage': 'SEED', 'id': 12475939, 'tags_v2': ['Service', 'Education and research', 'Communications and information technology', 'Business (B2B)'], 'funding': 'SEED', 'accuracy_descr': 'An error occurred: Rate limit reached for gpt-4 in organization org-oRz5Ro6gqG7Ai0TxGFV2BCXL on tokens per min (TPM): Limit 10000, Used 8087, Requested 2096. Please try again in 1.098s. Visit https://platform.openai.com/account/rate-limits to learn more.', 'accuracy': ['1.098']}]
    print("---------------------------------")
    print(enriched_user_input)
    print("---------------------------------")

    # TODO: include more clients -> allow the user to implement their own clients
    client = HarmonicClient()

    # TODO[hard]: choose endoint call according to user_input (use api_config file)
    similar_sites = await client.get_similar_sites(company_id)
    ids = reduce(lambda a, v: a + [v.split(":")[-1]], similar_sites["results"], [])
    similar_companies = await client.get_companies_info_by_ids(ids)
    return similar_companies


def validate_response(enriched_user_input, similar_companies):
    # TODO: can vectore search be better?
    client = OpenAIClient()
    system_prompt = f"""
    You are a vector search engine that measures the distance a company
    description and whatever the user will prompt next.
    Give the answer in a normalized accuracy from 0 to 1.
    The first company description is: {enriched_user_input}.
    """

    final_companies = []
    for entry in similar_companies:
        filtered_entry = {field: entry[field] for field in COMPANY_FIELDS if field in entry}
        filtered_entry["tags_v2"] = reduce(lambda a, v: a + [v["display_value"]], filtered_entry["tags_v2"], [])
        filtered_entry["funding"] = filtered_entry["funding"]["funding_stage"]
        # filtered_entry["investors"] = reduce(lambda a, v: a+[v["name"]], filtered_entry["funding"]["investors"], [])
        inputs = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(filtered_entry)}
        ]
        res = client.query_chat(inputs)

        # hallucination: sometimes the AI will give you more info than you asked for
        if len(res) > 5:
            # TODO: maybe the user wants this always?
            filtered_entry["accuracy_descr"] = res
            res = re.findall("\d+\.\d+", res)
            filtered_entry["accuracy"] = res
        else:
            filtered_entry["accuracy"] = res
        
        final_companies.append(filtered_entry)

    print(final_companies)
    return final_companies

async def main(user_input = "Get me the competitors of motionsociety.com") -> dict:
    """
    This is the happy path for query searching. Many things yet TODO!

    To modularize the endpoint calls, we will use the Executors (eg. BossExecutor)
    """
    # return [{'name': 'Captiv8', 'description': 'Captiv8 offers an influencer marketing platform that leverages artificial intelligence and predictive analytics to identify and engage social media creators, enhancing the effectiveness of marketing campaigns. The platform utilizes first-party creator data to optimize return on investment and streamline marketing operations.', 'headcount': 185, 'stage': 'SEED', 'id': 1372198, 'tags_v2': ['Business (B2B)', 'Communications and information technology', 'Service', 'Data Analytics', 'Artificial intelligence'], 'funding': 'SEED', 'accuracy': '0.85'}, {'name': 'Spotter', 'description': 'Spotter provides a platform that leverages artificial intelligence to offer financial tools specifically designed for YouTube content creators, facilitating their growth and success. The platform includes a video catalog that enhances watch-time metrics and optimizes advertising strategies for brands.', 'headcount': 237, 'stage': 'SERIES_D', 'id': 56727483, 'tags_v2': ['Consumer products and services', 'Business services', 'Communications and information technology', 'Consumer (B2C)', 'Business (B2B)', 'Education and research', 'Service', 'Software', 'Hardware'], 'funding': 'SERIES_D', 'accuracy': '0.72'}, {'name': 'Aive', 'description': 'Aive is a generative AI video platform designed for large-scale video automation, offering simplified video creation, reduced post-production costs, and improved productivity through automation and collaboration. The platform enables users to enhance video post-production, distribution, and creative collaboration with features such as data-driven video creation, workflow automation, and dynamic cookieless distribution.', 'headcount': 59, 'stage': 'SEED', 'id': 20264588, 'tags_v2': ['Artificial intelligence', 'Service', 'Communications and information technology', 'Business (B2B)', 'Data Analytics'], 'funding': 'SEED', 'accuracy': '0.82'}, {'name': 'Jellysmack', 'description': 'Jellysmack provides a service that leverages AI technology and first-party data to enhance content optimization for creators, facilitating increased revenue and audience engagement across multiple social media platforms. Their methodology includes multi-platform distribution and strategic brand partnerships to maximize reach and effectiveness.', 'headcount': 803, 'stage': 'SERIES_D', 'id': 486126, 'tags_v2': ['Data Analytics', 'Communications and information technology', 'Artificial intelligence', 'Service', 'Consumer (B2C)', 'Consumer products and services'], 'funding': 'SERIES_D', 'accuracy_descr': 'The similarity between Motion Society and Jellysmack is approximately 0.88. This high score indicates a strong similarity between the two companies, given their shared focus on content optimization for social media platforms and the use of advanced technologies.', 'accuracy': ['0.88']}, {'name': 'Electrify Video Partners', 'description': 'Electrify Video Partners specializes in acquiring and enhancing established YouTube channels through strategic investments and tailored business growth strategies aimed at increasing audience engagement and revenue. The company utilizes investment methodologies and resources to support creators in effectively expanding their brands.', 'headcount': 50, 'stage': 'SERIES_C', 'id': 9894929, 'tags_v2': ['Consumer (B2C)', 'Communications and information technology', 'Service'], 'funding': 'SERIES_C', 'accuracy': '0.75'}, {'name': 'onomy', 'description': 'Onomy offers a platform that provides free educational content aimed at adults, focusing on personal development, career advancement, and personal finance through formats like podcasts and web series. The service employs bite-sized content to enhance accessibility and relevance for young adults.', 'headcount': 9, 'stage': 'SEED', 'id': 1489866, 'tags_v2': ['Data Analytics', 'Consumer (B2C)', 'Service', 'Consumer products and services'], 'funding': 'SEED', 'accuracy': '0.4'}, {'name': 'Olyn', 'description': 'Olyn offers a pay-per-view hosting platform that allows creators to distribute media content directly to consumers, utilizing advanced streaming technologies for high-resolution video and multi-language support. The platform incorporates security features such as API keys and tokenization to safeguard content during distribution.', 'headcount': 20, 'stage': 'PRE_SEED', 'id': 21501749, 'tags_v2': ['Consumer products and services', 'Business services', 'Business (B2B)', 'Service', 'Consumer (B2C)', 'Software'], 'funding': 'PRE_SEED', 'accuracy': '0.71'}, {'name': 'Linius', 'description': 'The primary offering is a Video Virtualization Engine™ that enables users to create customized video compilations by selecting specific moments from extensive video libraries, leveraging AI and machine learning for efficient content discovery. It includes robust APIs and interactive tools designed to enhance community engagement and improve viewer experiences.', 'headcount': 21, 'stage': 'SERIES_A', 'id': 703761, 'tags_v2': ['Business services', 'Business (B2B)', 'Blockchain', 'Communications and information technology', 'Artificial intelligence', 'Data Analytics', 'Service'], 'funding': 'SERIES_A', 'accuracy_descr': 'An error occurred: Rate limit reached for gpt-4 in organization org-oRz5Ro6gqG7Ai0TxGFV2BCXL on tokens per min (TPM): Limit 10000, Used 8188, Requested 2121. Please try again in 1.854s. Visit https://platform.openai.com/account/rate-limits to learn more.', 'accuracy': ['1.854']}, {'name': 'Matchmade', 'description': 'Matchmade offers an automated platform for influencer marketing that utilizes machine learning and big data to connect brands with creators based on audience demographics. The service tracks over 16 million YouTube channels and synchronizes 2.5 million videos every hour, streamlining the contracting and payment processes for marketing campaigns.', 'headcount': 11, 'stage': 'SERIES_A', 'id': 1371863, 'tags_v2': ['Business (B2B)', 'Consumer (B2C)', 'Artificial intelligence', 'Communications and information technology', 'Data Analytics', 'Service'], 'funding': 'SERIES_A', 'accuracy_descr': 'An error occurred: Rate limit reached for gpt-4 in organization org-oRz5Ro6gqG7Ai0TxGFV2BCXL on tokens per min (TPM): Limit 10000, Used 8137, Requested 2114. Please try again in 1.506s. Visit https://platform.openai.com/account/rate-limits to learn more.', 'accuracy': ['1.506']}, {'name': 'ByUs Media', 'description': 'ByUs Media specializes in producing athlete-focused video content and digital marketing strategies, particularly for name, image, and likeness (NIL) initiatives. Their offerings include creative strategy and branded content, such as mini-documentaries and short-form videos tailored for the sports and lifestyle sectors.', 'headcount': 5, 'stage': 'SEED', 'id': 12475939, 'tags_v2': ['Service', 'Education and research', 'Communications and information technology', 'Business (B2B)'], 'funding': 'SEED', 'accuracy_descr': 'An error occurred: Rate limit reached for gpt-4 in organization org-oRz5Ro6gqG7Ai0TxGFV2BCXL on tokens per min (TPM): Limit 10000, Used 8087, Requested 2096. Please try again in 1.098s. Visit https://platform.openai.com/account/rate-limits to learn more.', 'accuracy': ['1.098']}]

    # TODO: make sure we have a domain in the search
    domain = re.findall(r'\b\w+\.\w+\b', user_input)[0]

    # TODO: include more clients -> allow the user to implement their own clients
    client = HarmonicClient()

    # TODO: make sure we need to do this (if we have a domain)
    company_info = await client.get_company_info_by_domain(domain)

    # TODO[hard]: choose endoint call according to user_input (use api_config file)
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

    final_companies = []
    for entry in similar_companies:
        filtered_entry = {field: entry[field] for field in COMPANY_FIELDS if field in entry}
        filtered_entry["tags_v2"] = reduce(lambda a, v: a + [v["display_value"]], filtered_entry["tags_v2"], [])
        filtered_entry["funding"] = filtered_entry["funding"]["funding_stage"]
        # filtered_entry["investors"] = reduce(lambda a, v: a+[v["name"]], filtered_entry["funding"]["investors"], [])
        inputs = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(filtered_entry)}
        ]
        res = client.query_chat(inputs)

        # hallucination: sometimes the AI will give you more info than you asked for
        if len(res) > 5:
            # TODO: maybe the user wants this always?
            filtered_entry["accuracy_descr"] = res
            res = re.findall("\d+\.\d+", res)
            filtered_entry["accuracy"] = res
        else:
            filtered_entry["accuracy"] = res
        
        final_companies.append(filtered_entry)

    print(final_companies)
    return final_companies

if __name__ == "__main__":
    asyncio.run(main())
