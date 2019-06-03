from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from blog.models import Article, Comment, CommentForm, ArticleForm  
# from django.contrib.auth import UserCreationForm


def home_page(request):
    return render(request, 'home.html',  {
        'articles': Article.objects.filter(draft = False).order_by('-published_date')
    })


def post_details(request, id): 
    article = Article.objects.get(id=id)
    comment = Comment(article=article)
    form = CommentForm(instance=comment)
    context = {'form': form, 'post': Article.objects.get(pk=id)}
    return render(request, 'post.html', context)

def post_article(request, id): 
    article = Article.objects.get(id=id)
    new_article = Article(article=article)
    form = ArticleForm(instance=new_article)
    context = {'form': form, 'post': Article.objects.get(pk=id)}
    return render(request, 'new_article.html', context)

# def create_comment(request):
#     comment_title = request.POST['comment_title']
#     comment_msg = request.POST['comment_message']
   
#     post_id = request.POST['article']
#     article = Article.objects.get(id=post_id)

#     comment = Comment(name=comment_title, message=comment_msg, article=article)
#     comment.save()

#     return redirect('post_details', id=post_id)

def new_comment(request):
    form = CommentForm()
    context = {'form': form}
    response = render(request, 'comments/post.html', context)
    return HttpResponse(response)


def create_comment(request):
    print(request.POST)
    article = Article.objects.get(id= request.POST['article'])
    comment = CommentForm(request.POST)
    comment.save()
    return redirect('post_details', id=article.id)

def create_new_article(request):
    # form = ArticleForm()
    # context = {'form': form}
    # response = render(request, 'new_article.html', context)
    # return HttpResponse(response)

    form = ArticleForm(request.POST)
    if form.is_valid():
        new_article = form.save()
        return HttpResponseRedirect('/home')
    else:
        context = { 'form': form }
        response = render(request, 'new_article.html', context)
        return HttpResponse(response)

def new_article(request):
    article = Article.objects.get(id= request.POST['article'])
    new_article = ArticleForm(request.POST)
    new_article.save()
    return redirect('post_details', id=article.id)

def signup(request):
    form = UserCreationForm(request.POST)
    context = {'form': form}
    response = render(request, 'new_article.html', context)
    return HttpResponse(response)

def signup_create(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        return HttpResponseRedirect('/')
    else:
        context = {'form': form}
        response = render(request, 'signup.html', context)
        return HttpResponse(response)


    