from django.db import models
from django.urls import reverse
from django.db.models import Q
import uuid

LOAN_STATUS = (
    ('m', 'Maintenance'),
    ('a', 'Available'),
    ('r', 'Reserved'),
)

class BookQuerySet(models.query.QuerySet):
    def search(self,query): 
        if query:
            query = query.strip()
            return self.filter(
                Q(book__title__icontains=query)|
                Q(book__author__icontains=query)|
                Q(book__isbn__icontains=query)|
                Q(book__genre__name__iexact=query)|
                Q(author__first_name__icontains=query)|
                Q(author__last_name__iexact=query)|
                Q(author__date_of_birth__icontains=query)|
                Q(author__date_of_death__iexact=query)                
                ).distinct()
        return self
 
class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

class Genre(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title   = models.CharField(max_length=200)
    author  = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    isbn    = models.CharField('ISBN', max_length=13)
    genre   = models.ManyToManyField(Genre)
    date_created       = models.DateTimeField(auto_now_add=True)
    date_modified      = models.DateTimeField(auto_now=True)
    objects = BookManager()

    def __str__(self):
        return self.title
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)  

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
