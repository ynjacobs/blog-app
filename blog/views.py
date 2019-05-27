from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from blog.models import Article


def home_page(request):
    return render(request, 'home.html',  {
        'articles': Article.objects.filter(draft = False).order_by('-published_date')
    })


def page_details(request, id): 
    return render(request, 'post.html', {
        'post': Article.objects.get(pk=id)
    })