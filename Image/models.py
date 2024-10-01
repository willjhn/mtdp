from pydantic import BaseModel, Field, field_validator

from tortoise.models import Model
from tortoise import fields


class ImageModel(Model):
    id = fields.CharField(max_length=64, primary_key=True)
    name = fields.CharField(max_length=32)
    description = fields.CharField(max_length=128, default='')
    delete = fields.BooleanField(default=False)

    class Meta:
        table = "IMAGE_MODEL"
