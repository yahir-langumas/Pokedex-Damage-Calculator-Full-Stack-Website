import requests 
from django.core.management.base import BaseCommand
from pokedata.models import Type

# Use the API to get the data for each move and store it in the database.

class Command(BaseCommand):
    def handle(self, *args, **options):
        type_id = ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "fairy"]
        type_id_index = 0
        while type_id_index < len(type_id):
            poke_api_response = requests.get(f"https://pokeapi.co/api/v2/type/{type_id[type_id_index]}/", timeout = 10)
            poke_api_response.raise_for_status()  # Raise an error if the request was unsuccessful  
            type_data = poke_api_response.json()
            type_name = type_data["name"]
            type_relation = { 
                "double_damage_from": [relation["name"] for relation in type_data["damage_relations"]["double_damage_from"]],
                "double_damage_to": [relation["name"] for relation in type_data["damage_relations"]["double_damage_to"]],
                "half_damage_from": [relation["name"] for relation in type_data["damage_relations"]["half_damage_from"]],
                "half_damage_to": [relation["name"] for relation in type_data["damage_relations"]["half_damage_to"]],
                "no_damage_from": [relation["name"] for relation in type_data["damage_relations"]["no_damage_from"]],
                "no_damage_to": [relation["name"] for relation in type_data["damage_relations"]["no_damage_to"]]
            }
            Type.objects.get_or_create(
                name = type_name,
                defaults = { 
                    "type_data" : type_relation
                }
            )
            type_id_index += 1