
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'surname', 'password1', 'password2']
    
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'username', 
                                                             'required': True, 
                                                             'placeholder': 'username', 
                                                             'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"}))
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name', 
                                                         'required': True, 
                                                         'placeholder': 'Name', 
                                                         'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'id': 'surname', 
                                                            'required': True, 
                                                            'placeholder': 'Surname', 
                                                            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 
                                                                    'data-popover-target': "popover-password", 
                                                                    'data-popover-placement':"bottom",
                                                                  'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 
                                                                  'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    
class PassChangeForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]
    
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 
                                                                     'class': "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 
                                                                      'data-popover-target': "popover-password", 
                                                                      'data-popover-placement':"bottom",
                                                                      'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 
                                                                      'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'}))
    