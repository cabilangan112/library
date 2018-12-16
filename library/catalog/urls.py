from django.urls import path
from . import views

app_name='catalog'


urlpatterns = [
    path('', views.BooksView.as_view(), name='book'),
    path('<title>', views.BookDetailView.as_view(), name='book'),
]