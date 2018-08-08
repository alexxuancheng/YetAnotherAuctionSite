from django.test import TestCase
from django.core.mail import send_mail,send_mass_mail
from django_dynamic_fixture import G
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
from decimal import Decimal
from auctions.models import Auction
from auctions.forms import AuctionCreateForm
from bids.models import Bid
from bids.forms import BidCreateForm
from django.contrib.auth import get_user_model

User = get_user_model()

class BidModelTest(TestCase):
	fixtures=['auctions.json','users.json','bids.json']

	def setUp(self):
		Bid.objects.create(
			bidder=User.objects.get(pk=2),
			auction=Auction.objects.last(),
			bid=7,
		)

	def test_bid_label(self):
		bid=Bid.objects.last()
		field_label = bid._meta.get_field('bid').verbose_name
		self.assertEquals(field_label,'bid')

	def test_clean(self):
		bid2=Bid.objects.create(
			bidder=User.objects.get(pk=2),
			auction=Auction.objects.filter(pk=7)[0],
			bid=2,
		)
		self.assertRaises(ValidationError,bid2.clean)

	def test_email_send(self):
		bid=Bid.objects.last()
		mail_send_success=send_mail(
				'subject:test send email',
				'message',
				'yuangao890@gmail.com',
				['yuangao890@gmail.com'],
				fail_silently=False
			)
		self.assertEquals(mail_send_success,1)

class BidCreateFormTest(TestCase):
	fixtures=['auctions.json','users.json']	

	def test_bid_label(self):
		form=BidCreateForm()
		self.assertEquals(form.fields['bid'].label,'Bid')

class BidCreateViewTest(TestCase):
	fixtures=['auctions.json','users.json','bids.json']
		
	def test_description_change(self):
		bid1=Bid.objects.create(
			bidder=User.objects.get(pk=2),
			auction=Auction.objects.filter(pk=4)[0],
			bid=5,
		)
		bid1.auction.version+=1
		self.assertTrue(messages)
		
	def test_bid_greater_than_any(self):
		bid1=Bid.objects.create(
			bidder=User.objects.get(pk=2),
			auction=Auction.objects.filter(pk=7)[0],
			bid=12,
		)
		bid2=Bid.objects.create(
			bidder=User.objects.get(pk=1),
			auction=Auction.objects.filter(pk=7)[0],
			bid=11,
		)
		self.assertTrue(messages)
