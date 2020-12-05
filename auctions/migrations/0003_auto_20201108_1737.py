# Generated by Django 3.1.3 on 2020-11-08 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlist_bid_comment_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='AuctionList',
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]