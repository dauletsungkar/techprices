from celery import shared_task
from .models import Shop, Sulpak, BelyiVeter, TechnoDom, Mechta


@shared_task
def update_data():
    shops = [TechnoDom(), Sulpak(), BelyiVeter(), Mechta()]
    for shop in shops:
        shop.get_data()