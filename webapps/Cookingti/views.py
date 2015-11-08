from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
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
	context['add_item_form'] = AddItemForm()
	session = {'page_type': '', 'item':  ''}
	return render(request, 'Cookingti/hs_main.html', context)

def search(request):
	
	if request.method != 'GET':
		print("not get")
		raise Http404();
	
	if not request.GET['type'] or request.GET['type'] is None:
		print("no type")
		raise Http404();
		
	if not request.GET['page'] or request.GET['page'] is None:
		print("no page")
		raise Http404();
		
	if not request.GET['query'] or request.GET['query'] is None:
		print("no query")
		raise Http404()
	
	query = request.GET['query']
	
	if request.GET['type'] == 'food':
		items = Food.objects.filter(name__contains=query)
		if len(items) == 0:
			raise Http404()
	elif request.GET['type'] == 'recipe':
		items = Recipe.objects.filter(name__iexact=query)
		if len(items) == 0:
			raise Http404()
	elif request.GET['type'] == 'equipment':
		items = Equipment.objects.filter(name__iexact=query)
		if len(items) == 0:
			raise Http404()
	else:
		raise Http404()

	print(items)

	template = ''
	if request.GET['page'] == 'search':
		template = 'Cookingti/hs_panel.html'
	elif request.GET['page'] == 'item':
		template = 'Cookingti/link_panel.html'

	item_html = []
	for item in items:
		item_html.append(render_to_string(template, {'item':item}))
		print(item_html)
		
	ret = ''.join(item_html)
	
	return HttpResponse(ret, content_type="text/html")
	


def profile(request):
	context = {'page_name': request.user.username}
	session = {'page_type': '', 'item':  ''}
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

	print item_type

	if item_type == 'food':
		item_new = Food.objects.all().filter(pk = id)
	elif item_type == 'recipe':
		item_new = Recipe.objects.all().filter(pk = id)
	else:
		item_new = Equipment.objects.all().filter(pk = id)

	
	context = {'page_name': 'Item', 'page_type': item_type, 'item':  item_new, 'user': request.user}
	#created to keep track of information across this method and postReview method
	session = {'page_type': item_type, 'item':  item_new}
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

	new_person = Person(user= new_user, wattage=request.POST["wattage"])
	new_person.save()

	return redirect('/Cookingti/')


def postReview(request):
	# We might not need the GET part depending on how the front end is 
	# being handled
		
	context = {'page_name': 'Item', 'page_type':session['page_type'],
	 'item':session['item']}

	if request.method == 'GET':
		context['form'] = ReviewForm()
		return render(request,  'Cookingti/item_main.html', context)

	#date will be added automatically
	new_entry = Review(user=request.user)
	form = ReviewForm(request.POST, instance = new_entry)
	if not form.is_valid():
		context['form'] = form
		return render(request,'Cookingti/item_main.html', context)
	form.save()
	return render(request,'Cookingti/item_main.html', context)



def postImage(request):
	# We might not need the GET part depending on how the front end is 
	# being handled
	context = {'page_name': 'Item', 'page_type':session['page_type'],
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


def addItem(request):
	if request.method == 'GET':
		return redirect('Cookingti/home')


	form = AddItemForm(request.POST)

	context = {}

	context['form'] = form
	    # Validates the form.
	if not form.is_valid():
		print "error"
		context['errors'] = form.errors
		return render(request, 'Cookingti/register.html', context)

	if form.cleaned_data['item_type'] == 'food':
		new_item = Food(name = form.cleaned_data['item'])
	elif form.cleaned_data['item_type'] == 'recipe':
		new_item = Recipe(name = form.cleaned_data['item'])
	else:
		new_item = Equipment(name = form.cleaned_data['item'])

	new_item.save()
 
	return redirect('Cookingti/home')


def postTime(request):
	return



