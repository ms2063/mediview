from django.urls import path
from posts.views import ask, post_add, post_detail

urlpatterns = [
    path('ask/',ask,name='ask'),
    path('post_add/',post_add,name='post_add'),
    path('posts/<int:post_id>/',post_detail,name='post_detail'),
]
