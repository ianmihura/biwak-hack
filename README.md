# TenX

![alt text](https://i.imgur.com/O8vZHPM.png)

> This project was built as part of the Data-Driven VC Hackathon organized by [Red River West](https://redriverwest.com) & [Bivwak! by BNP Paribas](https://bivwak.bnpparibas/)

## Concept description

Transform your questions into concrete answers with our intelligent APIs!

Unify your dataset search with natural language. You write your query, and we convert it to 
the relevant SQL, API, GraphQL or other queries.

- Simplify access to complex data: Speak in natural language, and we handle the rest.
- APIs at your service: Take advantage of a vast library of documented APIs, ready to meet your needs.
- Precise and tailored answers: Harness the power of our tools to achieve reliable and fast results.
- Save time and energy: Reduce your searches and maximize your efficiency.

The demo is using [Harmonize api](https://console.harmonic.ai/docs/api-reference/fetch) 
as a dataset example.

## Boot project
1. `python -m venv .`
2. `pip install -r requirements.txt`
3. `source ./bin/activate`
4. Add your **Harmonic** and **OpenAI** keys to the `.env` file
5. Launch the project with `streamlit run interface.py`

---

### Demo explanaiton

We created a mock of how the backend will work, the file is `happy.py`.
We perform a query search for competitors of a specified domain using various client APIs.

- **Description**: The main asynchronous function that processes user input to find competitors for a given domain. It retrieves company information, finds similar sites, and evaluates them using a vector search engine.
- **Parameters**:
  - `user_input` (str): A string containing the user query, defaulting to "Get me the competitors of motionsociety.com".
- **Returns**: A dictionary containing a list of similar companies with their details and accuracy ratings.

#### Key Steps:
1. **Domain Extraction**: Uses a regular expression to extract the domain from the user input.
    - TODO: We will replace this with a real (and modular) extractor
2. **Client Initialization**: Initializes the `HarmonicClient` to fetch company information based on the domain.
    - TODO: make this modular with the Executors, and configurable apis
3. **API Calls**:
    - Retrieves company info using Harmonic API
    - Fetches similar sites using Harmonic API
    - Gathers detailed information for similar companies using Harmonic API
4. **Vector Search**: Initializes `OpenAIClient` and constructs a system prompt for the vector search.
    - TODO: Considering migrating this to a real vector search
5. **Data Processing**:
    - Filters relevant fields from the company data.
    - Queries the OpenAI model to get accuracy ratings for each company.

### BossExecutor

*TODO document the executors*

## Modular APIs

*We only support Harmonize API for now.*

To integrate your own data provider APIs, you must:
1. Include the secrets to the .env file
2. Add the name of the endpoint to `api_config.py`
3. Provide a list of callable endpoints, or a Swagger spec

**For SQL queries**

*We still don't support SQL queries*

