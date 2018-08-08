from django import forms
from .models import Bid
from django.utils import timezone
from django.core.exceptions import ValidationError

class BidCreateForm(forms.ModelForm):
	class Meta:
		model=Bid
		fields=['bid','auction']


	# deadline=forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

	# def clean_deadline(self):
	# 	deadline = self.cleaned_data['deadline']
	# 	if deadline < (timezone.now()+timezone.timedelta(hours=72)):
	# 		raise ValidationError("The duration of the auction has to be at least 72h")

	# def save(self,commit=True):
	# 	auction=super(AuctionCreateForm,self).save(commit=False)
	# 	if commit:
	# 		auction.send_activation_email()
	# 	return auction