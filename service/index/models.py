from uuid import uuid4

from django.db import models
from django.contrib.postgres.fields import ArrayField

__all__ = ['ImageIndex', 'FaceIndex']


class ImageIndex(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d")


class FaceIndex(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    image_id = models.ForeignKey(ImageIndex, on_delete=models.CASCADE)
    face_vector = ArrayField(models.FloatField(null=False))
