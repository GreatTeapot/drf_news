from __future__ import annotations

from django.db import models

from common.models.base import BaseModel
from config import settings


class News(BaseModel):
    title = models.CharField(max_length=200,
                             null=False,
                             blank=False,
                             unique=True
                             )
    content = models.TextField()
    is_publish = models.BooleanField(default=False)
    author_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='news',
                                  verbose_name='author',
                                  null=True,
                                  blank=True,)

    class Meta:
        verbose_name = 'News parameters'
        indexes = [
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return (f'{self.title}'
                f'({self.is_publish})'
                f'({self.author_id})')

