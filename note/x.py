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


"""
测试，上传github
"""
