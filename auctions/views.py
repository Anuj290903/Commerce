from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import AuctionListingForm
from .models import User, AuctionListing, AuctionBid, Category

# Improve feature : Correct image display
# Improve feature : Create a category in create listing page.
# Add feature : Add Auctions Bids (Real Time)
# Add feature : Add auction comments
# Add feature : Add watchlist
# Add feature : Add close auction
# Add feature : Add winner announcement
# Add feature : Add user profile page

def index(request):
    items = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "list": items
        })

def item(request, ID):
    thing = AuctionListing.objects.get(id=ID)
    return render(request, "auctions/item.html", {
        "item": thing,
        "category": Category.objects.filter(items=thing),
        "bids": AuctionBid.objects.filter(item=thing),
        # "comments": auction_comments.objects.filter(listing=obj)
        })

def category(request, name):
    cat = Category.objects.get(name=name)
    return render(request, "auctions/category.html", {
        "title": cat.name,
        "items": cat.items.all()
        })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
        })

@login_required(login_url="login")
def create(request):
    if request.method == 'GET':
        form = AuctionListingForm(user=request.user)
        return render(request, "auctions/create.html", {
            "form": form
        })
    else:
        form = AuctionListingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
        
def watchlist(request):
    pass

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
