from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import AuctionListingForm, CategoryForm, BidForm, CommentForm
from .models import User, AuctionListing, AuctionBid, Category, AuctionComment, Watchlist
from django.conf import settings

# Improve feature : Correct image upload

def index(request):
    items = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "list": items
        })

def cls_listing(request):
    items = AuctionListing.objects.filter(active=False)
    return render(request, "auctions/cls_listings.html", {
        "list": items
        })

def item(request, ID):
    thing = AuctionListing.objects.get(id=ID)
    bform = BidForm()
    cform = CommentForm()
    obj = Watchlist.objects.filter(user=request.user, item=thing)
    if obj.exists():
        obj = True
    else:
        obj = False
    return render(request, "auctions/item.html", {
        "item": thing,
        "category": Category.objects.filter(items=thing),
        "bids": AuctionBid.objects.filter(item=thing),
        "form": bform,
        "user": request.user,
        "cform": cform,
        "comments": AuctionComment.objects.filter(item=thing),
        "exists": obj,
        })

def category(request, name):
    obj = Category.objects.get(name=name)
    list = AuctionListing.objects.filter(category=obj)
    return render(request, "auctions/category.html", {
        "title": name,
        "items": list
        })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
        })

@login_required(login_url="login")
def create(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_l = form.save(commit=False)
            new_l.seller = request.user
            new_l.active = True
            new_l.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = AuctionListingForm()

    return render(request, "auctions/create.html", {
        "form": form,
        "message": "Create Listing"
    })
        
@login_required(login_url="login")        
def create_cat(request):
    if request.method == "GET":
        form = CategoryForm()
        return render(request, "auctions/create_cat.html", {
            "message": "Add Category",
            "form": form
        })
    else:
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("categories")) 
        else:
            return HttpResponseRedirect(reverse("create_cat"))
        
@login_required(login_url="login")        
def add_bid(request, ID):
    if request.method == "POST":
        form = BidForm(request.POST or None)
        if form.is_valid():
            thing = AuctionListing.objects.get(id=ID)
            prev_bids = AuctionBid.objects.filter(item=thing)
            for bidd in prev_bids:
                if bidd.bid >= form.cleaned_data["bid"]:
                    return HttpResponseRedirect(reverse("item", args=(ID,)))
            if thing.starting_bid >= form.cleaned_data["bid"]:
                return HttpResponseRedirect(reverse("item", args=(ID,)))
            new_bid = form.save(commit=False)
            new_bid.bidder = request.user
            new_bid.item = AuctionListing.objects.get(id=ID)
            new_bid.save()
            return HttpResponseRedirect(reverse("item", args=(ID,)))
        else:
            return HttpResponseRedirect(reverse("item", args=(ID,)))
    else:
        return HttpResponseRedirect(reverse("item", args=(ID,)))
    
@login_required(login_url="login")
def close(request, ID):
    if request.method == "POST":
        thing = AuctionListing.objects.get(id=ID)
        thing.active = False
        bids = AuctionBid.objects.filter(item=thing)
        win = thing.seller
        least = thing.starting_bid
        for bid in bids:
            if bid.bid > least:
                win=bid.bidder
                least=bid.bid
        thing.winner = win
        thing.fin_price = least
        thing.save()
        return HttpResponseRedirect(reverse("item", args=(ID,)))
    else:
        return HttpResponseRedirect(reverse("item", args=(ID,)))    

@login_required(login_url="login")
def add_comment(request, ID):
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.commenter = request.user
            new_comment.item = AuctionListing.objects.get(id=ID)
            new_comment.save()
            return HttpResponseRedirect(reverse("item", args=(ID,)))
    else:
        return HttpResponseRedirect(reverse("item", args=(ID,)))
    
@login_required(login_url="login")
def user_prof(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/profile.html", {
            "user": request.user,
            "listing": AuctionListing.objects.filter(seller=request.user),
            "winning": AuctionListing.objects.filter(winner=request.user),
        })    

@login_required(login_url="login")
def add_list(request, ID):
    item = AuctionListing.objects.get(id=ID)
    new_list = Watchlist(user=request.user, item=item)
    new_list.save()
    return HttpResponseRedirect(reverse("item", args=(ID,))) 

@login_required(login_url="login")
def remove_list(request, ID):
    item = AuctionListing.objects.get(id=ID)
    list = Watchlist.objects.get(user=request.user, item=item)
    list.delete()
    return HttpResponseRedirect(reverse("item", args=(ID,)))       

@login_required(login_url="login")
def watchlist(request):
    list = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html",{
        "list": list
    })

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
