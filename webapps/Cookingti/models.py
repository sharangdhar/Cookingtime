from django.db import models
from django.contrib.auth.models import User


TEXT_SIZE = 500



class Person(models.Model):
	user = models.ForeignKey(User, related_name='person')
	wattage = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)
	def __unicode_(self):
			return self.user.first_name

class Photo(models.Model):
	user = models.ForeignKey(User)
	picture = models.ImageField(upload_to='photos', blank=True)


class Food(models.Model):
	amazon_id = models.IntegerField(blank=True, null=True)
	name = models.CharField(max_length=TEXT_SIZE)
	stars = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	photos = models.ForeignKey(Photo, blank=True, null=True)
	avgConst = models.FloatField(default=4.18)
	numConst = models.IntegerField(default=1, blank=True)
	
	def __unicode_(self):
		return self.name

class Review(models.Model):
	user = models.ForeignKey(User, blank=True)
	title = models.CharField(max_length=TEXT_SIZE, default="")
	stars = models.IntegerField(default=0, blank=True, null=True)
	review = models.CharField(max_length = TEXT_SIZE)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	photos = models.ForeignKey(Photo, blank=True, null=True)
	item = models.ForeignKey(Food, related_name='reviews')
	
	def __unicode_(self):
		return self.review

'''
class CookingTime(models.Model):
	user = models.ForeignKey(User, blank=True)
	heatingConst = models.FloatField(default=4.18) # Approximation of heating curve
	date = models.DateTimeField(auto_now_add=True, blank=True)
	def __unicode_(self):
		return self.user.first_name
'''

class Equipment(models.Model):
	amazon_id = models.IntegerField(blank=True, null=True)
	name = models.CharField(max_length=TEXT_SIZE)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	stars = models.IntegerField(blank=True, null=True)
	photos = models.ForeignKey(Photo, blank=True, null=True)
	def __unicode_(self):
		return self.name


class Recipe(models.Model):
	user = models.ForeignKey(User, blank=True)
	name = models.CharField(max_length=TEXT_SIZE, default="")
	text = models.CharField(max_length=TEXT_SIZE, default="", blank=True, null=True)
	foods = models.ManyToManyField(Food, related_name='recipes')
	text = models.CharField(max_length = TEXT_SIZE, blank=True, default="")
	date = models.DateTimeField(auto_now_add=True, blank=True)
	photos = models.ForeignKey(Photo, blank=True, null=True)
	def __unicode_(self):
		return self.text
        




