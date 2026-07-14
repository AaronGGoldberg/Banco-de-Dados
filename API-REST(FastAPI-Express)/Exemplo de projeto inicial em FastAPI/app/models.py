# app/models.py
from pydantic import BaseModel, Field
from typing import Optional

from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class VeiculoORM(Base):
    __tablename__ = "veiculos"
    
    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(8), unique=True, nullable=False, index=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    ano_fabricacao = Column(Integer, nullable=False)
    cor = Column(String(30), nullable=False)
    quilometragem = Column(Float, default=0.0, nullable=False)
 
 
class VeiculoBase(BaseModel):
    # ... note:: O Pydantic é usado para validação de dados e definição de schemas.
    # ... note:: O Field é usado para definir restrições e exemplos de cada campo. 
    # Como campo   obrigatório, usamos o valor `...` (ellipsis) para indicar que o campo é obrigatório.
    # Placa do veículo: formato Mercosul (7) ou antigo com hífen (8 chars)
    placa: str = Field(..., min_length=7, max_length=8, examples=["ABC1D23"])
    # Marca fabricante: entre 2 e 50 caracteres
    marca: str = Field(..., min_length=2, max_length=50)
    # Nome do modelo: entre 1 e 50 caracteres
    modelo: str = Field(..., min_length=1, max_length=50)
    # Ano de fabricação: entre 1950 e 2026
    ano_fabricacao: int = Field(..., ge=1950, le=2026)
    # Cor do veículo: até 30 caracteres
    cor: str = Field(..., max_length=30)
    # Quilometragem rodada: não pode ser negativa, padrão 0
    quilometragem: float = Field(default=0.0, ge=0)
 
 
class VeiculoCreate(VeiculoBase):
    """Schema usado na criação (POST)."""
    pass
 
 
class VeiculoUpdate(BaseModel):
    """Schema usado na atualização parcial (PATCH) - todos os campos opcionais."""
    placa: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano_fabricacao: Optional[int] = None
    cor: Optional[str] = None
    quilometragem: Optional[float] = None
 
 
class Veiculo(VeiculoBase):
    """Schema de resposta (inclui o identificador gerado pelo servidor)."""
    id: int
    class Config:
        from_attributes = True

