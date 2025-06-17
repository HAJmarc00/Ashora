from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
]