from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from User.views import user_router
from Project.views import project_router

from config import mtdp_config

# app = FastAPI(docs_url=None, redoc_url=None, debug=mtdp_config.DEBUG_MODE)
app = FastAPI(title=mtdp_config.APP_TITLE, summary='', description='', version=mtdp_config.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

register_tortoise(app=app, config=mtdp_config.TORTOISE_ORM)

app.include_router(user_router, prefix='/user', tags=['用户接口'])
app.include_router(project_router, prefix='/project', tags=['项目接口'], dependencies=[])

# 初始化
if mtdp_config.DEBUG_MODE is True:
    @app.post('/init', summary='初始化app', description='创建管理员用户,创建PATH', tags=['初始化接口'])
    async def init_app():
        # 通过检查是否存在管理员用户来判断是否初始化过
        Path(mtdp_config.DATASET_PATH).mkdir()
        Path(mtdp_config.PROJECT_PATH).mkdir()
        Path(mtdp_config.ENVIRONMENT_PATH).mkdir()
