import logging
from functools import wraps

import aiohttp.web

from aiojson.response import BadResponse, GoodResponse
from aiojson.exception import ApiException

routes = aiohttp.web.RouteTableDef()

log = logging.getLogger("aiojson." + __name__)


def route(method, path, **kwargs):
    def func_wrap(func):
        async def arg_wrap(*inner_args, **inner_kwargs):
            try:
                result = await func(*inner_args, **inner_kwargs)
                if isinstance(result, aiohttp.web.Response):
                    return result
                return GoodResponse(result)
            except ApiException as e:
                return BadResponse(e.message, status=e.status)
            except Exception as e:
                log.exception(e)
                return BadResponse("Something went wrong. Please try again later")

        func_wrap.__dict__ = arg_wrap.__dict__
        func_wrap.__name__ = arg_wrap.__name__
        func_wrap.__doc__ = arg_wrap.__doc__
        func_wrap.__defaults__ = arg_wrap.__defaults__
        return method(path, **kwargs)(arg_wrap)
    return func_wrap


def get(path: str, **kwargs):
    return route(routes.get, path, **kwargs)


def post(path: str, **kwargs):
    return route(routes.post, path, **kwargs)


def delete(path: str, **kwargs):
    return route(routes.delete, path, **kwargs)


def put(path: str, **kwargs):
    return route(routes.put, path, **kwargs)


def patch(path: str, **kwargs):
    return route(routes.patch, path, **kwargs)


def head(path: str, **kwargs):
    return route(routes.head, path, **kwargs)


def view(path: str, **kwargs):
    return route(routes.view, path, **kwargs)
