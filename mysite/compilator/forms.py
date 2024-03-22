from .models import Folder, File, User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ("title", "description", "creation_date", "parent_folder")

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ("title", "description", "creation_date", "parent_folder")

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password')