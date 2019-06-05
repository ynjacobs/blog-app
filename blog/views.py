from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from blog.models import Article, Comment, CommentForm, ArticleForm, LoginForm  
# from django.contrib.auth import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


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

@login_required
def create_new_article(request):
    # form = ArticleForm()
    # context = {'form': form}
    # response = render(request, 'new_article.html', context)
    # return HttpResponse(response)

    # form = ArticleForm(request.POST)
    # if form.is_valid():
    #     new_article = form.save()
    #     return HttpResponseRedirect('/home')
    # else:
    #     context = { 'form': form }
    #     response = render(request, 'new_article.html', context)
    #     return HttpResponse(response)
    if request.method == 'POST':
        article = Article(user = request.user)
        article.user = request.user
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # instance.user = request.user
            # create_new_article = form.save()
            return HttpResponseRedirect('/home')
        else:
            context = { 'form': form }
            response = render(request, 'new_article.html', context)
            return HttpResponse(response)
    else:
        form = ArticleForm()
        context = { 'form': form }
        response = render(request, 'new_article.html', context)
        return HttpResponse(response)


def new_article(request):
    article = Article.objects.get(id= request.POST['article'])
    new_article = ArticleForm(request.POST)
    instance.user = request.user
    new_article.save()
    return redirect('post_details', id=article.id)

# def signup(request):
#     form = UserCreationForm(request.POST)
#     context = {'form': form}
#     response = render(request, 'new_article.html', context)
#     return HttpResponse(response)

# def signup_create(request):
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#         new_user = form.save()
#         return HttpResponseRedirect('/')
#     else:
#         context = {'form': form}
#         response = render(request, 'signup.html', context)
#         return HttpResponse(response)

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/home')
    else:
        form = UserCreationForm()
    html_response =  render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)


@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id, user=request.user.pk)
    article_form = ArticleForm(request.POST, instance=article)

    
    if article_form.is_valid():
        article_form.save()
        return redirect('post_details', id=id) 
    else:
        return render(request, 'edit_article.html', {
            'article_form': article_form,
            'article.id': id,
            'error_msg': 'You have invalid form, try again!'
        })
    