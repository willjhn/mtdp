from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response, JSONResponse
from tortoise.queryset import QuerySetSingle, QuerySet

from aiohttp import ClientSession
from docker.models.containers import Container

from .models import ProjectModel, ProjectInputJson
from User.models import UserModel
from Container.models import ContainerModel
from DataSet.models import DataSetModel
from User.views import check_user

from Docker.client import docker_client
from util.generator import gen

from json import dumps

project_router = APIRouter()


async def check_container(container_id: str) -> ContainerModel:
    container = await ContainerModel.get_or_none(id=container_id)
    if container:
        return container
    else:
        raise HTTPException(status_code=404, detail='check_container_容器不存在')


async def check_dataset(dataset_id: int) -> DataSetModel:
    dataset = await DataSetModel.get_or_none(id=dataset_id)
    if dataset:
        return dataset
    else:
        raise HTTPException(status_code=404, detail='check_dataset_数据集不存在')


async def check_project(project_id: int) -> ProjectModel:
    project = await ProjectModel.get_or_none(id=project_id)
    if project:
        return project
    else:
        raise HTTPException(status_code=404, detail='check_project_项目不存在')


@project_router.post('/create', summary='创建项目', description='#请求体JSON包括</br>*`项目名`* `name`')
async def create_project(request: Request, project_input_json: ProjectInputJson) -> str:
    user = check_user(request.headers.get('token'))
    dataset = await check_dataset(project_input_json.dataset_id)
    container = await check_container(project_input_json.container_id)
    project = ProjectModel(
        id=gen.get_int_id(),
        name=project_input_json.project_name,
        container=container,
        dataset=dataset,
        user=user,
        description=project_input_json.description
    )
    await project.save()
    return 'create_project_项目创建成功'


@project_router.get('/get_list', summary='获取项目信息列表', description='获取当前登录用户的所有项目信息列表')
async def get_project_list(request: Request):
    user: UserModel = await check_user(request.headers.get('token'))
    project_list: list[ProjectModel] = await user.project_list
    project_output_list_json: list[dict] = []
    for project in project_list:
        container: ContainerModel = await project.container
        dataset: DataSetModel = await project.dataset
        user: UserModel = await project.user
        project_output_dict = {
            'project_id': project.id,
            'project_name': project.name,
            'container_id': container.id,
            'container_name': container.name,
            'dataset_id': dataset.id,
            'dataset_name': dataset.name,
            'user_id': user.id,
            'user_name': user.name,
            'description': project.description
        }
        project_output_list_json.append(project_output_dict)
    return project_output_list_json


@project_router.post('/run/{project_id}', summary='运行项目', description='通过url中的project_id运行对应项目')
async def run_project(request: Request, project_id: int) -> str:
    """
    运行通过关联 数据集 和 容器的 项目
    启动后立即返回

    运行项目时,规定一个路径(数据卷)来存放数据集和 训练/检测结果
    容器中的python项目代码中 是否要 返回一个信号, 通知后端数据结果?


    created（已创建）：
    当您使用 docker create 命令创建一个容器但尚未启动它时，容器处于此状态。容器的文件系统结构和配置已经准备完毕，但是还没有开始运行任何进程。
    restarting（重启中）：
    此状态表明容器正在尝试按照其重启策略进行重启。可能是由于容器意外退出，或者由于某种原因被触发了重启。
    running（运行中）：
    容器已成功启动并正在运行其主进程。容器内的服务或应用处于活跃状态，可以正常提供服务。
    removing（迁移中）：
    当发出 docker rm 或 docker stop 命令并带有 -t 参数（等待一定时间后自动移除容器）时，容器会在停止后进入移除队列，这时显示为“迁移中”。此状态意味着Docker正在清除与该容器相关的资源。
    paused（暂停）：
    容器被挂起，其进程暂停运行，但仍保留在内存中。容器可以随时恢复到运行状态，而不需要重新启动进程。
    exited（停止）：
    容器已停止运行，它的主进程已经退出。退出状态码会与容器一同记录下来，可通过 docker inspect 查看。容器虽已停止，但其文件系统仍被保留。
    dead（死亡）：
    容器已经停止，并且其曾经运行过的进程也无法再次启动，通常是因为容器内部发生了严重的错误或者其所在的Docker守护进程本身出现问题。
    """
    user = await check_user(request.headers.get('token'))
    project = await check_project(project_id)
    container: ContainerModel = await project.container
    dataset: DataSetModel = await project.dataset
    # 通过数据库中的字段判断project是否start
    if project.status == 'finished':
        return f'run_project_项目已完成,无法再次运行'
    elif project.status == 'running':
        return f'run_project_项目正在运行,无法多次启动'
    elif project.status == 'created':
        pass
    elif project.status == 'error':
        pass
    else:
        raise HTTPException(status_code=, detail=f'run_project_status错误')
    #
    container: Container = docker_client.containers.get(container_id=container.id)
    if container.status != 'running':
        # 尝试启动容器
        container.start()
        if docker_client.containers.get(container_id=container.id).status != 'running':
            raise HTTPException(status_code=500, detail='run_project_容器无法启动')
    command_body: bytes = dumps({'project_id': project.id, 'dataset_id': dataset.id}).encode()
    host: str = container.attrs.get('NetworkSettings').get('IPAddress')
    response = await send_command(host=host, body=command_body)
    if

    return


async def send_command(host: str, body: bytes, port: int = 5000, router: int = 'detect'):
    async with ClientSession() as session:
        async with session.post(f'http://{host}:{port}/{router}', data=body) as response:
            return await response.text()
