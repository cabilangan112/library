from django.urls import path
from . import views

app_name='catalog'


urlpatterns = [

#Book
    path('<int:pk>/', views.RemoveView, name='remove'),
    path('genres/', views.GenreView.as_view(), name='genres'),
    path('pdf/', views.Pdf.as_view(), name='pdf'),
    path('pdf/<int:pk>/', views.Pdf.as_view(), name='pdf'),
    path('renew/<int:pk>/', views.Renew, name='renew'),
    path('borrowed/<int:pk>/', views.borrowed, name='borrowed'),
    path('return/<int:pk>/', views.Return, name='returned'),
    path('', views.BooksView.as_view(), name='books'),
    path('<title>', views.BookDetailView.as_view(), name='book'),
    path('reserve-detail/<title>', views.ReserveDetailView.as_view(), name='reserve-detail'),
    path('edit/<title>', views.book_edit, name='edit-book'),

    path('book/create/', views.BookDetailView.as_view(), name='book-create'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

#Authors

    path('authors/', views.AuthorView.as_view(), name='authors'),
    path('<last_name>', views.AuthorDetailView.as_view(), name='author'),
    path('<last_name>', views.book_edit, name='edit-author'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),

#Genre
 
    path('<name>', views.book_edit, name='edit-genre'),
    path('genre/create/', views.GenreCreateView.as_view(), name='genre-create'),
    path('genre/<name>', views.GenreDetailView.as_view(), name='genre'),
#Borrow
    path('borrow/<title>', views.borrow, name='borrow'),
    path('reserve/<title>', views.Reserves, name='reserve'),
]