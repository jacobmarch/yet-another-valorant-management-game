from pydantic import BaseModel, Field

class Player(BaseModel):
    first_name: str
    last_name: str
    username: str
    rating: int = Field(ge=1, le=100)
    role: str = Field(min_length=3, max_length=10)