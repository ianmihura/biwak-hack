from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def query_chat(self, messages: list, max_tokens: int = 150, temperature: float = 0.7):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return completion.choices[0].message["content"].strip()
        except Exception as e:
            return f"An error occurred: {e}"


if __name__ == "__main__":
    API_KEY = "oIFYr6dvblfyiLBWRypP+n9ENfeY8LHKNwrYw+dLBQg="
    client = OpenAIClient(api_key=API_KEY)

    # Sample messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."}
    ]

    # Query the client
    # response = client.query_chat(messages)
    # print(response)
