# Import Api data into database 
import requests 
from django.core.management.base import BaseCommand
from pokedata.models import Moves

# Use the API to get the data for each move and store it in the database.

class Command(BaseCommand):
    def handle(self, *args, **options):
        move_id = 1
        max_move_id = 919 
        while move_id <= max_move_id: 
            poke_api_response = requests.get(f"https://pokeapi.co/api/v2/move/{move_id}/", timeout = 10)
            poke_api_response.raise_for_status()  # Raise an error if the request was unsuccessful  
            move_data = poke_api_response.json()
            damage_class = move_data["damage_class"]["name"]
            type = move_data["type"]["name"]
            # Meta refers to the metadata of the move, so attributes like move effect such as "has a 30% chance to paralyze the target"
            # or "increases the user's speed by 1 stage" would be stored in this field.
            # Also the stat changes of the move would be stored in this field.
            if move_data["meta"] is not None: 
                meta = {
                    "ailment": move_data["meta"]["ailment"]["name"] if move_data["meta"]["ailment"] else None,
                    "category": move_data["meta"]["category"]["name"],
                    "min_hits": move_data["meta"]["min_hits"],
                    "max_hits": move_data["meta"]["max_hits"],
                    "min_turns": move_data["meta"]["min_turns"],
                    "max_turns": move_data["meta"]["max_turns"],
                    "drain": move_data["meta"]["drain"],
                    "healing": move_data["meta"]["healing"],
                    "crit_rate": move_data["meta"]["crit_rate"],
                    "ailment_chance": move_data["meta"]["ailment_chance"],
                    "flinch_chance": move_data["meta"]["flinch_chance"],
                    "stat_chance": move_data["meta"]["stat_chance"]
                } 
            else: 
                meta = None
            Moves.objects.get_or_create(
                move_id = move_data["id"], 
                defaults = { 
                    "name" : move_data["name"], 
                    "power": move_data["power"], 
                    "accuracy" : move_data["accuracy"],
                    "priority": move_data["priority"],
                    "pp" : move_data["pp"],
                    "effect_chance": move_data["effect_chance"],
                    "damage_class" : damage_class, 
                    "type" : type, 
                    "meta" : meta, 
                    "stat_changes" : move_data["stat_changes"]
                }
            ) 


            move_id += 1 
