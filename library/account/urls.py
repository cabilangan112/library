from django.urls import path
from . import views

app_name='account'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='post'),
    path('<email>/', views.ProfileDetailView.as_view(), name='detail'),
    path('reserve/<email>/', views.ProfileReserveView.as_view(), name='detail-reserve'),
    path('profile/edit/<id_number>/', views.EditProfileView.as_view(), name='edit_profile'),
    path('password/edit/<id_number>/', views.EditPassword.as_view(), name='edit_password'),
]