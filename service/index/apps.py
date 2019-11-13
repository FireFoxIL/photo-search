from django.apps import AppConfig

from ml.core import FaceRegModel


class MachineLearningModel(AppConfig):
    name = 'facereg'
    face_reg = FaceRegModel()
