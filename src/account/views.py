from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from datetime import date, timedelta
from .forms import RegistrationForm, AccountAuthenticationForm
from myapp.models import Borrow
from .models import UserRating
from myapp.views import change_img_url

# Create your views here.
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST) 
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else: #GET request
        form = RegistrationForm()
        context['registration_form'] = form
    for field in context['registration_form']:
        print(field.label)
    return render(request, 'account/register.html', context)

def login_view(request): 
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            print('no')
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            print(email)
            if user:
                login(request, user)
                return redirect("home")
    else:#GET
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def account(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        borrow_details = Borrow.objects.filter(member=user)
        # context['borrowings'] = {'details':list(borrow_details), 'warning':[]}
        # date_to_return = borrow_details.first().borrow_date + timedelta(days=max_days)
        today = date.today()
        context['borrowings'] = overdue_check(borrow_details, today)
        # if date_to_return > today:
        #     borrow_details.first
        print(context['borrowings'][0].book.img_url)
    return render(request, 'account/account.html', context)

def fine_calculator(date_to_return, fine, today):
    # today = date.today()
    diff = today- date_to_return
    return diff.days * fine

def overdue_check(borrow_details, today):
    warning = ""
    detail_list = list(borrow_details)
    for detail in detail_list:
        date_to_return = detail.return_date
        if date_to_return < today:
            # print(date_to_return)
            fine = fine_calculator(date_to_return, 10, today)
            warning='Warned you have to pay Rs {}'.format(fine)   
        else:
            warning='You have to return the book on {}'.format(date_to_return)
        detail.warning = warning
        detail.book.img_url = str(detail.book.image_field).split('static/',1)[-1]

    return detail_list

def user_ratings_create(request, book_id):
    try:
        # Get the authenticated user (assuming you have authentication)
        if request.user.is_authenticated:
            user = request.user
            # Insert a new user rating into the UserRating table
            UserRating.objects.create(book_id=book_id, user=user)
        
        return JsonResponse({'message': 'User rating updated successfully'})
    except:
        return JsonResponse({'message': 'Error updating user rating'}, status=500)    
        
def user_ratings_delete(request, book_id):
    try:
        # Get the authenticated user (assuming you have authentication)
        if request.user.is_authenticated:
            user = request.user
            # delete the relevent recors
            user_rating = UserRating.objects.filter(book_id=book_id, user=user).first()
            user_rating.delete()
        
        return JsonResponse({'message': 'User rating updated successfully'})
    except:
        return JsonResponse({'message': 'Error updating user rating'}, status=500)        
