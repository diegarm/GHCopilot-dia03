from fastapi import APIRouter, Depends, Query

from app.api.dependencias import obter_listar_consultas
from app.core.casos_uso.listar_consultas import ListarConsultas
from app.core.comum import Resultado
from app.core.modelos import Consulta, Paginacao

rotas = APIRouter(tags=["consultas"])


# Historico paginado para manter a resposta leve mesmo com muitos registros.
@rotas.get("/consultas", response_model=Resultado[Paginacao[Consulta]])
async def listar_consultas(
    caso: ListarConsultas = Depends(obter_listar_consultas),
    pagina: int = Query(default=1, ge=1),
    tamanho: int = Query(default=10, ge=1, le=100),
) -> Resultado[Paginacao[Consulta]]:
    return await caso.executar(pagina=pagina, tamanho=tamanho)
