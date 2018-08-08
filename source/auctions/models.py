from django.conf import settings
from django.urls import reverse
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.core.mail import send_mail,send_mass_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse as api_reverse
import datetime
from .utils import code_generator

User=settings.AUTH_USER_MODEL

class Auction(models.Model):
	seller 			=models.ForeignKey(User,on_delete=models.CASCADE)
	name 			=models.CharField(max_length=120)
	description 	=models.TextField(null=True,blank=True)
	minprice		=models.DecimalField(max_digits=8,decimal_places=2)
	deadline	 	=models.DateTimeField(auto_now=False)
	

	timestamp		=models.DateTimeField(auto_now_add=True)
	updated			=models.DateTimeField(auto_now=True)

	version 		=models.IntegerField(default=0)

	activation_key 	=models.CharField(max_length=120,blank=True,null=True)
	activated 		=models.BooleanField(default=False)
	banned			=models.BooleanField(default=False)
	due				=models.BooleanField(default=False)
	adjudicated		=models.BooleanField(default=False)


	def __str__(self,*args,**kwargs):
		return self.name

	def get_absolute_url(self):
		return reverse('my-auctions-detail-update', kwargs={'pk': self.pk})

	def send_activation_email(self):
		if not self.activated:
			self.activation_key=code_generator()
			self.save()
			print(self.pk)
			path_=reverse('activate-auction',kwargs={'code':self.activation_key})
			path1_=reverse('my-auctions-detail-update',kwargs={'pk': self.pk})
			subject = 'Activate Auction'
			from_email = settings.DEFAULT_FROM_EMAIL
			message = f'Activate your auction here:{path_}'
			recipient_list =['yuangao890@gmail.com'] 
			# recipient_list =[self.user.email] 
			html_message = f'<p>Activate your auction here:  http://127.0.0.1:8000{path_}</p><p>Check your created auction here: http://127.0.0.1:8000{path1_}</p>'
			print(html_message)

			# task_mail.delay(self.activation_key,self.pk)
	# 		
			sent_email=send_mail(
				subject,
				message,
				'yuangao890@gmail.com',
				recipient_list,
				fail_silently=False, 
				html_message=html_message
			)
			return sent_email


		def save(self, *args, **kwargs):
			now=timezone.now().strftime("%Y-%m-%d %H:%M:%S")
			deadline=self.deadline
				
			if type(self.deadline) is datetime.datetime:
				deadline=self.deadline.strftime("%Y-%m-%d %H:%M:%S")

			if self.activated and deadline < now:
				self.due=True
				self.activated=False


			if self.due and not self.adjudicated:
				other_bidders_email=[self.seller.email]
				# for x in self.bidders.all():
				# 	other_bidders_email.append(x.email)

				subject='A winner has beed selected!'		
				path_=reverse('make-bid',kwargs={'pk':self.pk,'version':self.version})
				message=f'{self.name} got a winner. '

				subject1='Congratulations! You win an auction on YAAS!'		
				path1_=reverse('make-bid',kwargs={'pk':self.pk,'version':self.version})
				message1=f'You are the winner of {self.name}. Check on http://127.0.0.1:8000{path1_}'

				subject2='A winner has beed selected!'		
				path2_=reverse('make-bid',kwargs={'pk':self.pk,'version':self.version})
				message2=f'{self.name} got a winner. Check on http://127.0.0.1:8000{path2_}'
				# recipient_list=other_bidders_email
				recipient_list=['yuangao890@gmail.com']

				datatuple=(
						(subject1,message1,'yuangao890@gmail.com',recipient_list),
						(subject2,message2,'yuangao890@gmail.com',recipient_list),	
					)
				send_mass_mail(
					datatuple,
					fail_silently=False
					)
				self.adjudicated=True







