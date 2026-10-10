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

# One-hit KO moves (Sturdy is immune to these).
OHKO_MOVES = {
    "fissure", "guillotine", "horn-drill", "sheer-cold",
}

# Explosive moves (Damp stops these from being used).
EXPLOSIVE_MOVES = {
    "explosion", "mind-blown", "misty-explosion", "self-destruct",
}

# Critical hit chance by crit stage (Gen 7+). Stage 3 and up always crits.
CRIT_CHANCE_BY_STAGE = {0: 1 / 24, 1: 1 / 8, 2: 1 / 2, 3: 1}

STATUS_EFFECTS = {
    "burn": {"attack_multiplier": 0.5, "self_inflicted_dmg": 0.0625 }, # 1/16 hp lost per turn
    "poison": {"self_inflicted_dmg": 0.125}, # consistent 1/8 hp per turn
    "badly-poison": {"self_inflicted_dmg": 0.0625,}, # badly poison ramps-up dmg after each turn (by 1/16)
    "paralysis": {"speed_multiplier": 0.5, "fully_paralyzed_chance": 0.25}, # fully_paralyzed -> 25% a pokemon won't act for 1 turn
    "sleep": {"sleep_min_turns": 1, "sleep_max_turns": 3}, # Sleep is determined from a random number of turns a pokemon is asleep for between the range of 1-3.
    "freeze": {"thaw_chance": 0.20},
}

WEATHER_EFFECTS = {
    "rain": {"boosted_type": "water", "boost_multiplier": 1.5, "weakened_type": "fire", "weaken_multiplier": 0.5, "turns": 5}, # water moves do 1.5x dmg, fire moves do 0.5x dmg
    "sun": {"boosted_type": "fire", "boost_multiplier": 1.5, "weakened_type": "water", "weaken_multiplier": 0.5, "prevents_status": ["freeze"], "turns": 5}, # fire moves do 1.5x dmg, water moves do 0.5x dmg, no pokemon can be frozen
    "sandstorm": {"self_inflicted_dmg": 0.0625, "immune_types": ["rock", "ground", "steel"], "immune_abilities": ["sand-veil", "sand-rush", "sand-force", "overcoat", "magic-guard"], "boosted_stat_type": "rock", "boosted_stat": "special-defense", "stat_multiplier": 1.5, "turns": 5}, # 1/16 hp lost per turn unless rock/ground/steel, rock types get 1.5x sp. def
    "snow": {"boosted_stat_type": "ice", "boosted_stat": "defense", "stat_multiplier": 1.5, "turns": 5}, # gen 9 replacement for hail -> no chip dmg, ice types get 1.5x def
    "hail": {"self_inflicted_dmg": 0.0625, "immune_types": ["ice"], "immune_abilities": ["ice-body", "snow-cloak", "overcoat", "magic-guard"], "turns": 5}, # gen 3-8 only -> 1/16 hp lost per turn unless ice type
    "heavy-rain": {"boosted_type": "water", "boost_multiplier": 1.5, "weakened_type": "fire", "weaken_multiplier": 0, "primal": True, "turns": None}, # primordial sea -> damaging fire moves fail. lasts until the user leaves the field
    "extreme-sun": {"boosted_type": "fire", "boost_multiplier": 1.5, "weakened_type": "water", "weaken_multiplier": 0, "prevents_status": ["freeze"], "primal": True, "turns": None}, # desolate land -> damaging water moves fail. lasts until the user leaves the field
    "strong-winds": {"removes_flying_weaknesses": True, "primal": True, "turns": None}, # delta stream -> moves that are super effective on flying types hit neutral instead
}

