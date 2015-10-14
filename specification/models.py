from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
	user = models.ForeignKey(User)
	microWattage = models.IntegerField()
	def __unicode_(self):
		return self.user.first_name

class Food(models.Model):
	amazon_id = models.IntegerField()
	reviews = models.ForeignKey(Review)
	def __unicode_(self):
		return self.reviews.review

class CookingTime(models.Model):
	user =  models.ForeignKey(User)
	heatingConst =  models.IntegerField()
	def __unicode_(self):
		return self.user.first_name

class Review(models.Model):
	stars = models.IntegerField(default=0, blank=False)
	review = models.CharField(max_length = 300)
	def __unicode_(self):
		return self.review

class Recipe(models.Model):
	reviews = models.ForeignKey(Review)
	foods  = models.ManytoManyField(Food)
	def __unicode_(self):
		return self.reviews.review