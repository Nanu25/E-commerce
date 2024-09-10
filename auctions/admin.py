from django.contrib import admin

# Register your models here.

from .models import Auction, Bid, Comment, Watchlist

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid", "image_url", "category", "creator", "is_active", "winner")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "auction", "bidder", "amount")

class CommentAdmin(admin.ModelAdmin):
    pass

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "auction")

admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)


