from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_services import generate_response, generate_response_stream
from app.core.exception import LLMProviderError
from app.core.rate_limiter import check_rate_limit

app = FastAPI(
    title="Castor",
    description="LLM-backend API",
    version="0.1.0"
)


@app.exception_handler(LLMProviderError)
async def llm_provider_error_handler(
    request: Request,
    exc: LLMProviderError
):
    return JSONResponse(
        status_code=502,
        content={
            "error": "llm_provider_error",
            "detail": str(exc)
        }
    )



@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "Castor"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    client_id = "default-user"

    allowed, retry_after = check_rate_limit(client_id)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "retry_after_seconds": retry_after,
            },
            headers={
                "Retry-After": str(retry_after),
            },
        )

    response = await generate_response(request.message)

    return ChatResponse(
        response=response,
        model="gemini-3.5-flash-lite",
    )


@app.post("/chat/stream")
async def chat_stream(
    request: ChatRequest
):

    return StreamingResponse(
        generate_response_stream(request.message),
        media_type = "text/plain"
    )