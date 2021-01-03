from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import setup, get_session

from random import randint


routes = web.RouteTableDef()


@routes.get("/")
async def index(r: web.Request) -> web.Response:
    s = await get_session(r)
    s["name"] = f"Artyom - {randint(1, 100)}"
    name = s["name"]
    return web.json_response({"name": name, "x": 100, "y": 100, "z": 250, "j": 22})


@routes.get("/name", name="get_name")
async def index(r: web.Request) -> web.Response:
    s = await get_session(r)
    name = s.get("name", "-")
    return web.json_response({"name": name})


@routes.get("/logout")
async def logout(r: web.Request) -> web.Response:
    s = await get_session(r)
    s.pop("name")
    resp = web.HTTPSeeOther(r.app.router["get_name"].url_for())
    return resp


async def init_func(args=None):
    app = web.Application()
    secret_key = b'\xc9\x11\xf3^k\x00\n\xb4l\xd4\xb8\xd5\xaaEY\x91\xbd\xf9\xb2~\x87\xac\xd9u^pn\xe9Ty3Q'
    setup(app, EncryptedCookieStorage(secret_key, cookie_name="react_app_nginx_test"))  # create session concept
    app.add_routes(routes)
    return app


async def init_func_gunicorn():
    app = await init_func()
    return app
