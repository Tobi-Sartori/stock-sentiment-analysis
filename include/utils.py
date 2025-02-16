import openai

from settings.settings import __ENV_SETTINGS__


def _call_fuelix(messages: list):
    client = openai.OpenAI(
        api_key=__ENV_SETTINGS__.FUEL_IX_API_KEY, base_url="https://proxy.fuelix.ai"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.0,
        max_tokens=8192,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content
