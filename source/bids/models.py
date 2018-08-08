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
from django.db.models import Max

from auctions.models import Auction

User=settings.AUTH_USER_MODEL

class Bid(models.Model):
	bidder			=models.ForeignKey(User,on_delete=models.CASCADE)
	auction 		=models.ForeignKey(Auction,on_delete=models.CASCADE)
	bid 			=models.DecimalField(max_digits=8,decimal_places=2)
	
	timestamp		=models.DateTimeField(auto_now_add=True)


	def __str__(self,*args,**kwargs):
		return self.auction.name

	def __init__(self, *args, **kwargs):
		super().__init__(*args,**kwargs)

	def get_absolute_url(self):
		return reverse('bid-create', kwargs={'pk': self.auction.pk,'version':self.auction.version})

	def clean(self,*args,**kwargs):
		bids=Bid.objects.filter(auction=self.auction)
		if not bids.exists():
			if self.bid<=self.auction.minprice:	
				raise ValidationError('Please enter bid more than minprice.')
		elif bids.exists():
			max_bid=bids.aggregate(Max('bid'))['bid__max']
			if self.bid<=max_bid:
				raise ValidationError('Please enter bid more than current bid.')







