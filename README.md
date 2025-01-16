# TenX

![alt text](https://i.imgur.com/O8vZHPM.png)

> This project was built as part of the Data-Driven VC Hackathon organized by [Red River West](https://redriverwest.com) & [Bivwak! by BNP Paribas](https://bivwak.bnpparibas/)

### Concept description

Transform your questions into concrete answers with our intelligent APIs!

Unify your dataset search with natural language. You write your query, and we convert it to 
the relevant SQL, API, GraphQL or other queries.

- Simplify access to complex data: Speak in natural language, and we handle the rest.
- APIs at your service: Take advantage of a vast library of documented APIs, ready to meet your needs.
- Precise and tailored answers: Harness the power of our tools to achieve reliable and fast results.
- Save time and energy: Reduce your searches and maximize your efficiency.

The demo is using [Harmonize api](https://console.harmonic.ai/docs/api-reference/fetch) 
as a dataset example.

### Boot project
1. `python -m venv .`
2. `pip install -r requirements.txt`
3. `source ./bin/activate`
4. Add your **Harmonic** and **OpenAI** keys to the `.env` file
5. Launch the project with `streamlit run interface.py`

### Modular APIs

**We only support Harmonize for now.**

To integrate your own data provider APIs, you must:
1. Include the secrets to the .env file
2. 

