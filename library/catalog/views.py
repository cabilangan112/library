from django.conf import settings
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
from account.models import User
from .models import Borrow,Book, Author, BookInstance, Genre, Reserve
from .forms import RenewBookModelForm,ReturnForm,BorrowedForm,RemoveForm,ReservedForm,RenewForm,BookModelForm,AuthorModelForm,GenreModelForm,BorrowForm,ReserveForm
from django.views.generic.base import TemplateView,View
from account.decorators import user_required,staff_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.utils import timezone
from .models import *
from .render import Render



class HomeView(View):
    def get(self, request, *args, **kwargs):
        book = Book.objects.all()[:3]
        context = {'book':book,}
        return render(request, "home.html", context)

class Pdf(View):

    def get(self, request):
        borrow = Borrow.objects.all()
        today = timezone.now()
        user  = request.user
        params = {
            'today': today,
            'user':user,
            'borrow': borrow,
             
        }
        return Render.render('catalog/pdf.html', params)

class PdfDetail(View):

    def get(self,pk, request):
        borrow = get_object_or_404(Borrow, pk=pk)
        today = timezone.now()
        params = {
            'today': today,
            'borrow': borrow,
            'request': request
        }
        return Render.render('catalog/pdf.html', params)


def borrow(request, title):
    book = get_object_or_404(Book, title=title)
    if request.method == 'POST':
        form = BorrowForm(request.POST, request.FILES)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.book = book
            borrow.borrower = request.user
            subject = 'NDMC Book Borrowing'
            html_content = render_to_string('email/email.html', {'borrow':borrow})
            text_content = strip_tags(html_content)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [borrow.borrower.email,]
            msg = EmailMultiAlternatives ( subject,html_content, email_from, recipient_list )
            msg.attach_alternative (html_content, "text/html")
            msg.send()
            borrow.save()
            return redirect('account:detail', email=request.user.email)
    else:
        form = BorrowForm()
    context = {'form': form,
                'book':book
                }
    return render(request, 'catalog/borrow-form.html', context)

def Return(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    if request.method == "POST":
        form = ReturnForm(request.POST, instance=borrow)
        if form.is_valid():           
            borrow = form.save(commit=False)
            subject = 'Return Book'
            html_content = render_to_string('email/email-return.html', {'borrow':borrow})
            text_content = strip_tags(html_content)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [borrow.borrower.email,]
            msg = EmailMultiAlternatives ( subject,html_content, email_from, recipient_list )
            msg.attach_alternative (html_content, "text/html")
            msg.send()
            borrow.save()
        return redirect('account:borrowed')
    else:
        form = ReturnForm(instance=borrow)
    return render(request, 'catalog/return-form.html',{'form': form,
        'borrow':borrow})


def Renew(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    if request.method == "POST":
        form = RenewForm(request.POST, instance=borrow)
        if form.is_valid():           
            borrow = form.save(commit=False)
            subject = 'Renew Date of Borrowing'
            html_content = render_to_string('email/email-renew.html', {'borrow':borrow})
            text_content = strip_tags(html_content)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [borrow.borrower.email,]
            msg = EmailMultiAlternatives ( subject,html_content, email_from, recipient_list )
            msg.attach_alternative (html_content, "text/html")
            msg.send()
            borrow.save()
        return redirect('account:profile')
    else:
        form = RenewForm(instance=borrow)
    return render(request, 'catalog/renew.html',{'form': form,
        'borrow':borrow})

def borrowed(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    if request.method == "POST":
        form = BorrowedForm(request.POST, instance=borrow)
        if form.is_valid():           
            borrow = form.save(commit=False)
            subject = 'The book that you reserve has been approved'
            html_content = render_to_string('email/email-renew.html', {'borrow':borrow})
            text_content = strip_tags(html_content)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [borrow.borrower.email,]
            msg = EmailMultiAlternatives ( subject,html_content, email_from, recipient_list )
            msg.attach_alternative (html_content, "text/html")
            msg.send()
            borrow.save()
        return redirect('account:profile')
    else:
        form = BorrowedForm(instance=borrow)
    return render(request, 'catalog/borrowed.html',{'form': form,
        'borrow':borrow})

class BorrowView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        book = Borrow.objects.all()
        qs = Book.objects.all().order_by("-title").search(query)

        if author and qs.exists():
            return render(request, "catalog/borrow_list.html",{'book':qs})
        return render(request, "catalog/borrow_list.html",{'book':qs})

def Reserves(request,title):
    book = get_object_or_404(Book, title=title)
    if request.method == 'POST':
        form = ReserveForm(request.POST, request.FILES)
        if form.is_valid():
            reserve = form.save(commit=False)
            reserve.book=book
            reserve.user = request.user
            subject = 'Book Reservation'
            html_content = render_to_string('email/email-reserve.html', {'reserve':reserve})
            text_content = strip_tags(html_content)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [reserve.user.email,]
            msg = EmailMultiAlternatives ( subject,html_content, email_from, recipient_list )
            msg.attach_alternative (html_content, "text/html")
            msg.send()
            reserve.save()
            return redirect('account:detail-reserve', email=request.user.email)
    else:
        form = ReserveForm()
    context = {'form': form,
                'book':book
                }
    return render(request, 'reserve-form.html', context)



def RemoveView(request, pk):
    reserve = get_object_or_404(Reserve, pk=pk)
    if request.method == "POST":
        form = RemoveForm(request.POST, instance=reserve)
        if form.is_valid():           
            reserve = form.save(commit=False)
            reserve.user = request.user
            reserve.save()
        return redirect('account:detail-reserve', email=request.user.email)
    else:
        form = RemoveForm(instance=reserve)
    return render(request, 'catalog/remove-form.html',
        {
            'form': form,
            'reserve':reserve
        }
        )

class ReserveView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        book = Reserve.objects.all()
        qs = Book.objects.all().order_by("-title").search(query)

        if author and qs.exists():
            return render(request, "catalog/reserve_list.html",{'book':qs})
        return render(request, "catalog/reserve_list.html",{'book':qs})

class ReserveDetailView(LoginRequiredMixin, View):
    def get(self, request, title, *args, **kwargs):
        book = get_object_or_404(Book, title=title)
        context = {'book':book,}
        return render(request, "catalog/reserve_detail.html", context)


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

