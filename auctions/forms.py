from django.forms import ModelForm
from .models import AuctionListing

class AuctionListingForm(ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super(AuctionListingForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['seller'].initial = user
    class Meta:
        model = AuctionListing
        fields = ["title", "starting_bid", "seller", "description", "category", "image_url"]
