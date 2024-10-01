from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from User.models import UserModel
from User.views import user_router
from Project.views import project_router

from config import mtdp_config

# app = FastAPI(docs_url=None, redoc_url=None, debug=mtdp_config.DEBUG_MODE)
app = FastAPI()

app.include_router(user_router, prefix='/user', tags=['用户接口'])
app.include_router(project_router, prefix='/project', tags=['项目接口'])

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# @app.middleware("http")
# async def check_user(request: Request, call_next):
#     """
#     中间件中的request和路径函数中的request,不是同一个对象
#     所以不能request.user = user
#     """
#     token = request.headers.get('token')
#     user = await UserModel.get_or_none(token=token, delete=False)
#     if user:
#         response = await call_next(request)
#         return response
#     else:
#         raise HTTPException(status_code=404, detail='middleware_check_user_用户不存在')


register_tortoise(app=app, config=mtdp_config.TORTOISE_ORM)
