# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# Ajuste usuário, senha, host, porta e nome do banco conforme seu ambiente
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/veiculos_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()