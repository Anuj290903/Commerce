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
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    image_url = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return f"{self.title} : {self.starting_bid} : By {self.seller}"
    
class AuctionBid(models.Model):    
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bid", default=1)
    def __str__(self):
        return f"{self.item} : {self.bid} : -by {self.bidder}"