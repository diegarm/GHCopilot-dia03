from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.core.casos_uso.listar_consultas import ListarConsultas
from app.core.modelos import Consulta


class RepositorioFalso:
    def __init__(self, consultas: list[Consulta]) -> None:
        self._consultas = consultas

    async def listar(self) -> list[Consulta]:
        return self._consultas


def _consulta(indice: int) -> Consulta:
    return Consulta(
        id=uuid4(),
        cep=f"000000{indice:02d}",
        consultado_em=datetime(2026, 1, 1, 12, indice, tzinfo=timezone.utc),
        encontrado=True,
    )


@pytest.mark.asyncio
async def test_executar_sem_parametros_retorna_primeira_pagina_padrao():
    consultas = [_consulta(indice) for indice in range(12)]
    caso = ListarConsultas(RepositorioFalso(consultas))

    resultado = await caso.executar()

    assert resultado.sucesso is True
    assert resultado.dados is not None
    assert resultado.dados.pagina == 1
    assert resultado.dados.tamanho == 10
    assert resultado.dados.total == 12
    assert resultado.dados.total_paginas == 2
    assert [consulta.cep for consulta in resultado.dados.itens] == [
        "00000000",
        "00000001",
        "00000002",
        "00000003",
        "00000004",
        "00000005",
        "00000006",
        "00000007",
        "00000008",
        "00000009",
    ]


@pytest.mark.asyncio
async def test_executar_com_pagina_e_tamanho_retorna_fatia_correta():
    consultas = [_consulta(indice) for indice in range(12)]
    caso = ListarConsultas(RepositorioFalso(consultas))

    resultado = await caso.executar(pagina=2, tamanho=5)

    assert resultado.sucesso is True
    assert resultado.dados is not None
    assert resultado.dados.pagina == 2
    assert resultado.dados.tamanho == 5
    assert resultado.dados.total == 12
    assert resultado.dados.total_paginas == 3
    assert [consulta.cep for consulta in resultado.dados.itens] == [
        "00000005",
        "00000006",
        "00000007",
        "00000008",
        "00000009",
    ]