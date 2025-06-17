from operator import index
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

class IndexPage(TemplateView):

    def get(self, request, **kwargs):

        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')[:9]

        for article in all_articles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        promote_data = []
        all_promote_article = Article.objects.filter(promote=True)
        for promote_article in all_promote_article:
            promote_data.append({
                'category': promote_article.category.title,
                'title': promote_article.title,
                'author': promote_article.author.user.first_name + ' ' + promote_article.author.user.last_name,
                'avatar': promote_article.author.avatar.url if promote_article.author.avatar else None,
                'created_at': promote_article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'cover': promote_article.cover.url if promote_article.cover else None,
            })

        context = {
            'article_data': article_data,
            'promote_article_data': promote_data
        }
        return render(request, 'index.html', context)
    
class ContactPage(TemplateView):
    template_name = 'page-contact.html'

class AboutPage(TemplateView):
    template_name = 'page-about.html'

class CategoryPage(TemplateView):

    template_name = 'category.html'

    # def get(self, request, **kwargs):
    #     categories = Category.objects.all()
    #     category_data = []

    #     for category in categories:
    #         articles = Article.objects.filter(category=category).order_by('-created_at')[:3]
    #         article_data = []
    #         for article in articles:
    #             article_data.append({
    #                 'title': article.title,
    #                 'cover': article.cover.url,
    #                 'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    #             })
    #         category_data.append({
    #             'title': category.title,
    #             'cover': category.cover.url,
    #             'articles': article_data
    #         })

    #     context = {
    #         'category_data': category_data
    #     }
    #     return render(request, self.template_name, context)

class SingleStandardPage(TemplateView):
    template_name = 'single-standard.html'

    # def get(self, request, **kwargs):
    #     article_id = kwargs.get('article_id')
    #     article = Article.objects.get(id=article_id)
    #     context = {
    #         'article': article
    #     }
    #     return render(request, self.template_name, context)

class StyleGuidePage(TemplateView):
    template_name = 'style-guide.html'

    # def get(self, request, **kwargs):
    #     context = {}
    #     return render(request, self.template_name, context)