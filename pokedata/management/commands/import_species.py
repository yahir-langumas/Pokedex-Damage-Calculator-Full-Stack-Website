# Import Api data into database 

import requests
from django.core.management.base import BaseCommand
from pokedata.models import Species 

# Use the API to get the data for each species (Pokemon) and store it in the database.

class Command(BaseCommand):
    def handle (self, *args, **options):
        species_id = 1
        max_species_id = 1025
        while species_id <= max_species_id:
            poke_api_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{species_id}/", timeout = 10)
            poke_api_response.raise_for_status()  # Raise an error if the request was unsuccessful
            pokemon_data = poke_api_response.json()
            pokemon_types = [type_info["type"]["name"] for type_info in pokemon_data["types"]]
            pokemon_abilities = [ability_info["ability"]["name"] for ability_info in pokemon_data["abilities"]]
            pokemon_stats = {stat_info["stat"]["name"]: stat_info["base_stat"] for stat_info in pokemon_data["stats"]}
            pokemon_total_stats = sum(pokemon_stats.values())
            Species.objects.get_or_create(
                pokedex_id = pokemon_data["id"], 
                defaults= { 
                    "name" : pokemon_data["name"],
                    "types" : pokemon_types,
                    "height" : pokemon_data["height"],
                    "weight" : pokemon_data["weight"],
                    "base_experience" : pokemon_data["base_experience"],
                    "abilities" : pokemon_abilities,
                    "stats" : pokemon_stats,
                    "total_stats" : pokemon_total_stats,
                    "sprite" : pokemon_data["sprites"]["other"]["official-artwork"]["front_default"],
                },
            )
            
            species_id +=1
        
