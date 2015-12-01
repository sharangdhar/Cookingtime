from django import forms

from django.contrib.auth.models import User

from Cookingti.models import *

class RegistrationForm(forms.Form):
	username = forms.CharField(max_length = 20, widget = forms.TextInput(attrs={"placeholder":"username"}))
	password1 = forms.CharField(max_length = 200, 
								label='Password', widget = forms.PasswordInput(attrs={"placeholder":"password"}))						  
	password2 = forms.CharField(max_length = 200, 
								label='Confirm password',widget = forms.PasswordInput(attrs={"placeholder":"confirm"}))
	firstname = forms.CharField(max_length = 200, 
								label='Firstname', widget = forms.TextInput(attrs={"placeholder":"first name"}))
	lastname = forms.CharField(max_length = 200, 
								label='Lastname', widget = forms.TextInput(attrs={"placeholder":"last name"}))
	email = forms.EmailField(max_length = 50, 
								label='Email', widget = forms.EmailInput(attrs={"placeholder":"email"}))
	wattage = forms.IntegerField(label='Wattage', widget = forms.NumberInput(attrs={"placeholder":"wattage"}))

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()

		# Confirms that the two password fields match
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		return cleaned_data

	def clean_username(self):
		# Confirms that the username is not already present in the
		# User model database.
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")

		return username


class ProfileForm(forms.Form):
	user_id = forms.IntegerField()
	user = ""
	person = ""
	
	firstname = forms.CharField(max_length = 200, label='Firstname')
	lastname = forms.CharField(max_length = 200, label='Lastname')
	email = forms.EmailField(max_length = 50, label='Email')
	wattage = forms.IntegerField(label='Wattage')


	def clean_user_id(self):
		user_id = self.cleaned_data.get('user_id')
		
		try:
			self.user = User.objects.get(id=user_id)
		except: 
			raise forms.ValidationError("Invalid user_id")
		
		try:
			self.person = Person.objects.get(user=self.user)
		except:
			raise forms.ValidationError("Could not find person for user")
		
		return user_id
		

#Form for changing the password
class ChangePasswordForm(forms.Form):
	password1 = forms.CharField(max_length = 200, 
								label='Password', widget = forms.PasswordInput())						  
	password2 = forms.CharField(max_length = 200, 
								label='Confirm password',widget = forms.PasswordInput())

	def clean(self):
		cleaned_data = super(ChangePasswordForm, self).clean()

		# Confirms that the two password fields match
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		return cleaned_data



class resetPassForm(forms.Form):
    email = forms.EmailField(max_length = 50, 
                                label='Enter Registered Email ID', widget = forms.EmailInput(attrs={'class': 'form-control'}))




class FoodReviewForm(forms.ModelForm):
	class Meta:
		model = FoodReview
		exclude = ('user','date', 'photos', 'item')


class RecipeReviewForm(forms.ModelForm):
	class Meta:
		model = RecipeReview
		exclude = ('user','date', 'photos', 'item')
		

class EquipmentReviewForm(forms.ModelForm):
	class Meta:
		model = EquipmentReview
		exclude = ('user','date', 'photos', 'item')




class FoodPhotoForm(forms.ModelForm):
	item_id = forms.IntegerField()

	class Meta:
		model = FoodPhoto
		exclude = ('user','item')
	
	def clean_item_id(self):
		item_id = self.cleaned_data.get('item_id')
		
		try:
			self.instance.item = Food.objects.get(id=item_id)
		except: 
			raise forms.ValidationError("Invalid item_id")
		
		return item_id

class PhotoDeleteForm(forms.Form):
	item_id = forms.IntegerField()
	
	photo_id = forms.IntegerField()
	photo = ''
	
	page_type = forms.CharField(max_length = 20)

		
	def clean(self):
		cleaned_data = super(PhotoDeleteForm, self).clean()
		
		page_type = cleaned_data.get('page_type')
		photo_id = cleaned_data.get('photo_id')
		item_id = cleaned_data.get('item_id')
		
		if page_type == 'food':
			try:
				item = Food.objects.get(id=item_id)
			except:
				raise forms.ValidationError("No such item")
		elif page_type == 'recipe':
			try:
				item = Recipe.objects.get(id=item_id)
			except:
				raise forms.ValidationError("No such item")
		elif page_type == 'equipment':
			try:
				item = Equipment.objects.get(id=item_id)
			except:
				raise forms.ValidationError("No such item")
		else:
			raise forms.ValidationError("Invalid Page type")
			
		try:

			self.photo = item.photos.get(id=photo_id)
		except:
			raise forms.ValidationError("No such image")
		
		return cleaned_data
		

class RecipePhotoForm(forms.ModelForm):
	item_id = forms.IntegerField()

	class Meta:
		model = RecipePhoto
		exclude = ('user','item')
	
	def clean_item_id(self):
		item_id = self.cleaned_data.get('item_id')
		
		try:
			self.instance.item = Recipe.objects.get(id=item_id)
		except: 
			raise forms.ValidationError("Invalid item_id")
		
		return item_id
		
		
