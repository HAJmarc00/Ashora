from rest_framework import serializers


class SingleArticleSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_null=False, max_length=255)
    cover = serializers.CharField(required=False, allow_null=True, max_length=255)
    content = serializers.CharField(required=True, allow_null=False, max_length=2048)
    created_at = serializers.DateTimeField(required=True, allow_null=False)


class SubmitArticleSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=128)
    cover = serializers.FileField(required=True, allow_null=False, allow_empty_file=False)
    content = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=2048)
    category_id = serializers.IntegerField(required=True, allow_null=False)
    author_id = serializers.IntegerField(required=True, allow_null=False)
    promote = serializers.BooleanField(required=True, allow_null=False)


class UpdateArticleSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True, allow_null=False)
    cover = serializers.FileField(required=False, allow_null=True, allow_empty_file=False)

class DeleteArticleSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True, allow_null=False)