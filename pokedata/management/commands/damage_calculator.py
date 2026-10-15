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
    "echoed-voice", "eerie-spell", "grass-whistle", "growl",
    "heal-bell", "howl", "hyper-voice", "metal-sound", "noble-roar",
    "overdrive", "parting-shot", "perish-song", "psychic-noise", "relic-song",
    "roar", "round", "screech", "sing", "snarl", "snore", "sparkling-aria",
    "supersonic", "torch-song", "uproar",
}

SLICING_MOVES = {
    "aerial-ace", "air-cutter", "air-slash", "aqua-cutter", "behemoth-blade",
    "bitter-blade", "ceaseless-edge", "cross-poison", "cut", "fury-cutter",
    "kowtow-cleave", "leaf-blade", "mighty-cleave", "night-slash", "population-bomb",
    "psyblade", "psycho-cut", "razor-leaf", "razor-shell", "sacred-sword",
    "secret-sword", "slash", "solar-blade", "stone-axe", "tachyon-cutter", "x-scissor",
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
    "bullet-punch", "comet-punch", "dizzy-punch", "double-iron-bash",
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

# Moves that force the target to switch out (Suction Cups stops these).
# Red Card does this too, but it's an item, so it'll go in with the items.
FORCE_SWITCH_MOVES = {
    "circle-throw", "dragon-tail", "roar", "whirlwind",
}

# Moves that take or destroy the target's held item (Sticky Hold stops these).
ITEM_REMOVING_MOVES = {
    "bug-bite", "corrosive-gas", "covet", "incinerate", "knock-off",
    "pluck", "switcheroo", "thief", "trick",
}

# Moves that make contact (Static, Rough Skin, Effect Spore, and Poison Point trigger on these).
CONTACT_MOVES = {
    "accelerock", "acrobatics", "aerial-ace", "anchor-shot", "aqua-jet",
    "aqua-step", "aqua-tail", "arm-thrust", "assurance", "astonish", "avalanche",
    "axe-kick", "behemoth-bash", "behemoth-blade", "bide", "bind", "bite",
    "bitter-blade", "blaze-kick", "body-press", "body-slam", "bolt-beak",
    "bolt-strike", "bounce", "branch-poke", "brave-bird", "breaking-swipe",
    "brick-break", "brutal-swing", "bug-bite", "bullet-punch", "ceaseless-edge",
    "chip-away", "circle-throw", "clamp", "close-combat", "collision-course",
    "comet-punch", "comeuppance", "constrict", "counter", "covet", "crabhammer",
    "cross-chop", "cross-poison", "crunch", "crush-claw", "crush-grip", "cut",
    "darkest-lariat", "dig", "dire-claw", "dive", "dizzy-punch", "double-edge",
    "double-hit", "double-iron-bash", "double-kick", "double-shock", "double-slap",
    "dragon-ascent", "dragon-claw", "dragon-hammer", "dragon-rush", "dragon-tail",
    "drain-punch", "draining-kiss", "drill-peck", "drill-run", "dual-chop",
    "dual-wingbeat", "dynamic-punch", "electro-drift", "endeavor", "extreme-speed",
    "facade", "fake-out", "false-surrender", "false-swipe", "feint-attack",
    "fell-stinger", "fire-fang", "fire-lash", "fire-punch", "first-impression",
    "fishious-rend", "flail", "flame-charge", "flame-wheel", "flare-blitz",
    "flip-turn", "floaty-fall", "fly", "flying-press", "focus-punch", "force-palm",
    "foul-play", "frustration", "fury-attack", "fury-cutter", "fury-swipes",
    "gear-grind", "giga-impact", "glaive-rush", "grass-knot", "grassy-glide",
    "guillotine", "gyro-ball", "hammer-arm", "hard-press", "head-charge",
    "head-smash", "headbutt", "headlong-rush", "heart-stamp", "heat-crash",
    "heavy-slam", "high-horsepower", "high-jump-kick", "hold-back", "horn-attack",
    "horn-drill", "horn-leech", "hyper-drill", "hyper-fang", "ice-ball", "ice-fang",
    "ice-hammer", "ice-punch", "ice-spinner", "infestation", "iron-head",
    "iron-tail", "jaw-lock", "jet-punch", "jump-kick", "karate-chop", "knock-off",
    "kowtow-cleave", "lash-out", "last-resort", "leaf-blade", "leech-life", "lick",
    "liquidation", "low-kick", "low-sweep", "lunge", "mach-punch", "mega-kick",
    "mega-punch", "megahorn", "metal-claw", "meteor-mash", "mighty-cleave",
    "mortal-spin", "multi-attack", "needle-arm", "night-slash", "nuzzle", "outrage",
    "payback", "peck", "petal-dance", "phantom-force", "plasma-fists", "play-rough",
    "pluck", "poison-fang", "poison-jab", "poison-tail", "population-bomb",
    "pounce", "pound", "power-trip", "power-up-punch", "power-whip", "psyblade",
    "psychic-fangs", "psyshield-bash", "punishment", "pursuit", "quick-attack",
    "rage", "rage-fist", "raging-bull", "rapid-spin", "razor-shell", "retaliate",
    "return", "revenge", "reversal", "rock-climb", "rock-smash", "rolling-kick",
    "rollout", "sacred-sword", "scratch", "seismic-toss", "shadow-claw",
    "shadow-force", "shadow-punch", "shadow-sneak", "sizzly-slide", "skitter-smack",
    "skull-bash", "sky-drop", "sky-uppercut", "slam", "slash", "smart-strike",
    "smelling-salts", "snap-trap", "solar-blade", "spark", "spectral-thief",
    "spin-out", "spirit-break", "steamroller", "steel-roller", "steel-wing",
    "stomp", "stomping-tantrum", "stone-axe", "storm-throw", "strength", "struggle",
    "submission", "sucker-punch", "sunsteel-strike", "super-fang", "supercell-slam",
    "superpower", "surging-strikes", "tackle", "tail-slap", "take-down",
    "temper-flare", "thief", "thrash", "throat-chop", "thunder-fang",
    "thunder-punch", "thunderous-kick", "trailblaze", "triple-axel", "triple-dive",
    "triple-kick", "trop-kick", "trump-card", "u-turn", "upper-hand", "v-create",
    "veevee-volley", "vice-grip", "vine-whip", "vital-throw", "volt-tackle",
    "wake-up-slap", "waterfall", "wave-crash", "wicked-blow", "wild-charge",
    "wing-attack", "wood-hammer", "wrap", "wring-out", "x-scissor", "zen-headbutt",
    "zing-zap", "zippy-zap",
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

# Effects that aren't major statuses but some abilities still block. Since Gen 8, Oblivious, Own Tempo, and Inner Focus also block Intimidate.
VOLATILE_IMMUNITY_ABILITIES = {
    "oblivious": {"infatuation", "taunt", "intimidate"},
    "own-tempo": {"confusion", "intimidate"},
    "inner-focus": {"flinch", "intimidate"},
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

# Abilities that stop Intimidate from lowering Attack.
INTIMIDATE_IMMUNITY_ABILITIES = {
    "clear-body", "full-metal-body", "hyper-cutter", "inner-focus",
    "oblivious", "own-tempo", "scrappy", "white-smoke",
}

# Statuses Synchronize passes back to the other Pokémon.
SYNCHRONIZE_STATUSES = {"burn", "paralysis", "poison", "badly-poison"}

# Types that can't get certain statuses.
STATUS_IMMUNE_TYPES = {
    "burn": {"fire"},
    "paralysis": {"electric"},
    "poison": {"poison", "steel"},
    "badly-poison": {"poison", "steel"},
    "freeze": {"ice"},
}

# Abilities Trace can't copy.
TRACE_BANNED_ABILITIES = {
    "as-one-glastrier", "as-one-spectrier", "battle-bond", "comatose", "commander",
    "disguise", "embody-aspect", "flower-gift", "forecast", "hunger-switch",
    "ice-face", "illusion", "imposter", "multitype", "neutralizing-gas",
    "poison-puppeteer", "power-construct", "power-of-alchemy", "protosynthesis",
    "quark-drive", "receiver", "rks-system", "schooling", "shields-down",
    "stance-change", "tera-shell", "tera-shift", "teraform-zero", "trace",
    "zen-mode", "zero-to-hero",
}

# Moves Normalize doesn't change to Normal type.
NORMALIZE_EXCEPTIONS = {
    "hidden-power", "judgment", "multi-attack", "natural-gift", "revelation-dance",
    "struggle", "techno-blast", "terrain-pulse", "weather-ball",
}

# Abilities Mold Breaker ignores.
BREAKABLE_ABILITIES = {
    "armor-tail", "aroma-veil", "aura-break", "battle-armor", "big-pecks", "bulletproof",
    "clear-body", "contrary", "damp", "dazzling", "disguise", "dry-skin",
    "earth-eater", "eelevate", "filter", "flash-fire", "flower-gift", "flower-veil",
    "fluffy", "friend-guard", "fur-coat", "good-as-gold", "grass-pelt", "guard-dog",
    "heatproof", "heavy-metal", "hyper-cutter", "ice-face", "ice-scales", "illuminate",
    "immunity", "inner-focus", "insomnia", "keen-eye", "leaf-guard", "levitate",
    "light-metal", "lightning-rod", "limber", "magic-bounce", "magma-armor", "marvel-scale",
    "minds-eye", "mirror-armor", "motor-drive", "multiscale", "oblivious", "overcoat",
    "own-tempo", "pastel-veil", "punk-rock", "purifying-salt", "queenly-majesty", "sand-veil",
    "sap-sipper", "shell-armor", "shield-dust", "simple", "snow-cloak", "solid-rock",
    "soundproof", "sticky-hold", "storm-drain", "sturdy", "suction-cups", "sweet-veil",
    "tangled-feet", "telepathy", "tera-shell", "thermal-exchange", "thick-fat", "unaware",
    "vital-spirit", "volt-absorb", "water-absorb", "water-bubble", "water-veil", "well-baked-body",
    "white-smoke", "wind-rider", "wonder-guard", "wonder-skin",
}

# Items that still work with Klutz.
KLUTZ_EXCEPTIONS = {
    "macho-brace", "power-anklet", "power-band", "power-belt", "power-bracer", "power-lens", "power-weight",
}


class DamageCalculator:
    # attacker_ability and defender_ability = the ability each Pokémon is using. If it's not given, it uses the Pokémon's first ability.
    def __init__(self, attacker: Species, defender: Species, move_type: str, move_power: int, move_name: str, status_effect_attacker: str, status_effect_defender: str, weather: str = None, terrain: str = None, attacker_ability: str = None, defender_ability: str = None):
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
        self.attacker_abilities = [attacker_ability or self.attacker.abilities[0]]
        self.defender_abilities = [defender_ability or self.defender.abilities[0]]

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
    def force_switch_move(self):
        return self.move_name in FORCE_SWITCH_MOVES
    def contact_move(self):
        return self.move_name in CONTACT_MOVES
    def item_removing_move(self):
        return self.move_name in ITEM_REMOVING_MOVES
    def status_move(self):
        return self.move_data.damage_class == "status"


    # Weather and terrain effects. Weather and terrain can be set by abilities, moves, or items. They can also be blocked by abilities.
    def current_weather(self):
        for abilities in (self.attacker_abilities, self.defender_abilities):
            if "cloud-nine" in abilities or "air-lock" in abilities:
                return None
        return self.weather
    
    def weather_effects(self):
        return WEATHER_EFFECTS.get(self.current_weather(), {})
    
    def terrain_effects(self):
        return TERRAIN_EFFECTS.get(self.terrain, {})

    # A Pokémon is grounded unless it is a Flying type or has Levitate. Terrain only affects grounded Pokémon.
    # Will add Air Balloon, Magnet Rise, and Gravity later once items and field moves are in.
    def grounded_attacker(self):
        return "flying" not in self.attacker.types and "levitate" not in self.attacker_abilities
    def grounded_defender(self):
        return "flying" not in self.defender.types and "levitate" not in self.defender_abilities

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
        for ability in self.attacker_abilities:
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
        for ability in self.defender_abilities:
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
        if self.status_move():
            return 1
        crit_stage = 0
        if self.move_data.meta is not None:
            crit_stage = self.move_data.meta.get("crit_rate") or 0
        crit_stage = min(crit_stage, 3)
        if random.random() < CRIT_CHANCE_BY_STAGE[crit_stage]:
            return 1.5
        return 1

    # Types, abilities, and the field can stop a Pokémon from getting a status.
    # incoming_status = the status a move or ability is trying to give. Returns True if it's blocked.
    def status_immune_attacker(self, incoming_status):
        for t in self.attacker.types:
            if t in STATUS_IMMUNE_TYPES.get(incoming_status, ()):
                return True
        for ability in self.attacker_abilities:
            blocked = STATUS_IMMUNITY_ABILITIES.get(ability)
            if blocked == "all" or blocked == incoming_status:
                return True
            if blocked == "poison" and incoming_status == "badly-poison":
                return True
        return self.field_blocks_status_attacker(incoming_status)
    def status_immune_defender(self, incoming_status):
        for t in self.defender.types:
            if t in STATUS_IMMUNE_TYPES.get(incoming_status, ()):
                return True
        for ability in self.defender_abilities:
            blocked = STATUS_IMMUNITY_ABILITIES.get(ability)
            if blocked == "all" or blocked == incoming_status:
                return True
            if blocked == "poison" and incoming_status == "badly-poison":
                return True
        return self.field_blocks_status_defender(incoming_status)

    # -------- Abilities -------- 

    # Guts boosts the bearer's Attack stat by 50% when it has a major status condition.
    def guts_ability_attacker(self):
        if "guts" not in self.attacker_abilities:
            return self.attacker.stats["attack"]
        if self.status_effects_attacker():
            return self.attacker.stats["attack"] * 1.5
        else:
            return self.attacker.stats["attack"]
    def guts_ability_defender(self):
        if "guts" not in self.defender_abilities:
                return self.defender.stats["attack"]
        if self.status_effects_defender():
            return self.defender.stats["attack"] * 1.5
        else:
            return self.defender.stats["attack"]

    # Toxic boost increases the Pokémon's physical Attack stat by 1.5× when it is poisoned
    def toxic_boost_ability_attacker(self):
        if "toxic-boost" not in self.attacker_abilities:
            return self.attacker.stats["attack"]
        if self.status_attacker == "poison" or self.status_attacker == "badly-poison":
            return self.attacker.stats["attack"] * 1.5
        else:
            return self.attacker.stats["attack"]
    def toxic_boost_ability_defender(self):
        if "toxic-boost" not in self.defender_abilities:
           return self.defender.stats["attack"]
        if self.status_defender == "poison" or self.status_defender == "badly-poison":
            return self.defender.stats["attack"] * 1.5
        else:
            return self.defender.stats["attack"]

    # Flare boost multiplies the user's Special Attack stat by 1.5× when the Pokémon is burned
    def flare_boost_ability_attacker(self):
        if "flare-boost" not in self.attacker_abilities:
            return self.attacker.stats["special-attack"]
        if self.status_attacker == "burn":
            return self.attacker.stats["special-attack"] * 1.5
        else:
            return self.attacker.stats["special-attack"]
    def flare_boost_ability_defender(self):
        if "flare-boost" not in self.defender_abilities:
            return self.defender.stats["special-attack"]
        if self.status_defender == "burn":
            return self.defender.stats["special-attack"] * 1.5
        else:
            return self.defender.stats["special-attack"]

    # Quick feet increases a Pokémon's Speed stat by 50% when it is affected by a major status ailment like poison, burn, paralysis, freeze, or sleep
    def quick_feet_ability_attacker(self):
        if "quick-feet" not in self.attacker_abilities:
            return self.attacker.stats["speed"]
        if self.status_effects_attacker():
            return self.attacker.stats["speed"] * 1.5
        else:
            return self.attacker.stats["speed"]
    def quick_feet_ability_defender(self):
        if "quick-feet" not in self.defender_abilities:
            return self.defender.stats["speed"]
        if self.status_effects_defender():
            return self.defender.stats["speed"] * 1.5
        else:
            return self.defender.stats["speed"]

    # Marvel scale boosts the user's Defense stat by 50% (1.5×) whenever it is afflicted with a major status condition(poison, burn, paralysis, freeze, or sleep).
    def marvel_scale_ability_attacker(self):
        if "marvel-scale" not in self.attacker_abilities:
            return self.attacker.stats["defense"]
        if self.status_effects_attacker():
            return self.attacker.stats["defense"] * 1.5
        else:
            return self.attacker.stats["defense"]
    def marvel_scale_ability_defender(self):
        if "marvel-scale" not in self.defender_abilities:
            return self.defender.stats["defense"]
        if self.status_effects_defender():
            return self.defender.stats["defense"] * 1.5
        else:
            return self.defender.stats["defense"]


    # Pure Power doubles the user's total physical Attack stat in battle.
    def pure_power_ability_attacker(self):
        if "pure-power" not in self.attacker_abilities:
           return self.attacker.stats["attack"]
        return self.attacker.stats["attack"] * 2
    def pure_power_ability_defender(self):
        if "pure-power" not in self.defender_abilities:
           return self.defender.stats["attack"]
        return self.defender.stats["attack"] * 2

    # Rock Head protects a Pokémon from taking recoil damage when using high-power physical attacks
    def rock_head_ability_attacker(self):
        if self.move_data.meta is None:
            return 0
        drain = self.move_data.meta.get("drain", 0)
        if "rock-head" in self.attacker_abilities and drain < 0:
            return 0
        return drain
    def rock_head_ability_defender(self):
        if self.move_data.meta is None:
            return 0
        drain = self.move_data.meta.get("drain", 0)
        if "rock-head" in self.defender_abilities and drain < 0:
            return 0
        return drain
        # Will add more logic to remove special effects of moves like recoil damage, stat changes, and status effects later.

    # Levitate is an ability that gives a Pokémon full immunity to Ground-type moves, Spikes, Toxic Spikes, and the Arena Trap ability.
    # Levitate also means the Pokémon isn't grounded, so terrain doesn't affect it (handled in grounded_attacker / grounded_defender).
    def levitate_ability_attacker(self):
        if "levitate" not in self.attacker_abilities:
            return self.move_power
        if self.move_type == "ground" and not self.status_move():
            return 0
        else:
            return self.move_power
    def levitate_ability_defender(self):
        if "levitate" not in self.defender_abilities:
            return self.move_power
        if self.move_type == "ground" and not self.status_move():
            return 0
        else:
            return self.move_power
        # Will add more logic later for the other effects of levitate like spikes, toxic spikes, and arena trap.

    # Makes the user immune to all direct damaging moves unless they are super-effective
    # Strong winds can turn a super-effective hit into a neutral one, so this uses type_effectiveness.
    def wonder_guard_ability_attacker(self):
        if "wonder-guard" not in self.attacker_abilities or self.status_move():
            return self.move_power
        if self.type_effectiveness_attacker() > 1:
            return self.move_power
        return 0
    def wonder_guard_ability_defender(self):
        if "wonder-guard" not in self.defender_abilities or self.status_move():
            return self.move_power
        if self.type_effectiveness_defender() > 1:
            return self.move_power
        return 0

    # Huge Power is a powerful Pokémon ability that doubles the user's actual Attack stat during battle
    def huge_power_ability_attacker(self):
        if "huge-power" not in self.attacker_abilities:
            return self.attacker.stats["attack"]
        return self.attacker.stats["attack"] * 2
    def huge_power_ability_defender(self):
        if "huge-power" not in self.defender_abilities:
            return self.defender.stats["attack"]
        return self.defender.stats["attack"] * 2
        # Will add more logic around IV and EV later to make it more accurate.

    # Bulletproof: The Pokémon is immune to ball and bomb moves.
    def bulletproof_ability_attacker(self):
        if "bulletproof" not in self.attacker_abilities:
            return self.move_power
        if self.ball_and_bomb_move():
            return 0
        else:
            return self.move_power
    def bulletproof_ability_defender(self):
        if "bulletproof" not in self.defender_abilities:
            return self.move_power
        if self.ball_and_bomb_move():
            return 0
        else:
            return self.move_power

    # Thick Fat: Halves the damage taken from Fire and Ice type moves.
    def thick_fat_ability_attacker(self):
        if "thick-fat" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire" or self.move_type == "ice":
            return self.move_power * 0.5
        else:
            return self.move_power
    def thick_fat_ability_defender(self):
        if "thick-fat" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire" or self.move_type == "ice":
            return self.move_power * 0.5
        else:
            return self.move_power

    # Filter: Reduces the damage taken from super-effective moves to 75%.
    # Strong winds can turn a super-effective hit into a neutral one, so this uses type_effectiveness.
    def filter_ability_attacker(self):
        if "filter" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.type_effectiveness_attacker() > 1:
            return self.move_power * 0.75
        return self.move_power
    def filter_ability_defender(self):
        if "filter" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.type_effectiveness_defender() > 1:
            return self.move_power * 0.75
        return self.move_power

    # Solid Rock: Same as Filter. Reduces the damage taken from super-effective moves to 75%.
    def solid_rock_ability_attacker(self):
        if "solid-rock" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.type_effectiveness_attacker() > 1:
            return self.move_power * 0.75
        return self.move_power
    def solid_rock_ability_defender(self):
        if "solid-rock" not in self.defender_abilities or not self.move_power:
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
        if "stench" not in self.attacker_abilities:
            return move_flinch_chance
        if self.status_move() or move_flinch_chance > 0:
            return move_flinch_chance
        return 0.10
    def stench_ability_defender(self):
        move_flinch_chance = 0
        if self.move_data.meta is not None:
            move_flinch_chance = (self.move_data.meta.get("flinch_chance") or 0) / 100
        if "stench" not in self.defender_abilities:
            return move_flinch_chance
        if self.status_move() or move_flinch_chance > 0:
            return move_flinch_chance
        return 0.10

    # Drizzle: Summons rain for 5 turns when the Pokémon enters battle.
    # It can't replace primal weather (heavy rain, extreme sun, strong winds).
    # Call this when the Pokémon switches in, then use weather_move_power() for the damage change.
    def drizzle_ability_attacker(self):
        if "drizzle" not in self.attacker_abilities:
            return self.weather
        if self.weather == "rain" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "rain"
        self.weather_turns = WEATHER_EFFECTS["rain"]["turns"]
        return self.weather
    def drizzle_ability_defender(self):
        if "drizzle" not in self.defender_abilities:
            return self.weather
        if self.weather == "rain" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "rain"
        self.weather_turns = WEATHER_EFFECTS["rain"]["turns"]
        return self.weather

    # Speed Boost: +1 Speed stage at the end of every turn, up to +6.
    # turns_on_field = how many turns have ended with this Pokémon already out.
    # Don't count the turn it switched in (a lead that started the battle does count turn 1).
    # Each stage is +50% of the base stat: +1 = 1.5x, +2 = 2x, ... +6 = 4x.
    def speed_boost_ability_attacker(self, turns_on_field):
        if "speed-boost" not in self.attacker_abilities:
            return self.attacker.stats["speed"]
        stage = min(turns_on_field, 6)
        return self.attacker.stats["speed"] * (2 + stage) / 2
    def speed_boost_ability_defender(self, turns_on_field):
        if "speed-boost" not in self.defender_abilities:
            return self.defender.stats["speed"]
        stage = min(turns_on_field, 6)
        return self.defender.stats["speed"] * (2 + stage) / 2

    # Battle Armor: Attacks landed on the Pokémon will never be critical hits.
    # Returns the crit multiplier to plug into the damage formula.
    def battle_armor_ability_attacker(self):
        if "battle-armor" not in self.attacker_abilities:
            return self.critical_hit_roll()
        return 1
    def battle_armor_ability_defender(self):
        if "battle-armor" not in self.defender_abilities:
            return self.critical_hit_roll()
        return 1

    # Sturdy: At full HP, survives a hit that would KO it with 1 HP left. Also immune to one-hit KO moves.
    # damage = the final damage you calculated for this hit. Returns the damage actually taken.
    def sturdy_ability_attacker(self, damage, current_hp, max_hp):
        if "sturdy" not in self.attacker_abilities:
            return damage
        if self.ohko_move():
            return 0
        if current_hp == max_hp and damage >= current_hp:
            return current_hp - 1
        return damage
    def sturdy_ability_defender(self, damage, current_hp, max_hp):
        if "sturdy" not in self.defender_abilities:
            return damage
        if self.ohko_move():
            return 0
        if current_hp == max_hp and damage >= current_hp:
            return current_hp - 1
        return damage

    # Damp: No Pokémon on the field can use explosive moves, and Aftermath won't trigger.
    # Damp affects the whole field, so it's one check instead of attacker/defender versions.
    def damp_on_field(self):
        return "damp" in self.attacker_abilities or "damp" in self.defender_abilities
    def damp_ability(self):
        if self.damp_on_field() and self.explosive_move():
            return 0
        return self.move_power

    # Limber: The Pokémon can't be paralyzed. Returns the status that actually sticks.
    def limber_ability_attacker(self):
        if "limber" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker == STATUS_IMMUNITY_ABILITIES["limber"]:
            return None
        return self.status_attacker
    def limber_ability_defender(self):
        if "limber" not in self.defender_abilities:
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
        if "sand-veil" not in self.attacker_abilities or self.current_weather() != "sandstorm":
            return accuracy
        return accuracy * 0.8
    def sand_veil_ability_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "sand-veil" not in self.defender_abilities or self.current_weather() != "sandstorm":
            return accuracy
        return accuracy * 0.8

    # Volt Absorb: Electric moves don't affect the Pokémon. Instead they heal 1/4 of its max HP.
    def volt_absorb_ability_attacker(self):
        if "volt-absorb" not in self.attacker_abilities or self.move_type != "electric":
            return self.move_power, 0
        return 0, 0.25
    def volt_absorb_ability_defender(self):
        if "volt-absorb" not in self.defender_abilities or self.move_type != "electric":
            return self.move_power, 0
        return 0, 0.25

    # Water Absorb: Water moves don't affect the Pokémon. Instead they heal 1/4 of its max HP.
    # In extreme sun, damaging water moves evaporate before they land, so there's nothing to absorb.
    def water_absorb_ability_attacker(self):
        if "water-absorb" not in self.attacker_abilities or self.move_type != "water":
            return self.move_power, 0
        if self.weather_move_power() == 0:
            return 0, 0
        return 0, 0.25
    def water_absorb_ability_defender(self):
        if "water-absorb" not in self.defender_abilities or self.move_type != "water":
            return self.move_power, 0
        if self.weather_move_power() == 0:
            return 0, 0
        return 0, 0.25

    # Static: When the Pokémon is hit by a contact move, the attacker has a 30% chance of getting paralyzed. Returns the status that actually sticks.
    def static_ability_attacker(self):
        if "static" not in self.attacker_abilities or not self.contact_move():
            return self.status_defender
        if self.status_effects_defender() or self.status_immune_defender("paralysis"):
            return self.status_defender
        if random.random() < 0.30:
            return "paralysis"
        return self.status_defender
    def static_ability_defender(self):
        if "static" not in self.defender_abilities or not self.contact_move():
            return self.status_attacker
        if self.status_effects_attacker() or self.status_immune_attacker("paralysis"):
            return self.status_attacker
        if random.random() < 0.30:
            return "paralysis"
        return self.status_attacker

    # Oblivious: The Pokémon can't be infatuated or taunted, and Intimidate doesn't lower its Attack.
    # incoming_effect = the effect a move or ability is trying to give ("infatuation", "taunt", "intimidate"). Returns True if Oblivious blocks it.
    def oblivious_ability_attacker(self, incoming_effect):
        if "oblivious" not in self.attacker_abilities:
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["oblivious"]
    def oblivious_ability_defender(self, incoming_effect):
        if "oblivious" not in self.defender_abilities:
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["oblivious"]


    # Compound Eyes: The Pokémon's moves are 30% more accurate. One-hit KO moves don't get the boost.
    # Returns the move's accuracy when this Pokémon uses it. None means the move never misses.
    # It can go over 100. That's fine, it just means the move always hits. I believe the game uses the value 110 for always hit moves
    def compound_eyes_ability_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "compound-eyes" not in self.attacker_abilities or self.ohko_move():
            return accuracy
        return accuracy * 1.3
    def compound_eyes_ability_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "compound-eyes" not in self.defender_abilities or self.ohko_move():
            return accuracy
        return accuracy * 1.3

    # Insomnia: The Pokémon can't fall asleep. Returns the status that actually sticks.
    # It also makes Rest fail and blocks Yawn's drowsiness. Will add those once Rest and Yawn are in.
    def insomnia_ability_attacker(self):
        if "insomnia" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker == STATUS_IMMUNITY_ABILITIES["insomnia"]:
            return None
        return self.status_attacker
    def insomnia_ability_defender(self):
        if "insomnia" not in self.defender_abilities:
            return self.status_defender
        if self.status_defender == STATUS_IMMUNITY_ABILITIES["insomnia"]:
            return None
        return self.status_defender

    # Color Change: After a damaging move hits the Pokémon, its type changes to that move's type.
    # Nothing happens if the move had no effect, the Pokémon fainted, or it already has that type.
    # Call after the hit lands. Returns the Pokémon's types after the hit.
    # The new type only lasts until it switches out, so don't save it to the database.
    def color_change_ability_attacker(self, current_hp):
        if "color-change" not in self.attacker_abilities:
            return self.attacker.types
        if self.status_move() or current_hp <= 0:
            return self.attacker.types
        if self.type_effectiveness_attacker() == 0 or self.move_type in self.attacker.types:
            return self.attacker.types
        return [self.move_type]
    def color_change_ability_defender(self, current_hp):
        if "color-change" not in self.defender_abilities:
            return self.defender.types
        if self.status_move() or current_hp <= 0:
            return self.defender.types
        if self.type_effectiveness_defender() == 0 or self.move_type in self.defender.types:
            return self.defender.types
        return [self.move_type]

    # Immunity: The Pokémon can't be poisoned or badly poisoned. Returns the status that actually sticks.
    def immunity_ability_attacker(self):
        if "immunity" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker == "poison" or self.status_attacker == "badly-poison":
            return None
        return self.status_attacker
    def immunity_ability_defender(self):
        if "immunity" not in self.defender_abilities:
            return self.status_defender
        if self.status_defender == "poison" or self.status_defender == "badly-poison":
            return None
        return self.status_defender

    # Flash Fire: Fire moves don't affect the Pokémon. Instead they turn on Flash Fire, which makes its own Fire moves do 1.5x dmg until it switches out.
    # Works on Will-O-Wisp too. In heavy rain, damaging Fire moves fail before they land, so nothing turns on.
    def flash_fire_ability_attacker(self):
        if "flash-fire" not in self.attacker_abilities or self.move_type != "fire":
            return self.move_power, False
        if self.move_power and self.weather_move_power() == 0:
            return 0, False
        return 0, True
    def flash_fire_ability_defender(self):
        if "flash-fire" not in self.defender_abilities or self.move_type != "fire":
            return self.move_power, False
        if self.move_power and self.weather_move_power() == 0:
            return 0, False
        return 0, True

    # Flash Fire boost: once Flash Fire is on, the Pokémon's Fire moves do 1.5x dmg.
    # flash_fire_active = the activated value you saved from flash_fire_ability.
    def flash_fire_boost_attacker(self, flash_fire_active):
        if "flash-fire" not in self.attacker_abilities or not flash_fire_active:
            return self.move_power
        if not self.move_power or self.move_type != "fire":
            return self.move_power
        return self.move_power * 1.5
    def flash_fire_boost_defender(self, flash_fire_active):
        if "flash-fire" not in self.defender_abilities or not flash_fire_active:
            return self.move_power
        if not self.move_power or self.move_type != "fire":
            return self.move_power
        return self.move_power * 1.5

    # Shield Dust: Blocks the extra effects of damaging moves used on this Pokémon, like Flamethrower's burn chance or Bite's flinch (Stench's flinch too).
    # It doesn't block the main effect of status moves (Will-O-Wisp still burns) or effects on the user.
    # Returns (ailment_chance, flinch_chance) as decimals, so roll them with: random.random() < chance
    def shield_dust_ability_attacker(self):
        ailment_chance, flinch_chance, _ = self.serene_grace_ability_defender()
        if "shield-dust" not in self.attacker_abilities or self.status_move():
            return ailment_chance, flinch_chance
        return 0, 0
    def shield_dust_ability_defender(self):
        ailment_chance, flinch_chance, _ = self.serene_grace_ability_attacker()
        if "shield-dust" not in self.defender_abilities or self.status_move():
            return ailment_chance, flinch_chance
        return 0, 0

    # Own Tempo: The Pokémon can't be confused, and Intimidate doesn't lower its Attack.
    # incoming_effect = the effect a move or ability is trying to give ("confusion", "intimidate"). 
    def own_tempo_ability_attacker(self, incoming_effect):
        if "own-tempo" not in self.attacker_abilities:
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["own-tempo"]
    def own_tempo_ability_defender(self, incoming_effect):
        if "own-tempo" not in self.defender_abilities:
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["own-tempo"]

    # Suction Cups: The Pokémon can't be forced out by Roar, Whirlwind, Dragon Tail, or Circle Throw.
    # Dragon Tail and Circle Throw still do their dmg, they just don't switch it out.
    # Returns True if the move forces this Pokémon out. Red Card gets blocked too, will add it with the items.
    def suction_cups_ability_attacker(self):
        if not self.force_switch_move():
            return False
        return "suction-cups" not in self.attacker_abilities
    def suction_cups_ability_defender(self):
        if not self.force_switch_move():
            return False
        return "suction-cups" not in self.defender_abilities

    # Intimidate: When the Pokémon enters battle, it lowers the opposing Pokémon's Attack by 1 stage. Returns the opposing Pokémon's Attack stat.
    def intimidate_ability_attacker(self):
        if "intimidate" not in self.attacker_abilities:
            return self.defender.stats["attack"]
        for ability in self.defender_abilities:
            if ability in INTIMIDATE_IMMUNITY_ABILITIES:
                return self.defender.stats["attack"]
        if "guard-dog" in self.defender_abilities:
            return self.defender.stats["attack"] * 1.5
        return self.defender.stats["attack"] * 2 / 3
    def intimidate_ability_defender(self):
        if "intimidate" not in self.defender_abilities:
            return self.attacker.stats["attack"]
        for ability in self.attacker_abilities:
            if ability in INTIMIDATE_IMMUNITY_ABILITIES:
                return self.attacker.stats["attack"]
        if "guard-dog" in self.attacker_abilities:
            return self.attacker.stats["attack"] * 1.5
        return self.attacker.stats["attack"] * 2 / 3

    # Shadow Tag: The opposing Pokémon can't switch out. Returns True if it's trapped.
    def shadow_tag_ability_attacker(self, switched_in_this_turn=False):
        if "shadow-tag" not in self.attacker_abilities or switched_in_this_turn:
            return False
        if "ghost" in self.defender.types or "shadow-tag" in self.defender_abilities:
            return False
        return True
    def shadow_tag_ability_defender(self, switched_in_this_turn=False):
        if "shadow-tag" not in self.defender_abilities or switched_in_this_turn:
            return False
        if "ghost" in self.attacker.types or "shadow-tag" in self.attacker_abilities:
            return False
        return True

    # Rough Skin: When the Pokémon is hit by a contact move, the attacker takes 1/8 of its max HP as dmg.
    def rough_skin_ability_attacker(self):
        if "rough-skin" not in self.attacker_abilities or not self.contact_move():
            return 0
        if "magic-guard" in self.defender_abilities:
            return 0
        return 0.125
    def rough_skin_ability_defender(self):
        if "rough-skin" not in self.defender_abilities or not self.contact_move():
            return 0
        if "magic-guard" in self.attacker_abilities:
            return 0
        return 0.125

    # Effect Spore: When the Pokémon is hit by a contact move, the attacker has a 30% chance of getting poisoned, paralyzed, or put to sleep. Grass types are immune.
    def effect_spore_ability_attacker(self):
        if "effect-spore" not in self.attacker_abilities or not self.contact_move():
            return self.status_defender
        if "grass" in self.defender.types or "overcoat" in self.defender_abilities or self.status_effects_defender():
            return self.status_defender
        roll = random.random()
        if roll < 0.11:
            incoming_status = "sleep"
        elif roll < 0.21:
            incoming_status = "paralysis"
        elif roll < 0.30:
            incoming_status = "poison"
        else:
            return self.status_defender
        if self.status_immune_defender(incoming_status):
            return self.status_defender
        return incoming_status
    def effect_spore_ability_defender(self):
        if "effect-spore" not in self.defender_abilities or not self.contact_move():
            return self.status_attacker
        if "grass" in self.attacker.types or "overcoat" in self.attacker_abilities or self.status_effects_attacker():
            return self.status_attacker
        roll = random.random()
        if roll < 0.11:
            incoming_status = "sleep"
        elif roll < 0.21:
            incoming_status = "paralysis"
        elif roll < 0.30:
            incoming_status = "poison"
        else:
            return self.status_attacker
        if self.status_immune_attacker(incoming_status):
            return self.status_attacker
        return incoming_status

    # Synchronize: If another Pokémon burns, paralyzes, or poisons this Pokémon, that Pokémon gets the same status.
    # incoming_status = the status this Pokémon just got. Returns the status that actually sticks on the other Pokémon.
    def synchronize_ability_attacker(self, incoming_status):
        if "synchronize" not in self.attacker_abilities or incoming_status not in SYNCHRONIZE_STATUSES:
            return self.status_defender
        if self.status_effects_defender() or self.status_immune_defender(incoming_status):
            return self.status_defender
        return incoming_status
    def synchronize_ability_defender(self, incoming_status):
        if "synchronize" not in self.defender_abilities or incoming_status not in SYNCHRONIZE_STATUSES:
            return self.status_attacker
        if self.status_effects_attacker() or self.status_immune_attacker(incoming_status):
            return self.status_attacker
        return incoming_status

    # Clear Body: Other Pokémon's moves and abilities can't lower this Pokémon's stats.
    # stage_change = how many stages the stat is changing. Returns the stage change that actually happens.
    def clear_body_ability_attacker(self, stage_change, from_opponent=True):
        if "clear-body" not in self.attacker_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def clear_body_ability_defender(self, stage_change, from_opponent=True):
        if "clear-body" not in self.defender_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Natural Cure: The Pokémon's status is cured when it switches out.
    def natural_cure_ability_attacker(self):
        if "natural-cure" not in self.attacker_abilities:
            return self.status_attacker
        return None
    def natural_cure_ability_defender(self):
        if "natural-cure" not in self.defender_abilities:
            return self.status_defender
        return None

    # Lightning Rod: Electric moves don't affect the Pokémon. Instead they raise its Sp. Atk by 1 stage.
    def lightning_rod_ability_attacker(self):
        if "lightning-rod" not in self.attacker_abilities or self.move_type != "electric":
            return self.move_power, 0
        return 0, 1
    def lightning_rod_ability_defender(self):
        if "lightning-rod" not in self.defender_abilities or self.move_type != "electric":
            return self.move_power, 0
        return 0, 1

    # Serene Grace: Doubles the chance of a move's extra effects happening.
    # Returns (ailment_chance, flinch_chance, stat_chance) as decimals, so roll them with: random.random() < chance
    def serene_grace_ability_attacker(self):
        ailment_chance = 0
        stat_chance = 0
        if self.move_data.meta is not None:
            ailment_chance = (self.move_data.meta.get("ailment_chance") or 0) / 100
            stat_chance = (self.move_data.meta.get("stat_chance") or 0) / 100
        flinch_chance = self.stench_ability_attacker()
        if "serene-grace" not in self.attacker_abilities or self.status_move():
            return ailment_chance, flinch_chance, stat_chance
        return min(ailment_chance * 2, 1), min(flinch_chance * 2, 1), min(stat_chance * 2, 1)
    def serene_grace_ability_defender(self):
        ailment_chance = 0
        stat_chance = 0
        if self.move_data.meta is not None:
            ailment_chance = (self.move_data.meta.get("ailment_chance") or 0) / 100
            stat_chance = (self.move_data.meta.get("stat_chance") or 0) / 100
        flinch_chance = self.stench_ability_defender()
        if "serene-grace" not in self.defender_abilities or self.status_move():
            return ailment_chance, flinch_chance, stat_chance
        return min(ailment_chance * 2, 1), min(flinch_chance * 2, 1), min(stat_chance * 2, 1)

    # Swift Swim: Doubles the Pokémon's Speed in rain.
    def swift_swim_ability_attacker(self):
        if "swift-swim" not in self.attacker_abilities:
            return self.attacker.stats["speed"]
        if self.current_weather() in ("rain", "heavy-rain"):
            return self.attacker.stats["speed"] * 2
        return self.attacker.stats["speed"]
    def swift_swim_ability_defender(self):
        if "swift-swim" not in self.defender_abilities:
            return self.defender.stats["speed"]
        if self.current_weather() in ("rain", "heavy-rain"):
            return self.defender.stats["speed"] * 2
        return self.defender.stats["speed"]

    # Chlorophyll: Doubles the Pokémon's Speed in harsh sunlight.
    def chlorophyll_ability_attacker(self):
        if "chlorophyll" not in self.attacker_abilities:
            return self.attacker.stats["speed"]
        if self.current_weather() in ("sun", "extreme-sun"):
            return self.attacker.stats["speed"] * 2
        return self.attacker.stats["speed"]
    def chlorophyll_ability_defender(self):
        if "chlorophyll" not in self.defender_abilities:
            return self.defender.stats["speed"]
        if self.current_weather() in ("sun", "extreme-sun"):
            return self.defender.stats["speed"] * 2
        return self.defender.stats["speed"]

    # Illuminate: The Pokémon's moves ignore the target's evasion changes, and its accuracy can't be lowered.
    # Returns the move's accuracy when this Pokémon uses it. None means the move never misses.
    def illuminate_ability_attacker(self, accuracy_stage=0, target_evasion_stage=0):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "illuminate" in self.attacker_abilities:
            target_evasion_stage = 0
        stage = max(-6, min(6, accuracy_stage - target_evasion_stage))
        if stage >= 0:
            return accuracy * (3 + stage) / 3
        return accuracy * 3 / (3 - stage)
    def illuminate_ability_defender(self, accuracy_stage=0, target_evasion_stage=0):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "illuminate" in self.defender_abilities:
            target_evasion_stage = 0
        stage = max(-6, min(6, accuracy_stage - target_evasion_stage))
        if stage >= 0:
            return accuracy * (3 + stage) / 3
        return accuracy * 3 / (3 - stage)

    # Illuminate: Other Pokémon can't lower this Pokémon's accuracy. Returns the stage change that actually happens.
    def illuminate_accuracy_drop_attacker(self, stage_change, from_opponent=True):
        if "illuminate" not in self.attacker_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def illuminate_accuracy_drop_defender(self, stage_change, from_opponent=True):
        if "illuminate" not in self.defender_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Trace: When the Pokémon enters battle, it copies the opposing Pokémon's ability. Returns the Pokémon's abilities after Trace.
    def trace_ability_attacker(self):
        if "trace" not in self.attacker_abilities:
            return self.attacker_abilities
        copied = [ability for ability in self.defender_abilities if ability not in TRACE_BANNED_ABILITIES]
        if not copied:
            return self.attacker_abilities
        return copied
    def trace_ability_defender(self):
        if "trace" not in self.defender_abilities:
            return self.defender_abilities
        copied = [ability for ability in self.attacker_abilities if ability not in TRACE_BANNED_ABILITIES]
        if not copied:
            return self.defender_abilities
        return copied

    # Poison Point: When the Pokémon is hit by a contact move, the attacker has a 30% chance of getting poisoned. Returns the status that actually sticks.
    def poison_point_ability_attacker(self):
        if "poison-point" not in self.attacker_abilities or not self.contact_move():
            return self.status_defender
        if self.status_effects_defender() or self.status_immune_defender("poison"):
            return self.status_defender
        if random.random() < 0.30:
            return "poison"
        return self.status_defender
    def poison_point_ability_defender(self):
        if "poison-point" not in self.defender_abilities or not self.contact_move():
            return self.status_attacker
        if self.status_effects_attacker() or self.status_immune_attacker("poison"):
            return self.status_attacker
        if random.random() < 0.30:
            return "poison"
        return self.status_attacker

    # Inner Focus: The Pokémon can't flinch, and Intimidate doesn't lower its Attack.
    # incoming_effect = the effect a move or ability is trying to give ("flinch", "intimidate"). Returns True if Inner Focus blocks it.
    def inner_focus_ability_attacker(self, incoming_effect):
        if "inner-focus" not in self.attacker_abilities:
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["inner-focus"]
    def inner_focus_ability_defender(self, incoming_effect):
        if "inner-focus" not in self.defender_abilities:
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["inner-focus"]

    # Magma Armor: The Pokémon can't be frozen. Returns the status that actually sticks.
    def magma_armor_ability_attacker(self):
        if "magma-armor" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker == STATUS_IMMUNITY_ABILITIES["magma-armor"]:
            return None
        return self.status_attacker
    def magma_armor_ability_defender(self):
        if "magma-armor" not in self.defender_abilities:
            return self.status_defender
        if self.status_defender == STATUS_IMMUNITY_ABILITIES["magma-armor"]:
            return None
        return self.status_defender

    # Water Veil: The Pokémon can't be burned. Returns the status that actually sticks.
    def water_veil_ability_attacker(self):
        if "water-veil" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker == STATUS_IMMUNITY_ABILITIES["water-veil"]:
            return None
        return self.status_attacker
    def water_veil_ability_defender(self):
        if "water-veil" not in self.defender_abilities:
            return self.status_defender
        if self.status_defender == STATUS_IMMUNITY_ABILITIES["water-veil"]:
            return None
        return self.status_defender

    # Magnet Pull: Opposing Steel types can't switch out. Returns True if it's trapped.
    def magnet_pull_ability_attacker(self, switched_in_this_turn=False):
        if "magnet-pull" not in self.attacker_abilities or switched_in_this_turn:
            return False
        if "steel" not in self.defender.types or "ghost" in self.defender.types:
            return False
        return True
    def magnet_pull_ability_defender(self, switched_in_this_turn=False):
        if "magnet-pull" not in self.defender_abilities or switched_in_this_turn:
            return False
        if "steel" not in self.attacker.types or "ghost" in self.attacker.types:
            return False
        return True

    # Soundproof: The Pokémon is immune to sound-based moves.
    def soundproof_ability_attacker(self):
        if "soundproof" not in self.attacker_abilities:
            return self.move_power
        if self.sound_move():
            return 0
        else:
            return self.move_power
    def soundproof_ability_defender(self):
        if "soundproof" not in self.defender_abilities:
            return self.move_power
        if self.sound_move():
            return 0
        else:
            return self.move_power

    # Rain Dish: Heals 1/16 of the Pokémon's max HP at the end of each turn in rain.
    def rain_dish_ability_attacker(self):
        if "rain-dish" not in self.attacker_abilities:
            return 0
        if self.current_weather() in ("rain", "heavy-rain"):
            return 0.0625
        return 0
    def rain_dish_ability_defender(self):
        if "rain-dish" not in self.defender_abilities:
            return 0
        if self.current_weather() in ("rain", "heavy-rain"):
            return 0.0625
        return 0

    # Sand Stream: Summons a sandstorm for 5 turns when the Pokémon enters battle.
    def sand_stream_ability_attacker(self):
        if "sand-stream" not in self.attacker_abilities:
            return self.weather
        if self.weather == "sandstorm" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "sandstorm"
        self.weather_turns = WEATHER_EFFECTS["sandstorm"]["turns"]
        return self.weather
    def sand_stream_ability_defender(self):
        if "sand-stream" not in self.defender_abilities:
            return self.weather
        if self.weather == "sandstorm" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "sandstorm"
        self.weather_turns = WEATHER_EFFECTS["sandstorm"]["turns"]
        return self.weather

    # Pressure: Moves used against the Pokémon use 1 extra PP. Returns how much PP the move uses.
    def pressure_ability_attacker(self):
        if "pressure" not in self.attacker_abilities:
            return 1
        return 2
    def pressure_ability_defender(self):
        if "pressure" not in self.defender_abilities:
            return 1
        return 2

    # Early Bird: The Pokémon wakes up from sleep twice as fast.
    # sleep_turns = how many turns it would normally sleep. Returns how many turns it actually sleeps.
    def early_bird_ability_attacker(self, sleep_turns):
        if "early-bird" not in self.attacker_abilities:
            return sleep_turns
        return sleep_turns // 2
    def early_bird_ability_defender(self, sleep_turns):
        if "early-bird" not in self.defender_abilities:
            return sleep_turns
        return sleep_turns // 2

    # Flame Body: When the Pokémon is hit by a contact move, the attacker has a 30% chance of getting burned. Returns the status that actually sticks.
    def flame_body_ability_attacker(self):
        if "flame-body" not in self.attacker_abilities or not self.contact_move():
            return self.status_defender
        if self.status_effects_defender() or self.status_immune_defender("burn"):
            return self.status_defender
        if random.random() < 0.30:
            return "burn"
        return self.status_defender
    def flame_body_ability_defender(self):
        if "flame-body" not in self.defender_abilities or not self.contact_move():
            return self.status_attacker
        if self.status_effects_attacker() or self.status_immune_attacker("burn"):
            return self.status_attacker
        if random.random() < 0.30:
            return "burn"
        return self.status_attacker

    # Run Away: The Pokémon can always flee from wild battles, even when it's trapped. Returns True if it can flee.
    def run_away_ability_attacker(self, trapped=False):
        if "run-away" in self.attacker_abilities:
            return True
        return not trapped
    def run_away_ability_defender(self, trapped=False):
        if "run-away" in self.defender_abilities:
            return True
        return not trapped

    # Keen Eye: The Pokémon's moves ignore the target's evasion changes, and its accuracy can't be lowered.
    # Returns the move's accuracy when this Pokémon uses it. None means the move never misses.
    def keen_eye_ability_attacker(self, accuracy_stage=0, target_evasion_stage=0):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "keen-eye" in self.attacker_abilities:
            target_evasion_stage = 0
        stage = max(-6, min(6, accuracy_stage - target_evasion_stage))
        if stage >= 0:
            return accuracy * (3 + stage) / 3
        return accuracy * 3 / (3 - stage)
    def keen_eye_ability_defender(self, accuracy_stage=0, target_evasion_stage=0):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "keen-eye" in self.defender_abilities:
            target_evasion_stage = 0
        stage = max(-6, min(6, accuracy_stage - target_evasion_stage))
        if stage >= 0:
            return accuracy * (3 + stage) / 3
        return accuracy * 3 / (3 - stage)

    # Keen Eye: Other Pokémon can't lower this Pokémon's accuracy. Returns the stage change that actually happens.
    def keen_eye_accuracy_drop_attacker(self, stage_change, from_opponent=True):
        if "keen-eye" not in self.attacker_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def keen_eye_accuracy_drop_defender(self, stage_change, from_opponent=True):
        if "keen-eye" not in self.defender_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Hyper Cutter: Other Pokémon's moves and abilities can't lower this Pokémon's Attack.
    # stat = the stat that's changing. Returns the stage change that actually happens.
    def hyper_cutter_ability_attacker(self, stat, stage_change, from_opponent=True):
        if "hyper-cutter" not in self.attacker_abilities:
            return stage_change
        if stat == "attack" and stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def hyper_cutter_ability_defender(self, stat, stage_change, from_opponent=True):
        if "hyper-cutter" not in self.defender_abilities:
            return stage_change
        if stat == "attack" and stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Pickup: If the Pokémon isn't holding an item, it picks up the item the other Pokémon used up this turn. Returns the item it's holding after.
    def pickup_ability_attacker(self, held_item, used_item):
        if "pickup" not in self.attacker_abilities or held_item:
            return held_item
        return used_item
    def pickup_ability_defender(self, held_item, used_item):
        if "pickup" not in self.defender_abilities or held_item:
            return held_item
        return used_item

    # Truant: The Pokémon can only use a move every other turn.
    # moved_last_turn = True if the Pokémon used a move last turn. Returns True if it can move this turn.
    def truant_ability_attacker(self, moved_last_turn):
        if "truant" not in self.attacker_abilities:
            return True
        return not moved_last_turn
    def truant_ability_defender(self, moved_last_turn):
        if "truant" not in self.defender_abilities:
            return True
        return not moved_last_turn

    # Hustle: Boosts the Pokémon's Attack stat by 50%.
    def hustle_ability_attacker(self):
        if "hustle" not in self.attacker_abilities:
            return self.attacker.stats["attack"]
        return self.attacker.stats["attack"] * 1.5
    def hustle_ability_defender(self):
        if "hustle" not in self.defender_abilities:
            return self.defender.stats["attack"]
        return self.defender.stats["attack"] * 1.5

    # Hustle: The Pokémon's physical moves are 20% less accurate. Returns the move's accuracy when this Pokémon uses it.
    def hustle_accuracy_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "hustle" not in self.attacker_abilities or self.move_data.damage_class != "physical":
            return accuracy
        return accuracy * 0.8
    def hustle_accuracy_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "hustle" not in self.defender_abilities or self.move_data.damage_class != "physical":
            return accuracy
        return accuracy * 0.8

    # Cute Charm: When the Pokémon is hit by a contact move, the attacker has a 30% chance of getting infatuated if they're opposite genders.
    # attacker_gender and defender_gender = "male", "female", or None. Returns True if the other Pokémon gets infatuated.
    def cute_charm_ability_attacker(self, attacker_gender, defender_gender):
        if "cute-charm" not in self.attacker_abilities or not self.contact_move():
            return False
        if attacker_gender is None or defender_gender is None or attacker_gender == defender_gender:
            return False
        if self.oblivious_ability_defender("infatuation"):
            return False
        return random.random() < 0.30
    def cute_charm_ability_defender(self, attacker_gender, defender_gender):
        if "cute-charm" not in self.defender_abilities or not self.contact_move():
            return False
        if attacker_gender is None or defender_gender is None or attacker_gender == defender_gender:
            return False
        if self.oblivious_ability_attacker("infatuation"):
            return False
        return random.random() < 0.30

    # Plus: Boosts the Pokémon's Sp. Atk by 50% if an ally has Plus or Minus. ally_abilities = the ally's abilities.
    def plus_ability_attacker(self, ally_abilities=None):
        if "plus" not in self.attacker_abilities or not ally_abilities:
            return self.attacker.stats["special-attack"]
        if "plus" in ally_abilities or "minus" in ally_abilities:
            return self.attacker.stats["special-attack"] * 1.5
        return self.attacker.stats["special-attack"]
    def plus_ability_defender(self, ally_abilities=None):
        if "plus" not in self.defender_abilities or not ally_abilities:
            return self.defender.stats["special-attack"]
        if "plus" in ally_abilities or "minus" in ally_abilities:
            return self.defender.stats["special-attack"] * 1.5
        return self.defender.stats["special-attack"]

    # Minus: Boosts the Pokémon's Sp. Atk by 50% if an ally has Plus or Minus. ally_abilities = the ally's abilities.
    def minus_ability_attacker(self, ally_abilities=None):
        if "minus" not in self.attacker_abilities or not ally_abilities:
            return self.attacker.stats["special-attack"]
        if "plus" in ally_abilities or "minus" in ally_abilities:
            return self.attacker.stats["special-attack"] * 1.5
        return self.attacker.stats["special-attack"]
    def minus_ability_defender(self, ally_abilities=None):
        if "minus" not in self.defender_abilities or not ally_abilities:
            return self.defender.stats["special-attack"]
        if "plus" in ally_abilities or "minus" in ally_abilities:
            return self.defender.stats["special-attack"] * 1.5
        return self.defender.stats["special-attack"]

    # Forecast: The Pokémon becomes Fire type in sun, Water type in rain, and Ice type in snow. Returns the Pokémon's types.
    def forecast_ability_attacker(self):
        if "forecast" not in self.attacker_abilities:
            return self.attacker.types
        weather = self.current_weather()
        if weather in ("sun", "extreme-sun"):
            return ["fire"]
        if weather in ("rain", "heavy-rain"):
            return ["water"]
        if weather in ("snow", "hail"):
            return ["ice"]
        return ["normal"]
    def forecast_ability_defender(self):
        if "forecast" not in self.defender_abilities:
            return self.defender.types
        weather = self.current_weather()
        if weather in ("sun", "extreme-sun"):
            return ["fire"]
        if weather in ("rain", "heavy-rain"):
            return ["water"]
        if weather in ("snow", "hail"):
            return ["ice"]
        return ["normal"]

    # Sticky Hold: Other Pokémon can't steal or remove the Pokémon's held item. Returns True if the move takes the item.
    def sticky_hold_ability_attacker(self):
        if not self.item_removing_move():
            return False
        return "sticky-hold" not in self.attacker_abilities
    def sticky_hold_ability_defender(self):
        if not self.item_removing_move():
            return False
        return "sticky-hold" not in self.defender_abilities

    # Shed Skin: The Pokémon has a 33% chance of curing its status at the end of each turn.
    def shed_skin_ability_attacker(self):
        if "shed-skin" not in self.attacker_abilities or not self.status_effects_attacker():
            return self.status_attacker
        if random.random() < 0.33:
            return None
        return self.status_attacker
    def shed_skin_ability_defender(self):
        if "shed-skin" not in self.defender_abilities or not self.status_effects_defender():
            return self.status_defender
        if random.random() < 0.33:
            return None
        return self.status_defender

    # Liquid Ooze: Moves that drain HP from this Pokémon hurt the attacker instead of healing it. Returns the move's drain.
    def liquid_ooze_ability_attacker(self):
        if self.move_data.meta is None:
            return 0
        drain = self.move_data.meta.get("drain", 0)
        if "liquid-ooze" in self.attacker_abilities and drain > 0:
            return -drain
        return drain
    def liquid_ooze_ability_defender(self):
        if self.move_data.meta is None:
            return 0
        drain = self.move_data.meta.get("drain", 0)
        if "liquid-ooze" in self.defender_abilities and drain > 0:
            return -drain
        return drain

    # Overgrow: Boosts the power of the Pokémon's Grass-type moves by 50% when its HP is 1/3 or less.
    def overgrow_ability_attacker(self, current_hp, max_hp):
        if "overgrow" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "grass" and current_hp <= max_hp / 3:
            return self.move_power * 1.5
        return self.move_power
    def overgrow_ability_defender(self, current_hp, max_hp):
        if "overgrow" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "grass" and current_hp <= max_hp / 3:
            return self.move_power * 1.5
        return self.move_power

    # Blaze: Boosts the power of the Pokémon's Fire-type moves by 50% when its HP is 1/3 or less.
    def blaze_ability_attacker(self, current_hp, max_hp):
        if "blaze" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire" and current_hp <= max_hp / 3:
            return self.move_power * 1.5
        return self.move_power
    def blaze_ability_defender(self, current_hp, max_hp):
        if "blaze" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire" and current_hp <= max_hp / 3:
            return self.move_power * 1.5
        return self.move_power

    # Torrent: Boosts the power of the Pokémon's Water-type moves by 50% when its HP is 1/3 or less.
    def torrent_ability_attacker(self, current_hp, max_hp):
        if "torrent" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "water" and current_hp <= max_hp / 3:
            return self.move_power * 1.5
        return self.move_power
    def torrent_ability_defender(self, current_hp, max_hp):
        if "torrent" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "water" and current_hp <= max_hp / 3:
            return self.move_power * 1.5
        return self.move_power

    # Swarm: Boosts the power of the Pokémon's Bug-type moves by 50% when its HP is 1/3 or less.
    def swarm_ability_attacker(self, current_hp, max_hp):
        if "swarm" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "bug" and current_hp <= max_hp / 3:
            return self.move_power * 1.5
        return self.move_power
    def swarm_ability_defender(self, current_hp, max_hp):
        if "swarm" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "bug" and current_hp <= max_hp / 3:
            return self.move_power * 1.5
        return self.move_power

    # Drought: Summons harsh sunlight for 5 turns when the Pokémon enters battle.
    def drought_ability_attacker(self):
        if "drought" not in self.attacker_abilities:
            return self.weather
        if self.weather == "sun" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "sun"
        self.weather_turns = WEATHER_EFFECTS["sun"]["turns"]
        return self.weather
    def drought_ability_defender(self):
        if "drought" not in self.defender_abilities:
            return self.weather
        if self.weather == "sun" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "sun"
        self.weather_turns = WEATHER_EFFECTS["sun"]["turns"]
        return self.weather

    # Arena Trap: Opposing Pokémon on the ground can't switch out. Returns True if it's trapped.
    def arena_trap_ability_attacker(self, switched_in_this_turn=False):
        if "arena-trap" not in self.attacker_abilities or switched_in_this_turn:
            return False
        if not self.grounded_defender() or "ghost" in self.defender.types:
            return False
        return True
    def arena_trap_ability_defender(self, switched_in_this_turn=False):
        if "arena-trap" not in self.defender_abilities or switched_in_this_turn:
            return False
        if not self.grounded_attacker() or "ghost" in self.attacker.types:
            return False
        return True

    # Vital Spirit: The Pokémon can't fall asleep.
    def vital_spirit_ability_attacker(self):
        if "vital-spirit" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker == STATUS_IMMUNITY_ABILITIES["vital-spirit"]:
            return None
        return self.status_attacker
    def vital_spirit_ability_defender(self):
        if "vital-spirit" not in self.defender_abilities:
            return self.status_defender
        if self.status_defender == STATUS_IMMUNITY_ABILITIES["vital-spirit"]:
            return None
        return self.status_defender

    # White Smoke: Other Pokémon's moves and abilities can't lower this Pokémon's stats.
    # stage_change = how many stages the stat is changing. Returns the stage change that actually happens.
    def white_smoke_ability_attacker(self, stage_change, from_opponent=True):
        if "white-smoke" not in self.attacker_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def white_smoke_ability_defender(self, stage_change, from_opponent=True):
        if "white-smoke" not in self.defender_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Shell Armor: Attacks landed on the Pokémon will never be critical hits.
    def shell_armor_ability_attacker(self):
        if "shell-armor" not in self.attacker_abilities:
            return self.critical_hit_roll()
        return 1
    def shell_armor_ability_defender(self):
        if "shell-armor" not in self.defender_abilities:
            return self.critical_hit_roll()
        return 1

    # Tangled Feet: Moves aimed at the Pokémon are half as accurate while it's confused.
    def tangled_feet_ability_attacker(self, confused):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "tangled-feet" not in self.attacker_abilities or not confused:
            return accuracy
        return accuracy * 0.5
    def tangled_feet_ability_defender(self, confused):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "tangled-feet" not in self.defender_abilities or not confused:
            return accuracy
        return accuracy * 0.5

    # Motor Drive: Electric-type moves don't affect the Pokémon. Instead they raise its Speed by 1 stage.
    def motor_drive_ability_attacker(self):
        if "motor-drive" not in self.attacker_abilities or self.move_type != "electric":
            return self.move_power, 0
        return 0, 1
    def motor_drive_ability_defender(self):
        if "motor-drive" not in self.defender_abilities or self.move_type != "electric":
            return self.move_power, 0
        return 0, 1

    # Rivalry: The Pokémon's moves do 25% more damage to the same gender and 25% less to the opposite gender.
    def rivalry_ability_attacker(self, attacker_gender, defender_gender):
        if "rivalry" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if attacker_gender is None or defender_gender is None:
            return self.move_power
        if attacker_gender == defender_gender:
            return self.move_power * 1.25
        return self.move_power * 0.75
    def rivalry_ability_defender(self, attacker_gender, defender_gender):
        if "rivalry" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if attacker_gender is None or defender_gender is None:
            return self.move_power
        if attacker_gender == defender_gender:
            return self.move_power * 1.25
        return self.move_power * 0.75

    # Steadfast: The Pokémon's Speed goes up 1 stage when it flinches. Returns the Speed stage change.
    def steadfast_ability_attacker(self, flinched):
        if "steadfast" not in self.attacker_abilities or not flinched:
            return 0
        return 1
    def steadfast_ability_defender(self, flinched):
        if "steadfast" not in self.defender_abilities or not flinched:
            return 0
        return 1

    # Snow Cloak: In snow, evasion goes up 25%, so moves aimed at it hit with 80% of their accuracy.
    def snow_cloak_ability_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "snow-cloak" not in self.attacker_abilities or self.current_weather() not in ("snow", "hail"):
            return accuracy
        return accuracy * 0.8
    def snow_cloak_ability_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "snow-cloak" not in self.defender_abilities or self.current_weather() not in ("snow", "hail"):
            return accuracy
        return accuracy * 0.8

    # Gluttony: The Pokémon eats Berries that work at 1/4 HP when it's at 1/2 HP instead. Returns the HP fraction the Berry works at.
    def gluttony_ability_attacker(self, berry_threshold):
        if "gluttony" not in self.attacker_abilities or berry_threshold != 0.25:
            return berry_threshold
        return 0.5
    def gluttony_ability_defender(self, berry_threshold):
        if "gluttony" not in self.defender_abilities or berry_threshold != 0.25:
            return berry_threshold
        return 0.5

    # Anger Point: When the Pokémon takes a critical hit, its Attack goes up to the max (+6). Returns its Attack stage after the hit.
    def anger_point_ability_attacker(self, attack_stage, critical_hit):
        if "anger-point" not in self.attacker_abilities or not critical_hit:
            return attack_stage
        return 6
    def anger_point_ability_defender(self, attack_stage, critical_hit):
        if "anger-point" not in self.defender_abilities or not critical_hit:
            return attack_stage
        return 6

    # Unburden: Doubles the Pokémon's Speed after its held item is used up or lost.
    def unburden_ability_attacker(self, item_lost):
        if "unburden" not in self.attacker_abilities or not item_lost:
            return self.attacker.stats["speed"]
        return self.attacker.stats["speed"] * 2
    def unburden_ability_defender(self, item_lost):
        if "unburden" not in self.defender_abilities or not item_lost:
            return self.defender.stats["speed"]
        return self.defender.stats["speed"] * 2

    # Heatproof: Halves the damage the Pokémon takes from Fire-type moves.
    def heatproof_ability_attacker(self):
        if "heatproof" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire":
            return self.move_power * 0.5
        return self.move_power
    def heatproof_ability_defender(self):
        if "heatproof" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire":
            return self.move_power * 0.5
        return self.move_power

    # Heatproof: Halves the damage the Pokémon takes from its burn. Returns the burn dmg as a fraction of its max HP.
    def heatproof_burn_damage_attacker(self):
        if self.status_attacker != "burn":
            return 0
        if "heatproof" in self.attacker_abilities:
            return STATUS_EFFECTS["burn"]["self_inflicted_dmg"] / 2
        return STATUS_EFFECTS["burn"]["self_inflicted_dmg"]
    def heatproof_burn_damage_defender(self):
        if self.status_defender != "burn":
            return 0
        if "heatproof" in self.defender_abilities:
            return STATUS_EFFECTS["burn"]["self_inflicted_dmg"] / 2
        return STATUS_EFFECTS["burn"]["self_inflicted_dmg"]

    # Simple: Doubles the Pokémon's stat changes. Returns the stage change that actually happens.
    def simple_ability_attacker(self, stage_change):
        if "simple" not in self.attacker_abilities:
            return stage_change
        return stage_change * 2
    def simple_ability_defender(self, stage_change):
        if "simple" not in self.defender_abilities:
            return stage_change
        return stage_change * 2

    # Dry Skin: Water-type moves heal the Pokémon 1/4 of its max HP instead of hurting it, but Fire-type moves do 25% more damage.
    def dry_skin_ability_attacker(self):
        if "dry-skin" not in self.attacker_abilities:
            return self.move_power, 0
        if self.move_type == "water":
            if self.weather_move_power() == 0:
                return 0, 0
            return 0, 0.25
        if self.move_type == "fire" and self.move_power:
            return self.move_power * 1.25, 0
        return self.move_power, 0
    def dry_skin_ability_defender(self):
        if "dry-skin" not in self.defender_abilities:
            return self.move_power, 0
        if self.move_type == "water":
            if self.weather_move_power() == 0:
                return 0, 0
            return 0, 0.25
        if self.move_type == "fire" and self.move_power:
            return self.move_power * 1.25, 0
        return self.move_power, 0

    # Dry Skin: Heals 1/8 of the Pokémon's max HP each turn in rain, but it loses 1/8 in harsh sunlight. Returns the HP change as a fraction of its max HP.
    def dry_skin_weather_attacker(self):
        if "dry-skin" not in self.attacker_abilities:
            return 0
        if self.current_weather() in ("rain", "heavy-rain"):
            return 0.125
        if self.current_weather() in ("sun", "extreme-sun"):
            return -0.125
        return 0
    def dry_skin_weather_defender(self):
        if "dry-skin" not in self.defender_abilities:
            return 0
        if self.current_weather() in ("rain", "heavy-rain"):
            return 0.125
        if self.current_weather() in ("sun", "extreme-sun"):
            return -0.125
        return 0

    # Download: When the Pokémon enters battle, it raises Sp. Atk if the opponent's Defense is higher, or Attack if its Sp. Def is higher. Returns the stat that goes up 1 stage.
    def download_ability_attacker(self):
        if "download" not in self.attacker_abilities:
            return None
        if self.defender.stats["defense"] >= self.defender.stats["special-defense"]:
            return "special-attack"
        return "attack"
    def download_ability_defender(self):
        if "download" not in self.defender_abilities:
            return None
        if self.attacker.stats["defense"] >= self.attacker.stats["special-defense"]:
            return "special-attack"
        return "attack"

    # Iron Fist: Boosts the power of the Pokémon's punching moves by 20%.
    def iron_fist_ability_attacker(self):
        if "iron-fist" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.punch_move():
            return self.move_power * 1.2
        return self.move_power
    def iron_fist_ability_defender(self):
        if "iron-fist" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.punch_move():
            return self.move_power * 1.2
        return self.move_power

    # Poison Heal: If the Pokémon is poisoned, it heals 1/8 of its max HP each turn instead of losing HP.
    def poison_heal_ability_attacker(self):
        if "poison-heal" not in self.attacker_abilities:
            return 0
        if self.status_attacker == "poison" or self.status_attacker == "badly-poison":
            return 0.125
        return 0
    def poison_heal_ability_defender(self):
        if "poison-heal" not in self.defender_abilities:
            return 0
        if self.status_defender == "poison" or self.status_defender == "badly-poison":
            return 0.125
        return 0

    # Adaptability: The Pokémon's same-type attack bonus (STAB) is 2x instead of 1.5x. Returns the STAB multiplier.
    def adaptability_ability_attacker(self):
        if self.move_type not in self.attacker.types:
            return 1
        if "adaptability" in self.attacker_abilities:
            return 2
        return 1.5
    def adaptability_ability_defender(self):
        if self.move_type not in self.defender.types:
            return 1
        if "adaptability" in self.defender_abilities:
            return 2
        return 1.5

    # Skill Link: The Pokémon's multi-hit moves always hit the max number of times. Returns how many times the move hits.
    def skill_link_ability_attacker(self):
        if self.move_data.meta is None or not self.move_data.meta.get("max_hits"):
            return 1
        min_hits = self.move_data.meta.get("min_hits") or 1
        max_hits = self.move_data.meta["max_hits"]
        if "skill-link" in self.attacker_abilities or min_hits == max_hits:
            return max_hits
        roll = random.random()
        if roll < 0.35:
            return 2
        elif roll < 0.70:
            return 3
        elif roll < 0.85:
            return 4
        return 5
    def skill_link_ability_defender(self):
        if self.move_data.meta is None or not self.move_data.meta.get("max_hits"):
            return 1
        min_hits = self.move_data.meta.get("min_hits") or 1
        max_hits = self.move_data.meta["max_hits"]
        if "skill-link" in self.defender_abilities or min_hits == max_hits:
            return max_hits
        roll = random.random()
        if roll < 0.35:
            return 2
        elif roll < 0.70:
            return 3
        elif roll < 0.85:
            return 4
        return 5

    # Hydration: Cures the Pokémon's status at the end of each turn in rain.
    def hydration_ability_attacker(self):
        if "hydration" not in self.attacker_abilities:
            return self.status_attacker
        if self.current_weather() in ("rain", "heavy-rain"):
            return None
        return self.status_attacker
    def hydration_ability_defender(self):
        if "hydration" not in self.defender_abilities:
            return self.status_defender
        if self.current_weather() in ("rain", "heavy-rain"):
            return None
        return self.status_defender

    # Solar Power: Boosts the Pokémon's Sp. Atk by 50% in harsh sunlight.
    def solar_power_ability_attacker(self):
        if "solar-power" not in self.attacker_abilities:
            return self.attacker.stats["special-attack"]
        if self.current_weather() in ("sun", "extreme-sun"):
            return self.attacker.stats["special-attack"] * 1.5
        return self.attacker.stats["special-attack"]
    def solar_power_ability_defender(self):
        if "solar-power" not in self.defender_abilities:
            return self.defender.stats["special-attack"]
        if self.current_weather() in ("sun", "extreme-sun"):
            return self.defender.stats["special-attack"] * 1.5
        return self.defender.stats["special-attack"]

    # Solar Power: The Pokémon loses 1/8 of its max HP each turn in harsh sunlight.
    def solar_power_damage_attacker(self):
        if "solar-power" not in self.attacker_abilities:
            return 0
        if self.current_weather() in ("sun", "extreme-sun"):
            return 0.125
        return 0
    def solar_power_damage_defender(self):
        if "solar-power" not in self.defender_abilities:
            return 0
        if self.current_weather() in ("sun", "extreme-sun"):
            return 0.125
        return 0

    # Normalize: All of the Pokémon's moves become Normal type and do 20% more damage. Returns the move's type and power.
    def normalize_ability_attacker(self):
        if "normalize" not in self.attacker_abilities or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "normal", self.move_power
        return "normal", self.move_power * 1.2
    def normalize_ability_defender(self):
        if "normalize" not in self.defender_abilities or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "normal", self.move_power
        return "normal", self.move_power * 1.2

    # Sniper: The Pokémon's critical hits do 2.25x damage instead of 1.5x. Returns the crit multiplier.
    def sniper_ability_attacker(self, critical_hit):
        if not critical_hit:
            return 1
        if "sniper" in self.attacker_abilities:
            return 2.25
        return 1.5
    def sniper_ability_defender(self, critical_hit):
        if not critical_hit:
            return 1
        if "sniper" in self.defender_abilities:
            return 2.25
        return 1.5

    # Magic Guard: The Pokémon only takes damage from attacks. Returns the indirect damage it actually takes.
    # indirect_damage = dmg from weather, status, recoil, Life Orb, etc.
    def magic_guard_ability_attacker(self, indirect_damage):
        if "magic-guard" not in self.attacker_abilities:
            return indirect_damage
        return 0
    def magic_guard_ability_defender(self, indirect_damage):
        if "magic-guard" not in self.defender_abilities:
            return indirect_damage
        return 0

    # No Guard: Moves used by or against the Pokémon always hit. Returns the move's accuracy. None means the move never misses.
    # No Guard works both ways, so it's one check instead of attacker/defender versions.
    def no_guard_on_field(self):
        return "no-guard" in self.attacker_abilities or "no-guard" in self.defender_abilities
    def no_guard_ability(self):
        if self.no_guard_on_field():
            return None
        return self.move_data.accuracy

    # Stall: The Pokémon always moves last among moves with the same priority. Returns the move's priority.
    def stall_ability_attacker(self):
        if "stall" not in self.attacker_abilities:
            return self.move_data.priority
        return self.move_data.priority - 0.1
    def stall_ability_defender(self):
        if "stall" not in self.defender_abilities:
            return self.move_data.priority
        return self.move_data.priority - 0.1

    # Technician: Boosts the power of the Pokémon's moves with 60 power or less by 50%.
    def technician_ability_attacker(self):
        if "technician" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_power <= 60:
            return self.move_power * 1.5
        return self.move_power
    def technician_ability_defender(self):
        if "technician" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_power <= 60:
            return self.move_power * 1.5
        return self.move_power

    # Leaf Guard: The Pokémon can't get a status condition in harsh sunlight.
    def leaf_guard_ability_attacker(self):
        if "leaf-guard" not in self.attacker_abilities:
            return self.status_attacker
        if self.current_weather() in ("sun", "extreme-sun"):
            return None
        return self.status_attacker
    def leaf_guard_ability_defender(self):
        if "leaf-guard" not in self.defender_abilities:
            return self.status_defender
        if self.current_weather() in ("sun", "extreme-sun"):
            return None
        return self.status_defender

    # Klutz: The Pokémon can't use its held item. Returns the item that still works.
    def klutz_ability_attacker(self, held_item):
        if "klutz" not in self.attacker_abilities or held_item in KLUTZ_EXCEPTIONS:
            return held_item
        return None
    def klutz_ability_defender(self, held_item):
        if "klutz" not in self.defender_abilities or held_item in KLUTZ_EXCEPTIONS:
            return held_item
        return None

    # Mold Breaker: The Pokémon's moves ignore abilities that would block or weaken them. Returns the target's abilities that still work.
    def mold_breaker_ability_attacker(self):
        if "mold-breaker" not in self.attacker_abilities:
            return self.defender_abilities
        return [ability for ability in self.defender_abilities if ability not in BREAKABLE_ABILITIES]
    def mold_breaker_ability_defender(self):
        if "mold-breaker" not in self.defender_abilities:
            return self.attacker_abilities
        return [ability for ability in self.attacker_abilities if ability not in BREAKABLE_ABILITIES]

    # Super Luck: Raises the Pokémon's critical hit ratio by 1 stage. Returns the move's crit stage.
    def super_luck_ability_attacker(self):
        crit_stage = 0
        if self.move_data.meta is not None:
            crit_stage = self.move_data.meta.get("crit_rate") or 0
        if "super-luck" in self.attacker_abilities:
            crit_stage += 1
        return min(crit_stage, 3)
    def super_luck_ability_defender(self):
        crit_stage = 0
        if self.move_data.meta is not None:
            crit_stage = self.move_data.meta.get("crit_rate") or 0
        if "super-luck" in self.defender_abilities:
            crit_stage += 1
        return min(crit_stage, 3)

    # Aftermath: If the Pokémon is knocked out by a contact move, the attacker takes 1/4 of its max HP as dmg.
    def aftermath_ability_attacker(self, fainted):
        if "aftermath" not in self.attacker_abilities or not fainted or not self.contact_move():
            return 0
        if self.damp_on_field() or "magic-guard" in self.defender_abilities:
            return 0
        return 0.25
    def aftermath_ability_defender(self, fainted):
        if "aftermath" not in self.defender_abilities or not fainted or not self.contact_move():
            return 0
        if self.damp_on_field() or "magic-guard" in self.attacker_abilities:
            return 0
        return 0.25

    # Anticipation: The Pokémon shudders if the opponent has a super-effective or one-hit KO move. Returns True if it shudders.
    def anticipation_ability_attacker(self):
        if "anticipation" not in self.attacker_abilities or self.status_move():
            return False
        return self.type_effectiveness_attacker() > 1 or self.ohko_move()
    def anticipation_ability_defender(self):
        if "anticipation" not in self.defender_abilities or self.status_move():
            return False
        return self.type_effectiveness_defender() > 1 or self.ohko_move()
        # Will check the opponent's whole moveset later. Right now it only checks the move being used.

    # Forewarn: When the Pokémon enters battle, it reveals the opponent's strongest move. Returns that move's name.
    # opponent_moves = the names of the opponent's moves.
    def forewarn_ability_attacker(self, opponent_moves):
        if "forewarn" not in self.attacker_abilities or not opponent_moves:
            return None
        strongest = max(opponent_moves, key=self.forewarn_move_power)
        if self.forewarn_move_power(strongest) == 0:
            return None
        return strongest
    def forewarn_ability_defender(self, opponent_moves):
        if "forewarn" not in self.defender_abilities or not opponent_moves:
            return None
        strongest = max(opponent_moves, key=self.forewarn_move_power)
        if self.forewarn_move_power(strongest) == 0:
            return None
        return strongest

    # The power Forewarn uses to compare moves.
    def forewarn_move_power(self, move_name):
        if move_name in OHKO_MOVES:
            return 150
        if move_name in ("counter", "mirror-coat", "metal-burst"):
            return 120
        move = Moves.objects.get(name=move_name)
        if move.damage_class == "status":
            return 0
        return move.power or 80

    # Unaware: The Pokémon ignores the opponent's stat changes. Returns the opponent's stat stage that counts.
    def unaware_ability_attacker(self, opponent_stage):
        if "unaware" not in self.attacker_abilities:
            return opponent_stage
        return 0
    def unaware_ability_defender(self, opponent_stage):
        if "unaware" not in self.defender_abilities:
            return opponent_stage
        return 0

    # Tinted Lens: The Pokémon's not very effective moves do double damage.
    def tinted_lens_ability_attacker(self):
        if "tinted-lens" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if 0 < self.type_effectiveness_defender() < 1:
            return self.move_power * 2
        return self.move_power
    def tinted_lens_ability_defender(self):
        if "tinted-lens" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if 0 < self.type_effectiveness_attacker() < 1:
            return self.move_power * 2
        return self.move_power

    # Slow Start: The Pokémon's Attack and Speed are halved for its first 5 turns in battle. Returns its Attack and Speed.
    def slow_start_ability_attacker(self, turns_on_field):
        attack = self.attacker.stats["attack"]
        speed = self.attacker.stats["speed"]
        if "slow-start" not in self.attacker_abilities or turns_on_field >= 5:
            return attack, speed
        return attack * 0.5, speed * 0.5
    def slow_start_ability_defender(self, turns_on_field):
        attack = self.defender.stats["attack"]
        speed = self.defender.stats["speed"]
        if "slow-start" not in self.defender_abilities or turns_on_field >= 5:
            return attack, speed
        return attack * 0.5, speed * 0.5

    # -------- Items -------- 
    # Items can be held by a Pokémon to boost its stats, change its type, or give it immunity to certain moves. Some items are consumed after one use, while others last until the Pokémon switches out or faints.
    # Will add after finishing abilities 
    def life_orb_item(self):
        pass
    def choice_band_item(self):
        pass