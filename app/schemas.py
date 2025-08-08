from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field

class LibroCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=255)
    autor_nombre: str = Field(..., min_length=1, max_length=100)
    autor_apellido: str = Field(..., min_length=1, max_length=100)
    nacionalidad: Optional[str] = Field(None, max_length=100)
    anio_publicacion: Optional[int] = Field(None, ge=0, le=9999)
    precio: Optional[Decimal] = None

class LibroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=255)
    anio_publicacion: Optional[int] = Field(None, ge=0, le=9999)

class LibroOut(BaseModel):
    id: int
    titulo: str
    autor: str
