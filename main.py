from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os

class Supplier(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    contact_info: str
    product_categories: str

class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    brand: str
    price: float
    category: str
    description: str
    supplier_id: int = Field(foreign_key="supplier.id")

app = FastAPI()
database_url = "sqlite:///./test.db"  
engine = create_engine(database_url, echo=True)
SQLModel.metadata.create_all(engine)

llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

@app.get("/products/")
async def get_products(brand: str = None):
    with Session(engine) as session:
        query = select(Product)
        if brand:
            query = query.where(Product.brand == brand)
        products = session.exec(query).all()

        if not products:
            raise HTTPException(status_code=404, detail="No products found.")

        return products

@app.get("/suppliers/")
async def get_suppliers(category: str = None):
    with Session(engine) as session:
        query = select(Supplier)
        if category:
            query = query.where(Supplier.product_categories.contains(category))
        suppliers = session.exec(query).all()

        if not suppliers:
            raise HTTPException(status_code=404, detail="No suppliers found.")

        return suppliers

@app.get("/summarize/")
async def summarize_product(product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")

        summary = llm(f"Summarize this product: {product.description}")
        return {"product": product, "summary": summary}