class EquipmentPhotoForm(forms.ModelForm):
	item_id = forms.IntegerField()

	class Meta:
		model = EquipmentPhoto
		exclude = ('user','item')
	
	def clean_item_id(self):
		item_id = self.cleaned_data.get('item_id')
		
		try:
			self.instance.item = Equipment.objects.get(id=item_id)
		except: 
			raise forms.ValidationError("Invalid item_id")
		
		return item_id


class BarcodePhotoForm(forms.ModelForm):
	class Meta:
		model = BarcodePhoto
		fields = ['picture']


class AddItemForm(forms.Form):
	item = forms.CharField(max_length = 20, widget = forms.TextInput())
	item_type = forms.CharField(max_length = 20, widget = forms.TextInput(attrs={"placeholder":"name"}))

	def clean(self):
		cleaned_data = super(AddItemForm, self).clean()

		item_type = cleaned_data.get('item_type')
		print item_type

		if item_type not in ['food', 'recipe', 'equipment']:
			raise forms.ValidationError("Invalid Item Type.")

		return cleaned_data
		



class TimeForm(forms.Form):
	item_id = forms.IntegerField()
	item = ''
	constant = forms.FloatField()
	
	def clean_item_id(self):
		item_id = self.cleaned_data.get('item_id')
		
		try:
			self.item = Food.objects.get(id=item_id)
		except:
			raise forms.ValidationError("Invalid item_id")
		
		return item_id
		



class RecipeTextForm(forms.ModelForm):
	item_id = forms.IntegerField()
	
	class Meta:
		model = Recipe
		fields = ('text',)
	
	def clean_item_id(self):
		item_id = self.cleaned_data.get('item_id')
		
		try:
			self.instance = Recipe.objects.get(id=item_id)
		except:
			raise forms.ValidationError("Invalid item_id")
		
		return item_id
		
		
		
		
class FoodReviewForm(forms.ModelForm):
	item_id = forms.IntegerField()
	
	class Meta:
		model = FoodReview
		exclude = ('user','date', 'item')
		
	def clean_item_id(self):
		item_id = self.cleaned_data.get('item_id')
		
		try:
			self.instance.item = Food.objects.get(id=item_id)
		except:
			raise forms.ValidationError("Invalid item_id")
		
		return item_id
	
	def clean_stars(self):
		stars = self.cleaned_data.get('stars')
		
		if stars < 1 or stars > 5:
			raise forms.ValidationError("Rating must be between 1 and 5 (inclusive)")
		
		return stars
		
		
class RecipeReviewForm(forms.ModelForm):
	item_id = forms.IntegerField()
	
	class Meta:
		model = RecipeReview
		exclude = ('user','date', 'item')
		
	def clean_item_id(self):
		item_id = self.cleaned_data.get('item_id')
		
		try:
			self.instance.item = Recipe.objects.get(id=item_id)
		except:
			raise forms.ValidationError("Invalid item_id")
		
		return item_id
	
	def clean_stars(self):
		stars = self.cleaned_data.get('stars')
		
		if stars < 1 or stars > 5:
			raise forms.ValidationError("Rating must be between 1 and 5 (inclusive)")
		
		return stars
		
		
class EquipmentReviewForm(forms.ModelForm):
	item_id = forms.IntegerField()
	
	class Meta:
		model = EquipmentReview
		exclude = ('user','date', 'item')
		
	def clean_item_id(self):
		item_id = self.cleaned_data.get('item_id')
		
		try:
			self.instance.item = Equipment.objects.get(id=item_id)
		except:
			raise forms.ValidationError("Invalid item_id")
		
		return item_id
	
	def clean_stars(self):
		stars = self.cleaned_data.get('stars')
		
		if stars < 1 or stars > 5:
			raise forms.ValidationError("Rating must be between 1 and 5 (inclusive)")
		
		return stars
		

class LinkForm(forms.Form):
	item_id = forms.IntegerField()
	item = ""
	
	link_id = forms.IntegerField()
	link_item = ""
	
	link_type = forms.CharField(max_length = 20)
	
	def clean_link_type(self):
		link_type = self.cleaned_data.get('link_type')
		
		if link_type not in ['food', 'recipe']:
			raise forms.ValidationError("Invalid Link Type.")
		
		return link_type
		
	
	def clean(self):
		cleaned_data = super(LinkForm, self).clean()
		
		link_type = cleaned_data.get('link_type')
		link_id = cleaned_data.get('link_id')
		item_id = cleaned_data.get('item_id')
		
		if link_type == 'food':
			try:
				self.link_item = Food.objects.get(id=link_id)
			except:
				raise forms.ValidationError("Invalid Link ID.")
				
			try:
				self.item = Recipe.objects.get(id=item_id)
			except:
				raise forms.ValidationError("Invalid Item ID.")
		else:
			try:
				self.link_item = Recipe.objects.get(id=link_id)
			except:
				raise forms.ValidationError("Invalid Link ID.")
				
			try:
				self.item = Food.objects.get(id=item_id)
			except:
				raise forms.ValidationError("Invalid Item ID.")
		
		return cleaned_data