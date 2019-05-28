from django.db import models

class Article(models.Model):
   title = models.CharField(max_length=255)
   body = models.TextField(max_length=1000)
   draft = models.BooleanField(default=True)
   published_date = models.DateField(blank=True, null=True)
   author = models.CharField(max_length=255)


class Comment(models.Model):
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  message = models.TextField()
  article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')   
