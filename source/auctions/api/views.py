from django.db.models import Q
from django.http import HttpResponse
from rest_framework import generics,serializers,mixins
from decimal import Decimal
from django.core.exceptions import ValidationError
from auctions.models import Auction
from bids.models import Bid
from .permissions import CustomerAccessPermission
from .serializers import AuctionSerializer,BidSerializer

class AuctionListAPIView(generics.ListAPIView):
	serializer_class 	=AuctionSerializer
	queryset			=Auction.objects.all()

	def get_queryset(self):
		qs=Auction.objects.all()
		query=self.request.GET.get('q')
		if query is not None:
			qs=qs.filter(
				Q(name__icontains=query)|
				Q(description__icontains=query)
			).distinct()
		return qs

class BidCreateAPIView(mixins.CreateModelMixin,generics.ListAPIView):
	serializer_class 	=BidSerializer
	queryset=Bid.objects.all()

	def perform_create(self, serializer):
		serializer.save(bidder=self.request.user)

	def post(self,request,*args,**kwargs):
		return self.create(request,*args,**kwargs)


		
