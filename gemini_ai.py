from google.generativeai import GenerativeModel
import os
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
model = GenerativeModel(model_name)

def gemini_product_answer(prompt: str, products: list[dict]):
    product_text = "\n".join(
        [f"- {p['name']}: {p['description']} (Rs {p['price']})" for p in products]
    )

    system_instruction = (
        "You are a product information assistant.\n"
        "Only answer about the products listed below.\n"
        "If the user asks anything else, reply:\n"
        "'I can only answer questions about products.'\n\n"
        f"Available products:\n{product_text}\n\n"
    )

    response = model.generate_content(system_instruction + prompt)
    return response.text
