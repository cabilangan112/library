from django.contrib import admin
from .models import Author, Genre, Book, BookInstance,Borrow,Reserved

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
 

class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

 
admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Borrow)
admin.site.register(Reserved)
admin.site.register(BookInstance,BookInstanceAdmin)
