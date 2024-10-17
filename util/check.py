from fastapi import Header, HTTPException, Depends, status
from tortoise.queryset import QuerySetSingle, QuerySet

from User.models import UserModel
from Project.models import ProjectModel
from DataSet.models import DataSetModel
from Environment.models import EnvironmentModel


async def check_user(token: str = Header(default=None)) -> UserModel | None:
    if token is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='check_user_TOKEN不存在')
    user = await UserModel.get_or_none(token=token, delete=False)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='check_user_用户不存在')
    return user


async def check_project(project_id: int) -> ProjectModel | None:
    project = await ProjectModel.get_or_none(id=project_id, delete=False)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='check_project_项目不存在')
    return project


async def check_dataset(dataset_id: int) -> DataSetModel | None:
    dataset = await DataSetModel.get_or_none(id=dataset_id, delete=False)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='check_dataset_数据集不存在')
    return dataset


async def check_environment(environment_id: int) -> EnvironmentModel | None:
    environment = await EnvironmentModel.get_or_none(id=environment_id, delete=False)
    if environment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='check_environment_运行环境不存在')
    return environment


async def check_project_for_run(project_id: int, user: UserModel = Depends(check_user)) -> ProjectModel | None:
    """
    判断url中的project_id对应的项目是否属于登录用户
    """
    project = await check_project(project_id)
    if project.user.id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='check_project_for_run_项目不属于当前用户')
    return project
