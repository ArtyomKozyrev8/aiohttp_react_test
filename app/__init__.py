from aiohttp import web
from aiohttp import WSMsgType
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import setup, get_session

from random import randint
import asyncio


routes = web.RouteTableDef()


async def send_to_socket(ws: web.WebSocketResponse):
    """helper func which send messages to socket"""
    for i in range(30):
        if ws.closed:
            break
        await ws.send_str("I am super socket server!!")
        await asyncio.sleep(5)


async def listen_to_socket(ws: web.WebSocketResponse):
    """helper func which Listen messages to socket"""
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())


@routes.get("/api/socket", name="socket")  # should be GET !!!
async def websocket_handler(req:  web.Request) -> web.WebSocketResponse:
    """Socket aiohttp handler"""
    ws = web.WebSocketResponse()
    await ws.prepare(req)

    t1 = asyncio.create_task(listen_to_socket(ws))
    t2 = asyncio.create_task(send_to_socket(ws))
    await t1, t2

    return ws


@routes.get("/api/get_val_from_server")
async def get_val_from_server(r: web.Request) -> web.Response:
    return web.json_response({"val": randint(100, 999)})


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
