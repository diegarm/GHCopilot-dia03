from math import ceil

from app.core.comum import Resultado
from app.core.contratos import ConsultaRepositorio
from app.core.modelos import Consulta, Paginacao


class ListarConsultas:
    def __init__(self, repositorio: ConsultaRepositorio) -> None:
        self._repositorio = repositorio

    async def executar(self, pagina: int = 1, tamanho: int = 10) -> Resultado[Paginacao[Consulta]]:
        consultas = await self._repositorio.listar()
        total = len(consultas)
        total_paginas = ceil(total / tamanho) if total else 0
        inicio = (pagina - 1) * tamanho
        fim = inicio + tamanho

        return Resultado[Paginacao[Consulta]].ok(
            Paginacao[Consulta](
                itens=consultas[inicio:fim],
                pagina=pagina,
                tamanho=tamanho,
                total=total,
                total_paginas=total_paginas,
            )
        )
