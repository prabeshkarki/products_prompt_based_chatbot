from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Product
from schemas import ProductBase, ProductOut, ChatRequest, ChatResponse
from gemini_ai import gemini_product_answer



app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


# product_crud
@app.post("/products", response_model=ProductOut)
def add_product(prod: ProductBase, db: Session = Depends(get_db)):
    new_prod = Product(**prod.dict())
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    return new_prod

@app.get("/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# chatbot
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    products = db.query(Product).all()

# convert to simple dict for Gemini 
    product_list = [{"name": p.name, "description": p.description, "price": p.price} for p in products]    
    reply = gemini_product_answer(req.message, product_list)
    return ChatResponse(reply=reply)