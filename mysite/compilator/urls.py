from django.urls import path
from .models import *
from . import views

app_name = 'compilator'

urlpatterns = [
    path('', views.Index, name="index"),
    path('folder/new/', views.NewFolderView, name='new_folder'),
    path('file/new/', views.NewFileView, name='new_file'),
    path('file/sections/', views.FixSections, name='fix_sections'),
    path('file/show/delete/', views.DeleteFile, name ='delete_file'),
    path('folder/show/delete/', views.DeleteFolder, name ='delete_folder'),
    path('file/show/', views.ShowFile, name="show_file"),
    path('file/compile/', views.Compile, name="compile"),
    path('file/download/', views.DownloadFile, name="download_file"),
    path('user/register/', views.Register, name="register"),
    path('user/login/', views.Login, name="login"),
    path('user/logout/', views.Logout, name="logout"),
    path('compilation/standard/', views.Standard, name="standard"),
    path('compilation/optimization/', views.Optimization, name="optimization"),
    path('compilation/procesor/', views.Procesor, name="procesor"),
    path('compilation/dependent/', views.Dependant, name="dependent"),
]