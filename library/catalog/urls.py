from django.urls import path
from . import views

app_name='catalog'


urlpatterns = [

#Book

    path('', views.BooksView.as_view(), name='books'),
    path('<title>', views.BookDetailView.as_view(), name='book'),
    path('<title>', views.book_edit, name='edit-book'),
    path('book/create/', views.BookDetailView.as_view(), name='book-create'),

#Authors

    path('authors/', views.AuthorView.as_view(), name='authors'),
    path('<last_name>', views.AuthorDetailView.as_view(), name='author'),
    path('<last_name>', views.book_edit, name='edit-author'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),

#Genre

    path('genres', views.GenreView.as_view(), name='genres'),
    path('<name>', views.GenreDetailView.as_view(), name='genre'),
    path('<name>', views.book_edit, name='edit-genre'),
    path('genre/create/', views.GenreCreateView.as_view(), name='genre-create'),


]