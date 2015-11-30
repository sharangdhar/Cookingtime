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
  
	url(r'^$', 'Cookingti.views.hs_views.home', name='blank'),
	url(r'^home$', 'Cookingti.views.hs_views.home', name='home'),
	url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'general/login.html', 'extra_context':{'page_name':'Log in'}}, name='login', ),
	url(r'^register$', 'Cookingti.views.register', name='register'),

	url(r'^profile/(?P<id>.+)$', 'Cookingti.views.profile',  name='profile'),
	url(r'^edit_profile/?$', 'Cookingti.views.editProfile',  name='edit_profile'),

	url(r'^search$', 'Cookingti.views.search', name='search'),
    url(r'^new_item_search$', 'Cookingti.views.hs_views.newItemSearch', name='addItem'),
    url(r'^new_item_create$', 'Cookingti.views.hs_views.newItemCreate', name='newItemCreate'),	
	url(r'^new_by_barcode$', 'Cookingti.views.hs_views.newByBarcode', name="new_by_barcode"),

    url(r'^post_img$', 'Cookingti.views.item_views.postImage', name='post_img'),
    url(r'^post_time$', 'Cookingti.views.item_views.postTime', name='post_time'),
	url(r'^post_recipe$', 'Cookingti.views.item_views.postRecipe', name='post_review'),
	url(r'^post_link$', 'Cookingti.views.item_views.postLink', name='post_link'),
	url(r'^post_review$', 'Cookingti.views.item_views.postReview', name='post_review'),
	
	url(r'^del_link$', 'Cookingti.views.item_views.delLink', name='del_link'),
	url(r'^del_image$', 'Cookingti.views.item_views.delImage', name='del_image'),
	
	url(r'^item/(?P<item_type>[\w-]+)/(?P<id>\d+)$', 'Cookingti.views.item_views.item', name='item'),
	url(r'^image/(?P<page_type>.+)/(?P<item_id>.+)/(?P<img_id>.+)$', 'Cookingti.views.getImage', name='image'),

	url(r'^barcode_image/?$', 'Cookingti.views.barcode', name='barcode'),
	url(r'^lookup_wattage/?$', 'Cookingti.views.lookupWattage', name="lookup_wattage"),

]
