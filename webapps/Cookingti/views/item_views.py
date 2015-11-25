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


@ensure_csrf_cookie	 # Gives CSRF token for later requests.
def item(request, item_type='', id = -1):
	
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
	return render(request, 'item/item_main.html', context)





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
	
	if not "review_id" in request.POST or not request.POST["review_id"]:
		review_id = 'new'
	else:
		review_id = request.POST["review_id"]
	
	context = {'page_name': 'Item', 'page_type':page_type}


	if page_type == 'food':
		if review_id == 'new':
			form = FoodReviewForm(request.POST)
		else:
			try: 
				obj = FoodReview.objects.get(id=review_id)
			except:
				resp = json.dumps({'status':'error','custom_errors':[{'message': 'review not found'}]})
				return HttpResponse(resp, content_type='application/json')
				
			form = FoodReviewForm(request.POST, instance=obj)
		
	elif page_type == 'recipe':
		if review_id == 'new':
			form = RecipeReviewForm(request.POST)
		else:
			try: 
				obj = RecipeReview.objects.get(id=review_id)
			except:
				resp = json.dumps({'status':'error','custom_errors':[{'message': 'review not found'}]})
				return HttpResponse(resp, content_type='application/json')
			
			form = RecipeReviewForm(request.POST, instance=obj)
		
	elif page_type == 'equipment':
		if review_id == 'new':
			form = EquipmentReviewForm(request.POST)
		else:
			try: 
				obj = EquipmentReview.objects.get(id=review_id)
			except:
				resp = json.dumps({'status':'error','custom_errors':[{'message': 'review not found'}]})
				return HttpResponse(resp, content_type='application/json')
			
			form = EquipmentReviewForm(request.POST, instance=obj)
		
	else:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'invalid page_type'}]})
		return HttpResponse(resp, content_type='application/json')
	
	
	if review_id != 'new' and request.user != obj.user:
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'this is not your review'}]})
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
		'html': render_to_string('item/reviews/review_panel.html', {'request': request, 'page_type':page_type, 'item':item, 'review':instance})
	})
	return HttpResponse(resp, content_type='application/json') 



@transaction.atomic
def postImage(request):

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
		'html': render_to_string('item/carousel/carousel_image.html', {'page_type':page_type, 'item':instance.item, 'image':instance})
	})
	return HttpResponse(resp, content_type='application/json')

@transaction.atomic
def delImage(request):
	if request.method != "POST":
		print("method not post")
		raise Http404
	
	# Check authentication
	if not request.user.is_authenticated():
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'Login required'}]})
		return HttpResponse(resp, content_type='application/json')

	form = PhotoDeleteForm(request.POST, request.FILES)
	
	if not form.is_valid():
		resp = json.dumps(
		{
			'status':'error',
			'errors': dict(form.errors.items())
		})
		return HttpResponse(resp, content_type='application/json')
		
	if not request.user == form.photo.user:	
		resp = json.dumps({'status':'error','custom_errors':[{'message': 'not your photo'}]})
		return HttpResponse(resp, content_type='application/json')
		

	form.photo.delete()
	
	resp = json.dumps({'status':'success'});
	
	return HttpResponse(resp, content_type='application/json')

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
	
	
	form = LinkForm(request.POST)
	if not form.is_valid():
		print(form.errors.items())
		raise Http404
	
	
	item = form.item
	link_item = form.link_item
	link_type = form.cleaned_data.get('link_type')
	
	if request.user != item.user:
		print("wrong user")
		raise Http404
	
	
	link_item.link.add(item)

	ret = render_to_string("item/bulk_sidebar/bulk_sidebar_item.html", {'request': request, 'link_item':link_item, 'item': item, 'link_item_type':link_type});
	
	return HttpResponse(ret, content_type="text/html")



@transaction.atomic
def delLink(request):
	
	if not request.user.is_authenticated():
		raise Http404
	
	if request.method != 'POST':
		raise Http404
	
	
	form = LinkForm(request.POST)
	if not form.is_valid():
		print('form error')
		print(form.errors.items())
		raise Http404
	
	
	item = form.item
	link_item = form.link_item
	link_type = form.cleaned_data.get('link_type')
	
	if request.user != item.user:
		print("wrong user")
		raise Http404
	
	
	link_item.link.remove(item)
	
	return HttpResponse("", content_type="text/html")
	