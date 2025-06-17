from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('contact/', views.ContactPage.as_view(), name='contact'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('category/', views.CategoryPage.as_view(), name='category'),
    path('single-standard/', views.SingleStandardPage.as_view(), name='single-standard'),
    path('style-guide/', views.StyleGuidePage.as_view(), name='style-guide'),
]