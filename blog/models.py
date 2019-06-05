from django.db import models
from django.forms import ModelForm
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from datetime import datetime, date
from pytz import timezone
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, Form
from django.contrib.auth.models import User

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())
         

class Article(models.Model):
   title = models.CharField(max_length=255)
   body = models.TextField(max_length=1000)
   draft = models.BooleanField(default=True)
   published_date = models.DateField(blank=True, null=True)
   author = models.CharField(max_length=255)
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'articles')


class Comment(models.Model):
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  message = models.TextField()
  article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')   

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message', 'article']

class ArticleForm(ModelForm):
  body = forms.CharField(min_length=2)
  class Meta:
    model = Article
    fields = ['title', 'body', 'draft', 'published_date', 'author']

  def clean_published_date(self):
        # localizing both dates
        publishedDate = self.cleaned_data['published_date']
        presentDate = date.fromtimestamp(datetime.now(timezone('America/Toronto')).timestamp())
        print(presentDate)
        print(publishedDate)
        isDraft = self.cleaned_data['draft']
        if isDraft:
            if publishedDate and publishedDate < presentDate:
                raise ValidationError('Specified date must be in the future!')
            else:
                return publishedDate
        else:
            if publishedDate and publishedDate > presentDate:
                raise ValidationError('Specified date must be in the past!')
            else:
                return publishedDate