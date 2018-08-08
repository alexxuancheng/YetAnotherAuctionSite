from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from auctions.models import Auction

User=get_user_model()

class AuctionAPITestCase(APITestCase):
	def setUp(self):
		user_test=User.objects.create(
			username='testuser',
			email='testuser@gmail.com'
		)
		user_test.set_password('somerandomtestpassword')
		user_test.save()
		auction_test =Auction.objects.create(
			seller=user_test,
			name='test_create_auction',
			description='descriptiondescriptiondescription',
			minprice='5.6',
			deadline='2018-03-25 14:30:59'
		)
	def test_single_user(self):
		user_count=User.objects.count() #objects.count()计算object被执行的次数的
		self.assertEqual(user_count,1) #判断a与1.b是否一致