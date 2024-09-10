from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("auction/<int:auction_id>/bid/", views.make_bid, name="make_bid"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("auction/<int:auction_id>/watchlist/", views.add_watchlist, name="add_watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>/", views.category_detail, name="category"),
    path("auction/<int:auction_id>/add_comment/", views.add_comment, name="add_comment"),
    path("auction/<int:auction_id>/remove_watchlist/", views.remove_watchlist, name="remove_watchlist"),
    path('close_auction/<int:auction_id>/', views.close_auction, name='close_auction'),
]
