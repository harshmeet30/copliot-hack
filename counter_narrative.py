import os
from openai import AzureOpenAI

class CounterNarrativeGenerator:
    def __init__(self, endpoint, deployment, subscription_key):
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=subscription_key,
            api_version="2024-05-01-preview",
        )
        self.deployment = deployment

    def generate_counter_narrative(self, input_text):
        chat_prompt = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant that generates constructive, empathetic, "
                    "and context-aware counter-narratives for the given text. "
                    "Your responses should promote positivity, mutual understanding, and civility. "
                    "If the text is already positive, maintain its tone while offering supportive insights. "
                    "Each counter-narrative should be concise and no more than 3 sentences."
                )
            },
            {
                "role": "user",
                "content": f"Generate a counter-narrative for the following text:\n\n{input_text}\n\nCounter-narrative:"
            }
        ]

        try:
            completion = self.client.chat.completions.create(
                model=self.deployment,
                messages=chat_prompt,
                max_tokens=150,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False
            )
            response_text = completion.choices[0].message.content.strip()
            return response_text

        except Exception as e:
            error_message = str(e)
            if "ResponsibleAIPolicyViolation" in error_message:
                return (
                    "Your input text violates Azure OpenAI's content policy. "
                    "Please rephrase your input to avoid violent, harmful, or inappropriate content."
                )
            return f"An unexpected error occurred: {error_message}"


