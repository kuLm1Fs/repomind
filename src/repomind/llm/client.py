from openai import OpenAI

def create_client(settings) -> OpenAI:
    return OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        )

def complete(messages: list[dict[str, str]], settings) -> str:
    client = create_client(settings=settings)

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        )
    
    content = response.choices[0].message.content

    return content or ""