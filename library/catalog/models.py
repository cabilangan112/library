from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
import uuid
User = settings.AUTH_USER_MODEL

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
                Q(title__icontains=query)|
                Q(author__last_name__icontains=query)|
                Q(isbn__icontains=query)|
                Q(author__last_name__icontains=query)|
                Q(borrow__borrower__last_name__icontains=query)|
                Q(borrow__borrower__first_name__icontains=query)|
                Q(borrow__borrower__last_name__iexact=query)|
                Q(borrow__borrower__first_name__iexact=query)|
                Q(genre__name__icontains=query)
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
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".title()

    @property
    def get_display_name(self):
        if self.first_name and self.last_name:
            return self.get_full_name
        return f"{self.email}"

class Borrow(models.Model):
    borrower           = models.ForeignKey(User, on_delete = models.CASCADE)
    book               = models.ForeignKey(Book, on_delete = models.CASCADE)
     
    due_back           = models.DateField(null=True, blank=True)
    date_of_renewal    = models.DateField(null=True, blank=True)
    
    borrow             = models.BooleanField(default=True)
    returned           = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_of_borrowing']

    def __str__(self):
        return f'{self.borrower} ({self.book.title})'


class Reserve(models.Model):
    user                 = models.ForeignKey(User, on_delete = models.CASCADE)
    book                 = models.ForeignKey(Book, on_delete = models.CASCADE)
    date_of_reservation  = models.DateTimeField(auto_now_add = True)
    due_date             = models.DateField(null=True, blank=True)
    
    reserve              = models.BooleanField(default=True)
    remove               = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_of_reservation']

    def __str__(self):
        return f'{self.user} ({self.book.title})'