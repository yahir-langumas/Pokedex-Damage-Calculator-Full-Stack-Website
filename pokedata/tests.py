from django.test import TestCase
from pokedata.models import Species, Moves
from pokedata.damage_calculator import DamageCalculator
from pokedata.stats import calculate_stats, make_build

# Builds a DamageCalculator from Pokémon and move names.
def make_calc(attacker, defender, move, attacker_ability=None, defender_ability=None, attacker_item=None, defender_item=None, weather=None, attacker_build=None, defender_build=None):
    move_data = Moves.objects.get(name=move)
    return DamageCalculator(Species.objects.get(name=attacker), Species.objects.get(name=defender), move_data.type, move_data.power, move_data.name, None, None, weather, None, attacker_ability, defender_ability, attacker_item, defender_item, attacker_build, defender_build)
 
 
class TypeAndWeatherTests(TestCase):
    fixtures = ["pokedata"]
 
    # Fire is super effective on Grass.
    def test_super_effective(self):
        self.assertEqual(make_calc("charizard", "venusaur", "flamethrower").type_effectiveness_defender(), 2)
 
    # Normal moves can't hit Ghost types.
    def test_immune(self):
        self.assertEqual(make_calc("snorlax", "gengar", "tackle").type_effectiveness_defender(), 0)
 
    # Rain boosts Water moves by 50%.
    def test_rain_boosts_water(self):
        self.assertEqual(make_calc("blastoise", "snorlax", "surf", weather="rain").weather_move_power(), 135)
 
 
class AbilityTests(TestCase):
    fixtures = ["pokedata"]
 
    # Levitate makes Ground moves miss.
    def test_levitate(self):
        self.assertEqual(make_calc("garchomp", "rotom", "earthquake", defender_ability="levitate").levitate_ability_defender(), 0)
 
    # Mold Breaker ignores Levitate.
    def test_mold_breaker_ignores_levitate(self):
        self.assertEqual(make_calc("excadrill", "rotom", "earthquake", "mold-breaker", "levitate").mold_breaker_ability_attacker(), [])
 
    # Huge Power doubles Attack.
    def test_huge_power(self):
        calc = make_calc("azumarill", "snorlax", "aqua-tail", attacker_ability="huge-power")
        self.assertEqual(calc.huge_power_ability_attacker(), calc.attacker_stats["attack"] * 2)
 
    # Thick Fat halves Fire damage.
    def test_thick_fat(self):
        self.assertEqual(make_calc("charizard", "snorlax", "flamethrower", defender_ability="thick-fat").thick_fat_ability_defender(), 45)
 
    # Technician boosts moves with 60 power or less.
    def test_technician(self):
        self.assertEqual(make_calc("scizor", "snorlax", "bullet-punch", attacker_ability="technician").technician_ability_attacker(), 60)
        
class ItemTests(TestCase):
    fixtures = ["pokedata"]
 
    # Oran Berry heals 10 HP at half HP or less.
    def test_oran_berry(self):
        self.assertEqual(make_calc("snorlax", "machamp", "tackle", attacker_item="oran-berry").oran_berry_item_attacker(40, 100), 10)
 
    # Klutz stops the Pokémon from using its item.
    def test_klutz(self):
        self.assertIsNone(make_calc("lopunny", "machamp", "tackle", attacker_ability="klutz", attacker_item="oran-berry").held_item_attacker())
 
    # Unnerve stops the other Pokémon from eating Berries.
    def test_unnerve(self):
        self.assertIsNone(make_calc("snorlax", "mewtwo", "tackle", defender_ability="unnerve", attacker_item="oran-berry").held_berry_attacker())