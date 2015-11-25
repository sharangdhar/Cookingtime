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
	
	

@transaction.atomic
def addItem(request):
	if request.method == 'GET':
		return redirect('Cookingti/home')

	# Check authentication
	if not request.user.is_authenticated():
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	form = AddItemForm(request.POST)

	context = {}

	context['new_form'] = form
		# Validates the form.
	if not form.is_valid():
		context['latest_foods'] = Food.objects.all().order_by('-date')[:5]
		context['highest_foods'] = Food.objects.all().order_by('-stars')[:5]
	
		context['latest_recipes'] = Recipe.objects.all().order_by('-date')[:5]
		context['highest_recipes'] = Recipe.objects.all().order_by('-stars')[:5]
	
		context['latest_equipments'] = Equipment.objects.all().order_by('-date')[:5]
		context['highest_equipments'] = Equipment.objects.all().order_by('-stars')[:5]
		session = {'page_type': '', 'item':	 ''}
		return render(request, 'hs/hs_main.html', context)

	if form.cleaned_data['item_type'] == 'food':
		new_item = Food(name = form.cleaned_data['item'])
	elif form.cleaned_data['item_type'] == 'recipe':
		new_item = Recipe(user=request.user, name = form.cleaned_data['item'])
	else:
		new_item = Equipment(name = form.cleaned_data['item'])
		
	new_item.user = request.user

	new_item.save()
 
	return redirect('/item/' + form.cleaned_data['item_type'] + '/' + str(new_item.id))
