from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductOut(ProductBase):
    id: int

    # class Config:
    #     orm_mode = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    