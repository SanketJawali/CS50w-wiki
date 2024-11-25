from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.displayPage, name="display"),
    path("wiki/", views.redirect, name="all_wiki"),
]
