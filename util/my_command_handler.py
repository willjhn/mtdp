import sys
from asyncio import subprocess
from pydantic import BaseModel

project_info = {}


class CommandJson(BaseModel):
    project_id: int
    dataset_id: int


async def handle_command(command: CommandJson):
    """
    后端传入运行YOLO的指令
    指令格式
    {
        "project_id": 123456,
        "dataset_id": 123456
    }

    project_info status包括 running, finished, error
    {
        123456: {
            "dataset_id": 123456,
            "status": "running",
        }
    }
    """

    if command.project_id in project_info:
        if project_info.get(command.project_id).get('status') == 'running':
            return f''
        elif project_info.get(command.project_id).get('status') == 'finished':
            return f''
        elif project_info.get(command.project_id).get('status') == 'error':
            # 尝试重新检测
            project_info[command.project_id]['status'] = 'running'
            return await start_process(command.project_id, command.dataset_id)
        else:
            return 'pass'
    else:
        project_info[command.project_id] = {'status': 'running', 'dataset_id': command.dataset_id}
        return await start_process(command.project_id, command.dataset_id)


async def start_process(project_id: int, dataset_id: int):
    cmd = f'{sys.executable} ./tmp/p.py'
    proc = await subprocess.create_subprocess_shell(cmd)
    ret_code = await proc.wait()
    if ret_code == 0:
        project_info[project_id]['status'] = 'finished'
        return f''
    else:
        project_info[project_id]['status'] = 'error'
        return f''


async def get_projects_info(project_id: int):
    return project_info.get(project_id).get('status')
