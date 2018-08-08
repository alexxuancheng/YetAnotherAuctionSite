from celery import Celery
from celery.schedules import crontab
from auctions.models import Auction

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, auction_save.s(), name='save_auction')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@app.task
def auction_save():
    for au in Auction.objects.all():
        if au.active or au.due:
            au.save()

@app.task
def test(arg):
    print(arg)