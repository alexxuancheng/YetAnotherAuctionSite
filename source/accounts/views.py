from django.contrib.auth import get_user_model
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,CreateView, DetailView,UpdateView
from accounts.models import Account
from .forms import RegisterForm,EmailForm,PasswordForm

User = get_user_model()

class HomeView(View):
	def get(self,request,*args,**kwargs):
		context={}
		return render(request,'home.html',context)

class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'registration/register.html'
	success_url = '/'

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect("/logout")
		return super(RegisterView, self).dispatch(*args, **kwargs)

class AccountView(LoginRequiredMixin,DetailView):
	template_name = 'accounts/account.html'
	def get_queryset(self):
		return User.objects.all()

class EmailUpdate(LoginRequiredMixin,UpdateView):
	form_class = EmailForm
	template_name = 'accounts/email-update.html'
	success_url = '/'

	def get_queryset(self):
		return User.objects.all()

class PasswordUpdate(LoginRequiredMixin,UpdateView):
	form_class = PasswordForm
	template_name = 'accounts/password-update.html'
	success_url = '/login/'

	def get_queryset(self):
		return User.objects.all()

