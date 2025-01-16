# TenX

![alt text](https://i.imgur.com/O8vZHPM.png)

> This project was built as part of the Data-Driven VC Hackathon organized by [Red River West](https://redriverwest.com) & [Bivwak! by BNP Paribas](https://bivwak.bnpparibas/)

## Boot project
1. `python -m venv .`
2. `pip install -r requirements.txt`
3. `source ./bin/activate`
4. Add your **Harmonic** and **OpenAI** keys to the `.env` file
5. Launch the project with `streamlit run interface.py`

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

## Modular APIs

*We only support Harmonic and OpenAI API for now.*

To integrate your own data provider APIs, you must:
1. Include the secrets to the .env file
2. Add the name of the endpoint to `api_config.py`
3. Provide a list of callable endpoints, or a Swagger spec

**For SQL queries**

*We still don't support SQL queries*

## Demo explanation

We created a mock of how the backend will work, the file is `main.py`.
We perform a query search for competitors of a specified domain using various client APIs.

The main function processes user input to find similar companies for a given comapny. It retrieves company information, finds similar sites, and evaluates them using a vector search engine.

1. **Domain Extraction**: Uses a regular expression to extract the domain from the user input.
2. **Client Initialization**: Initializes the `HarmonicClient` to fetch company information based on the domain.
3. **API Calls**:
    - Retrieves company info using Harmonic API
    - Fetches similar sites using Harmonic API
    - Gathers detailed information for similar companies using Harmonic API
4. **Validation**: Initializes `OpenAIClient` and validated the results from API calls with LLM.

### Boss Executor

#### Overview
The `BossExecutor` class orchestrates the execution of tasks using various executors, such as SQL and API calls. For now we are only implementing `HarmonicClient` and `OpenAIClient` to generate and execute steps based on user queries. This class is particularly useful for handling workflows that involve stepwise execution.

#### Improvements
- We still have to integrate more API clients, and plug the Executors to the frontend
- Integrate the accuracy measure into the Executor

---

#### Class: `BossExecutor`

##### Methods

###### `__init__(self)`
Initializes the `BossExecutor` instance and creates instances of:
- `SqlExecutor` for executing SQL queries.
- `HarmonicClient` for interacting with the Harmonic API.

---

###### `async execute_step_with_input(self, executor, query, dependencies)`
Executes a step using the specified executor (e.g., SQL or API call). If dependencies are provided, they override the query input.

- **Parameters:**
  - `executor` (*str*): Type of executor to use (e.g., `SqlExecutor`, `HarmonicClient`).
  - `query` (*str* | *dict*): The query to execute. For `HarmonicClient`, this should be a dictionary with keys: `method`, `url`, and `body`.
  - `dependencies` (*str* | *list*): Optional dependencies required for execution.
- **Returns:**
  - Result of the executed query or task.
- **Raises:**
  - `ValueError`: If the executor type is unknown.

---

###### `async smart_generate_executions(self, question: str, flow_orchestrator: OpenAIClient, query_generator: OpenAIClient, harmonic_client: HarmonicClient)`
Generates and executes a sequence of steps based on a user query. This method manages dependencies, orchestrates execution, and aggregates results.

- **Parameters:**
  - `question` (*str*): The query or problem statement to resolve.
  - `flow_orchestrator` (*OpenAIClient*): Client for orchestrating the logical flow.
  - `query_generator` (*OpenAIClient*): Client for generating specific queries or API calls.
  - `harmonic_client` (*HarmonicClient*): Client for executing API calls.
- **Returns:**
  - Result of the final step executed.
- **Notes:**
  - Results from previous steps are aggregated and used as dependencies for subsequent steps.

---

###### `async flow_orchestrator(self, question: str, client: OpenAIClient)`
Generates logical steps to answer a given question using the Harmonic API documentation.

- **Parameters:**
  - `question` (*str*): The question to answer.
  - `client` (*OpenAIClient*): Client for interacting with OpenAI's API.
- **Returns:**
  - Raw result from the `query_chat` method of `OpenAIClient`.
  - Expected format: Array of dictionaries containing step details:
    - `step_number` (*int*): Step index.
    - `step_description` (*str*): Description of the step.
    - `rest_api_method` (*str*): HTTP method (e.g., POST, GET, or N/A).
    - `url` (*str*): API endpoint.
    - `pre_condition` (*str*): Preconditions for executing the step.
    - `dependencies` (*list[int]*): List of dependent step numbers.

---

###### `async api_generator(self, task: str, pre_info: str, dependency_data: list[int], client: OpenAIClient)`
Generates API call details based on a task, precondition, and dependency data.

- **Parameters:**
  - `task` (*str*): Description of the task.
  - `pre_info` (*str*): Additional context or preconditions.
  - `dependency_data` (*list[int]*): Data from dependencies.
  - `client` (*OpenAIClient*): Client for API call generation.
- **Returns:**
  - Dictionary containing API call details:
    - `url` (*str*): API endpoint.
    - `method` (*str*): HTTP method (POST or GET).
    - `body` (*str*): Constructed request body.
  - If generation fails, returns a string starting with `Error!!!`.

---

###### `async generic_task(self, task: str, dependency_data: list[int], client: OpenAIClient)`
Executes a generic task based on the provided task description and dependency data.

- **Parameters:**
  - `task` (*str*): Task description.
  - `dependency_data` (*list[int]*): Data from dependencies.
  - `client` (*OpenAIClient*): Client for task execution.
- **Returns:**
  - Result of the executed task.
