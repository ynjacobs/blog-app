from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from blog.models import Article, Comment


def home_page(request):
    return render(request, 'home.html',  {
        'articles': Article.objects.filter(draft = False).order_by('-published_date')
    })


def post_details(request, id): 
    return render(request, 'post.html', {
        'post': Article.objects.get(pk=id)
    })

def create_comment(request):
    comment_title = request.POST['comment_title']
    comment_msg = request.POST['comment_message']
   
    post_id = request.POST['article']
    article = Article.objects.get(id=post_id)

    comment = Comment(name=comment_title, message=comment_msg, article=article)
    comment.save()

    return redirect('post_details', id=post_id)
