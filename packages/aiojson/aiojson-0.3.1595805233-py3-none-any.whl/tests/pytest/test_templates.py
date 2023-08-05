import aiohttp.web
import pytest

from aiojson import routes
from aiojson.template import JsonTemplate, DataMissing, WrongDataType, UnknownFields


@pytest.mark.parametrize("method", [
    routes.get,
    routes.post,
    routes.patch,
    routes.put,
    routes.delete]
)
async def test_good(aiohttp_client, method):
    routes.routes._items.clear()

    @method("/test")
    @JsonTemplate({
        "interface": str,
        "__required__": ["interface"]
    })
    async def test(request, validated_data):
        return {"interfaces": [validated_data["interface"]]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)('/test', json={"interface": "en2"})
    assert resp.status == 200
    body = await resp.json()
    assert {"error": False, "result": {"interfaces": ["en2"]}} == body


@pytest.mark.parametrize("method", [
    routes.get,
    routes.post,
    routes.patch,
    routes.put,
    routes.delete]
)
async def test_missing_data(aiohttp_client, method):
    routes.routes._items.clear()

    @method("/test")
    @JsonTemplate({
        "interface": str,
        "__required__": ["interface"]
    })
    async def test(request, validated_data):
        return {"interfaces": [validated_data["interface"]]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)('/test', json={"interfaces": "en2"})
    assert resp.status == 400
    body = await resp.json()
    assert {"error": True, "reason": {
        "text": DataMissing.text,
        "path": "interface",
        "code": DataMissing.__name__
    }} == body


@pytest.mark.parametrize("method", [
    routes.get,
    routes.post,
    routes.patch,
    routes.put,
    routes.delete]
)
async def test_unknown_fields(aiohttp_client, method):
    routes.routes._items.clear()

    @method("/test")
    @JsonTemplate({
        "interface": str,
        "__required__": ["interface"]
    }, ignore_unknown=False)
    async def test(request, validated_data):
        return {"interfaces": [validated_data["interface"]]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)('/test', json={
        "interface": "en2",
        "test": True,
        "test2": False
    })
    assert resp.status == 400
    body = await resp.json()
    assert {"error": True, "reason": {
        "text": UnknownFields.text,
        "path": ["test", "test2"],
        "code": UnknownFields.__name__
    }} == body

@pytest.mark.parametrize("method", [
    routes.get,
    routes.post,
    routes.patch,
    routes.put,
    routes.delete]
)
async def test_unknown_fields(aiohttp_client, method):
    routes.routes._items.clear()

    @method("/test")
    @JsonTemplate({
        "interface": int,
        "test": int,
        "__required__": ["interface"]
    }, ignore_unknown=False)
    async def test(request, validated_data):
        return {"interfaces": [validated_data["interface"]]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)('/test', json={
        "interface": ["en2"],
    })
    assert resp.status == 400
    body = await resp.json()
    assert {"error": True, "reason": {
        "text": WrongDataType.text,
        "path": "interface",
        "code": WrongDataType.__name__
    }} == body
