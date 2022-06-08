from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Auction, Bid , Category, Image, User
from .forms import AuctionForm, ImageForm, CommentForm, BidForm

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
        'categories_count': Category.objects.all().count(),
        'auctions': auctions,
        'expensive_auctions': expensive_auctions,
        'auctions_count': Auction.objects.all().count(),
        'bids_count': Bid.objects.all().count(),
        'users_count': User.objects.all().count(),
        'pages': pages,
        'title': 'Dashboard'
    })

def active(request):

    return render (request, 'active.html', {})

def create_auction(request):

    return render(request, 'create_auction.html', {})

def watch(request):

    return render(request, 'watch.html', {})

