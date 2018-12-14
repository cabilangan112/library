from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Course,Department
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
)
from .forms import UserLoginForm, UserRegisterForm

class LoginView(TemplateView):
	"""
	Display log in page where registered users can log in
	"""
	template_name = "registration/login.html"

	def get_context_data(self, *args, **kwargs):
		context = super(LoginView, self).get_context_data(*args, **kwargs)
		title = "Login"
		form = UserLoginForm(self.request.POST or None)
		context.update({
			"title":title,
			"form":form,
		})
		return context

	def post(self, *args, **kwargs):
		context = self.get_context_data()
		form = context.get('form')
		if form.is_valid():
			user = form.save()
			login(self.request, user)
			return redirect("/")

		return render(self.request, self.template_name, context)

class RegisterView(TemplateView):
	"""
	Display register in page where registered users can log in
	"""
	template_name = "registration/registration_form.html"

	def get_context_data(self, *args, **kwargs):
		context = super(RegisterView, self).get_context_data(*args, **kwargs)
		title = "register"
		form = UserRegisterForm(self.request.POST or None,
								self.request.FILES or None)
		context.update({
			"title":title,
			"form":form,
		})
		return context

	def post(self, *args, **kwargs):
		context = self.get_context_data()
		form = context.get('form')
		if form.is_valid():
			user = form.save()
			login(self.request, user,backend='django.contrib.auth.backends.ModelBackend')
			return redirect("/")
		return render(self.request, self.template_name, context)