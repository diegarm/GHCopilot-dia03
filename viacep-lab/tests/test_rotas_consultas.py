import httpx
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_listar_consultas_com_historico_populado_retorna_primeira_pagina():
    transporte = httpx.ASGITransport(app=app)

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=transporte, base_url="http://teste") as cliente:
            resposta = await cliente.get("/consultas")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["sucesso"] is True
    assert corpo["dados"]["pagina"] == 1
    assert corpo["dados"]["tamanho"] == 10
    assert corpo["dados"]["total"] == 42
    assert corpo["dados"]["total_paginas"] == 5
    assert len(corpo["dados"]["itens"]) == 10


@pytest.mark.asyncio
async def test_listar_consultas_com_parametros_retorna_subconjunto_correspondente():
    transporte = httpx.ASGITransport(app=app)

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=transporte, base_url="http://teste") as cliente:
            resposta = await cliente.get("/consultas", params={"pagina": 2, "tamanho": 15})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["dados"]["pagina"] == 2
    assert corpo["dados"]["tamanho"] == 15
    assert corpo["dados"]["total"] == 42
    assert corpo["dados"]["total_paginas"] == 3
    assert len(corpo["dados"]["itens"]) == 15
