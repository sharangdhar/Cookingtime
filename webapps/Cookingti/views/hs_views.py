from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse, Http404
from mimetypes import guess_type
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie

# Decorator to use built-in authentication system
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import json
import markdown

from Cookingti.models import *
from Cookingti.forms import *

#amaozn product api
from amazonproduct import API



def home(request):	
	context = {'page_name':'Home'}
	context['latest_foods'] = Food.objects.all().order_by('-date')[:5]
	context['highest_foods'] = Food.objects.all().order_by('-stars')[:5]
	
	context['latest_recipes'] = Recipe.objects.all().order_by('-date')[:5]
	context['highest_recipes'] = Recipe.objects.all().order_by('-stars')[:5]
	
	context['latest_equipments'] = Equipment.objects.all().order_by('-date')[:5]
	context['highest_equipments'] = Equipment.objects.all().order_by('-stars')[:5]
	
	context['add_item_form'] = AddItemForm()
	session = {'page_type': '', 'item':	 ''}
	return render(request, 'hs/hs_main.html', context)
	

def amazon_res(page_type, words):
	api = API(locale='us')

	if page_type == 'food':
		topic = 'Grocery'
	else:
		topic = 'HomeGarden'
	
	results = api.item_search(topic , Keywords=words, ResponseGroup="ItemAttributes, OfferSummary, Images", paginate = False)


 	items = []
	for it in results.Items.Item:
		asin = it.ASIN
		title = it.ItemAttributes.Title
		link = it.DetailPageURL
		
		try:
			price = it.OfferSummary.LowestNewPrice.FormattedPrice
		except:
			price = "no price available"
			
		try: 
			image = it.SmallImage.URL
		except:
			image = ""
		
		if page_type == 'food':
			try:
				item = Food.objects.get(asin=asin)
				print(item.name)
			except:
				item = False
				print('doesnt exist')
		else:
			try:
				item = Equipment.objects.get(asin=asin)
			except:
				item = False
		
		items.append({'asin':asin, 'title':title, 'link':link, 'price':price, 'image':image, 'db':item})
		
	return items



@transaction.atomic
def newItemSearch(request):
	if request.method == 'GET':
		return redirect('Cookingti/home')

	# Check authentication
	if not request.user.is_authenticated():
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	form = AddItemForm(request.POST)

	context = {}



	if not form.is_valid():
		context['latest_foods'] = Food.objects.all().order_by('-date')[:5]
		context['highest_foods'] = Food.objects.all().order_by('-stars')[:5]
	
		context['latest_recipes'] = Recipe.objects.all().order_by('-date')[:5]
		context['highest_recipes'] = Recipe.objects.all().order_by('-stars')[:5]
	
		context['latest_equipments'] = Equipment.objects.all().order_by('-date')[:5]
		context['highest_equipments'] = Equipment.objects.all().order_by('-stars')[:5]
		session = {'page_type': '', 'item':	 ''}
		return render(request, 'hs/hs_main.html', context)


	if form.cleaned_data['item_type'] == 'recipe':

		item = Recipe(user=request.user, name=form.cleaned_data['item'])
		item.save()
		return redirect('item', 'recipe', item.id)


	items = []
	items = amazon_res(form.cleaned_data['item_type'], form.cleaned_data['item'])

	context['page_type'] = form.cleaned_data['item_type'];
	context['items'] = items
	context['form'] = form
	context['query'] = form.cleaned_data['item']
	
	return render(request, 'hs/add_item_search_main.html', context)



@transaction.atomic
def newItemCreate(request):
	
	if not 'type' in request.POST or not request.POST['type']:
		print('no type')
		raise Http404
		
	if not 'title' in request.POST or not request.POST['title']:
		print('no title')
		raise Http404


	if request.POST['type'] == 'food':
		item = Food(user=request.user, name=request.POST['title'])
	elif request.POST['type'] == 'equipment':
		item = Equipment(user=request.user, name=request.POST['title'])
	else:
		print('bad type')
		raise Http404
			
			
	if not 'asin' in request.POST or not request.POST['asin']:
		print('no asin')
		pass
	else:
		item.asin = request.POST['asin']
		
	item.save()

	return redirect('item', request.POST['type'], item.id)


