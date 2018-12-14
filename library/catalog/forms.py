from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .model import Genre,Book,BookInstance, Author

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
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}

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

    class Meta:
        model = Book
        fields = ['due_back']
 