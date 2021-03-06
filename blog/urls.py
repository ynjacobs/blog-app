"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import *



urlpatterns = [
    path('home/', home_page),
    path('admin/', admin.site.urls),
    path('home/<int:id>', post_details, name='post_details'),
    path('home/<int:id>', post_article, name='post_article'),
    path('create_comment/', create_comment, name='create_comment'),
    path('create_article/', create_new_article, name='create_article'),
    path('accounts/signup', signup, name='signup'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('signup/', signup, name='signup'),
    path('home/edit/<int:id>', edit_article, name='edit_article'),

]