# Terrain only affects grounded pokemon (anything that isn't a flying type or doesn't have levitate).
TERRAIN_EFFECTS = {
    "electric-terrain": {"boosted_type": "electric", "boost_multiplier": 1.3, "prevents_status": ["sleep"], "turns": 5}, # grounded pokemon's electric moves do 1.3x dmg, grounded pokemon can't fall asleep
    "grassy-terrain": {"boosted_type": "grass", "boost_multiplier": 1.3, "heal": 0.0625, "halved_moves": ["bulldoze", "earthquake", "magnitude"], "turns": 5}, # grounded pokemon's grass moves do 1.3x dmg, grounded pokemon heal 1/16 hp per turn, earthquake/bulldoze/magnitude do 0.5x dmg to grounded targets
    "misty-terrain": {"weakened_type": "dragon", "weaken_multiplier": 0.5, "prevents_status": ["all"], "turns": 5}, # dragon moves do 0.5x dmg to grounded targets, grounded pokemon can't get a major status or confusion
    "psychic-terrain": {"boosted_type": "psychic", "boost_multiplier": 1.3, "blocks_priority": True, "turns": 5}, # grounded pokemon's psychic moves do 1.3x dmg, grounded pokemon are protected from priority moves
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
    def __init__(self, attacker: Species, defender: Species, move_type: str, move_power: int, move_name: str, status_effect_attacker: str, status_effect_defender: str, weather: str = None, terrain: str = None):
        self.attacker = attacker
        self.defender = defender
        self.move_type = move_type
        self.move_power = move_power
        self.move_name = move_name
        self.attacker_learnset = Learnset.objects.get(species_id=self.attacker.pokedex_id)
        self.defender_learnset = Learnset.objects.get(species_id=self.defender.pokedex_id)
        self.attacker_types_data = [Type.objects.get(name=t).type_data for t in self.attacker.types]
        self.defender_types_data = [Type.objects.get(name=t).type_data for t in self.defender.types]
        self.move_data = Moves.objects.get(name=self.move_name)
        self.status_attacker = status_effect_attacker
        self.status_defender = status_effect_defender
        self.weather = weather 
        self.terrain = terrain 
        self.weather_turns = WEATHER_EFFECTS[weather]["turns"] if weather in WEATHER_EFFECTS else 0 # None -> primal weather, never runs out on its own
        self.terrain_turns = TERRAIN_EFFECTS[terrain]["turns"] if terrain in TERRAIN_EFFECTS else 0

    def status_effects_attacker(self):
        return self.status_attacker in STATUS_EFFECTS
    def status_effects_defender(self):
        return self.status_defender in STATUS_EFFECTS
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
    def ohko_move(self):
        return self.move_name in OHKO_MOVES
    def explosive_move(self):
        return self.move_name in EXPLOSIVE_MOVES


    # Weather and terrain effects. Weather and terrain can be set by abilities, moves, or items. They can also be blocked by abilities.
    def current_weather(self):
        for pokemon in (self.attacker, self.defender):
            if "cloud-nine" in pokemon.abilities or "air-lock" in pokemon.abilities:
                return None
        return self.weather
    
    def weather_effects(self):
        return WEATHER_EFFECTS.get(self.current_weather(), {})
    
    def terrain_effects(self):
        return TERRAIN_EFFECTS.get(self.terrain, {})

    # A Pokémon is grounded unless it is a Flying type or has Levitate. Terrain only affects grounded Pokémon.
    # Will add Air Balloon, Magnet Rise, and Gravity later once items and field moves are in.
    def grounded_attacker(self):
        return "flying" not in self.attacker.types and "levitate" not in self.attacker.abilities
    def grounded_defender(self):
        return "flying" not in self.defender.types and "levitate" not in self.defender.abilities

    # Rain, sun, and their primal versions boost or weaken moves of certain types.
    def weather_move_power(self):
        if not self.move_power:
            return self.move_power
        effects = self.weather_effects()
        if effects.get("boosted_type") == self.move_type:
            return self.move_power * effects["boost_multiplier"]
        if effects.get("weakened_type") == self.move_type:
            return self.move_power * effects["weaken_multiplier"]
        return self.move_power

    # Terrain boosts moves used by a grounded attacker, and weakens some moves that hit a grounded target.
    def terrain_move_power(self):
        if not self.move_power:
            return self.move_power
        effects = self.terrain_effects()
        power = self.move_power
        if self.grounded_attacker() and effects.get("boosted_type") == self.move_type:
            power *= effects["boost_multiplier"]
        if self.grounded_defender() and effects.get("weakened_type") == self.move_type:
            power *= effects["weaken_multiplier"]
        if self.grounded_defender() and self.move_name in effects.get("halved_moves", []):
            power *= 0.5
        return power

    # Weather chip damage at the end of each turn, as a fraction of max HP (same as self_inflicted_dmg)
    # Wonder Guard does NOT block this, since it only stops direct attacks. (HAHA, I know, right? Wonder Guard is a terrible ability. Its not Im joking!)
    def weather_damage_attacker(self):
        effects = self.weather_effects()
        if "self_inflicted_dmg" not in effects:
            return 0
        for t in self.attacker.types:
            if t in effects["immune_types"]:
                return 0
        for ability in self.attacker.abilities:
            if ability in effects["immune_abilities"]:
                return 0
        return effects["self_inflicted_dmg"]
    def weather_damage_defender(self):
        effects = self.weather_effects()
        if "self_inflicted_dmg" not in effects:
            return 0
        for t in self.defender.types:
            if t in effects["immune_types"]:
                return 0
        for ability in self.defender.abilities:
            if ability in effects["immune_abilities"]:
                return 0
        return effects["self_inflicted_dmg"]

    # Sandstorm boosts Rock types' Special Defense by 50%. Snow boosts Ice types' Defense by 50%.
    def weather_stat_attacker(self, stat):
        effects = self.weather_effects()
        if effects.get("boosted_stat") == stat and effects.get("boosted_stat_type") in self.attacker.types:
            return self.attacker.stats[stat] * effects["stat_multiplier"]
        return self.attacker.stats[stat]
    def weather_stat_defender(self, stat):
        effects = self.weather_effects()
        if effects.get("boosted_stat") == stat and effects.get("boosted_stat_type") in self.defender.types:
            return self.defender.stats[stat] * effects["stat_multiplier"]
        return self.defender.stats[stat]

    # Grassy Terrain heals grounded Pokémon 1/16 of their max HP at the end of each turn.
    def terrain_heal_attacker(self):
        if not self.grounded_attacker():
            return 0
        return self.terrain_effects().get("heal", 0)
    def terrain_heal_defender(self):
        if not self.grounded_defender():
            return 0
        return self.terrain_effects().get("heal", 0)

    # Psychic Terrain protects grounded Pokémon from priority moves. Returns True if the move is blocked.
    def terrain_blocks_priority_attacker(self):
        if not self.terrain_effects().get("blocks_priority"):
            return False
        if not self.grounded_attacker():
            return False
        return self.move_data.priority > 0
    def terrain_blocks_priority_defender(self):
        if not self.terrain_effects().get("blocks_priority"):
            return False
        if not self.grounded_defender():
            return False
        return self.move_data.priority > 0

    # Sun stops freezing. Electric Terrain stops grounded Pokémon from falling asleep.
    # Misty Terrain stops grounded Pokémon from getting any major status or confusion.
    # incoming_status = the status a move or ability is trying to give. Returns True if the field blocks it.
    def field_blocks_status_attacker(self, incoming_status):
        if incoming_status in self.weather_effects().get("prevents_status", []):
            return True
        if self.grounded_attacker():
            terrain_blocks = self.terrain_effects().get("prevents_status", [])
            if "all" in terrain_blocks or incoming_status in terrain_blocks:
                return True
        return False
    def field_blocks_status_defender(self, incoming_status):
        if incoming_status in self.weather_effects().get("prevents_status", []):
            return True
        if self.grounded_defender():
            terrain_blocks = self.terrain_effects().get("prevents_status", [])
            if "all" in terrain_blocks or incoming_status in terrain_blocks:
                return True
        return False

    # Call these once at the end of every turn. Weather and terrain end when their turns run out.
    # Primal weather has turns = None, so it never runs out on its own.
    def end_of_turn_weather(self):
        if self.weather_turns:
            self.weather_turns -= 1
            if self.weather_turns == 0:
                self.weather = None
        return self.weather
    def end_of_turn_terrain(self):
        if self.terrain_turns:
            self.terrain_turns -= 1
            if self.terrain_turns == 0:
                self.terrain = None
        return self.terrain


    # Type effectiveness of the move against a Pokémon (0, 0.25, 0.5, 1, 2, or 4).
    # Strong winds remove the Flying type's weaknesses, so those hits count as neutral instead of super effective.
    def type_effectiveness_attacker(self):
        removes_flying_weaknesses = self.weather_effects().get("removes_flying_weaknesses", False)
        multiplier = 1
        for type_name, type_data in zip(self.attacker.types, self.attacker_types_data):
            if self.move_type in type_data["double_damage_from"]:
                if not (removes_flying_weaknesses and type_name == "flying"):
                    multiplier *= 2
            elif self.move_type in type_data["half_damage_from"]:
                multiplier *= 0.5
            elif self.move_type in type_data["no_damage_from"]:
                multiplier *= 0
        return multiplier
    def type_effectiveness_defender(self):
        removes_flying_weaknesses = self.weather_effects().get("removes_flying_weaknesses", False)
        multiplier = 1
        for type_name, type_data in zip(self.defender.types, self.defender_types_data):
            if self.move_type in type_data["double_damage_from"]:
                if not (removes_flying_weaknesses and type_name == "flying"):
                    multiplier *= 2
            elif self.move_type in type_data["half_damage_from"]:
                multiplier *= 0.5
            elif self.move_type in type_data["no_damage_from"]:
                multiplier *= 0
        return multiplier

    # Rolls for a critical hit. Returns the damage multiplier: 1.5 on a crit, 1 otherwise.
    # High-crit moves (Slash, Stone Edge, etc.) store their crit stage in meta["crit_rate"].
    def critical_hit_roll(self):
        if not self.move_power:
            return 1
        crit_stage = 0
        if self.move_data.meta is not None:
            crit_stage = self.move_data.meta.get("crit_rate") or 0
        crit_stage = min(crit_stage, 3)
        if random.random() < CRIT_CHANCE_BY_STAGE[crit_stage]:
            return 1.5
        return 1

    # -------- Abilities -------- 

    # Guts boosts the bearer's Attack stat by 50% when it has a major status condition.
    def guts_ability_attacker(self):
        if "guts" not in self.attacker.abilities:
            return self.attacker.stats["attack"]
        if self.status_effects_attacker():
            return self.attacker.stats["attack"] * 1.5
        else:
            return self.attacker.stats["attack"]
    def guts_ability_defender(self):
        if "guts" not in self.defender.abilities:
                return self.defender.stats["attack"]
        if self.status_effects_defender():
            return self.defender.stats["attack"] * 1.5
        else:
            return self.defender.stats["attack"]

    # Toxic boost increases the Pokémon's physical Attack stat by 1.5× when it is poisoned
    def toxic_boost_ability_attacker(self):
        if "toxic-boost" not in self.attacker.abilities:
            return self.attacker.stats["attack"]
        if self.status_attacker == "poison" or self.status_attacker == "badly-poison":
            return self.attacker.stats["attack"] * 1.5
        else:
            return self.attacker.stats["attack"]
    def toxic_boost_ability_defender(self):
        if "toxic-boost" not in self.defender.abilities:
           return self.defender.stats["attack"]
        if self.status_defender == "poison" or self.status_defender == "badly-poison":
            return self.defender.stats["attack"] * 1.5
        else:
            return self.defender.stats["attack"]

    # Flare boost multiplies the user's Special Attack stat by 1.5× when the Pokémon is burned
    def flare_boost_ability_attacker(self):
        if "flare-boost" not in self.attacker.abilities:
            return self.attacker.stats["special-attack"]
        if self.status_attacker == "burn":
            return self.attacker.stats["special-attack"] * 1.5
        else:
            return self.attacker.stats["special-attack"]
    def flare_boost_ability_defender(self):
        if "flare-boost" not in self.defender.abilities:
            return self.defender.stats["special-attack"]
        if self.status_defender == "burn":
            return self.defender.stats["special-attack"] * 1.5
        else:
            return self.defender.stats["special-attack"]

    # Quick feet increases a Pokémon's Speed stat by 50% when it is affected by a major status ailment like poison, burn, paralysis, freeze, or sleep
    def quick_feet_ability_attacker(self):
        if "quick-feet" not in self.attacker.abilities:
            return self.attacker.stats["speed"]
        if self.status_effects_attacker():
            return self.attacker.stats["speed"] * 1.5
        else:
            return self.attacker.stats["speed"]
    def quick_feet_ability_defender(self):
        if "quick-feet" not in self.defender.abilities:
            return self.defender.stats["speed"]
        if self.status_effects_defender():
            return self.defender.stats["speed"] * 1.5
        else:
            return self.defender.stats["speed"]

    # Marvel scale boosts the user's Defense stat by 50% (1.5×) whenever it is afflicted with a major status condition(poison, burn, paralysis, freeze, or sleep).
    def marvel_scale_ability_attacker(self):
        if "marvel-scale" not in self.attacker.abilities:
            return self.attacker.stats["defense"]
        if self.status_effects_attacker():
            return self.attacker.stats["defense"] * 1.5
        else:
            return self.attacker.stats["defense"]
    def marvel_scale_ability_defender(self):
        if "marvel-scale" not in self.defender.abilities:
            return self.defender.stats["defense"]
        if self.status_effects_defender():
            return self.defender.stats["defense"] * 1.5
        else:
            return self.defender.stats["defense"]


    # Pure Power doubles the user's total physical Attack stat in battle.
    def pure_power_ability_attacker(self):
        if "pure-power" not in self.attacker.abilities:
           return self.attacker.stats["attack"]
        return self.attacker.stats["attack"] * 2
    def pure_power_ability_defender(self):
        if "pure-power" not in self.defender.abilities:
           return self.defender.stats["attack"]
        return self.defender.stats["attack"] * 2

    # Rock Head protects a Pokémon from taking recoil damage when using high-power physical attacks
    def rock_head_ability_attacker(self):
        if self.move_data.meta is None:
            return 0
        drain = self.move_data.meta.get("drain", 0)
        if "rock-head" in self.attacker.abilities and drain < 0:
            return 0
        return drain
    def rock_head_ability_defender(self):
        if self.move_data.meta is None:
            return 0
        drain = self.move_data.meta.get("drain", 0)
        if "rock-head" in self.defender.abilities and drain < 0:
            return 0
        return drain
        # Will add more logic to remove special effects of moves like recoil damage, stat changes, and status effects later.

    # Levitate is an ability that gives a Pokémon full immunity to Ground-type moves, Spikes, Toxic Spikes, and the Arena Trap ability.
    # Levitate also means the Pokémon isn't grounded, so terrain doesn't affect it (handled in grounded_attacker / grounded_defender).
    def levitate_ability_attacker(self):
        if "levitate" not in self.attacker.abilities:
            return self.move_power
        if self.move_type  == "ground":
            return self.move_power * 0
        else:
            return self.move_power
    def levitate_ability_defender(self):
        if "levitate" not in self.defender.abilities:
            return self.move_power
        if self.move_type  == "ground":
            return self.move_power * 0
        else:
            return self.move_power
        # Will add more logic later for the other effects of levitate like spikes, toxic spikes, and arena trap.

    # Makes the user immune to all direct damaging moves unless they are super-effective
    # Strong winds can turn a super-effective hit into a neutral one, so this uses type_effectiveness.
    def wonder_guard_ability_attacker(self):
        if "wonder-guard" not in self.attacker.abilities:
            return self.move_power
        if self.type_effectiveness_attacker() > 1:
            return self.move_power
        return self.move_power * 0
    def wonder_guard_ability_defender(self):
        if "wonder-guard" not in self.defender.abilities:
            return self.move_power
        if self.type_effectiveness_defender() > 1:
            return self.move_power
        return self.move_power * 0

    # Huge Power is a powerful Pokémon ability that doubles the user's actual Attack stat during battle
    def huge_power_ability_attacker(self):
        if "huge-power" not in self.attacker.abilities:
            return self.attacker.stats["attack"]
        return self.attacker.stats["attack"] * 2
    def huge_power_ability_defender(self):
        if "huge-power" not in self.defender.abilities:
            return self.defender.stats["attack"]
        return self.defender.stats["attack"] * 2
        # Will add more logic around IV and EV later to make it more accurate.

    # Bulletproof: The Pokémon is immune to ball and bomb moves.
    def bulletproof_ability_attacker(self):
        if "bulletproof" not in self.attacker.abilities:
            return self.move_power
        if self.ball_and_bomb_move():
            return self.move_power * 0
        else:
            return self.move_power
    def bulletproof_ability_defender(self):
        if "bulletproof" not in self.defender.abilities:
            return self.move_power
        if self.ball_and_bomb_move():
            return self.move_power * 0
        else:
            return self.move_power

    # Thick Fat: Halves the damage taken from Fire and Ice type moves.
    def thick_fat_ability_attacker(self):
        if "thick-fat" not in self.attacker.abilities:
            return self.move_power
        if self.move_type == "fire" or self.move_type == "ice":
            return self.move_power * 0.5
        else:
            return self.move_power
    def thick_fat_ability_defender(self):
        if "thick-fat" not in self.defender.abilities:
            return self.move_power
        if self.move_type == "fire" or self.move_type == "ice":
            return self.move_power * 0.5
        else:
            return self.move_power

    # Filter: Reduces the damage taken from super-effective moves to 75%.
    # Strong winds can turn a super-effective hit into a neutral one, so this uses type_effectiveness.
    def filter_ability_attacker(self):
        if "filter" not in self.attacker.abilities:
            return self.move_power
        if self.type_effectiveness_attacker() > 1:
            return self.move_power * 0.75
        return self.move_power
    def filter_ability_defender(self):
        if "filter" not in self.defender.abilities:
            return self.move_power
        if self.type_effectiveness_defender() > 1:
            return self.move_power * 0.75
        return self.move_power

    # Solid Rock: Same as Filter. Reduces the damage taken from super-effective moves to 75%.
    def solid_rock_ability_attacker(self):
        if "solid-rock" not in self.attacker.abilities:
            return self.move_power
        if self.type_effectiveness_attacker() > 1:
            return self.move_power * 0.75
        return self.move_power
    def solid_rock_ability_defender(self):
        if "solid-rock" not in self.defender.abilities:
            return self.move_power
        if self.type_effectiveness_defender() > 1:
            return self.move_power * 0.75
        return self.move_power

    # Stench: 10% chance to make the target flinch when the move deals damage.
    # Doesn't stack with moves that already have a flinch chance (Bite keeps its own 30%).
    # Returns the flinch chance as a decimal, so roll it with: random.random() < chance
    def stench_ability_attacker(self):
        move_flinch_chance = 0
        if self.move_data.meta is not None:
            move_flinch_chance = (self.move_data.meta.get("flinch_chance") or 0) / 100
        if "stench" not in self.attacker.abilities:
            return move_flinch_chance
        if not self.move_power or move_flinch_chance > 0:
            return move_flinch_chance
        return 0.10
    def stench_ability_defender(self):
        move_flinch_chance = 0
        if self.move_data.meta is not None:
            move_flinch_chance = (self.move_data.meta.get("flinch_chance") or 0) / 100
        if "stench" not in self.defender.abilities:
            return move_flinch_chance
        if not self.move_power or move_flinch_chance > 0:
            return move_flinch_chance
        return 0.10

    # Drizzle: Summons rain for 5 turns when the Pokémon enters battle.
    # It can't replace primal weather (heavy rain, extreme sun, strong winds).
    # Call this when the Pokémon switches in, then use weather_move_power() for the damage change.
    def drizzle_ability_attacker(self):
        if "drizzle" not in self.attacker.abilities:
            return self.weather
        if WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "rain"
        self.weather_turns = WEATHER_EFFECTS["rain"]["turns"]
        return self.weather
    def drizzle_ability_defender(self):
        if "drizzle" not in self.defender.abilities:
            return self.weather
        if WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "rain"
        self.weather_turns = WEATHER_EFFECTS["rain"]["turns"]
        return self.weather

    # Speed Boost: +1 Speed stage at the end of every turn, up to +6.
    # turns_on_field = how many turns have ended with this Pokémon already out.
    # Don't count the turn it switched in (a lead that started the battle does count turn 1).
    # Each stage is +50% of the base stat: +1 = 1.5x, +2 = 2x, ... +6 = 4x.
    def speed_boost_ability_attacker(self, turns_on_field):
        if "speed-boost" not in self.attacker.abilities:
            return self.attacker.stats["speed"]
        stage = min(turns_on_field, 6)
        return self.attacker.stats["speed"] * (2 + stage) / 2
    def speed_boost_ability_defender(self, turns_on_field):
        if "speed-boost" not in self.defender.abilities:
            return self.defender.stats["speed"]
        stage = min(turns_on_field, 6)
        return self.defender.stats["speed"] * (2 + stage) / 2

    # Battle Armor: Attacks landed on the Pokémon will never be critical hits.
    # Returns the crit multiplier to plug into the damage formula.
    def battle_armor_ability_attacker(self):
        if "battle-armor" not in self.attacker.abilities:
            return self.critical_hit_roll()
        return 1
    def battle_armor_ability_defender(self):
        if "battle-armor" not in self.defender.abilities:
            return self.critical_hit_roll()
        return 1

    # Sturdy: At full HP, survives a hit that would KO it with 1 HP left. Also immune to one-hit KO moves.
    # damage = the final damage you calculated for this hit. Returns the damage actually taken.
    def sturdy_ability_attacker(self, damage, current_hp, max_hp):
        if "sturdy" not in self.attacker.abilities:
            return damage
        if self.ohko_move():
            return 0
        if current_hp == max_hp and damage >= current_hp:
            return current_hp - 1
        return damage
    def sturdy_ability_defender(self, damage, current_hp, max_hp):
        if "sturdy" not in self.defender.abilities:
            return damage
        if self.ohko_move():
            return 0
        if current_hp == max_hp and damage >= current_hp:
            return current_hp - 1
        return damage

    # Damp: No Pokémon on the field can use explosive moves, and Aftermath won't trigger.
    # Damp affects the whole field, so it's one check instead of attacker/defender versions.
    def damp_on_field(self):
        return "damp" in self.attacker.abilities or "damp" in self.defender.abilities
    def damp_ability(self):
        if self.damp_on_field() and self.explosive_move():
            return 0
        return self.move_power
        # When you add Aftermath, have it check damp_on_field() before dealing its damage.

    # Limber: The Pokémon can't be paralyzed. Returns the status that actually sticks.
    def limber_ability_attacker(self):
        if "limber" not in self.attacker.abilities:
            return self.status_attacker
        if self.status_attacker == STATUS_IMMUNITY_ABILITIES["limber"]:
            return None
        return self.status_attacker
    def limber_ability_defender(self):
        if "limber" not in self.defender.abilities:
            return self.status_defender
        if self.status_defender == STATUS_IMMUNITY_ABILITIES["limber"]:
            return None
        return self.status_defender

    # Sand Veil: In a sandstorm, evasion goes up 25%, so moves aimed at it hit with 80% of their accuracy (1 / 1.25 = 0.8).
    # Returns the move's accuracy against this Pokémon. None means the move never misses.
    # Sand Veil's immunity to sandstorm chip damage is in WEATHER_EFFECTS["sandstorm"]["immune_abilities"].
    def sand_veil_ability_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "sand-veil" not in self.attacker.abilities or self.current_weather() != "sandstorm":
            return accuracy
        return accuracy * 0.8
    def sand_veil_ability_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "sand-veil" not in self.defender.abilities or self.current_weather() != "sandstorm":
            return accuracy
        return accuracy * 0.8

    # Volt Absorb: Electric moves don't affect the Pokémon. Instead they heal 1/4 of its max HP.
    # Returns (move_power, hp_healed). hp_healed is a fraction of max HP.
    def volt_absorb_ability_attacker(self):
        if "volt-absorb" not in self.attacker.abilities or self.move_type != "electric":
            return self.move_power, 0
        return 0, 0.25
    def volt_absorb_ability_defender(self):
        if "volt-absorb" not in self.defender.abilities or self.move_type != "electric":
            return self.move_power, 0
        return 0, 0.25

    # Water Absorb: Water moves don't affect the Pokémon. Instead they heal 1/4 of its max HP.
    # In extreme sun, damaging water moves evaporate before they land, so there's nothing to absorb.
    # Returns (move_power, hp_healed). 
    def water_absorb_ability_attacker(self):
        if "water-absorb" not in self.attacker.abilities or self.move_type != "water":
            return self.move_power, 0
        if self.weather_move_power() == 0:
            return 0, 0
        return 0, 0.25
    def water_absorb_ability_defender(self):
        if "water-absorb" not in self.defender.abilities or self.move_type != "water":
            return self.move_power, 0
        if self.weather_move_power() == 0:
            return 0, 0
        return 0, 0.25

    # Static: needs a contact flag for each move, which the current move data doesn't have. Skipped for now.

    # -------- Items -------- 
    # Items can be held by a Pokémon to boost its stats, change its type, or give it immunity to certain moves. Some items are consumed after one use, while others last until the Pokémon switches out or faints.
    # Will add after finishing abilities 
    def life_orb_item(self):
        pass
    def choice_band_item(self):
        pass