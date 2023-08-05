import aiohttp.web
import pytest

from aiojson.middleware import error_middleware


async def test_good404(aiohttp_client):

    app = aiohttp.web.Application(middlewares=[error_middleware])
    client = await aiohttp_client(app)
    resp = await client.get('/test3123')
    assert resp.status == 404
    body = await resp.json()
    assert {"error": True, "reason": {"text": "Not Found", "code": "NotFound"}} == body
