from django.urls import path

from . import views
from .views import search

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.funct, name="funct"),
    path("search", views.search, name="search"),
    path("random", views.random,name="random"),
    path("newpage", views.newpage, name="newpage"),
    path("wiki/<str:name>/edit", views.edit, name="edit")
]
