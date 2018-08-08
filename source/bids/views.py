from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.db.models import Max
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView
import copy
from django.contrib import messages
from .forms import BidCreateForm
from auctions.models import Auction
from .models import Bid
# Create your views here.
class BidCreateView(CreateView):
	form_class=BidCreateForm
	template_name='bids/bid_create.html'
	queryset=Auction.objects.all()

	def get_context_data(self,*args,**kwargs):
		context=super(BidCreateView,self).get_context_data(*args,**kwargs)
		pk=self.kwargs.get('pk')
		auction=Auction.objects.filter(pk=pk)[0]
		context['auction']=auction
		bids=Bid.objects.filter(auction=auction)
		bid_times=bids.count()
		context['bid_times']=bid_times
		if bids:
			context['current_bid_price']=bids.aggregate(Max('bid'))['bid__max']
			context['current_bid']=bids.filter(bid=context['current_bid_price'])[0]
		return context

	def get_object(self):
		pk=self.kwargs.get('pk')
		obj=Auction.objects.filter(pk=pk)[0]
		self.request.session['version']=obj.version
		return obj

	def get_initial(self):
		initial=super().get_object()
		return {'auction':self.get_object()}

	def form_valid(self,form):
		au=self.get_object()
		instance=form.save(commit=False)
		bids=Bid.objects.filter(auction=au)
		max_bid=bids.aggregate(Max('bid'))['bid__max']


		# op2:soft deadlines
		now=timezone.now()
		deadline=instance.auction.deadline

		if (deadline-now) < timezone.timedelta(minutes=5):
			deadline+=timezone.timedelta(minutes=5)

		if self.kwargs.get('version')!= au.version:
			messages.add_message(self.request,messages.ERROR,'The auction description has been changed, please replace your bid again.')
			return HttpResponseRedirect(reverse('bid-create',kwargs={'pk': au.pk,'version':au.version}))

		elif instance.bid<=max_bid:
			messages.add_message(self.request,messages.ERROR,'A bid has been make before you. Please replace new bid.')
			return HttpResponseRedirect(reverse('bid-create',kwargs={'pk': au.pk,'version':au.version}))
			
		else:
			instance.bidder=self.request.user
			instance.auction=self.get_object()
			instance.save()

			bids=Bid.objects.filter(auction=instance.auction)
			other_bidders_email=[instance.bidder.email]
			for x in bids:
				other_bidders_email.append(x.bidder.email)		

			subject='New bid registered on YAAS'		
			path_=reverse('bid-create',kwargs={'pk': instance.auction.id,'version':instance.auction.version})
			message=f'A new bid has beed registered on {instance.auction.name}'
			# recipient_list=other_bidders_email
			recipient_list=['yuangao890@gmail.com']
			send_mail(
					subject,
					message,
					'yuangao890@gmail.com',
					recipient_list,
					fail_silently=False, 
					html_message=f'<p>Hi, a new bid has beed registered on <b>{instance.auction.name}</b></p><p>http://127.0.0.1:8000{path_}</p>'
				)			
		
			return super(BidCreateView,self).form_valid(form)


class MyBidListView(LoginRequiredMixin,ListView):
	template_name='bids/my_bids_list.html'
	def get_queryset(self):
		bids=Bid.objects.filter(bidder=self.request.user)
		return bids








