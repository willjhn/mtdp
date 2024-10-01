from pydantic import BaseModel, Field, field_validator

from tortoise.models import Model
from tortoise import fields


class DataSetModel(Model):
    id = fields.BigIntField(primary_key=True)
    name = fields.CharField(max_length=32)
    user = fields.ForeignKeyField('models.UserModel', related_name='dataset_list')
    description = fields.CharField(max_length=128, default='')
    delete = fields.BooleanField(default=False)

    class Meta:
        table = "DATASET_MODEL"
