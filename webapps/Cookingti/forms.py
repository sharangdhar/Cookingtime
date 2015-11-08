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

#Form for changing the password
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(max_length = 200, 
                                label='Password', widget = forms.PasswordInput())                         
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',widget = forms.PasswordInput())

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ChangePasswordForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

#Form for getting the initial email to send reset password link to
class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length = 50, 
                                label='Enter Registered Email ID', widget = forms.EmailInput())


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user','date')

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('user',)

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


