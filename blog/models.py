from django.db import models

class Article(models.Model):
   title = models.CharField(max_length=255)
   body = models.TextField(max_length=1000)
   draft = models.BooleanField(default=True)
   published_date = models.DateField(blank=True, null=True)
   author = models.CharField(max_length=255)


   
