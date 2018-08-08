from rest_framework import serializers
from django.db.models import Max
from auctions.models import Auction
from bids.models import Bid

class AuctionSerializer(serializers.ModelSerializer):
	# url =serializers.SerializerMethodField(read_only=True)
	class Meta:
		model=Auction
		fields=[
			# 'url',
			'pk',
			'seller',
			'name',
			'description',
			'minprice',
			'deadline',
		]

class BidSerializer(serializers.ModelSerializer):
	class Meta:
		model=Bid
		fields=[
			'bidder',
			'auction',
			'bid'
		]	
		read_only_fields = (
			'bidder',
		)

	def validate_auction(self,value):
		request=self.context.get('request')
		au=Auction.objects.filter(seller=request.user)
		if value in au:
			raise serializers.ValidationError('You can not bid on your own auctions.')
		return value

	def validate_bid(self,value):
		bids=Bid.objects.filter(auction=self.initial_data['auction'])
		au=Auction.objects.filter(pk=self.initial_data['auction'])[0]
		print(au)
		if bids:
			max_bid=bids.aggregate(Max('bid'))['bid__max']
			print(type(max_bid))
			print(type(value))
			if value <= max_bid:
				raise serializers.ValidationError('Please bid more than the newest bid.')
		else:
			if value <= au.minprice:
				raise serializers.ValidationError('Please bid more than the minprice of the auction.')
		return value
