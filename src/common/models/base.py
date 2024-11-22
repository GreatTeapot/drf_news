from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model. Used to initialize objects in other models.
    """
    objects = models.Manager()

    class Meta:
        abstract = True
