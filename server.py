import asyncio
import os
import aiosqlite
from aiohttp import web
import jinja2
import aiohttp_jinja2
import logging
from logging.handlers import SysLogHandler


log = logging.getLogger('nnn')
router = web.RouteTableDef()


def init_logger():
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = SysLogHandler(address='/dev/log')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

@router.get("/")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request):
    ret = []
    async with aiosqlite.connect('db_test.db') as db:
        async with db.execute("SELECT * FROM status_app") as cursor:
            async for row in cursor:
                ret.append( { "status": 'Сервис работает' if row[1] else 'Сервис остановлен' } )
    return {"response": ret}

@router.get("/start")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request):
    print('start')
    ret = []
    command = 'sudo systemctl start nginx'
    proc = await asyncio.create_subprocess_shell(
        command)
    if not proc.returncode:
        print('sucess')
    async with aiosqlite.connect('db_test.db') as db:
        await db.execute("UPDATE status_app SET status=1 WHERE id=1")
        await db.commit()

    log.debug('Start nginx')
    raise web.HTTPFound('/')

@router.get("/stop")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request):
    print('stop')
    ret = []
    command = 'sudo systemctl stop nginx'
    await asyncio.create_subprocess_shell(
        command)
    async with aiosqlite.connect('db_test.db') as db:
        await db.execute("UPDATE status_app SET status=0 WHERE id=1")
        await db.commit()
    log.debug('Stop nginx')
    raise web.HTTPFound('/')

@router.get("/restart")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request):
    print('restart')
    ret = []
    command =  'sudo systemctl restart nginx'
    await asyncio.create_subprocess_shell(
       command)
    log.debug('Restart nginx')
    raise web.HTTPFound('/')


app = web.Application()

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
    )

app.add_routes(router)

if __name__ == '__main__':
    init_logger()
    web.run_app(app)