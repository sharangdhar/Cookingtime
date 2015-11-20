"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
  
	url(r'^$', 'Cookingti.views.home', name='home'),
	url(r'^home$', 'Cookingti.views.home', name='home'),
	url(r'^profile$', 'Cookingti.views.profile',  name='profile'),
	url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'Cookingti/login.html', 'extra_context':{'page_name':'Log in'}}, name='login', ),
	url(r'^register$', 'Cookingti.views.register', name='register'),

	url(r'^search$', 'Cookingti.views.search', name='search'),
    url(r'^new_item$', 'Cookingti.views.addItem', name='addItem'),

    #url(r'^post_review$', 'Cookingti.views.postReview', name='post_review'),
    url(r'^post_img$', 'Cookingti.views.postImage', name='post_img'),
    url(r'^post_time$', 'Cookingti.views.postTime', name='post_time'),
	url(r'^post_recipe$', 'Cookingti.views.postRecipe', name='post_review'),
	url(r'^post_link$', 'Cookingti.views.postLink', name='post_link'),
	url(r'^post_review$', 'Cookingti.views.postReview', name='post_review'),
	
	url(r'^item/(?P<item_type>[\w-]+)/(?P<id>\d+)$', 'Cookingti.views.item', name='item'),
	url(r'^image/(?P<page_type>.+)/(?P<item_id>.+)/(?P<img_id>.+)$', 'Cookingti.views.getImage', name='image'),
]
