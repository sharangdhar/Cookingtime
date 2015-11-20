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
		template = 'Cookingti/hs_panel.html'
	elif request.GET['page'] == 'item':
		template = 'Cookingti/bulk_sidebar_search_dropdown_item.html'
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
	return render(request, 'Cookingti/profile.html', context)


#valid item types are 'food','recipe', 'equipment'
@ensure_csrf_cookie	 # Gives CSRF token for later requests.
@transaction.atomic # Should only be if post
def item(request, item_type='', id = -1):
	'''
	# Posting a review
	if request.method == "POST":
		context = {'page_name': 'Item'}
		
		# Check authentication
		if not request.user.is_authenticated():
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
			
		#date will be added automatically
		
		if not request.POST['page_type'] or not 'page_type' in request.POST:
			print("no page_type")
			raise Http404
			
		page_type = request.POST['page_type']
		
			
		if not request.POST['item_id'] or not 'item_id' in request.POST:
			print('no item_id')
			raise Http404
		
		item_id = request.POST['item_id']
		item = ""	
		if page_type == 'food':
			try:
				item = Food.objects.get(id=item_id)
			except:
				print('no item')
				raise Http404
			new_entry = FoodReview(user=request.user, item=item)
			new_form = FoodReviewForm(request.POST, instance=new_entry)
			
		elif page_type == 'recipe':
			try:
				item = Recipe.objects.get(id=item_id)				
			except:
				print('no item')
				raise Http404
			new_entry = RecipeReview(user=request.user, item=item)
			new_form = RecipeReviewForm(request.POST, instance=new_entry)
			
		elif page_type == 'equipment':
			try:
				item = Equipment.objects.get(id=item_id)
			except:
				print('no item')
				raise Http404
			new_entry = EquipmentReview(user=request.user, item=item)
			new_form = EquipmentReviewForm(request.POST, instance=new_entry)
		
		
						
		context = {'page_name': item.name, 'page_type': item_type, 'item':	item, 'user': request.user}
		
		if context['page_type'] == "food":
			context['link_item_type'] = 'recipe'
		elif context['page_type'] == "recipe":
			context['link_item_type'] = 'food'
		
		if not new_form.is_valid():
			print("form errors")
			context['review_form'] = new_form
			session = {'page_type': item_type, 'item':	item}
			return render(request, 'Cookingti/item_main.html', context)
			
		new_form.save()
		
		
		# UPDATE STARS
		total = item.starsFloat * item.numReviews
		new_num = item.numReviews + 1
		
		new_float = (total + new_form.cleaned_data['stars'])/new_num
		
		item.starsFloat = new_float
		item.stars = int(round(new_float))
		item.numReviews = new_num
		item.save()
		
		if context['page_type'] == "food":
			context['link_item_type'] = 'recipe'
		elif context['page_type'] == "recipe":
			context['link_item_type'] = 'food'
		
		
		session = {'page_type': item_type, 'item':	item}
		return redirect("/item/" + page_type + "/" + str(item.id))
	'''
	
	
	
	
	if request.method != 'GET':
		print("not get")
		raise Http404()

	
	item_flag = True

	# item flag will be true if user enters wrong url
	if (item_type=='food' or item_type=='recipe' or item_type=='equipment'):
		item_flag = False

	if (item_flag or (id < 0)):
		print ("wrong parameters")
		raise Http404()


	if item_type == 'food':
		try:
			item_new = Food.objects.get(pk = id)
		except:
			raise Http404
	elif item_type == 'recipe':
		try:
			item_new = Recipe.objects.all().get(pk = id)
		except:
			raise Http404
	else:
		try:
			item_new = Equipment.objects.get(pk = id)
		except:
			raise Http404

		
	context = {'page_name': item_new.name, 'page_type': item_type, 'item':	item_new, 'user': request.user}
	
	if context['page_type'] == "food":
		context['review_form'] = FoodReviewForm()
		context['photo_form'] = FoodPhotoForm()
		context['link_item_type'] = 'recipe'
	elif context['page_type'] == "recipe":
		context['review_form'] = RecipeReviewForm()
		context['photo_form'] = RecipePhotoForm()
		context['link_item_type'] = 'food'
	elif context['page_type'] == "equipment":
		context['photo_form'] = EquipmentPhotoForm()
		context['review_form'] = EquipmentReviewForm()
	
	#created to keep track of information across this method and postReview method
	session = {'page_type': item_type, 'item':	item_new}
	return render(request, 'Cookingti/item_main.html', context)


@transaction.atomic
def postReview(request):
	if request.method != "POST":
		raise Http404
	
	if not request.user.is_authenticated():
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'Login required'}]})
		return HttpResponse(resp, content_type='application/json')
		
		
	if not "page_type" in request.POST or not request.POST["page_type"]:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'page_type required'}]})
		return HttpResponse(resp, content_type='application/json')
	page_type = request.POST["page_type"]
	
	context = {'page_name': 'Item', 'page_type':page_type}


	if page_type == 'food':
		form = FoodReviewForm(request.POST)
	elif page_type == 'recipe':
		form = RecipeReviewForm(request.POST)
	elif page_type == 'equipment':
		form = EquipmentReviewForm(request.POST)
	else:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'invalid page_type'}]})
		return HttpResponse(resp, content_type='application/json')
	

	if not form.is_valid():
		resp = json.dumps(
		{
			'status':'error',
			'errors': dict(form.errors.items())
		})
		return HttpResponse(resp, content_type='application/json')
	
	
	instance = form.save(commit=False)
	instance.user = request.user
	instance = form.save()
	
	
	# UPADATE STARS
	item = instance.item
	total = item.starsFloat * item.numReviews
	new_num = item.numReviews + 1
	
	new_float = (total + instance.stars)/new_num
	
	item.starsFloat = new_float
	item.stars = int(round(new_float))
	item.numReviews = new_num
	item.save()
	
	

	resp = json.dumps(
	{
		'status':'success',
		'html': render_to_string('Cookingti/review_panel.html', {'page_type':page_type, 'review':instance})
	})
	return HttpResponse(resp, content_type='application/json') 




