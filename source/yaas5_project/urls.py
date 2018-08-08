from django.contrib import admin
from django.urls import path,re_path,include
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls.i18n import i18n_patterns
from auctions.models import Auction

from accounts.views import RegisterView,AccountView,EmailUpdate,PasswordUpdate

from auctions.views import (
    HomeView,
    AuctionListView,
    AuctionCreateView,
    AuctionUpdateView,
    AuctionBanView,
    BannedAuctionListView,
    activate_user_view
)
from bids.views import BidCreateView,MyBidListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auctions.api.urls',namespace='auctions-api')),
    
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),

    path('', HomeView.as_view(),name='home'),
    path('auctions/<slug:pk>/ban/', AuctionBanView.as_view(),name='auction-ban'),
    path('banned_auctions/', BannedAuctionListView.as_view(),name='auction-banned'),

    path('bids/<slug:pk>/<slug:version>/', BidCreateView.as_view(),name='bid-create'),

    path('my_auctions/create/',AuctionCreateView.as_view(),name='auction-create'),
    path('my_auctions/<slug:pk>/',AuctionUpdateView.as_view(),name='my-auctions-detail-update'),
    path('my_auctions/',AuctionListView.as_view(),name='my-auctions-list'),  
    path('my_bids/',MyBidListView.as_view(),name='my-bids-list'),

    path('account/<slug:pk>/',AccountView.as_view(),name='myaccount'),
    path('account/<slug:pk>/emailupdate/',EmailUpdate.as_view(),name='emailupdate'),
    path('account/<slug:pk>/passwordupdate/',PasswordUpdate.as_view(),name='passwordupdate'),

    re_path(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view,name='activate-auction'),
    path('i18n/', include('django.conf.urls.i18n'))
]

urlpatterns += i18n_patterns(    
    path('', HomeView.as_view(),name='home'),
    path('my_bids/',MyBidListView.as_view(),name='my-bids-list'),
    path('banned_auctions/', BannedAuctionListView.as_view(),name='auction-banned'),
    path('my_auctions/create/',AuctionCreateView.as_view(),name='auction-create'),
    path('my_auctions/<slug:pk>/',AuctionUpdateView.as_view(),name='my-auctions-detail-update'),
    path('my_auctions/',AuctionListView.as_view(),name='my-auctions-list'),  
    path('my_bids/',MyBidListView.as_view(),name='my-bids-list'),
    path('account/<slug:pk>/',AccountView.as_view(),name='myaccount'),
    
)





