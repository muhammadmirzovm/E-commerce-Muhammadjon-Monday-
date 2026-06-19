from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from .forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        response =  super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request,  "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        return response
    
    def form_invalid(self, form):
        response =  super().form_invalid(form)
        messages.error(self.request,  "Ro'yxatdan o'tishda xatolik yuz berdi!")
        return response
    
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    def form_valid(self, form):
        messages.success(self.request, 'Tizimga kirdingiz!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Login yoki parol xato !')
        return super().form_invalid(form)
    
class CustomLogoutView(LogoutView):
    next_page = 'home'
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Tizimdan chiqdingiz!")
        return super().dispatch(request, *args, **kwargs)
    