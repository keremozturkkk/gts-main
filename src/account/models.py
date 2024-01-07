import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator

class UserManager(BaseUserManager):
	
	def create_user(self, username, password=None):
		if not username:
			raise ValueError('Kullanıcı adı zorunludur.')

		user = self.model(
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password):
		user = self.create_user(
			password=password,
			username=username,
		)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser, PermissionsMixin):
	
	username = models.CharField(max_length=18, 
			     unique=True, 
				 help_text=("Zorunlu. 18 karakter veya daha az. Sadece harfler, rakamlar ve @/./+/-/_ işaretleri."),
        		 validators=[UnicodeUsernameValidator()],)
	
	name = models.CharField(max_length=30)
	surname = models.CharField(max_length=30)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	
	objects = UserManager()

	def __str__(self):
		return self.username
	
    #TODO PERMISSION SYSTEM
	def has_perm(self, perm, obj=None):
		return self.is_staff

	#TODO MODULE BASED VIEW PERM SYSTEM
	def has_module_perms(self, app_label):
		return True
	


