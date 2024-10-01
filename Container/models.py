from pydantic import BaseModel, Field, field_validator

from tortoise.models import Model
from tortoise import fields


class ContainerModel(Model):
    id = fields.CharField(max_length=64, primary_key=True)
    name = fields.CharField(max_length=32)
    user = fields.ForeignKeyField('models.UserModel', related_name='container_list')
    description = fields.CharField(max_length=128, default='')
    delete = fields.BooleanField(default=False)

    class Meta:
        table = "CONTAINER_MODEL"
