from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
import os
# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=20)
    # dob = models.DateField()
    
    def __str__(self):
        return self.name
    
class Genre(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

def upload_location(instance, filename):
    file_path = 'static/book_imgs/{title}_{filename}'.format(title = str(instance.title).replace(" ",""), filename = filename)
    return file_path

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    no_of_books = models.IntegerField(default=0)
    pub_date = models.DateField("date published", default=None)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    # img_url = models.CharField(max_length=200,null=True, default=None)
    view_count = models.BigIntegerField(default=0)
    image_field = models.ImageField(upload_to=upload_location, null=True, blank=False)

    def __str__(self):
        return self.title
    
    # def save(self, *args, **kwargs):
    #     print(str(self.image_field)) # need to fix this when saving for the time and when changing the image a conflict is popping up
    #     if "book" in self.image_field:
    #          self.img_url = str(self.image_field).split('static/',1)[-1]
    #          print('update')
    #     else:
    #         self.img_url = upload_location(self, self.image_field)
    #         print('first')

    #     print(self.img_url)
    #     super(Book, self).save(*args, **kwargs)


# class Member(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.CharField(max_length=30)

#     def __str__(self):
#         return self.name

class Borrow(models.Model):
    book =  models.ForeignKey(Book, on_delete=models.CASCADE)
    member =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrow_date = models.DateField("date and time burrowed")
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Borrowed: {self.book.title} by {self.member.username} on {self.borrow_date}"