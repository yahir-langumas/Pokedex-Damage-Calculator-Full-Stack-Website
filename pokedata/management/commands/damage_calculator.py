# DMG Calculator 
from pokedata.models import Species
from pokedata.models import Moves
from pokedata.models import Learnset
from pokedata.models import Type
import random

# Hard coding moves and abilities that have special properties that effect damage calculations and interactions with other moves and abilities.

SOUND_MOVES = {
    "alluring-voice", "boomburst", "bug-buzz", "chatter", "clanging-scales",
    "clangorous-soul", "clangorous-soulblaze", "confide", "disarming-voice",
    "dragon-cheer", "echoed-voice", "eerie-spell", "grass-whistle", "growl",
    "heal-bell", "howl", "hyper-voice", "metal-sound", "noble-roar",
    "overdrive", "parting-shot", "perish-song", "psychic-noise", "relic-song",
    "roar", "round", "screech", "sing", "snarl", "snore", "sparkling-aria",
    "supersonic", "torch-song", "uproar",
}

SLICING_MOVES = {
    "aerial-ace", "air-cutter", "air-slash", "aqua-cutter", "behemoth-blade",
    "bitter-blade", "ceaseless-edge", "cross-poison", "crush-claw", "cut",
    "dire-claw", "dragon-claw", "fury-cutter", "kowtow-cleave", "leaf-blade",
    "mighty-cleave", "night-slash", "population-bomb", "psyblade", "psycho-cut",
    "razor-leaf", "razor-shell", "sacred-sword", "secret-sword", "shadow-claw",
    "slash", "solar-blade", "stone-axe", "tachyon-cutter", "x-scissor",
}

CLAW_MOVES = {
    "crush-claw", "dire-claw", "dragon-claw", "hone-claws",
    "metal-claw", "shadow-claw",
}

BITING_MOVES = {
    "bite", "crunch", "fire-fang", "fishious-rend", "hyper-fang",
    "ice-fang", "jaw-lock", "poison-fang", "psychic-fangs", "thunder-fang",
}
PUNCHING_MOVES = {
    "bullet-punch", "comet-punch", "dizzy-punch", "double-iron-bash", "double-shock",
    "drain-punch", "dynamic-punch", "fire-punch", "focus-punch", "hammer-arm",
    "headlong-rush", "ice-hammer", "ice-punch", "jet-punch", "mach-punch",
    "mega-punch", "meteor-mash", "plasma-fists", "power-up-punch", "rage-fist",
    "shadow-punch", "sky-uppercut", "surging-strikes", "thunder-punch", "wicked-blow",
}

PULSE_MOVES = {
    "aura-sphere", "dark-pulse", "dragon-pulse", "heal-pulse",
    "origin-pulse", "terrain-pulse", "water-pulse",
}

WIND_MOVES = {
    "aeroblast", "air-cutter", "bleakwind-storm", "blizzard", "fairy-wind",
    "gust", "heat-wave", "hurricane", "icy-wind", "petal-blizzard",
    "sandsear-storm", "sandstorm", "springtide-storm", "tailwind", "twister",
    "whirlwind", "wildbolt-storm",
}

BALL_AND_BOMB_MOVES = {
    "acid-spray", "aura-sphere", "barrage", "beak-blast", "bullet-seed",
    "egg-bomb", "electro-ball", "energy-ball", "focus-blast", "gyro-ball",
    "ice-ball", "magnet-bomb", "mist-ball", "mud-bomb", "octazooka",
    "pollen-puff", "pyro-ball", "rock-blast", "rock-wrecker", "searing-shot",
    "seed-bomb", "shadow-ball", "sludge-bomb", "syrup-bomb", "weather-ball",
    "zap-cannon",
}

POWDER_AND_SPORE_MOVES = {
    "cotton-spore", "magic-powder", "poison-powder", "powder",
    "rage-powder", "sleep-powder", "spore", "stun-spore",
}

STATUS_EFFECTS = { 
    "burn": {"attack_multiplier": 0.5, "self_inflicted_dmg": 0.0625 }, # 1/16 hp lost per turn 
    "poison": {"self_inflicted_dmg": 0.125}, # consistent 1/8 hp per turn 
    "badly-poison": {"self_inflicted_dmg": 0.0625,}, # badly poison ramps-up dmg after each turn (by 1/16) 
    "paralysis": {"speed_multiplier": 0.5, "fully_paralyzed_chance": 0.25}, # fully_paralyzed -> 25% a pokemon won't act for 1 turn 
    "sleep": {"sleep_min_turns": 1, "sleep_max_turns": 3}, # Sleep is determined from a random number of turns a pokemon is asleep for between the range of 1-3.
    "freeze": {"thaw_chance": 0.20},
} 
  
STATUS_IMMUNITY_ABILITIES = {
    "limber": "paralysis", "insomnia": "sleep", "vital-spirit": "sleep",
    "water-veil": "burn", "water-bubble": "burn", "immunity": "poison",
    "pastel-veil": "poison", "magma-armor": "freeze", "own-tempo": "confusion",     
    "comatose": "all", "purifying-salt": "all",      
}

STATUS_STAT_BOOST_ABILITIES = {
    "guts": "attack", "marvel-scale": "defense", "quick-feet": "speed",    
}

STATUS_MOVE_POWER_BOOST_ABILITIES = {
    "toxic-boost": "poison", "flare-boost": "burn",    
}

