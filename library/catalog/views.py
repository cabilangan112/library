from django.contrib.auth import login
from django.shortcuts import render, Http404, get_object_or_404, redirect
from django.views.generic import (ListView,DetailView,CreateView,UpdateView, View)
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
from django.contrib.auth import get_user_model
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Book, Author, BookInstance, Genre,Borrow,Reserve
from .forms import RenewBookModelForm,BookModelForm,AuthorModelForm,GenreModelForm,BorrowForm,ReserveForm
from django.views.generic.base import TemplateView,View
from account.decorators import user_required,staff_required
 

class HomeView(View):
    def get(self, request, *args, **kwargs):
        book = Book.objects.all()[:3]
        context = {'book':book,}
        return render(request, "home.html", context)


def Borrow(request, title):
    book = get_object_or_404(Book, title=title)
    if request.method == 'POST':
        form = BorrowForm(request.POST, request.FILES)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.book= book
            borrow.borrower = request.user
            borrow.save()
            return redirect('/posts')
    else:
        form = BorrowForm()
    context = {'form': form,
                'book':book
                }
    return render(request, 'catalog/borrow-form.html', context)


class BorrowView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        book = Borrow.objects.all()
        qs = Book.objects.all().order_by("-title").search(query)

        if author and qs.exists():
            return render(request, "catalog/borrow_list.html",{'book':qs})
        return render(request, "catalog/borrow_list.html",{'book':qs})

def Reserve(request,title):
    book = get_object_or_404(Book, title=title)
    if request.method == 'POST':
        form = ReserveForm(request.POST, request.FILES)
        if form.is_valid():
            reserve = form.save(commit=False)
            reserve.book= book
            reserve.user = request.user
            reserve.save()
            return redirect('/posts')
    else:
        form = ReserveForm()
    context = {'form': form,
                'book':book
                }
    return render(request, 'reserve-form.html', context)


class ReserveView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        book = Reserve.objects.all()
        qs = Book.objects.all().order_by("-title").search(query)

        if author and qs.exists():
            return render(request, "catalog/reserve_list.html",{'book':qs})
        return render(request, "catalog/reserve_list.html",{'book':qs})

class BooksView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        book = Book.objects.all().order_by("title").search(query)

        if book.exists():
            return render(request, "catalog/book_list.html",{'book':book})
        return render(request, "catalog/book_list.html",{'book':book})
 
class BookDetailView(LoginRequiredMixin, View):
    def get(self, request, title, *args, **kwargs):
        book = get_object_or_404(Book, title=title)
        context = {'book':book,}
        return render(request, "catalog/book_detail.html", context)

class BookCreateView(LoginRequiredMixin,View):
    form_class = BookModelForm
    initial = {'key':'value'}
    template_name = 'catalog/book-form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/')
        else:
            form = BookModelForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

def book_edit(LoginRequiredMixin,request,title):
    post = get_object_or_404(Book,title=title)
    if request.method == "POST":
        form = BookModelForm(request.POST, instance=post)
        if posts.user == request.user: 
            if form.is_valid():           
                post = form.save(commit=False)
 
                post.save()
            return redirect('/posts', title=post.title)
    else:
        form = BookModelForm(instance=post)
    return render(request, 'edit-book.html', {'form': form})


def renew_book_librarian(LoginRequiredMixin,request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed') )
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

# Author

class AuthorView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        author = Author.objects.all()
        qs = Book.objects.all().order_by("-author").search(query)

        if author and qs.exists():
            return render(request, "catalog/author_list.html",{'author':qs})
        return render(request, "catalog/author_list.html",{'author':qs})

class AuthorDetailView(View):
    def get(self, request, last_name, *args, **kwargs):
        author = get_object_or_404(Author, last_name=last_name)
        context = {'author':author,}
        return render(request, "catalog/author_detail.html", context)

class AuthorCreateView(View):
    form_class = AuthorModelForm
    initial = {'key':'value'}
    template_name = 'catalog/author-form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/')
        else:
            form = AuthorModelForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

def author_edit(request,last_name):
    author = get_object_or_404(Author,last_name=last_name)
    if request.method == "POST":
        form = BookModelForm(request.POST, instance=post)
        if posts.user == request.user: 
            if form.is_valid():           
                post = form.save(commit=False)
 
                post.save()
            return redirect('/', last_name=author.last_name)
    else:
        form = BookModelForm(instance=post)
    return render(request, 'edit-author.html', {'form': form})

#Genre

class GenreView(View):
    def get(self, request, *args, **kwargs):

        genre = Genre.objects.all()
        query = self.request.GET.get('q')
        qs = Book.objects.all().order_by("-genre").search(query)
        
        if genre and qs.exists():
            return render(request, "catalog/genre_list.html",{'genre':genre})
        return render(request, "catalog/genre_list.html",{'genre':genre})

class GenreDetailView(View):
    def get(self, request, name, *args, **kwargs):
        genre = get_object_or_404(Genre, name=name)
        context = {'genre':genre,}
        return render(request, "catalog/Genre_detail.html", context)

class GenreCreateView(View):
    form_class = GenreModelForm
    initial = {'key':'value'}
    template_name = 'catalog/author-form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/')
        else:
            form = GenreModelForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

def Genre_edit(request,name):
    genre = get_object_or_404(Genre,name=name)
    if request.method == "POST":
        form = BookModelForm(request.POST, instance=post)
        if posts.user == request.user: 
            if form.is_valid():           
                post = form.save(commit=False)
 
                post.save()
            return redirect('/posts', name=genre.name)
    else:
        form = BookModelForm(instance=post)
    return render(request, 'edit-genre.html', {'form': form})
