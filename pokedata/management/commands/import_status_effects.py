# Import Api data into database 

import requests
from django.core.management.base import BaseCommand
from pokedata.models import Status_Effect