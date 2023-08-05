import aiohttp.web
import pytest

from aiojson import routes
from aiojson.exception import ApiException


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
    async def test(request):
        return {"interfaces": ["en2"]}

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)('/test')
    assert resp.status == 200
    body = await resp.json()
    assert {"error": False, "result": {"interfaces": ["en2"]}} == body


@pytest.mark.parametrize("method", [
    routes.get,
    routes.post,
    routes.patch,
    routes.put,
    routes.delete],
)
@pytest.mark.parametrize("exception", [ApiException, Exception])
async def test_bad_exceptions(aiohttp_client, method, exception):

    routes.routes._items.clear()

    error_message = {"missing_fields": "test", "text": "Some required fields are missing"}

    @method("/test")
    async def test(request):
        raise exception(error_message)

    app = aiohttp.web.Application()
    app.router.add_routes(routes.routes)
    client = await aiohttp_client(app)
    resp = await getattr(client, method.__name__)('/test')
    assert resp.status == 400 if exception == Exception else 500
    body = await resp.json()
    if exception == Exception:
        assert {"error": True, "reason": "Something went wrong. Please try again later"} == body
    else:
        assert {"error": True, "reason": error_message} == body
