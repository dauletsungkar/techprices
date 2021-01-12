from celery import shared_task
from .logic import Shop, Sulpak, BelyiVeter, TechnoDom, Mechta


@shared_task
def update_data():
    shops = [Mechta(), TechnoDom(), Sulpak(), BelyiVeter()]
    for shop in shops:
        shop.get_data()
