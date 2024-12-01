from api.spectacular.urls import urlpatterns as doc_urls
from users.urls import urlpatterns as user_urls
from news.urls import urlpatterns as news_urls


app_name = 'api'

urlpatterns = []

urlpatterns += doc_urls
urlpatterns += user_urls
urlpatterns += news_urls
