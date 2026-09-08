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


class DamageCalculator:
    def __init__(self, attacker: Species, defender: Species, move_type: str, move_power: int): 
        self.attacker = attacker
        self.defender = defender
        self.move_type = move_type
        self.move_power = move_power
        self.attacker_learnset = Learnset.objects.get(species_id=self.attacker.pokedex_id)

    def sound_move(self): 
        pass
    def cut_move(self):
        pass
    def levitate_ability(self):
        pass
    def wonder_guard_ability(self):
        "wonder-guard" in self.defender.abilities
        pass
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

        