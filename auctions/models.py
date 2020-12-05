from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchlist")

class Listing(models.Model):
    LISTING_CATEGORIES = [
        ('BOOKS', 'Books'),
        ('MUSIC', 'Music'),
        ('GAMES', 'Games'),
        ('ELECTRONICS', 'Electronics'),
        ('HOME', 'Home'),
        ('TOYS', 'Toys'),
        ('SPORTS', 'Sports'),
        ('FASHION', 'Fashion')
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", null=True)
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(decimal_places=2, verbose_name="Starting Bid", max_digits=15)
    image = models.URLField(blank=True, verbose_name="Image URL", null=True)
    category = models.CharField(choices=LISTING_CATEGORIES, blank=True, verbose_name="Category", max_length=200, null=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    bid_price = models.DecimalField(decimal_places=2, verbose_name="Bid Price", max_digits=15, null=True)

    def __str__(self):
        return f"{self.bidder} bid ${self.bid_price} for {self.listing}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    content = models.TextField(verbose_name="Comment", default="")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.commenter} commented on {self.listing} ({self.timestamp.date()})"

