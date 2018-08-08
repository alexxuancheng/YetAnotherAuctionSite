#!/usr/bin/python3
from celery import Celery
from auctions.models import Auction

app = Celery('yaas5_project', broker='amqp://guest@localhost//')

@app.task
def auction_save():
    for au in Auction.objects.all():
    	au.save()