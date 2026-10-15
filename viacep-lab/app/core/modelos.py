from datetime import datetime
from uuid import UUID

from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class Endereco(BaseModel):
    cep: str
    logradouro: str
    bairro: str
    localidade: str
    uf: str


class Consulta(BaseModel):
    id: UUID
    cep: str
    consultado_em: datetime
    encontrado: bool


class Paginacao(BaseModel, Generic[T]):
    itens: list[T]
    pagina: int
    tamanho: int
    total: int
    total_paginas: int
