from __future__ import annotations

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt import authentication as jwt_authentication

from common.views import mixins
from news.models.news import News
from news.permissions import author as news_permissions
from news.serializers import news as news_serializer


@extend_schema_view(
    create = extend_schema(
        summary='Create a news',
        tags=['News'],
    ),
    update = extend_schema(
        summary='Update a news',
        tags=['News'],
    ),
    list = extend_schema(
        summary='Retrieve a news ',
        tags=['News'],
    ),
    search = extend_schema(
        summary='Search a news ',
        tags=['News'],
))
class NewsViewSet(mixins.CRUDListViewSet,):
    """ViewSet """
    queryset = News.objects.all()
    authentication_classes = (jwt_authentication.JWTAuthentication,)
    permission_classes = (news_permissions.IsAuthor,)
    multi_permission_classes = {
        'search': (AllowAny, IsAuthenticated),
        'list': (IsAuthenticated, AllowAny),
    }
    serializer_class = news_serializer.NewsSerializer
    multi_serializer_class = {
        'list': news_serializer.NewsSerializer,
        'create': news_serializer.NewsCreateSerializer,
        'update': news_serializer.NewsUpdateSerializer,
        'search': news_serializer.NewsSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete')
    ordering = ('title', 'id')


    def filter_queryset(self, queryset):
        """Filter articles based on user authentication"""
        user = self.request.user
        if not user.is_authenticated:
            return queryset.filter(is_publish=True)
        return queryset

    def get_queryset(self):
        """Override to apply filtering logic"""
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)
