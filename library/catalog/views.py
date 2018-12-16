from django.contrib.auth import login
from django.shortcuts import render, Http404, get_object_or_404, redirect
from django.views.generic import (ListView,DetailView,CreateView,UpdateView, View)
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
from django.contrib.auth import get_user_model
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookModelForm
from django.views.generic.base import TemplateView,View


class HomeView(TemplateView):
    template_name = 'home.html'

class BooksView(View):
    def get(self, request, *args, **kwargs):
        book = Book.objects.all()
        context = {'book':book,}
        return render(request, "catalog/book_list.html", context)

class BookDetailView(View):
    def get(self, request, title, *args, **kwargs):
        book = get_object_or_404(Book, title=title)
        context = {'book':book,}
        return render(request, "catalog/book_detail.html", context)

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
 
def renew_book_librarian(request, pk):
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