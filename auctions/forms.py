from django.forms import ModelForm
from .models import AuctionListing, Category, AuctionBid, AuctionComment

class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "starting_bid", "description", "category", "image"]

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]        

class BidForm(ModelForm):
    class Meta:
        model = AuctionBid
        fields = ["bid"]

class CommentForm(ModelForm):
    class Meta:
        model = AuctionComment
        fields = ["comment"]