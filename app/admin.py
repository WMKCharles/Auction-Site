from django.contrib import admin
from .models import User, Auction, Bid, Category, Comment, Image

# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Image)