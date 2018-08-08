from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView


from .forms import AuctionCreateForm,AuctionUpdateForm
from .models import Auction
from bids.models import Bid
# Create your views here.
class HomeView(ListView):
	template_name='auctions/auction_list.html'
	def get_queryset(self):
		return Auction.objects.all()
		
	def get_context_data(self,*args,**kwargs):
		context=super(HomeView,self).get_context_data(*args,**kwargs)
		query=self.request.GET.get('q')
		context['object_list']=Auction.objects.all().order_by('-updated')

		if query:			
			context['object_list']=Auction.objects.filter(name__icontains=query)
		return context

class AuctionListView(LoginRequiredMixin,ListView):
	template_name='auctions/my_auction_list.html'
	def get_queryset(self):
		return Auction.objects.filter(seller=self.request.user)

class AuctionCreateView(LoginRequiredMixin,CreateView):
	form_class=AuctionCreateForm
	template_name='auctions/my_auction_create.html'

	def form_valid(self,form):
		instance=form.save(commit=False)
		instance.seller=self.request.user
		instance.deadline=self.request.POST.get('deadline')
		
		return super(AuctionCreateView,self).form_valid(form)

class AuctionUpdateView(LoginRequiredMixin,UpdateView):
	form_class=AuctionUpdateForm
	template_name='auctions/my_auction_update.html'

	def get_queryset(self):
		return Auction.objects.filter(seller=self.request.user)

	def form_valid(self,form):
		instance=form.save(commit=False)
		instance.version+=1	
		return super(AuctionUpdateView,self).form_valid(form)

class AuctionBanView(LoginRequiredMixin,View):
	def post(self, request, *args, **kwargs):
		auction_pk=self.kwargs.get('pk')
		auction=Auction.objects.filter(pk=auction_pk)[0]

		auction.activated=False
		auction.banned=True
		auction.save()

		bids=Bid.objects.filter(auction=auction)

		other_bidders_email=[auction.seller.email]
		for x in bids:
			other_bidders_email.append(x.bidder.email)

		subject='An Auction Banned'		
		path_=reverse('bid-create',kwargs={'pk': auction_pk})
		message=f'{auction.name} has been banned.'
		# recipient_list=other_bidders_email
		recipient_list=['yuangao890@gmail.com']
		send_mail(
				subject,
				message,
				'yuangao890@gmail.com',
				recipient_list,
				fail_silently=False, 
				html_message=f'<p><b>{auction.name}</b> has beed banned</p><p>Check on http://127.0.0.1:8000{path_}</p>'
			)
		return redirect("/")
		
class BannedAuctionListView(LoginRequiredMixin,ListView):
	template_name='auctions/auction_banned_list.html'
	def get_queryset(self):
		return Auction.objects.filter(banned=True).order_by('-updated')

def activate_user_view(request, code=None, *args, **kwargs):
	if code:
		qs = Auction.objects.filter(activation_key=code)
		if qs.exists() and qs.count() == 1:
			auction = qs.first()
			if not auction.activated:
				auction.activated=True
				auction.activation_key=None
				auction.save()
				return redirect("/")
	return redirect("/")