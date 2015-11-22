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
			print("len = 0")
			raise Http404()
	elif request.GET['type'] == 'recipe':
		items = Recipe.objects.filter(name__contains=query)
		if len(items) == 0:
			print("len = 0")
			raise Http404()
	elif request.GET['type'] == 'equipment':
		items = Equipment.objects.filter(name__contains=query)
		if len(items) == 0:
			print("len = 0")
			raise Http404()
	else:
		raise Http404()


	template = ''
	if request.GET['page'] == 'search':
		template = 'hs/hs_panel.html'
	elif request.GET['page'] == 'item':
		template = 'item/bulk_sidebar/bulk_sidebar_search_dropdown_item.html'
	else:
		print("invalid page")
		raise Http404

	item_html = []
	for item in items:
		# if request.GET['page'] == 'search':
			item_html.append(render_to_string(template, {'item':item, 'type':request.GET['type']}))
		# elif request.GET['page'] == 'item':
			# item_html.append(render_to_string(template, {'link_item':item, 'link_item_type':request.GET['type']}))

		
	ret = ''.join(item_html)
	
	return HttpResponse(ret, content_type="text/html")
	


def profile(request):
	context = {'page_name': request.user.username}
	session = {'page_type': '', 'item':	 ''}
	return render(request, 'general/profile.html', context)







@transaction.atomic
def register(request):

	context = {'page_name':'Register'}

	if request.user.is_authenticated():
		return redirect('Cookingti/home')

	# Just display the registration form if this is a GET request.
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'general/register.html', context)

	# Creates a bound form from the request POST parameters and makes the 
	# form available in the request context dictionary.
	form = RegistrationForm(request.POST)

	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return render(request, 'general/register.html', context)


	# Logs in the new user and redirects to his/her todo list
	new_user = User.objects.create_user(username= request.POST['username'], password = request.POST['password1'],
		first_name=request.POST["firstname"],last_name= request.POST["lastname"], email=request.POST["email"] )
	new_user.save()

	new_user = authenticate(username=form.cleaned_data['username'],
							password=form.cleaned_data['password1'])

	login(request, new_user)

	new_person = Person(user= new_user, wattage=request.POST["wattage"])
	new_person.save()

	return redirect('Cookingti/home')



	
def getImage(request, page_type, item_id, img_id):
	
	if page_type == 'food':
		item = get_object_or_404(Food, id=item_id)
	elif page_type == 'recipe':
		item = get_object_or_404(Recipe, id=item_id)
	elif page_type == 'equipment':
		item = get_object_or_404(Equipment, id=item_id)
	else:
		raise Http404()
	
	try:
		image = item.photos.get(id=img_id)
	except:
		raise Http404
		
		
	content_type = guess_type(image.picture.name)
	return HttpResponse(image.picture, content_type=content_type)
	
		
