from django.test import TestCase
from django.core.mail import send_mail,send_mass_mail
from django_dynamic_fixture import G
from django.utils import timezone
from decimal import Decimal
from auctions.models import Auction
from auctions.forms import AuctionCreateForm
from bids.models import Bid
from django.contrib.auth import get_user_model

User = get_user_model()

class AuctionModelTest(TestCase):
	fixtures=['auctions.json','users.json']

	def setUp(self):
		Auction.objects.create(
			seller=User.objects.get(pk=1),
			name='test',
			description='testusertestusertestusertestuser',
			minprice=6,
			deadline=timezone.now()+timezone.timedelta(days=4),
			version=0,
			activated=True,
			banned=False,
			due=False,
			adjudicated=False,
		)

	def test_name_label(self):
		auction=Auction.objects.last()
		field_label = auction._meta.get_field('name').verbose_name
		self.assertEquals(field_label,'name')

	def test_name_max_length(self):
		auction=Auction.objects.last()
		max_length = auction._meta.get_field('name').max_length
		self.assertEquals(max_length,120)

	def test_email_send(self):
		auction=Auction.objects.last()
		mail_send_success=send_mail(
				'subject:test send email',
				'message',
				'yuangao890@gmail.com',
				['yuangao890@gmail.com'],
				fail_silently=False
			)
		self.assertEquals(mail_send_success,1)

class AuctionCreateFormTest(TestCase):
	fixtures=['auctions.json','users.json']	

	def test_name_label(self):
		form=AuctionCreateForm()
		self.assertEquals(form.fields['name'].label,'Name')

	def test_clean_deadline_bigger_than_72h(self):
		form_data={
			'name':'test',
			'description':'testusertestusertestusertestuser',
			'minprice':6,
			'deadline':timezone.now()+timezone.timedelta(days=4),
		}
		form=AuctionCreateForm(data=form_data)
		self.assertTrue(form.is_valid())

	def test_clean_deadline_less_than_72h(self):
		form_data={
			'name':'test',
			'description':'testusertestusertestusertestuser',
			'minprice':6,
			'deadline':timezone.now()+timezone.timedelta(days=1),
		}
		form=AuctionCreateForm(data=form_data)
		self.assertFalse(form.is_valid())


# for i in range(0,50):
# 	instance_user = G(User,username='test_user_'+str(i))
# 	instance_auction=G(
# 		Auction,
# 		seller=instance_user,
# 		name=instance_user.username+'auction',
# 		description=instance_user.username+'description',
# 		minprice=i+0.1,
# 		deadline=timezone.now()+timezone.timedelta(hours=72+i),
# 		version=0,
# 		activated=True,
# 		banned=False,
# 		due=False,
# 		adjudicated=False,
# 	)
# 	print(instance_user.id)
# 	print(instance_user.username)
# 	print(instance_auction.id)
# 	print(instance_auction.seller)
# 	print(instance_auction.name)
# 	print(instance_auction.description)
# 	print(instance_auction.minprice)
# 	print(instance_auction.deadline)
# 	print(instance_auction.version)
# 	print(instance_auction.activated)

# for i in range(0,10):
# 	instance_bid=G(
# 		Bid,
# 		bidder=User.objects.filter(pk=310+i)[0],
# 		auction=Auction.objects.filter(pk=220+i)[0],
# 		bid=Auction.objects.filter(pk=220+i)[0].minprice+Decimal(0.1),
# 	)
# 	print(instance_bid.bidder)
# 	print(instance_bid.auction)
# 	print(instance_bid.bid)


		
