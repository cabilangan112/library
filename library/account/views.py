from django.shortcuts import render
from django.views.generic.base import TemplateView,View
from django.shortcuts import get_object_or_404, redirect
from .models import Course,Department
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
)
from django.views import generic
from.models import User
from django.urls import reverse	
from .forms import UserLoginForm, UserRegisterForm,EditProfileForm,EditPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.all()
        context = {'user':user,}
        return render(request, "profile/profile_list.html", context)

class ProfileDetailView(View):
    def get(self, request, email, *args, **kwargs):
        user = get_object_or_404(User, email=email)
        context = {'user':user,}
        return render(request, "profile/profile_detail.html", context)

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
			return redirect("home")

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

class EditProfileView(LoginRequiredMixin, generic.TemplateView):
    """
    Edit the currently logged in user's profile
    """
    login_url = 'login'
    template_name = 'profile-edit.html'

    def get(self, id_number, *args, **kwargs):
        title = 'Edit Profile'
        user = self.request.user
        users = User.objects.all()
 
        instance = get_object_or_404(User,id_number=id_number, user=user)

        initial_data = {
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'Year':user.Year,
        }

        form = EditProfileForm(
            self.request.POST or None, 
            initial=initial_data,
        )

        context = {
            'title':title,
            'instance': instance,
            'prof_instance':instance,
            'form':form,
            'users':users,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        title = 'Edit Profile'
        user = self.request.user
        id = user.id
        users = User.objects.all()
        instance = get_object_or_404(User, user=user)

        initial_data = {
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'Year':user.Year, 
        }
        form = EditProfileForm(
            self.request.POST or None, 
            initial=initial_data,
        )

        if form.is_valid():
            form.save(user=user)
            return HttpResponseRedirect(reverse('/'))

        context = {
        	'title':title,
            'instance': instance,
            'prof_instance':instance,
            'form':form,
            'users':users,
        }

        return render(self.request, self.template_name, context)

class EditPassword(LoginRequiredMixin, generic.TemplateView):
    """
    Edit the currently logged in user's password
    """    
    login_url = 'login'
    template_name='password-edit.html'

    def get(self, id_number, *args, **kwargs):
        title = 'Edit Password'
        user = self.request.user
        users = User.objects.all()
        instance = get_object_or_404(User, id_number=id_number, user=user)

        form = EditPasswordForm(
            self.request.POST or None
        )

        context = {
            'title':title,
            'form':form,
            'prof_instance':instance,
            'users':users,
        }

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        title = 'Edit Password'
        users = User.objects.all()
        user = self.request.user
        instance = get_object_or_404(User, user=user)

        form = EditPasswordForm(
            self.request.POST or None
        )

        if form.is_valid():
            form.save(user=user)
            login(self.request, user)
            return HttpResponseRedirect(reverse('/'))

        context = {
            'title':title,
            'form':form,
            'prof_instance':instance,
            'users':users,
        }

        return render(self.request, self.template_name, context)

