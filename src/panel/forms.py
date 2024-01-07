from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from .models import Thesis, Type, Language, Institute, Subject, Keyword, University

from account.models import User

class NewThesisForm(forms.ModelForm):

    class Meta:
        model = Thesis
        fields = ['title', 'abstract', 'type', 'language', 'institute', 'subjects', 'write_date', 'page_no']

    author = User
    title = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'id': 'title', 'required': True, 'placeholder': 'Thesis Title', 'class': "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    abstract = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'id': 'abstract', 'required': True, 'rows':'8', 'placeholder': 'Thesis Abstract', 'class': "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg shadow-sm border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    type = forms.ModelChoiceField(queryset=Type.objects.all().order_by("name"), empty_label=None, widget=forms.Select(attrs={'name':"type", 'id':"type", 'class': "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 disabled:opacity-70 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    language = forms.ModelChoiceField(queryset=Language.objects.all().order_by("name"), empty_label=None, widget=forms.Select(attrs={'name':"language", 'id':"language", 'class': "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 disabled:opacity-70 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    institute = forms.ModelChoiceField(queryset=Institute.objects.all().order_by("university__name"), empty_label=None, widget=forms.Select(attrs={'name':"institute", 'id':"institute", 'class': "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 disabled:opacity-70 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all().order_by("heading"), widget=forms.SelectMultiple(attrs={'name':"subjects", 'id':"subjects", 'class': "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 disabled:opacity-70 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    write_date = forms.DateField(localize=False, input_formats=['%d/%m/%Y'], widget=forms.DateInput(format="%d/%m/%Y", attrs={'id': 'write_date', 'required': True, 'datepicker': True, 'placeholder': 'Please select a date.','datepicker-format':'dd/mm/yyyy', 'class': "rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    page_no = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'page', 'required': True, 'placeholder': 'Page Count', 'class': "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 disabled:opacity-70 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    

class NewInstituteForm(forms.ModelForm):
    
    class Meta:
        model = Institute
        fields = ['name', 'university']
    
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'name', 'required': True, 'placeholder': 'Institute Name', 'class': "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 disabled:opacity-70 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    university = forms.ModelChoiceField(queryset=University.objects.all().order_by("name"), empty_label=None, widget=forms.Select(attrs={'name':"university", 'id':"university", 'class': "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 disabled:opacity-70 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    