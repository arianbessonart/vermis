# -*- coding: utf-8 -*-
from django import forms
from models import Contact
from django.core.exceptions import ValidationError


class ContactForm(forms.ModelForm):
	"""docstring for ContactForm"""
	class Meta:
		model = Contact
		widgets = {
			'f_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
			'l_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido'}),
			'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
			'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Teléfono'}),
		}
		