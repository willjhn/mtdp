from pydantic import BaseModel, Field

from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField


class UserModel(Model):
    id = fields.BigIntField(primary_key=True)
    email = fields.CharField(max_length=32)
    password = fields.CharField(max_length=32)
    name = fields.CharField(max_length=16)
    token = fields.CharField(max_length=32)
    description = fields.CharField(max_length=128, default='')
    project = None
    delete = fields.BooleanField(default=False)

    class Meta:
        table = "USER_MODEL"


class UserInfoJson(BaseModel):
    email: str
    password: str
    name: str
    description: str
