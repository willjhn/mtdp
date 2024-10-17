from asyncio import create_subprocess_exec
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks

environment_router = APIRouter()


@environment_router.post('/create', summary='', description='')
async def create_environment() -> str:
    pass


@environment_router.post('/upload_code/{environment_id}', summary='', description='')
async def upload_code():
    pass

# import asyncio
# import os
# import sys
# import venv
#
# print(os.getcwd())
# venv.create('./tmp/xenv', clear=True, with_pip=True)
# command = ['tmp/xenv/Scripts/pip', '-V']
# command = ['tmp/xenv/Scripts/python', '-m', 'pip', 'install', 'pyhuajiguai']
# command = ['tmp/xenv/Scripts/python', 'p.py']
# process = await asyncio.create_subprocess_exec(*command, cwd='./tmp')
# code = await process.wait()
# print(code, '----------')
