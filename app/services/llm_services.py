import os

from dotenv import load_dotenv
from google import genai 
from typing import AsyncGenerator

from app.core.exception import LLMProviderError

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI KEY not found")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"

async def generate_response(
    message: str
) -> str:
    
    try:

        interaction = await client.aio.interactions.create(
            model=MODEL,
            input=message
        )

        return interaction.output_text

    
    except Exception as exc:
        raise LLMProviderError(
            " The LLM provider has failed to generate response "
        ) from exc


async def generate_response_stream(
    message: str,
) -> AsyncGenerator[str, None]:

    try:
        stream = await client.aio.interactions.create(
            model=MODEL,
            input=message,
            stream=True
        )
    
        async for event in stream:
            if event.event_type == "delta":
                if event.delta.type == "text":
                    yield event.delta.text
                
   
    except Exception:
        yield "\n[ERROR: Stream interrupted.]\n"
        