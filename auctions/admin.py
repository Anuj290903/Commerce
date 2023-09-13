from django.contrib import admin
from .models import AuctionListing, User, AuctionBid, Category, Watchlist, AuctionComment

# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(User)
admin.site.register(AuctionBid)
admin.site.register(Category)
admin.site.register(AuctionComment)
admin.site.register(Watchlist)