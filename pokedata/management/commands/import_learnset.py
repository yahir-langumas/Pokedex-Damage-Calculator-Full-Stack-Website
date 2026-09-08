# Import Api data into database 
import requests 
from django.core.management.base import BaseCommand
from pokedata.models import Learnset

class Command(BaseCommand): 
    def handle (self, *args, **options):
            species_id = 1
            max_species_id = 1025
            while species_id <= max_species_id:
                poke_api_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{species_id}/", timeout = 10)
                poke_api_response.raise_for_status()  # Raise an error if the request was unsuccessful
                pokemon_learnset = poke_api_response.json()
                moves_known = set()
                # A set is used to used to here because pokemon can learn the same move in multiple ways, like leveling up or TM's. 
                # Used to avoid duplicates in the moves list for a pokemon.
                for move_entry in pokemon_learnset["moves"]: 
                     for version_detail in move_entry["version_group_details"]: 
                          # Using Scarlet-Violet as the game version to determine the moves a pokemon can learn.
                          # Currently all pokemon are updated, until Pokemon Champions add all Pokemon from the pokedex. 
                          if version_detail["version_group"]["name"] == "scarlet-violet": 
                               moves_known.add(move_entry["move"]["name"])
                pokedex_id = pokemon_learnset["id"]
                Learnset.objects.get_or_create( 
                     species_id = pokedex_id,
                     defaults = {
                         "name": pokemon_learnset["name"],
                         "moves": list(moves_known)
                     }
                )
                species_id += 1