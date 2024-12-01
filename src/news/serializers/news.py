
from rest_framework import serializers
from news.models.news import News

class NewsSerializer(serializers.ModelSerializer):
    """Serializer for the News model"""

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'is_publish', 'author_id', 'created_at']
        read_only_fields = ['author_id']


class NewsCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating """
    author_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'is_publish', 'author_id']


class NewsUpdateSerializer(NewsCreateSerializer):
    pass