from operator import index
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


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

class AllArticleApiView(APIView):

    def get(self,request, **kwargs):
        try:
            all_articles = Article.objects.all().order_by('-created_at')[:10]
            data = []

            for article in all_articles:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'category': article.category.title,
                    'author': article.author.user.first_name + ' ' + article.author.user.last_name,
                })

            return Response({'data': data}, status=status.HTTP_200_OK)

        except :
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class SingleArticleApiView(APIView):

    def get(self, request, **kwargs):
        try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title__contains=article_title)
            serialized_data = SingleArticleSerializer(article, many=True)
            data = serialized_data.data
            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
class SearchArticleApiView(APIView):

    def get(self, request, **kwargs):
        try:
            from django.db.models import Q

            query = request.GET.get('query')
            articles = Article.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
            data = []

            for article in articles:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'category': article.category.title,
                    'author': article.author.user.first_name + ' ' + article.author.user.last_name,
                    'promote': article.promote,
                })

            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
class SubmitArticleApiView(APIView):


    def post(self, request, format=None):
        try:
            serializer = SubmitArticleSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status': 'Bad Request.',
                    'errors': serializer.errors  # ← این خیلی مهمه
                }, status=status.HTTP_400_BAD_REQUEST)

            title = serializer.validated_data.get('title')
            cover = request.FILES.get('cover')
            if not cover:
                return Response({'error': 'Cover file is required.'}, status=status.HTTP_400_BAD_REQUEST)

            content = serializer.validated_data.get('content')
            category_id = serializer.validated_data.get('category_id')
            author_id = serializer.validated_data.get('author_id')
            promote = serializer.validated_data.get('promote')

            user = User.objects.get(id=author_id)
            author = UserProfile.objects.get(user=user)
            category = Category.objects.get(id=category_id)

            article = Article.objects.create(
                title=title,
                cover=cover,
                content=content,
                category=category,
                author=author,
                promote=promote
            )

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': "Bad Request.", 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateArticleApiView(APIView):

    def post(self, request, format=None):
        try:
            serializer = UpdateArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES.get('cover')  
            else:
                return Response({
                    'status': 'Bad Request.',
                    'errors': serializer.errors 
                }, status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).update(
                cover=cover
            )
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': "Bad Request.", 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteArticleApiView(APIView):

    def post(self, request, format=None):
        try:
            serializer = DeleteArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
            else:
                return Response({
                    'status': 'Bad Request.',
                    'errors': serializer.errors 
                }, status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).delete()
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': "Bad Request.", 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)