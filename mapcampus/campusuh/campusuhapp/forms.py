from django import forms
from django.db import connection

class HomeSearch(forms.Form):
	search = forms.CharField(required=True)

class ObjectsSearch(forms.Form):
	search = forms.CharField(required=True)

class ObjectsSearchAdvanced(forms.Form):
	search = forms.CharField(required=False)
	ObjectType = forms.CharField(required=False)