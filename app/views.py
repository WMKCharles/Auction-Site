from unicodedata import category
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Auction, Bid , Category, Image, User
from .forms import AuctionForm, ImageForm, CommentForm, BidForm, LoginForm, UserRegistrationForm

def register(request):
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def index(request):
    auctions = Auction.objects.all()
    expensive_auctions = Auction.objects.order_by('-starting_bid')[:4]
    for auction in auctions:
        auction.image = auction.get_images.first()

    page = request.GET.get('page', 1)
    paginator = Paginator(auctions, 6)

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(paginator.num_pages)
        
    return render (request, 'index.html', {
        'categories': Category.objects.all(),
        'categories_count': Category.objects.all().count(),
        'auctions': auctions,
        'expensive_auctions': expensive_auctions,
        'auctions_count': Auction.objects.all().count(),
        'bids_count': Bid.objects.all().count(),
        'users_count': User.objects.all().count(),
        'pages': pages,
        'title': 'Dashboard'
    })

@login_required
def create_auction(request):
    ImageFormSet = forms.modelformset_factory(Image, form = ImageForm)
    if request.method == 'POST':
        auction_form = AuctionForm(request.POST, request.FILES)
        image_form = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if auction_form.is_valid() and image_form.is_valid():
            new_auction = auction_form.save(commit=False)
            new_auction.creator = request.user
            new_auction.save()

            for auction_form in image_form.cleaned_data:
                if auction_form:
                    image = auction_form['image']

                    new_image = Image(auction=new_auction, image=image)
                    new_image.save()

            return render(request, 'create_auction.html', {
                'categories': Category.objects.all(),
                'auction_form':AuctionForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
                'title': 'Create Auction',
                'success': True
            })

        else:
            return render(request, 'create_auction.html', {
                'categories':Category.objects.all(),
                'auction_form': AuctionForm(),
                'image_form':ImageFormSet(queryset=Image.objects.none()),
                'title':'Create Auction'
            })
    else:
        return render(request, 'create_auction.html', {
                'categories':Category.objects.all(),
                'auction_form': AuctionForm(),
                'image_form':ImageFormSet(queryset=Image.objects.none()),
                'title':'Create Auction'
            })


def active (request):
    '''
    It renders a page that displays all of 
    the currently active auction listings
    Active auctions are paginated: 3 per page
    '''
    category_name = request.GET.get('category_name', None)
    if category_name is not None:
        auctions = Auction.objects.filter(active=True, category=category_name)
    else:
        auctions = Auction.objects.filter(active=True)

    for auction in auctions:
        auction.image = auction.get_images.first()
        if request.user in auction.watchers.all():
            auction.is_watched = True
        else:
            auction.is_watched = False

    # Show 3 active auctions per page
    page = request.GET.get('page', 1)
    paginator = Paginator(auctions, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'active.html', {
        'categories': Category.objects.all(),
        'auctions': auctions,
        'auctions_count': auctions.count(),
        'pages': pages,
        'title': 'Active Auctions'
    })


def watch(request):

    return render(request, 'watch.html', {})

