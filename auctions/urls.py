from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_listings, name="category_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_comment/<str:listing_id>", views.add_comment, name="add_comment"),
    path("add_bid/<str:listing_id>", views.add_bid, name="add_bid"),
    path("toggle_watchlist/<str:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("close_auction/<str:listing_id>", views.close_auction, name="close_auction")
]