@transaction.atomic
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

@transaction.atomic
def postImage(request):
	# We might not need the GET part depending on how the front end is 
	# being handled
	
	if request.method != "POST":
		print("method not post")
		raise Http404
	
	# Check authentication
	if not request.user.is_authenticated():
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'Login required'}]})
		return HttpResponse(resp, content_type='application/json')
		
	
	if not "page_type" in request.POST or not request.POST["page_type"]:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'page_type required'}]})
		return HttpResponse(resp, content_type='application/json')
	page_type = request.POST["page_type"]
	
	context = {'page_name': 'Item', 'page_type':page_type}


	if page_type == 'food':
		form = FoodPhotoForm(request.POST, request.FILES)
	elif page_type == 'recipe':
		form = RecipePhotoForm(request.POST, request.FILES)
	elif page_type == 'equipment':
		form = EquipmentPhotoForm(request.POST, request.FILES)
	else:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'invalid page_type'}]})
		return HttpResponse(resp, content_type='application/json')
	

	if not form.is_valid():
		resp = json.dumps(
		{
			'status':'error',
			'errors': dict(form.errors.items())
		})
		return HttpResponse(resp, content_type='application/json')
		

	instance = form.save(commit=False)
	instance.user = request.user
	instance = form.save()
	

	resp = json.dumps(
	{
		'status':'success',
		'html': render_to_string('Cookingti/carousel_image.html', {'page_type':page_type, 'item':instance.item, 'image':instance})
	})
	return HttpResponse(resp, content_type='application/json')
	

	
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
		return render(request, 'Cookingti/hs_main.html', context)

	if form.cleaned_data['item_type'] == 'food':
		new_item = Food(name = form.cleaned_data['item'])
	elif form.cleaned_data['item_type'] == 'recipe':
		new_item = Recipe(user=request.user, name = form.cleaned_data['item'])
	else:
		new_item = Equipment(name = form.cleaned_data['item'])

	new_item.save()
 
	return redirect('Cookingti/item/' + form.cleaned_data['item_type'] + '/' + str(new_item.id))


@transaction.atomic
def postTime(request):
	
	if request.method != 'POST':
		raise Http404
		
		
	if not request.user.is_authenticated():
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'Login required'}]})
		return HttpResponse(resp, content_type='application/json')
		
	
		
	form = TimeForm(request.POST)
	if not form.is_valid():
		resp = json.dumps({'status':'error','errors': dict(form.errors.items())})
		return HttpResponse(resp, content_type='application/json')


	item = form.item
	new_const = form.cleaned_data['constant']
	
	total = item.numConst * item.avgConst
	new_num = item.numConst + 1

	item.avgConst = (total + new_const)/(new_num)
		
	item.numConst = new_num
	item.save();
	
	
	resp = json.dumps(
	{
		'status':'success',
		'result':item.avgConst
	})
	return HttpResponse(resp, content_type='application/json')



@transaction.atomic
def postRecipe(request):
	
	if request.method != 'POST':
		raise Http404
		
	if not request.user.is_authenticated():
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'Login required'}]})
		return HttpResponse(resp, content_type='application/json')
		
	
	form = RecipeTextForm(request.POST)
	if not form.is_valid():
		resp = json.dumps({'status':'error','errors': dict(form.errors.items())})
		return HttpResponse(resp, content_type='application/json')
		
	instance = form.save(commit=False)
	if instance.user != request.user:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'Wrong user'}]})
		return HttpResponse(resp, content_type='application/json')
		
	instance = form.save()
		
	rendered = markdown.markdown(instance.text)
	
	
	resp = json.dumps(
	{
		'status':'success',
		'html':rendered
	})
	return HttpResponse(resp, content_type="text/json")
	

@transaction.atomic
def postLink(request):
	
	if not request.user.is_authenticated():
		
		raise Http404
		
	if request.method != 'POST':
		print('not post')
		raise Http404
	
	
	
	
	if not 'item_id' in request.POST or not request.POST['item_id']:
		print('no item_id')
		raise Http404
	item_id = request.POST['item_id']
	
	
	if not 'link_id' in request.POST or not request.POST['link_id']:
		print('no link_id')
		raise Http404
	link_id = request.POST['link_id']
	
	
	if not 'link_type' in request.POST or not request.POST['link_type']:
		print("no type")
		raise Http404();
	link_type = request.POST['link_type']
	
	
	
	
	
	if link_type == "recipe":
		try:
			link_item = Recipe.objects.get(id = link_id)
			item = Food.objects.get(id= item_id)

			item.link.add(link_item)
			print(item.link.all())
		except:
			print("couldn't get items")
			raise Http404
	elif link_type == "food":
		try:
			link_item = Food.objects.get(id = link_id)
			item = Recipe.objects.get(id = item_id)

			link_item.link.add(item)
			print(link_item.link.all())			
		except:
			print("couldn't get items")
			raise Http404
	else:
		print("bad link type")
	
		

	ret = render_to_string("Cookingti/bulk_sidebar_item.html", {'item':link_item, 'type':link_type});
	
	return HttpResponse(ret, content_type="text/html")