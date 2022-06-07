from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required
def index(request):

    return render (request, 'index.html', {})

def active(request):

    return render (request, 'active.html', {})

def create_auction(request):

    return render(request, 'create_auction.html', {})

def watch(request):

    return render(request, 'watch.html', {})

