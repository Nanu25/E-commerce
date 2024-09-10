from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class Auction(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     image_url = models.URLField(blank=True)
#     category = models.CharField(max_length=200, blank=True, default="")
#     def __str__(self):
#         return self.title


class Auction(models.Model):
    CATEGORY_CHOICES = [
        ('Fashion', 'Fashion'),
        ('Electronics', 'Electronics'),
        ('Toys', 'Toys'),
        ('Home', 'Home'),
        ('Books', 'Books'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_auctions")

    def __str__(self):
        return self.title

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bidder} bid {self.amount} on {self.auction}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    is_true = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"  # Display first 20 characters

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_watchlist")

    def __str__(self):
        return f"{self.user.username}'s watchlist for {self.auction.title}"