STATUS_CURE_ABILITIES = {
    "natural-cure": "on-switch-out", "shed-skin": "end-of-turn-chance", "hydration": "end-of-turn-if-raining", 
    "healer": "end-of-turn-chance-ally", 
}



class DamageCalculator:
    def __init__(self, attacker: Species, defender: Species, move_type: str, move_power: int, move_name: str, status_effect: str):
        self.attacker = attacker
        self.defender = defender
        self.move_type = move_type
        self.move_power = move_power
        self.move_name = move_name
        self.attacker_learnset = Learnset.objects.get(species_id=self.attacker.pokedex_id)
        self.defender_learnset = Learnset.objects.get(species_id=self.defender.pokedex_id)
        self.defender_types_data = [Type.objects.get(name=t).type_data for t in self.defender.types]
        self.move_data = Moves.objects.get(name=self.move_name)
        self.status = status_effect
    def status_effects(self): 
        return self.status in STATUS_EFFECTS
    def sound_move(self): 
        return self.move_name in SOUND_MOVES
    def cut_move(self):
        return self.move_name in SLICING_MOVES
    def claw_move(self):
        return self.move_name in CLAW_MOVES
    def bite_move(self):
        return self.move_name in BITING_MOVES
    def punch_move(self):
        return self.move_name in PUNCHING_MOVES
    def pulse_move(self):
        return self.move_name in PULSE_MOVES
    def wind_move(self):
        return self.move_name in WIND_MOVES
    def ball_and_bomb_move(self):
        return self.move_name in BALL_AND_BOMB_MOVES
    def powder_and_spore_move(self):
        return self.move_name in POWDER_AND_SPORE_MOVES

    # Guts boosts the bearer's Attack stat by 50% when it has a major status condition.
    def guts_ability(self): 
        if "guts" not in self.attacker.abilities: 
            return self.attacker.stats["attack"] 
        if self.status_effects(): 
            return self.attacker.stats["attack"] * 1.5
        else: 
            return self.attacker.stats["attack"]

    # Toxic boost increases the Pokémon's physical Attack stat by 1.5× when it is poisoned
    def toxic_boost_ability(self): 
        if "toxic-boost" not in self.attacker.abilities: 
            return self.attacker.stats["attack"]  
        if self.status == "poison" or self.status == "badly-poison": 
            return self.attacker.stats["attack"] * 1.5 
        else: 
            return self.attacker.stats["attack"]

    # Flare boost multiplies the user's Special Attack stat by 1.5× when the Pokémon is burned
    def flare_boost_ability(self): 
        if "flare-boost" not in self.attacker.abilities: 
            return self.attacker.stats["special-attack"]
        if self.status == "burn": 
            return self.attacker.stats["special-attack"] * 1.5 
        else: 
            return self.attacker.stats["special-attack"]

    # Quick feet increases a Pokémon's Speed stat by 50% when it is affected by a major status ailment like poison, burn, paralysis, freeze, or sleep
    def quick_feet_ability(self): 
        if "quick-feet" not in self.attacker.abilities: 
            return self.attacker.stats["speed"]
        if self.status_effects(): 
            return self.attacker.stats["speed"] * 1.5 
        else: 
            return self.attacker.stats["speed"]
        
    # Pure Power doubles the user's total physical Attack stat in battle.
    def pure_power_ability(self): 
        if "pure-power" not in self.attacker.abilities: 
           return self.attacker.stats["attack"] 
        return self.attacker.stats["attack"] * 2
         
    # Rock Head protects a Pokémon from taking recoil damage when using high-power physical attacks
    def rock_head_ability(self):
        if self.move_data.meta is None:
            return 0
        drain = self.move_data.meta.get("drain", 0)
        if "rock-head" in self.attacker.abilities and drain < 0:
            return 0
        return drain
        # Will add more logic to remove special effects of moves like recoil damage, stat changes, and status effects later.
    
    # Levitate is an ability that gives a Pokémon full immunity to Ground-type moves, Spikes, Toxic Spikes, and the Arena Trap ability.
    def levitate_ability(self):
        if "levitate" not in self.defender.abilities: 
            return self.move_power 
        if self.move_type  == "ground": 
            return self.move_power * 0 
        else: 
            return self.move_power
        # Will add more logic later for the other effects of levitate like spikes, toxic spikes, and arena trap.

    # Makes the user immune to all direct damaging moves unless they are super-effective
    def wonder_guard_ability(self):
        if "wonder-guard" not in self.defender.abilities:
            return self.move_power
        multiplier = 1
        for type_data in self.defender_types_data:
            if self.move_type in type_data["double_damage_from"]:
                multiplier *= 2
            elif self.move_type in type_data["half_damage_from"]:
                multiplier *= 0.5
            elif self.move_type in type_data["no_damage_from"]:
                multiplier *= 0

        if multiplier > 1:
            return self.move_power
        return self.move_power * 0
    
    # Huge Power is a powerful Pokémon ability that doubles the user's actual Attack stat during battle   
    def huge_power_ability(self):
        if "huge-power" not in self.attacker.abilities: 
            return self.attacker.stats["attack"] 
        return self.attacker.stats["attack"] * 2
        # Will add more logic around IV and EV later to make it more accurate.

    def thick_fat_ability(self):
        pass
    def filter_ability(self):
        pass
    def solid_rock_ability(self):
        pass
    def life_orb_item(self):
        pass
    def choice_band_item(self):
        pass
 