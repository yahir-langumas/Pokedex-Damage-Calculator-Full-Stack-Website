# DMG Calculator 
# Need a class for spefic move types like sounds, cut .... ect
# Need a class for specific abilities that have special effects like levitate, wonder guard ...  etc
# Need a class for specific damage booster abilities like huge power ..... ect
# Need a class for specific damage reducer abilities like thick fat, filter, solid rock ...  ect
# Need a class for specific damage booster items like life orb, choice band, choice specs, choice scarf ...  ect
# Need a class for specific damage reducer items like assault vest, safety goggles, ...  ect
# Need a class for specific weather effects like sun, rain, sandstorm, hail ...  ect
# Need a class for specific terrain effects like electric terrain, grassy terrain, psychic terrain ...  ect
# Need a class for specific field effects like trick room, magic room, wonder room ...  ect (Not to necessary for DMG but nice to have)
# Need a class for specific status effects like burn, paralysis, poison, sleep, freeze ...  ect
# Need a class for specific stat changes like attack, defense, special attack, special defense, speed ... ect
from pokedata.models import Species
from pokedata.models import Moves
from pokedata.models import Learnset
from pokedata.models import Type

# hard coding moves that have special effects like sound moves, cut moves, and other moves that have special effects.

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

class DamageCalculator:
    def __init__(self, attacker: Species, defender: Species, move_type: str, move_power: int):
        self.attacker = attacker
        self.defender = defender
        self.move_type = move_type
        self.move_power = move_power
        self.attacker_learnset = Learnset.objects.get(species_id=self.attacker.pokedex_id)
        self.defender_learnset = Learnset.objects.get(species_id=self.defender.pokedex_id)
        self.defender_types_data = [Type.objects.get(name=t).type_data for t in self.defender.types]

    def sound_move(self): 
        return self.move_type in SOUND_MOVES
    def cut_move(self):
        return self.move_type in SLICING_MOVES
    def claw_move(self):
        return self.move_type in CLAW_MOVES
    def bite_move(self):
        return self.move_type in BITING_MOVES
    def punch_move(self):
        return self.move_type in PUNCHING_MOVES
    def pulse_move(self):
        return self.move_type in PULSE_MOVES
    def wind_move(self):
        return self.move_type in WIND_MOVES
    def ball_and_bomb_move(self):
        return self.move_type in BALL_AND_BOMB_MOVES
    def powder_and_spore_move(self):
        return self.move_type in POWDER_AND_SPORE_MOVES
    
    def levitate_ability(self):
        if "levitate" not in self.defender.abilities: 
            return self.move_power 
        if self.move_type  == "ground": 
            return self.move_power * 0 
        else: 
            return self.move_power

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
       
    def huge_power_ability(self):
        pass
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

        