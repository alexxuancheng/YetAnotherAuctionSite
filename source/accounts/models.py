from django.conf import settings
from django.db import models
from django.utils import translation
from django.db.models.signals import post_save

User=settings.AUTH_USER_MODEL

class Account(models.Model):
	user 			=models.OneToOneField(User,on_delete=models.CASCADE)
	# language 		=models.CharField(max_length=120)
	email 			=models.EmailField(max_length=120)
	password 		=models.CharField(max_length=120)
	timestamp		=models.DateTimeField(auto_now_add=True)
	updated			=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username


def post_save_user_receiver(sender,instance,created,*args,**kwargs):
	if created:
		account,is_created=Account.objects.get_or_create(
			user=instance,
			email=instance.email,
			)

post_save.connect(post_save_user_receiver,sender=User)