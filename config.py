from pydantic_settings import BaseSettings
from pathlib import Path


class MTDPConfig(BaseSettings):
    DEBUG_MODE: bool = False
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
                'models': ['User.models', 'Project.models', 'Container.models', 'DataSet.models', 'Image.models', 'aerich.models'],
                'default_connection': 'default',
            }
        },
        'use_tz': False,
        'timezone': 'Asia/Shanghai'
    }
    DOCKER_URL: str = 'tcp://192.168.1.172:2375'
    CONFIG_PATH: str = __file__
    CODE_PATH: str = Path(CONFIG_PATH).parent.__str__()
    VENV_DIR: str = 'MTDP_VENVS'
    VENV_PATH: str = Path(CONFIG_PATH).parent.parent.joinpath(VENV_DIR).__str__()


mtdp_config = MTDPConfig()
