from __future__ import annotations
from django.contrib import admin
from news.models.news import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publish', 'author_id')
    search_fields = ('title',)
    list_filter = ('is_publish',)


admin.site.register(News, NewsAdmin)
