from django.urls import path

from . import views
app_name="encyclo"
urlpatterns = [
    path("", views.index, name="index"),
    #path("wiki/", views.wiki, name="wiki"),
    
    path("wiki/<str:title>", views.title,name="title"),
    path("search/", views.search,name="search"),
    path("add_page/", views.createnewpg,name="createnewpg"),
    path("check/", views.check,name="check"),
    path("edit/<str:title_name>", views.editpage,name="editpage"),
    path("/random", views.randompage,name="randompage")
    
]

