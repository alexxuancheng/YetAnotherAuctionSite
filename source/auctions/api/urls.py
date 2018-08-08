from django.urls import path,include,re_path
from .views import AuctionListAPIView,BidCreateAPIView
app_name = 'auctions'

urlpatterns = [
    path('auctions/', AuctionListAPIView.as_view(),name='api-auction-list'),
    path('bids/', BidCreateAPIView.as_view(),name='api-bid-create'),
    # re_path(r'^(?P<pk>\d+)$', BidCreateAPIView.as_view(),name='api-bid-create'),
]

