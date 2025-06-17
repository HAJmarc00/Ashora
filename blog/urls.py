from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('contact/', views.ContactPage.as_view(), name='contact'),
]