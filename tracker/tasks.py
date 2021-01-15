"""This module stores all tasks of the tracker application"""
from celery import shared_task
from .logic import Sulpak, BelyiVeter, TechnoDom, Mechta


@shared_task
def update_data():
    """This periodic task collects data from all stores and updates the database"""
    shops = [Mechta(), Sulpak(), BelyiVeter(), TechnoDom()]
    for shop in shops:
        shop.get_data()
