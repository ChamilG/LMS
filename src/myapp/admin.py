from django.contrib import admin
from myapp.models import Author
from myapp.models import Book
from myapp.models import Genre
from myapp.models import Borrow
from myapp.models import Publisher



# Register your models here.
class BookAdmin(admin.ModelAdmin):
    exclude = ['img_url']

admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Borrow)
admin.site.register(Publisher)