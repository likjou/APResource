from cProfile import label
from logging import FileHandler
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import TorFile

class UploadFile(forms.ModelForm):

    file_field= forms.FileField()

    class Meta:
        model = TorFile
        fields = ('title','desc', 'file_field', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'my-title-class uploadinput', 'placeholder':'Title'})
        self.fields['desc'].widget.attrs.update({'class': 'my-desc-class uploadinput','placeholder':'Description'})
        self.fields['file_field'].widget.attrs.update({'class': 'my-filedield-class filefield', 'accept':'.torrent'})
        self.fields['category'].widget.attrs.update({'class': 'my-category-class uploadinput'})
   
class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'my-username-class updateinput', 'placeholder':'Username'})
        self.fields['email'].widget.attrs.update({'class': 'my-email-class updateinput','placeholder':'Email'})
        self.fields['first_name'].widget.attrs.update({'class': 'my-firstname-class updateinput', 'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'my-lastname-class updateinput','placeholder':'Last Name'})
   
   
   
   