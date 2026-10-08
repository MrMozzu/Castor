from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    
    message: str = Field(
        ..., 
        min_length=1,
        description="The user's message."
    )


class ChatResponse(BaseModel):

    response: str
    model: str