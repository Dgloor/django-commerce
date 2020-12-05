from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Max, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True).annotate(highest_bid_price=Max('bids__bid_price')),
        "page": "home"
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


class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'create'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Submit'))


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs["placeholder"] = "Enter comment"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add Comment'))


class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_price']

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)
        super(NewBidForm, self).__init__(*args, **kwargs)
        self.fields["bid_price"].widget.attrs["placeholder"] = "Enter bid"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Place Bid'))

    def clean(self):
        bid_price = self.cleaned_data["bid_price"]
        bids = Bid.objects.filter(listing=self.listing)
        if bids:
            highest_bid_price = bids.order_by("bid_price").last().bid_price
            if bid_price <= highest_bid_price:
                raise ValidationError(
                    "Bid must be greater than any bids already placed")
        else:
            if bid_price < self.listing.price:
                raise ValidationError(
                    "Bid must be as large as the starting bid")


@login_required
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]

            listing = Listing(creator=request.user, title=title,
                              description=description, price=price, image=image, category=category)
            listing.save()
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create.html", {
                "listing_form": form
            })

    return render(request, "auctions/create.html", {
        "listing_form": NewListingForm()
    })


def listing_page_utility(request, listing_id):
    listing = Listing.objects.annotate(highest_bid_price=Max(
        'bids__bid_price'), num_bids=Count('bids__id')).get(id=listing_id)
    comments = Comment.objects.filter(listing=listing)

    if request.user.is_authenticated:
        in_watchlist = listing in request.user.watchlist.all()
    else:
        in_watchlist = False

    return listing, comments, in_watchlist


def listing(request, listing_id):
    listing, comments, in_watchlist = listing_page_utility(request, listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "comment_form": NewCommentForm(),
        "bid_form": NewBidForm(),
        "in_watchlist": in_watchlist
    })


@login_required
def add_comment(request, listing_id):
    listing, comments, in_watchlist = listing_page_utility(request, listing_id)

    form = NewCommentForm(request.POST)

    if form.is_valid():
        content = form.cleaned_data["content"]
        comment = Comment(
            listing=listing, commenter=request.user, content=content)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "comment_form": form,
            "bid_form": NewBidForm(),
            "in_watchlist": in_watchlist
        })


@login_required
def add_bid(request, listing_id):
    listing, comments, in_watchlist = listing_page_utility(request, listing_id)

    form = NewBidForm(request.POST, listing=listing)

    if form.is_valid():
        bid_price = form.cleaned_data["bid_price"]
        bid = Bid(listing=listing, bidder=request.user, bid_price=bid_price)
        bid.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "comment_form": NewCommentForm(),
            "bid_form": form,
            "in_watchlist": in_watchlist
        })


@login_required
def toggle_watchlist(request, listing_id):
    listing, _, in_watchlist = listing_page_utility(request, listing_id)

    if in_watchlist:
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)

    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


@login_required
def close_auction(request, listing_id):
    listing, _, _ = listing_page_utility(request, listing_id)
    winning_bid = Bid.objects.filter(
        listing=listing).order_by("bid_price").last()

    if winning_bid:
        listing.winner = winning_bid.bidder

    listing.active = False
    listing.save()

    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def categories(request):
    categories = Listing.objects.filter(active=True).order_by(
        "category").values_list("category", flat=True).distinct()
    categories = [category.capitalize()
                  for category in categories if category is not None]
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_listings(request, category):
    return render(request, "auctions/index.html", {
        "category": category,
        "listings": Listing.objects.filter(category=category.upper()).filter(active=True),
        "page": "category"
    })


@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist.all(),
        "page": "watchlist"
    })
