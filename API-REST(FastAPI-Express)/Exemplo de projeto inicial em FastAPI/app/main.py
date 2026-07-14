# app/main.py
from fastapi import FastAPI
from app.routers import veiculos
from app.database import Base, engine
from app import models
 
app = FastAPI(
    title="API de Veículos",
    description="API construída na disciplina de PABD - TADS/IFRN",
    version="1.0.0",
)
 
app.include_router(veiculos.router)
 
 
@app.get("/")
def read_root():
    return {"mensagem": "API de Veículos no ar!"}

Base.metadata.create_all(bind=engine)