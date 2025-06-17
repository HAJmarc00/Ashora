from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime

def validate_file_extension(value):
    import os 
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions are: ' + ', '.join(valid_extensions))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='files/user_avatar/', blank=False, null=False, validators=[validate_file_extension])
    description = models.CharField(max_length=512, blank=False, null=False)

    def __str__(self):
        return self.user.username
    
class Article(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False)
    cover = models.FileField(upload_to='files/article_cover/', blank=False, null=False, validators=[validate_file_extension])
    content = RichTextUploadingField(blank=False, null=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=False, null=False)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, blank=False, null=False)
    promote = models.BooleanField(default=False, blank=False , null=False)


class Category(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False)
    cover = models.FileField(upload_to='files/category_cover/', blank=False, null=False, validators=[validate_file_extension])

    def __str__(self):
        return self.title