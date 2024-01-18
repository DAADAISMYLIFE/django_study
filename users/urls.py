from django.urls import path
from . import views

urlpatterns = [
    path("view", views.UserGet.as_view()),
    path("create", views.UserPost.as_view()),
    path("update", views.UserPut.as_view()),
    path("delete", views.UserDel.as_view()),
]
