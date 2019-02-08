from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import Genre,Book,BookInstance, Author,Borrow,Reserve

class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']
 
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))
 
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
 
       return data
       
    class Meta:
        model  = BookInstance
        fields = ['due_back']
        labels = {'due_back': ('Renewal date')}
        help_texts = {'due_back': ('Enter a date between now and 4 weeks (default 3).')}

class BookModelForm(forms.ModelForm):
    title   = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    summary = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Summary'}))
    author  = forms.ModelChoiceField(queryset=Author.objects.all())
    isbn    = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': 'ISBN'}))
    genre   = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())

    def save(self):
        data = self.cleaned_data

        book = Book(
            title   = data['title'],
            summary = data['summary'],
            author  = data['author'],
            isbn    = data['isbn'],
            genre   = data['genre'],
        )
        book.save()

class BookInstanceModelForm(forms.ModelForm):

    class Meta:
        model = BookInstance
        fields = [
            'id',
            'book',
            'imprint',
            'due_back',
            ]

class AuthorModelForm(forms.ModelForm):
    first_name    = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    last_name     = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Summary'}))
    date_of_birth = forms.DateField(label='What is your birth date?', widget=forms.SelectDateWidget)
    data_of_death = forms.DateField(label='Death', widget=forms.SelectDateWidget)

    def save(self):
        data = self.cleaned_data

        book = Author(
            first_name      = data['first_name'],
            last_name       = data['last_name'],
            date_of_birth   = data['date_of_birth'],
            data_of_death   = data['data_of_death'], 
        )

        book.save()

class GenreModelForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = [
            'name'
            ]

class BorrowForm(forms.ModelForm):

    class Meta:
        model = Borrow
        exclude = ('borrower','book','date_of_renewal',)
        fields = [
            'borrower',
            'book',
            'due_back',
   
            'date_of_renewal',
            'borrow',
            ]

class ReserveForm(forms.ModelForm):

    class Meta:
        model = Reserve
        exclude = ('user','book','remove')
        fields = [
            'user',
            'book',
            'due_date',
            'reserve',
 
            ]

    def clean_book(self):
        book    = self.data.get('book')
        book_qs = Reserve.objects.filter(book=book)
        if book_qs.exists():
            raise forms.ValidationError("This Fucking Book has already been used")
        return book
            
class ReturnForm(forms.ModelForm):

    class Meta:
        model = Borrow
        exclude = ('borrower','book',)
        fields = [
            'borrower',
            'book',
            'due_back',
            'date_of_renewal',
            'returned',
            ]

class RemoveForm(forms.ModelForm):

    class Meta:
        model = Reserve
 
        fields = [
            'user',
            'book',
            'due_date',
            'remove'
            ]

class RenewForm(forms.ModelForm):

    class Meta:
        model = Borrow
        exclude = ('borrower','book','returned',)
        fields = [
            'borrower',
            'book',
            'due_back',
            'date_of_renewal',
            
            ]

class BorrowedForm(forms.ModelForm):

    class Meta:
        model = Borrow
        exclude = ('borrower','book','date_of_renewal',)
        fields = [
            'borrower',
            'book',
            'due_back',
   
            'date_of_renewal',
            'borrowed',
            ]
