from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for money.
    description = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="items", blank=True, null=True)
    image = models.ImageField(upload_to='auctions/media/', blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winnings", blank=True, null=True)
    fin_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.title} : {self.starting_bid} : By {self.seller}"
    
class AuctionBid(models.Model):    
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bid", default=1)
    def __str__(self):
        return f"{self.item} : {self.bid} : -by {self.bidder}"
    
class AuctionComment(models.Model):
    comment = models.CharField(max_length=256)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    def __str__(self):
        return f"{self.item} : {self.comment} - by {self.commenter}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist")
    def __str__(self):
        return f"{self.user} : {self.item}"