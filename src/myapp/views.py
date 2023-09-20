from django.shortcuts import render, get_object_or_404
from django.db.models import Func
from django.http import JsonResponse
from .models import Book, Borrow, Genre
from account.models import User,UserRating
# from myapp.views import search_view

# Create your views here.

def home(request):
    context = {}
    random_books = change_img_url(Book.objects.order_by(Func(function='RAND'))[:4])
    popular_books = Book.objects.order_by('title') # create a user rating and order by that
    latest_books = Book.objects.order_by('-pub_date') # need to change put pub date
    context['popular_books'] = assign_ratings(change_img_url(popular_books))
    context['latest_books'] = assign_ratings(change_img_url(latest_books))
    context['random_books'] = random_books

    return render(request, 'myapp/home.html', context)

def search_view(request):
    # to get the searched book
    book = None
    if request.method == "POST":
        searched_book = request.POST.get("search_query", "").strip() # this to get the name by removing white spaces
        print(searched_book)
        exist = Book.objects.filter(title=searched_book).exists()
        if exist:
            book = Book.objects.filter(title=searched_book).first()
        else:
            book = 'empty'
    # print(book)
    return book

def search_result(request): # this should change by adding a parameter keyword and change url with adding parameters
    context = {}
    keyword = request.POST.get("keyword", "").strip()
    context['search_books'] = []
    exist = Book.objects.filter(title__icontains=keyword).exists()
    if exist:
        context['search_books'] = assign_ratings(change_img_url(Book.objects.filter(title__icontains=keyword)))
    return render(request,'myapp/search_result.html', context)

def genre_view():
    pass

def change_img_url(Book):
    'this is to remove static/ part from the address'
    book_list = list(Book)
    for book in book_list:
        book.img_url = str(book.image_field).split('static/',1)[-1]
    return book_list

def book_detail(request, book_id):
    context = {}
    query = Book.objects.prefetch_related('genre').select_related('author', 'publisher')
    book = get_object_or_404(query, id=book_id)
    book.img_url = str(book.image_field).split('static/',1)[-1]
    context['book'] = book
    if request.user.is_authenticated:
        user = request.user
        user_rated = UserRating.objects.filter(book_id=book_id, user=request.user).exists()
        votes = UserRating.objects.filter(book_id=book_id).count()
        rating = calculate_rating(votes)
        context['user_rated'] = user_rated
        context['votes'] = votes
        context['rate'] = rating
    return render(request,  'myapp/book_detail.html', context)

def calculate_rating(votes):
    Total = User.objects.count()
    rate = round(votes/Total * 10,1)
    return rate

def assign_ratings(Book):
    book_list = list(Book)
    for book in book_list:
        votes = UserRating.objects.filter(book_id=book.id).count()
        rating = calculate_rating(votes)
        book.rating = rating
    return book_list

def increase_no_of_views(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
        book.view_count += 1
        book.save()
        return JsonResponse({'message': 'User rating updated successfully'})
    except Book.DoesNotExist:
        return JsonResponse({'message': 'Error updating user rating'}, status=404) 
        
def categories_view(request, category):
    context = {}
    context["category_books"] = []
    context["category_name"] = category
    genre_objects = Genre.objects.filter(type__iexact=category)
    if genre_objects.exists():
        genre_id = genre_objects.first().id
        category_books = change_img_url(Book.objects.filter(genre_id=genre_id))
        context["category_books"] = category_books
    return render(request,  'myapp/categories.html', context)

def about(request):
    return render(request, 'myapp/about.html')