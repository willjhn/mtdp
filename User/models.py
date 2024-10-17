from pydantic import BaseModel
from tortoise.models import Model
from tortoise import fields

USER_LEVEL_ADMIN = 'ADMIN'


class UserModel(Model):
    id = fields.BigIntField(primary_key=True)
    email = fields.CharField(max_length=32)
    password = fields.CharField(max_length=32)
    name = fields.CharField(max_length=16)
    level = fields.CharField(max_length=16)
    token = fields.CharField(max_length=32)
    description = fields.CharField(max_length=128, default='')
    delete = fields.BooleanField(default=False)
    create = fields.DatetimeField(auto_now_add=True)
    update = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "USER_MODEL"


class UserInfoJson(BaseModel):
    email: str
    password: str
    name: str
    description: str
