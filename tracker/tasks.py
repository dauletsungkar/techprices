from celery import shared_task
from .models import Shop


@shared_task
def update_data():
    shops = Shop.objects.all()
    for shop in shops:
        shop.hello_world()

