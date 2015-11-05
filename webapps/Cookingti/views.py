from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
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
	context = {}
	return render(request, 'Cookingti/hs_main.html', context)



def profile(request):
	context = {}
	return render(request, 'Cookingti/profile.html', context)


def register(request):

	context = {}

	if request.user.is_authenticated():
		return redirect('/Cookingti/profile')

	# Just display the registration form if this is a GET request.
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'Cookingti/registration.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
	form = RegistrationForm(request.POST)

	context['form'] = form

    # Validates the form.
	if not form.is_valid():

		context['errors'] = form.errors
		return render(request, 'Cookingti/registration.html', context)


    # Logs in the new user and redirects to his/her todo list
	new_user = User.objects.create_user(username= request.POST['username'], password = request.POST['password1'],
		first_name=request.POST["firstname"],last_name= request.POST["lastname"], email=request.POST["email"] )
	new_user.save()

	new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

	login(request, new_user)

	return redirect('/Cookingti/')












