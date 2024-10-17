from asyncio import create_subprocess_exec
from pathlib import Path

from fastapi import APIRouter, Request, BackgroundTasks, HTTPException, Depends, status
from fastapi.responses import Response, JSONResponse
from tortoise.queryset import QuerySetSingle, QuerySet

from .models import ProjectModel, ProjectInputJson, PROJECT_STATUS_CREATED, PROJECT_STATUS_RUNNING, PROJECT_STATUS_FINISHED, PROJECT_STATUS_ERROR
from User.models import UserModel
from Environment.models import EnvironmentModel
from DataSet.models import DataSetModel

from util.check import check_user, check_dataset, check_environment, check_project_for_run
from util.generator import gen
from config import mtdp_config

project_router = APIRouter()


@project_router.post('/create', summary='创建项目', description='#请求体JSON包括</br>*`项目名`* `name`')
async def create_project(project_json: ProjectInputJson, user: UserModel = Depends(check_user)) -> str:
    dataset = await check_dataset(project_json.dataset_id)
    environment = await check_environment(project_json.environment_id)
    project = ProjectModel(
        id=gen.get_int_id(),
        name=project_json.project_name,
        status=PROJECT_STATUS_CREATED,
        environment=environment,
        dataset=dataset,
        user=user,
        description=project_json.description
    )
    await project.save()
    Path(mtdp_config.PROJECT_PATH).joinpath(str(project.id)).mkdir()
    return 'create_project_项目创建成功'


@project_router.get('/get_list', summary='获取项目信息列表', description='获取当前登录用户的所有项目信息列表')
async def get_projects(user: UserModel = Depends(check_user)) -> list[dict]:
    projects: list[ProjectModel] = await user.projects
    projects_json: list[dict] = []
    for project in projects:
        environment: EnvironmentModel = await project.environment
        dataset: DataSetModel = await project.dataset
        project_json = {
            'project_id': project.id,
            'project_name': project.name,
            'project_status': project.status,
            'environment_id': environment.id,
            'environment_name': environment.name,
            'dataset_id': dataset.id,
            'dataset_name': dataset.name,
            'description': project.description
        }
        projects_json.append(project_json)
    return projects_json


@project_router.get('/get/{project_id}', summary='获取单个项目信息', description='获取当前登录用户的单个项目信息列表')
async def get_project() -> dict:
    pass


@project_router.get('/result_url/{project_id}', summary='获取项目结果url', description='获取项目运行结果中的图像的url列表,前端可以通过这些url请求单个图像数据')
async def get_result_url() -> list[str]:
    pass


@project_router.get('/result_image/{project_id}/{image_file}', summary='获取检测好的图像', description='通过url获取图像数据')
async def get_result_image():
    pass


@project_router.post('/run/{project_id}', summary='运行项目', description='通过url中的project_id运行对应项目')
async def run_project(background_tasks: BackgroundTasks, project: ProjectModel = Depends(check_project_for_run)) -> str:
    if project.status == PROJECT_STATUS_FINISHED:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='run_project_项目已运行完成_无法重复运行')
    elif project.status == PROJECT_STATUS_RUNNING:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='run_project_项目正在运行_无法重复运行')
    elif project.status == PROJECT_STATUS_CREATED:
        project.status = PROJECT_STATUS_RUNNING
        await project.save()
        background_tasks.add_task(run_task, project.id)
        return 'run_project_项目已启动'
    elif project.status == PROJECT_STATUS_ERROR:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='run_project_项目运行出错_无法重复运行')
    else:
        pass


async def run_task(project_id: int):
    """
        MTDP
            runserver.py
        MTDP_DATASETS
            {dataset_id}
                1.png
                2.png
        MTDP_PROJECTS
            {project_id}
                1.png
                2.png
        MTDP_ENVIRONMENTS
            {environment_id}
                Libs
                Scripts
                    python.exe
                code
                    main.py

    代码如YOLOv5中的main.py需要自行编写,以实现这样的接口 python main.py --input input_path --output output_path
    input_path 和 output_path 都是绝对路径
    input_path 和 output_path 下都是一些类似图片的资源,不能再包含其他文件夹!
    """
    project: ProjectModel = await ProjectModel.get(id=project_id)
    environment: EnvironmentModel = await project.environment
    dataset: DataSetModel = await project.dataset
    python_path: Path = Path(mtdp_config.ENVIRONMENT_PATH).joinpath(str(environment.id)).joinpath('Scripts').joinpath('python')
    input_path: Path = Path(mtdp_config.DATASET_PATH).joinpath(str(dataset.id))
    output_path: Path = Path(mtdp_config.PROJECT_PATH).joinpath(str(project.id))
    command: list[str] = [str(python_path), 'main.py', '--input', str(input_path), '--output', str(output_path)]
    cwd: Path = Path(mtdp_config.ENVIRONMENT_PATH).joinpath(str(environment.id)).joinpath('code')
    process = await create_subprocess_exec(*command, cwd=cwd)
    return_code: int = await process.wait()
    project: ProjectModel = await ProjectModel.get(id=project_id)
    if return_code == 0:
        project.status = PROJECT_STATUS_FINISHED
    else:
        project.status = PROJECT_STATUS_ERROR
    await project.save()
