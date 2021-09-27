import asyncio
import os
from typing import Dict

import aiosqlite
from aiohttp import web
import jinja2
import aiohttp_jinja2
import sqlite3

import subprocess


router = web.RouteTableDef()

@router.get("/")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request):
    ret = []
    async with aiosqlite.connect('db_test.db') as db:
        async with db.execute("SELECT * FROM status_app") as cursor:
            async for row in cursor:
                ret.append(
                    {
                        "status": row[1],
                    }
                )
    return {"posts": ret}

@router.get("/start")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request):
    ret = []
    async with aiosqlite.connect('db_test.db') as db:
        await db.execute("UPDATE status_app SET status=1 WHERE id=1")
        await db.commit()

    raise web.HTTPFound('/')

@router.get("/stop")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request):
    ret = []
    async with aiosqlite.connect('db_test.db') as db:
        await db.execute("UPDATE status_app SET status=0 WHERE id=1")
        await db.commit()

    raise web.HTTPFound('/')

@router.get("/restart")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request):
    ret = []
    proc = await asyncio.create_subprocess_shell(
        'sudo systemctl restart cron.service')
    print(proc)
    stdout, stderr = await proc.communicate()

    print(f'[sudo systemctl stop nginx exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')



    raise web.HTTPFound('/')



app = web.Application()

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
    )


app.add_routes(router)


if __name__ == '__main__':
    web.run_app(app)