from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Auction, Watchlist, Comment, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        auction = Auction(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            creator=request.user,  # Set the creator to the logged-in user
            is_active=True
        )
        auction.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html")


def listing(request, listing_id):
    auction = get_object_or_404(Auction, pk=listing_id)
    comments = auction.comments.all()
    in_watchlist = False

    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(user=request.user, auction=auction).exists()

    return render(request, "auctions/listing.html", {
        "auction": auction,
        "comments": comments,
        "in_watchlist": in_watchlist
    })


@login_required
def make_bid(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    if request.method == "POST":
        bid_amount = float(request.POST["bid_amount"])

        # Check if the bid is higher than the current starting bid
        if bid_amount > auction.starting_bid:
            # Create a new bid
            new_bid = Bid(
                auction=auction,
                bidder=request.user,
                amount=bid_amount
            )
            new_bid.save()

            # Update the auction's starting_bid to the new highest bid
            auction.starting_bid = bid_amount
            auction.winner = request.user
            auction.save()

            message = "Your bid was successfully placed!"
        else:
            message = "Your bid must be higher than the current bid."

        return render(request, "auctions/listing.html", {
            "auction": auction,
            "message": message,
        })

    return redirect(reverse("index"))
def add_watchlist(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    user = request.user

    if request.method == "POST" and user.is_authenticated:
        watchlist_item, created = Watchlist.objects.get_or_create(user=user, auction=auction)
        if created:
            message = "Auction added to your watchlist."
        else:
            message = "This auction is already in your watchlist."
        return redirect(reverse("listing", args=[auction_id]))

    return redirect("index")
@login_required
def watchlist(request):
    user = request.user
    watchlist_auctions = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlist_auctions": watchlist_auctions
    })

def remove_watchlist(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    user = request.user

    if request.method == "POST":
        #test if the auction is in the user's watchlist
        #watchlist_item = Watchlist.objects.get(user=user, auction=auction)
        #watchlist_item.delete()
        #check if the auction is in the user's watchlist
        watchlist_item = Watchlist.objects.filter(user=user, auction=auction)
        if watchlist_item.exists():
            watchlist_item.delete()
        else:
            message = "This auction is not in your watchlist."

        return redirect(reverse("listing", args=[auction_id]))

    return redirect(reverse("listing", args=[auction_id]))

def categories(request):
    category_list = ["Fashion", "Electronics", "Toys", "Home", "Books", "Other"]
    return render(request, "auctions/categories.html", {
        "categories": category_list
    })

def category_detail(request, category):
    auctions_in_category = Auction.objects.filter(category=category)
    return render(request, "auctions/category_detail.html", {
        "category": category,
        "auctions": auctions_in_category
    })


@login_required
def add_comment(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    if request.method == "POST":
        content = request.POST.get("comment")
        if content:
            comment = Comment.objects.create(
                auction=auction,
                user=request.user,
                content=content
            )
            comment.save()
            return redirect(reverse("listing", args=[auction_id]))

    return redirect(reverse("listing", args=[auction_id]))


# @login_required
# def close_auction(request, auction_id):
#     auction = get_object_or_404(Auction, pk=auction_id)
#
#     if request.method == "POST":
#         auction.is_active = False
#         auction.save()
#         return redirect(reverse("listing", args=[auction.id]))
#
#     return redirect("index")

@login_required
def close_auction(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)

    if request.method == "POST" and auction.creator == request.user:
        auction.is_active = False

        # Get the highest bid
        highest_bid = auction.bids.order_by('-amount').first()

        if highest_bid:
            auction.winner = highest_bid.bidder  # Assuming you add a winner field to the Auction model
        auction.save()

        return redirect(reverse("listing", args=[auction.id]))

    return redirect("index")