from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from news.views.news import NewsViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
]
