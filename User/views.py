from fastapi import APIRouter, Request, HTTPException

from .models import UserModel, UserInfoJson

user_router = APIRouter()


async def check_user(token: str) -> UserModel:
    """
    """
    user = await UserModel.get_or_none(token=token, delete=False)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail='User_views_check_user_用户不存在')


@user_router.post('/create', summary='创建用户', description='#请求体JSON包括</br>*`用户名`* `user_name`')
async def create_user(user_info: UserInfoJson):
    return user_info.model_dump_json()


@user_router.get('/hello', summary='获取用户信息', description='获取当前登录用户的信息')
async def get_user():
    return 'hello'
