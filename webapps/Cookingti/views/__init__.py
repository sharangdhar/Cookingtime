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


# added for barcode decoding
import zbar
from PIL import Image
import os

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
	




@ensure_csrf_cookie
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
	
	
	
	if request.POST['barcode']:
		microwave = Microwave(barcode=request.POST['barcode'], wattage=request.POST['wattage'])
		microwave.save()

	return redirect(reverse('home'))



	
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
	
		
@ensure_csrf_cookie	
def profile(request, id):
	context = {'page_name': request.user.username}
	
	try:
		user = User.objects.get(id=id);
	except:
		raise Http404
	
	context['user'] = user
	return render(request, 'general/profile_main.html', context)


@transaction.atomic
def editProfile(request):
	if request.method != "POST":
		print("method not post")
		raise Http404
	
	# Check authentication
	if not request.user.is_authenticated():
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'Login required'}]})
		return HttpResponse(resp, content_type='application/json')
	
	form = ProfileForm(request.POST)
	
	if not form.is_valid():
		resp = json.dumps(
		{
			'status':'error',
			'errors': dict(form.errors.items())
		})
		return HttpResponse(resp, content_type='application/json')
	
	
	if request.user != form.user:	
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'not your profile'}]})
		return HttpResponse(resp, content_type='application/json')
		
	form.user.first_name = form.cleaned_data.get("firstname")
	form.user.last_name = form.cleaned_data.get("lastname")
	form.user.email = form.cleaned_data.get("email")
	form.user.save()
	
	form.person.wattage = form.cleaned_data.get("wattage")
	form.person.save()
	
	resp = json.dumps(
	{
		'status':'success', 
		'data':
		{
			'firstname': form.cleaned_data.get("firstname"),
			'lastname': form.cleaned_data.get("lastname"),
			'email': form.cleaned_data.get("email"),
			'wattage': form.cleaned_data.get("wattage")
		}
	})
	return HttpResponse(resp, content_type='application/json')
	


def image_decode(img):

	#creating a reader
	scanner = zbar.ImageScanner()

	#configuring the reader
	scanner.parse_config('enable')

	#getting image data
	pil = Image.open(settings.MEDIA_ROOT + img).convert('L')

	# width data for image
	width = pil.size[0]

	#height data for image
	height= pil.size[1]

	raw_data = pil.tobytes()

	# all image data added together
	image = zbar.Image(width, height, 'Y800', raw_data)

	#scan for image barcode
	scanner.scan(image)
	
	
	for info in image:
		return info

def barcode(request):
	context = {}
	if request.method == 'GET':
		print("method not post")
		raise Http404
		
	form = BarcodePhotoForm(request.POST,request.FILES)

	if not form.is_valid():
		resp = json.dumps(
		{
			'status':'error',
			'errors': dict(form.errors.items())
		})
		return HttpResponse(resp, content_type='application/json')

	item = form.save()
	data = image_decode(item.picture.name)
	os.remove(settings.MEDIA_ROOT + item.picture.name)
	item.delete()
<<<<<<< HEAD
	
	if data == None:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'No barcode found in image'}]})
		return HttpResponse(resp, content_type='application/json')

	
	resp = json.dumps(
	{
		'status':'success', 
		'data':
		{
			'type':str(data.type),
			'barcode':str(data.data)
		}
	})
	
	return HttpResponse(resp, content_type='application/json')
=======
	return redirect(reverse('register'))


@transaction.atomic
@login_required
def change_password(request):
	context = {}
	if request.method == 'GET':
		context['form'] = ChangePasswordForm()
		return render(request, 'general/change_password.html', context)

	form = ChangePasswordForm(request.POST)

	context['form'] = form

	if not form.is_valid():
		return render(request, 'general/change_password.html', context)

	new_password = form.cleaned_data['password1']
>>>>>>> 97c5ab539f09d5685c847d29bfec6abb82bd7a02

	currentUser =  User.objects.get(id= request.user.id)
	currentUser.set_password(new_password)
	currentUser.save()

	currentUser = authenticate(username=currentUser.username, password=new_password)

	login(request,currentUser)

	return redirect('/profile/' + str(request.user.id))


def resetPassword(request):
	context = {}
	return 

def lookupWattage(request):
	if request.method == 'GET':
		print("method not post")
		raise Http404
	
	if not 'barcode' in request.POST or not request.POST['barcode']:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'No request barcode'}]})
		return HttpResponse(resp, content_type='application/json')

	
	try:
		microwave = Microwave.objects.get(barcode=request.POST['barcode'])
	except:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'No entry found. Please enter wattage manually.'}]})
		return HttpResponse(resp, content_type='application/json')

	resp = json.dumps(
	{
		'status':'success', 
		'data':
		{
			'wattage': microwave.wattage,
		}
	})
	
	return HttpResponse(resp, content_type='application/json')




