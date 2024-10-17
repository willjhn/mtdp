from pathlib import Path
from pydantic_settings import BaseSettings


class MTDPConfig(BaseSettings):
    TORTOISE_ORM: dict = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': '127.0.0.1',
                    'port': '5432',
                    'user': 'postgres',
                    'password': 'postgres',
                    'database': 'mtdpdb',
                }
            },
        },
        'apps': {
            'models': {
                'models': ['User.models', 'Project.models', 'Environment.models', 'DataSet.models', 'aerich.models'],
                'default_connection': 'default',
            }
        },
        'use_tz': False,
        'timezone': 'Asia/Shanghai'
    }
    # DOCKER_URL: str = 'tcp://192.168.1.172:2375'

    APP_TITLE: str = '探地雷达图像检测'
    APP_VERSION: str = '0.1.0'
    DEBUG_MODE: bool = False

    CONFIG_PATH: str = __file__
    ENVIRONMENT_DIR: str = 'MTDP_ENVIRONMENTS'
    ENVIRONMENT_PATH: str = Path(CONFIG_PATH).parent.parent.joinpath(ENVIRONMENT_DIR).__str__()
    DATASET_DIR: str = 'MTDP_DATASETS'
    DATASET_PATH: str = Path(CONFIG_PATH).parent.parent.joinpath(DATASET_DIR).__str__()
    PROJECT_DIR: str = 'MTDP_PROJECTS'
    PROJECT_PATH: str = Path(CONFIG_PATH).parent.parent.joinpath(PROJECT_DIR).__str__()


mtdp_config = MTDPConfig()

TORTOISE_ORM = mtdp_config.TORTOISE_ORM
