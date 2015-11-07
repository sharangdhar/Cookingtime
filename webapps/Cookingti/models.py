from django.db import models
from django.contrib.auth.models import User


TEXT_SIZE = 500



class Person(models.Model):
	user = models.ForeignKey(User)
	wattage = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)
	def __unicode_(self):
			return self.user.first_name

class Photo(models.Model):
	user = models.ForeignKey(User)
	picture = models.ImageField(upload_to='photos', blank=True)


class Review(models.Model):
	user = models.ForeignKey(User)
	stars = models.IntegerField(default=0, blank=False)
	review = models.CharField(max_length = TEXT_SIZE)
	date = models.DateTimeField(auto_now_add=True)
	photos = models.ForeignKey(Photo)
	def __unicode_(self):
		return self.review

class Food(models.Model):
	amazon_id = models.IntegerField(blank=True, null=True)
	name = models.CharField(max_length=TEXT_SIZE)
	reviews = models.ForeignKey(Review, blank=True, null=True)
	stars = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	photos = models.ForeignKey(Photo, null=True)

	def __unicode_(self):
		return self.name

class CookingTime(models.Model):
	user = models.ForeignKey(User)
	heatingConst = models.IntegerField() # Approximation of heating curve
	date = models.DateTimeField(auto_now_add=True)
	def __unicode_(self):
		return self.user.first_name
        
class Equipment(models.Model):
	amazon_id = models.IntegerField()
	name = models.CharField(max_length=TEXT_SIZE)
	reviews = models.ForeignKey(Review)
	date = models.DateTimeField(auto_now_add=True)
	photos = models.ForeignKey(Photo)
	def __unicode_(self):
		return self.name



class Recipe(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=TEXT_SIZE, default="")
	reviews = models.ForeignKey(Review)
	foods  = models.ManyToManyField(Food)
	text = models.CharField(max_length = TEXT_SIZE)
	date = models.DateTimeField(auto_now_add=True)
	photos = models.ForeignKey(Photo)
	def __unicode_(self):
		return self.text
        




