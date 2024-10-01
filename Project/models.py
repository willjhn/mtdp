from pydantic import BaseModel, Field, field_validator

from tortoise.models import Model
from tortoise import fields


class ProjectModel(Model):
    id = fields.BigIntField(primary_key=True)
    name = fields.CharField(max_length=32)
    status = fields.CharField(max_length=16)
    container = fields.ForeignKeyField('models.ContainerModel', related_name='project_list')
    dataset = fields.ForeignKeyField('models.DataSetModel', related_name='project_list')
    user = fields.ForeignKeyField('models.UserModel', related_name='project_list')
    description = fields.CharField(max_length=128, default='')
    delete = fields.BooleanField(default=False)

    class Meta:
        table = "PROJECT_MODEL"


class ProjectInputJson(BaseModel):
    project_name: str
    container_id: str
    dataset_id: int
    description: str = ''

    @field_validator('container_id')
    def test(cls, value):
        assert len(value) == 64, 'field_validator_container_id'
        return value


class ProjectOutputJson(BaseModel):
    project_name: str
    container_id: str
    dataset_id: int
    description: str = ''
