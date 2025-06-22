from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('contact/', views.ContactPage.as_view(), name='contact'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('category/', views.CategoryPage.as_view(), name='category'),
    path('single-standard/', views.SingleStandardPage.as_view(), name='single-standard'),
    path('style-guide/', views.StyleGuidePage.as_view(), name='style-guide'),

    path('article/', views.SingleArticleApiView.as_view(), name='single_article'),
    path('article/all/', views.AllArticleApiView.as_view(), name='all_article'),
    path('article/search/', views.SearchArticleApiView.as_view(), name='search_article'),
    path('article/submit/', views.SubmitArticleApiView.as_view(), name='submit_article'),
    path('article/update-cover/', views.UpdateArticleApiView.as_view(), name='update_article'),
    path('article/delete/', views.DeleteArticleApiView.as_view(), name='delete_article'),
]