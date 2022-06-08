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

def create_auction(request):
    ImageFormSet = forms.modelformset_factory(Image, form = ImageForm, extra =2)
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

            
def active(request):

    return render (request, 'active.html', {})


def watch(request):

    return render(request, 'watch.html', {})

