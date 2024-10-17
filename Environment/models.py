from tortoise.models import Model
from tortoise import fields


class EnvironmentModel(Model):
    id = fields.BigIntField(primary_key=True)
    name = fields.CharField(max_length=32)
    user = fields.ForeignKeyField('models.UserModel', related_name='environments')
    code = fields.BooleanField(default=False)
    description = fields.CharField(max_length=128, default='')
    delete = fields.BooleanField(default=False)
    create = fields.DatetimeField(auto_now_add=True)
    update = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "ENVIRONMENT_MODEL"
