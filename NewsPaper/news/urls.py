from django.urls import path
from .views import PostsList, PostDetail, PostsSearchList, PostCreate, PostUpdate, PostDelete, subscription


urlpatterns = [
    # path означает "путь". В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    path('', PostsList.as_view()),  # Основная страница.
    path('<int:pk>', PostDetail.as_view(), name='post'),  # Вывод по одному объекту
    path('search/', PostsSearchList.as_view(), name='posts_filters'),  # Поиск объектов
    path('add/', PostCreate.as_view(), name='post_create'),  # Создание объектов
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),  # Редактирование объектов
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),  # Удаление объектов as_view()!!!
    path('subscription/', subscription, name='subscription'),  # поле подписаться
            ]
