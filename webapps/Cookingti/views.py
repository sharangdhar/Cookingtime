from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse, Http404
from mimetypes import guess_type
from django.core import serializers

# Decorator to use built-in authentication system
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import json

from Cookingti.models import *
from Cookingti.forms import *


def home(request):
	context = {'page_name':'Home'}
	
	context['foods_'] = Food.objects.all();
	context['recipies_'] = Recipe.objects.all();
	context['equipments_'] = Equipment.objects.all()
	session = {'type': '', 'item':  ''}
	return render(request, 'Cookingti/hs_main.html', context)

def search(request):
	
	if request.method != 'GET':
		print("not get")
		raise Http404();
	
	if not request.GET['type'] or request.GET['type'] is None:
		print("no type")
		raise Http404();
		
	if not request.GET['query'] or request.GET['query'] is None:
		pritn("no query")
		raise Http404()
	
	query = request.GET['query']
	
	if request.GET['type'] == 'food':
		items = Food.objects.filter(name__contains=query)
	elif request.GET['type'] == 'recipe':
		items = Food.objects.filter(name__contains=query)
	elif request.GET['type'] == 'equipment':
		items = Equipment.objects.filter(name__contains=query)
	else:
		print('bad type')
		raise Http404()

	item_html = []
	for item in items:
		item_html = render(request, 'Cookingti/hs_panel.html', {item:item})
	
	return HttpResponse(response_text, content_type="application/json")
	


def profile(request):
	context = {'page_name': request.user.username}
	session = {'type': '', 'item':  ''}
	return render(request, 'Cookingti/profile.html', context)



#valid item types are 'food','recipe', 'equipment'
def item(request, item_type='', id = -1):
	
	if request.method != 'GET':
		print("not get")
		raise Http404()

	
	item_flag = True

	# item flag will be true if user enters wrong url
	if (item_type=='food' or item_type=='recipe' or item_type=='equip'):
		item_flag = False

	if (item_flag or (id < 0)):
		print ("wrong parameters")
		raise Http404()


	if item_type == 'food':
		item_new = Food.objects.all().filter(pk = id)
	elif item_type == 'recipe':
		item_new = Recipe.objects.all().filter(pk = id)
	else:
		item_new = Equipment.objects.all().filter(pk = id)

	
	context = {'page_name': 'Item', 'type': item_type, 'item':  item_new, 'user': request.user}
	#created to keep track of information across this method and postReview method
	session = {'type': item_type, 'item':  item_new}
	return render(request, 'Cookingti/item_main.html', context)



def register(request):

	context = {'page_name':'Register'}

	if request.user.is_authenticated():
		return redirect('/Cookingti/profile')

	# Just display the registration form if this is a GET request.
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'Cookingti/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
	form = RegistrationForm(request.POST)

	context['form'] = form

    # Validates the form.
	if not form.is_valid():
		return render(request, 'Cookingti/register.html', context)


    # Logs in the new user and redirects to his/her todo list
	new_user = User.objects.create_user(username= request.POST['username'], password = request.POST['password1'],
		first_name=request.POST["firstname"],last_name= request.POST["lastname"], email=request.POST["email"] )
	new_user.save()

	new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

	login(request, new_user)

	return redirect('/Cookingti/')


def postReview(request):
	# We might not need the GET part depending on how the front end is 
	# being handled
		
	context = {'page_name': 'Item', 'type':session['type'],
	 'item':session['item']}

	if request.method == 'GET':
		context['form'] = ReviewForm()
		return render(request,  'Cookingti/item_main.html', context)

	#date will be added automatically
	new_entry = ReviewForm(user=request.user)
	form = ReviewForm(request.POST, instance = new_entry)
	if not form.is_valid():
		context['form'] = form
		return render(request,'Cookingti/item_main.html', context)
	form.save()
	return render(request,'Cookingti/item_main.html', context)



def postImage(request):
	# We might not need the GET part depending on how the front end is 
	# being handled
		
	context = {'page_name': 'Item', 'type':session['type'],
	 'item':session['item']}

	if request.method == 'GET':
		context['form'] = PhotoForm()
		return render(request,  'Cookingti/item_main.html', context)

	#date will be added automatically
	new_entry = PhotoForm(user=request.user)
	form = PhotoForm(request.POST, instance = new_entry)
	if not form.is_valid():
		context['form'] = form
		return render(request,'Cookingti/item_main.html', context)
	form.save()
	return render(request,'Cookingti/item_main.html', context)


def postTime(request):
	return



