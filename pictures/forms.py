from pictures.models import Images
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserChangeForm
from django.forms import Textarea
import datetime
from taggit.forms import TagField
from taggit.forms import TagWidget
from dal import autocomplete
from taggit.models import Tag
from pictures.models import Profile

username_regex =  RegexValidator(r'^(?!\.)(?!.*\.$)(?!.*?\.\.)[a-zA-Z0-9._ ]+$', 'You may only use alphanumeric characters and/or periods and hyphen')
alphanumeric = RegexValidator(r"^(?:[^\W_]|[ '-])+$", 'Only alphanumeric characters are allowed.')

class ImagesForm(forms.ModelForm):
    description= forms.CharField(
        label='',
        max_length=180,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Whats this image about?',
                'style': 'resize:none',
                'rows': 3,
                'cols': 40}))
    
    class Meta:
        model = Images
        labels = {
            "tags": "",
        }
        help_texts = {
            'tags': ' ',
        }
        fields = ('description','image_photo','tags',)
        
    
    def __init__(self, *args, **kwargs): 
        super(ImagesForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields.pop('image_photo')
        else:
            self.fields['image_photo'].widget.attrs['required'] = 'required'
        self.fields['tags'].widget.attrs['class'] = 'row ml-h'
        self.fields['tags'].widget.attrs['placeholder'] = 'Add tags'

class EditProfileForm(UserChangeForm): 
    
	username = forms.CharField(
		max_length=255,
		min_length=1,
		required=True,
		validators=[username_regex],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Username",
				"class": "form-control mb-2",
				
			}
		)
	)

	first_name = forms.CharField(
		max_length=255,
		min_length=1,
		required=True,
		validators=[alphanumeric],
		widget=forms.TextInput(
			attrs={
				"placeholder": "First name",
				"class": "form-control mb-2",
    			
			}
		)
	)

	last_name = forms.CharField(
		max_length=255,
		min_length=1,
		required=True,
		validators=[alphanumeric],
		widget=forms.TextInput(
			attrs={
				"placeholder": "Last name",
				"class": "form-control mb-2",
    			
			}
		)
	)
    
	bio = forms.CharField(
		required=False,
		widget=forms.Textarea(
			attrs={
				"placeholder":"Tell everyone something about yourself",
				"class": "form-control mt-3",
				"rows":"5",
    		
			}
		)
	)
  
	password = None
 
	error_css_class = "error"
 
	class Meta:
		model = Profile
		fields=('username','email','first_name','last_name','profile_image','bio',)
		help_texts = {
			"profile_image":"Choose a new image or select the check box to remove your existing image"
		}
        
