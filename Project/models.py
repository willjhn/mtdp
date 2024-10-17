from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status
from tortoise.models import Model
from tortoise import fields

PROJECT_STATUS_CREATED = 'CREATED'
PROJECT_STATUS_RUNNING = 'RUNNING'
PROJECT_STATUS_FINISHED = 'FINISHED'
PROJECT_STATUS_ERROR = 'ERROR'


class ProjectModel(Model):
    id = fields.BigIntField(primary_key=True)
    name = fields.CharField(max_length=32)
    status = fields.CharField(max_length=16)
    environment = fields.ForeignKeyField('models.EnvironmentModel', related_name='projects')
    dataset = fields.ForeignKeyField('models.DataSetModel', related_name='projects')
    user = fields.ForeignKeyField('models.UserModel', related_name='projects')
    description = fields.CharField(max_length=128, default='')
    delete = fields.BooleanField(default=False)
    create = fields.DatetimeField(auto_now_add=True)
    update = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "PROJECT_MODEL"


class ProjectInputJson(BaseModel):
    project_name: str
    environment_id: int
    dataset_id: int
    description: str = ''

    @classmethod
    @field_validator('project_name')
    def check_project_name(cls, value: str):
        if len(value) == 0 or len(value) > 32:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='check_project_name_项目名格式错误')
        return value

    @classmethod
    @field_validator('description')
    def check_description(cls, value: str):
        if len(value) > 128:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='check_description_描述信息格式错误')
        return value
