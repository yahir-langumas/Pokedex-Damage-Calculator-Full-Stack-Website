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

    
class StatTests(TestCase):
    fixtures = ["pokedata"]
 
    # With no build, a Pokémon is level 50 with 0 EVs, 31 IVs and a neutral nature.
    def test_default_build(self):
        machamp = Species.objects.get(name="machamp")
        self.assertEqual(calculate_stats(machamp.stats), {"hp": 165, "attack": 150, "defense": 100, "special-attack": 85, "special-defense": 105, "speed": 75})
 
    # 4 HP / 252 Atk / 252 Spe Jolly Garchomp. Matches Smogon's calc.
    def test_evs_and_nature(self):
        garchomp = Species.objects.get(name="garchomp")
        stats = calculate_stats(garchomp.stats, {"evs": {"hp": 4, "attack": 252, "speed": 252}, "nature": "jolly"})
        self.assertEqual((stats["hp"], stats["attack"], stats["special-attack"], stats["speed"]), (184, 182, 90, 169))
 
    # Lower levels mean lower stats.
    def test_level(self):
        garchomp = Species.objects.get(name="garchomp")
        self.assertEqual(calculate_stats(garchomp.stats, {"level": 1})["hp"], 13)
 
    # Shedinja always has 1 HP.
    def test_shedinja(self):
        shedinja = Species.objects.get(name="shedinja")
        self.assertEqual(calculate_stats(shedinja.stats, pokedex_id=shedinja.pokedex_id)["hp"], 1)
 
    # Levels over 50, more than 510 EVs and IVs over 31 aren't allowed.
    def test_bad_builds(self):
        for build in ({"level": 51}, {"evs": {"attack": 252, "speed": 252, "hp": 8}}, {"ivs": {"speed": 32}}):
            with self.assertRaises(ValueError):
                make_build(build)
 
    # The calculator uses real stats, so Choice Band boosts Machamp's level 50 Attack (150).
    def test_calculator_uses_real_stats(self):
        self.assertEqual(make_calc("machamp", "snorlax", "close-combat", attacker_item="choice-band").choice_band_item_attacker(), 225)

# Tests for the calc's helper functions: Speed, Protosynthesis/Quark Drive, weight, battle forms, ignored abilities and move type.
class SpeedTests(TestCase):
    fixtures = ["pokedata"]

    # A level 50 Garchomp with 0 Speed EVs has 122 Speed.
    def test_base_speed(self):
        self.assertEqual(make_calc("garchomp", "snorlax", "earthquake").final_speed_attacker(), 122)

    # +1 Speed is 1.5x.
    def test_speed_stage(self):
        self.assertEqual(make_calc("garchomp", "snorlax", "earthquake").final_speed_attacker({"speed": 1}), 183)

    # Choice Scarf is 1.5x and Iron Ball is 0.5x.
    def test_speed_items(self):
        self.assertEqual(make_calc("garchomp", "snorlax", "earthquake", attacker_item="choice-scarf").final_speed_attacker(), 183)
        self.assertEqual(make_calc("garchomp", "snorlax", "earthquake", attacker_item="iron-ball").final_speed_attacker(), 61)

    # Paralysis halves Speed, unless the Pokémon has Quick Feet (which boosts it 1.5x instead).
    def test_paralysis(self):
        species = Species.objects.get(name="garchomp")
        paralyzed = DamageCalculator(species, Species.objects.get(name="snorlax"), "ground", 100, "earthquake", "paralysis", None)
        quick_feet = DamageCalculator(species, Species.objects.get(name="snorlax"), "ground", 100, "earthquake", "paralysis", None, attacker_ability="quick-feet")
        self.assertEqual(paralyzed.final_speed_attacker(), 61)
        self.assertEqual(quick_feet.final_speed_attacker(), 183)

    # Swift Swim doubles Speed in rain.
    def test_swift_swim(self):
        self.assertEqual(make_calc("kingdra", "snorlax", "surf", attacker_ability="swift-swim", weather="rain").final_speed_attacker(), 210)

    # The defender version: Chlorophyll doubles Speed in sun.
    def test_defender_speed(self):
        self.assertEqual(make_calc("snorlax", "venusaur", "tackle", defender_ability="chlorophyll", weather="sun").final_speed_defender(), 200)

    # Quark Drive with Booster Energy boosts Iron Bundle's Speed (its highest stat) by 1.5x.
    def test_quark_drive_speed(self):
        self.assertEqual(make_calc("iron-bundle", "snorlax", "hydro-pump", attacker_ability="quark-drive", attacker_item="booster-energy").final_speed_attacker(), 234)


class ParadoxStatTests(TestCase):
    fixtures = ["pokedata"]

    # Without Protosynthesis or Quark Drive, nothing gets boosted.
    def test_not_active(self):
        self.assertIsNone(make_calc("garchomp", "snorlax", "earthquake").paradox_boosted_stat_attacker())

    # Quark Drive only works with Booster Energy or Electric Terrain.
    def test_needs_booster_or_terrain(self):
        self.assertIsNone(make_calc("iron-bundle", "snorlax", "hydro-pump", attacker_ability="quark-drive").paradox_boosted_stat_attacker())

    # Iron Bundle's highest stat is Speed.
    def test_highest_stat(self):
        self.assertEqual(make_calc("iron-bundle", "snorlax", "hydro-pump", attacker_ability="quark-drive", attacker_item="booster-energy").paradox_boosted_stat_attacker(), "speed")

    # Stat stages count, so +2 Sp. Atk makes Sp. Atk the highest instead.
    def test_stat_stages_count(self):
        calc = make_calc("iron-bundle", "snorlax", "hydro-pump", attacker_ability="quark-drive", attacker_item="booster-energy")
        self.assertEqual(calc.paradox_boosted_stat_attacker({"special-attack": 2}), "special-attack")

    # Great Tusk's Attack and Defense tie, and Attack wins ties.
    def test_ties_go_to_attack(self):
        self.assertEqual(make_calc("great-tusk", "snorlax", "headlong-rush", attacker_ability="protosynthesis", weather="sun").paradox_boosted_stat_attacker(), "attack")

    # The defender version.
    def test_defender(self):
        self.assertEqual(make_calc("snorlax", "iron-bundle", "tackle", defender_ability="quark-drive", defender_item="booster-energy").paradox_boosted_stat_defender(), "speed")


class WeightTests(TestCase):
    fixtures = ["pokedata"]

    # Weight is in hectograms. Snorlax is 460 kg.
    def test_base_weight(self):
        self.assertEqual(make_calc("snorlax", "machamp", "heavy-slam").final_weight_attacker(), 4600)

    # Heavy Metal doubles weight, Light Metal and Float Stone halve it.
    def test_weight_changes(self):
        self.assertEqual(make_calc("snorlax", "machamp", "heavy-slam", attacker_ability="heavy-metal").final_weight_attacker(), 9200)
        self.assertEqual(make_calc("snorlax", "machamp", "heavy-slam", attacker_ability="light-metal").final_weight_attacker(), 2300)
        self.assertEqual(make_calc("snorlax", "machamp", "heavy-slam", attacker_item="float-stone").final_weight_attacker(), 2300)

    # Light Metal and Float Stone together quarter it.
    def test_light_metal_and_float_stone(self):
        self.assertEqual(make_calc("snorlax", "machamp", "heavy-slam", attacker_ability="light-metal", attacker_item="float-stone").final_weight_attacker(), 1150)

    # The defender version.
    def test_defender_weight(self):
        self.assertEqual(make_calc("machamp", "snorlax", "low-kick", defender_ability="heavy-metal").final_weight_defender(), 9200)


class BattleFormTests(TestCase):
    fixtures = ["pokedata"]

    # change_form swaps in the new form and recalculates its stats, without changing the Pokémon from the database.
    def test_change_form(self):
        calc = make_calc("groudon", "snorlax", "earthquake")
        original = calc.attacker
        primal_stats = {"hp": 100, "attack": 180, "defense": 160, "special-attack": 150, "special-defense": 90, "speed": 90}
        calc.change_form("attacker", "groudon-primal", ["ground", "fire"], primal_stats, "desolate-land")
        self.assertEqual((calc.attacker.name, calc.attacker.types, calc.attacker_abilities), ("groudon-primal", ["ground", "fire"], ["desolate-land"]))
        self.assertEqual(calc.attacker_stats["attack"], 200)
        self.assertEqual(original.name, "groudon")

    # Red Orb turns Groudon into Primal Groudon.
    def test_red_orb(self):
        calc = make_calc("groudon", "snorlax", "earthquake", attacker_item="red-orb")
        calc.use_battle_forms()
        self.assertEqual((calc.attacker.name, calc.attacker.types, calc.attacker_abilities), ("groudon-primal", ["ground", "fire"], ["desolate-land"]))

    # Blue Orb turns a defending Kyogre into Primal Kyogre.
    def test_blue_orb_defender(self):
        calc = make_calc("snorlax", "kyogre", "tackle", defender_item="blue-orb")
        calc.use_battle_forms()
        self.assertEqual((calc.defender.name, calc.defender_abilities), ("kyogre-primal", ["primordial-sea"]))

    # Aegislash goes into Blade Forme to attack, but King's Shield keeps it in Shield Forme.
    def test_stance_change(self):
        attacking = make_calc("aegislash-shield", "machamp", "shadow-ball")
        attacking.use_battle_forms()
        self.assertEqual(attacking.attacker.name, "aegislash-blade")
        self.assertEqual(attacking.attacker_stats["attack"], 160)
        shielding = make_calc("aegislash-shield", "machamp", "kings-shield")
        shielding.use_battle_forms()
        self.assertEqual(shielding.attacker.name, "aegislash-shield")

    # Castform turns Water type in rain.
    def test_castform(self):
        calc = make_calc("castform", "snorlax", "weather-ball", weather="rain")
        calc.use_battle_forms()
        self.assertEqual((calc.attacker.name, calc.attacker.types), ("castform-rainy", ["water"]))

    # Arceus turns Fire type with a Flame Plate.
    def test_arceus(self):
        calc = make_calc("arceus", "snorlax", "judgment", attacker_item="flame-plate")
        calc.use_battle_forms()
        self.assertEqual((calc.attacker.name, calc.attacker.types), ("arceus-fire", ["fire"]))

    # Ogerpon's Wellspring Mask makes it Grass/Water with Water Absorb.
    def test_ogerpon(self):
        calc = make_calc("ogerpon", "snorlax", "ivy-cudgel", attacker_item="wellspring-mask")
        calc.use_battle_forms()
        self.assertEqual((calc.attacker.name, calc.attacker.types, calc.attacker_abilities), ("ogerpon-wellspring-mask", ["grass", "water"], ["water-absorb"]))

    # Nothing changes for a Pokémon without a form-changing item or ability.
    def test_no_form(self):
        calc = make_calc("garchomp", "snorlax", "earthquake")
        calc.use_battle_forms()
        self.assertEqual(calc.attacker.name, "garchomp")


class IgnoreAbilityTests(TestCase):
    fixtures = ["pokedata"]

    # Without Mold Breaker, Levitate stays.
    def test_nothing_ignored(self):
        calc = make_calc("garchomp", "bronzong", "earthquake", defender_ability="levitate")
        calc.ignore_abilities()
        self.assertEqual(calc.defender_abilities, ["levitate"])

    # Mold Breaker ignores Levitate.
    def test_mold_breaker(self):
        calc = make_calc("excadrill", "bronzong", "earthquake", "mold-breaker", "levitate")
        calc.ignore_abilities()
        self.assertEqual(calc.defender_abilities, [""])

    # Ability Shield protects Levitate from Mold Breaker.
    def test_ability_shield(self):
        calc = make_calc("excadrill", "bronzong", "earthquake", "mold-breaker", "levitate", defender_item="ability-shield")
        calc.ignore_abilities()
        self.assertEqual(calc.defender_abilities, ["levitate"])

    # Mold Breaker can't ignore Shadow Shield.
    def test_unbreakable_ability(self):
        calc = make_calc("excadrill", "lunala", "earthquake", "mold-breaker", "shadow-shield")
        calc.ignore_abilities()
        self.assertEqual(calc.defender_abilities, ["shadow-shield"])

    # Sunsteel Strike ignores abilities like Mold Breaker does.
    def test_ability_ignoring_move(self):
        calc = make_calc("solgaleo", "bronzong", "sunsteel-strike", "full-metal-body", "levitate")
        calc.ignore_abilities()
        self.assertEqual(calc.defender_abilities, [""])

    # Neutralizing Gas turns off the other Pokémon's ability, on either side.
    def test_neutralizing_gas(self):
        attacking = make_calc("weezing", "bronzong", "sludge-bomb", "neutralizing-gas", "levitate")
        attacking.ignore_abilities()
        self.assertEqual((attacking.attacker_abilities, attacking.defender_abilities), (["neutralizing-gas"], [""]))
        defending = make_calc("garchomp", "weezing", "earthquake", "rough-skin", "neutralizing-gas")
        defending.ignore_abilities()
        self.assertEqual(defending.attacker_abilities, [""])


class MoveTypeTests(TestCase):
    fixtures = ["pokedata"]

    # Weather Ball's type matches the weather.
    def test_weather_ball(self):
        for weather, move_type in (("sun", "fire"), ("rain", "water"), ("sandstorm", "rock"), ("snow", "ice"), (None, "normal")):
            self.assertEqual(make_calc("castform", "snorlax", "weather-ball", weather=weather).final_move_type(), (move_type, False))

    # Utility Umbrella keeps Weather Ball Normal type in rain.
    def test_weather_ball_umbrella(self):
        self.assertEqual(make_calc("pelipper", "snorlax", "weather-ball", attacker_item="utility-umbrella", weather="rain").final_move_type(), ("normal", False))

    # Plates, Drives, Memories and Masks change Judgment, Techno Blast, Multi-Attack and Ivy Cudgel.
    def test_item_moves(self):
        self.assertEqual(make_calc("arceus", "snorlax", "judgment", attacker_item="zap-plate").final_move_type(), ("electric", False))
        self.assertEqual(make_calc("genesect", "snorlax", "techno-blast", attacker_item="douse-drive").final_move_type(), ("water", False))
        self.assertEqual(make_calc("silvally", "snorlax", "multi-attack", attacker_item="fire-memory").final_move_type(), ("fire", False))
        self.assertEqual(make_calc("ogerpon", "snorlax", "ivy-cudgel", attacker_item="hearthflame-mask").final_move_type(), ("fire", False))
        self.assertEqual(make_calc("ogerpon", "snorlax", "ivy-cudgel").final_move_type(), ("grass", False))

    # Terrain Pulse matches the terrain, but only if the user is on the ground.
    def test_terrain_pulse(self):
        grounded = DamageCalculator(Species.objects.get(name="garchomp"), Species.objects.get(name="snorlax"), "normal", 50, "terrain-pulse", None, None, terrain="electric-terrain")
        flying = DamageCalculator(Species.objects.get(name="pelipper"), Species.objects.get(name="snorlax"), "normal", 50, "terrain-pulse", None, None, terrain="electric-terrain")
        self.assertEqual(grounded.final_move_type(), ("electric", False))
        self.assertEqual(flying.final_move_type(), ("normal", False))

    # Revelation Dance matches the user's first type.
    def test_revelation_dance(self):
        self.assertEqual(make_calc("charizard", "snorlax", "revelation-dance").final_move_type(), ("fire", False))

    # Hidden Power's type comes from the IVs. All 31 IVs is Dark.
    def test_hidden_power(self):
        self.assertEqual(make_calc("snorlax", "machamp", "hidden-power").final_move_type(), ("dark", False))
        fire_ivs = {"attack": 30, "special-attack": 30, "speed": 30}
        self.assertEqual(make_calc("snorlax", "machamp", "hidden-power", attacker_build={"ivs": fire_ivs}).final_move_type(), ("fire", False))
        ice_ivs = {"attack": 30, "defense": 30}
        self.assertEqual(make_calc("snorlax", "machamp", "hidden-power", attacker_build={"ivs": ice_ivs}).final_move_type(), ("ice", False))

    # Struggle has no type.
    def test_struggle(self):
        self.assertEqual(make_calc("snorlax", "gengar", "struggle").final_move_type(), ("typeless", False))

    # Pixilate turns Normal moves Fairy type (and boosts them), but leaves other types alone.
    def test_pixilate(self):
        self.assertEqual(make_calc("sylveon", "snorlax", "hyper-voice", attacker_ability="pixilate").final_move_type(), ("fairy", True))
        self.assertEqual(make_calc("sylveon", "snorlax", "shadow-ball", attacker_ability="pixilate").final_move_type(), ("ghost", False))

    # Normalize turns every move Normal type and boosts it, even moves that were already Normal.
    def test_normalize(self):
        self.assertEqual(make_calc("delcatty", "snorlax", "shadow-ball", attacker_ability="normalize").final_move_type(), ("normal", True))
        self.assertEqual(make_calc("delcatty", "snorlax", "hyper-voice", attacker_ability="normalize").final_move_type(), ("normal", True))

    # Liquid Voice turns sound moves Water type, without a power boost.
    def test_liquid_voice(self):
        self.assertEqual(make_calc("primarina", "snorlax", "boomburst", attacker_ability="liquid-voice").final_move_type(), ("water", False))

    # A move with nothing changing it keeps its type.
    def test_no_change(self):
        self.assertEqual(make_calc("gengar", "snorlax", "shadow-ball").final_move_type(), ("ghost", False))
class TypeEffectivenessTests(TestCase):
    fixtures = ["pokedata"]

    # Fire is super effective on Grass.
    def test_super_effective(self):
        self.assertEqual(make_calc("charizard", "venusaur", "flamethrower").final_type_effectiveness(155), 2)

    # Normal moves can't hit Ghost types.
    def test_immune(self):
        self.assertEqual(make_calc("snorlax", "gengar", "tackle").final_type_effectiveness(120), 0)

    # Scrappy lets Normal moves hit Ghost types. Normal is neutral on Gengar's Poison type.
    def test_scrappy(self):
        self.assertEqual(make_calc("kangaskhan", "gengar", "tackle", attacker_ability="scrappy").final_type_effectiveness(120), 1)

    # Mind's Eye lets Fighting moves hit Ghost types. Fighting is resisted by Gengar's Poison type.
    def test_minds_eye(self):
        self.assertEqual(make_calc("machamp", "gengar", "close-combat", attacker_ability="minds-eye").final_type_effectiveness(120), 0.5)

    # Freeze-Dry is super effective on Water types.
    def test_freeze_dry(self):
        self.assertEqual(make_calc("lapras", "vaporeon", "freeze-dry").final_type_effectiveness(205), 2)
        self.assertEqual(make_calc("lapras", "gyarados", "freeze-dry").final_type_effectiveness(170), 4)

    # Flying Press counts as Fighting and Flying. Both are super effective on Breloom.
    def test_flying_press(self):
        self.assertEqual(make_calc("hawlucha", "breloom", "flying-press").final_type_effectiveness(135), 4)

    # Ring Target removes immunities, so Normal moves hit Gengar for neutral dmg.
    def test_ring_target(self):
        self.assertEqual(make_calc("snorlax", "gengar", "tackle", defender_item="ring-target").final_type_effectiveness(120), 1)

    # Iron Ball and Thousand Arrows let Ground moves hit Flying types for neutral dmg.
    def test_iron_ball_and_thousand_arrows(self):
        self.assertEqual(make_calc("garchomp", "charizard", "earthquake").final_type_effectiveness(153), 0)
        self.assertEqual(make_calc("garchomp", "charizard", "earthquake", defender_item="iron-ball").final_type_effectiveness(153), 1)
        self.assertEqual(make_calc("garchomp", "charizard", "thousand-arrows").final_type_effectiveness(153), 1)

    # Strong winds take away the Flying type's weaknesses, so Electric only hits Gyarados 2x instead of 4x.
    def test_strong_winds(self):
        self.assertEqual(make_calc("pikachu", "gyarados", "thunderbolt").final_type_effectiveness(170), 4)
        self.assertEqual(make_calc("pikachu", "gyarados", "thunderbolt", weather="strong-winds").final_type_effectiveness(170), 2)

    # Tera Shell makes every hit not very effective while Terapagos is at full HP.
    def test_tera_shell(self):
        calc = make_calc("machamp", "terapagos", "close-combat", defender_ability="tera-shell")
        full_hp = calc.defender_stats["hp"]
        self.assertEqual(calc.final_type_effectiveness(full_hp), 0.5)
        self.assertEqual(calc.final_type_effectiveness(full_hp - 1), 2)

class MoveBlockedTests(TestCase):
    fixtures = ["pokedata"]

    # A normal hit isn't blocked.
    def test_not_blocked(self):
        self.assertFalse(make_calc("machamp", "snorlax", "close-combat").move_blocked())

    # Levitate and Air Balloon block Ground moves, but Thousand Arrows still hits.
    def test_levitate_and_air_balloon(self):
        self.assertTrue(make_calc("garchomp", "bronzong", "earthquake", defender_ability="levitate").move_blocked())
        self.assertTrue(make_calc("garchomp", "heatran", "earthquake", defender_item="air-balloon").move_blocked())
        self.assertFalse(make_calc("garchomp", "bronzong", "thousand-arrows", defender_ability="levitate").move_blocked())

    # Abilities that absorb a type block moves of that type.
    def test_absorb_abilities(self):
        for move, ability in (("flamethrower", "flash-fire"), ("flamethrower", "well-baked-body"), ("surf", "water-absorb"), ("surf", "storm-drain"), ("surf", "dry-skin"),
                              ("thunderbolt", "volt-absorb"), ("thunderbolt", "lightning-rod"), ("thunderbolt", "motor-drive"), ("energy-ball", "sap-sipper"),
                              ("earthquake", "earth-eater"), ("hurricane", "wind-rider")):
            self.assertTrue(make_calc("mew", "snorlax", move, defender_ability=ability).move_blocked(), f"{ability} should block {move}")

    # Soundproof blocks sound moves and Bulletproof blocks ball and bomb moves.
    def test_soundproof_and_bulletproof(self):
        self.assertTrue(make_calc("mew", "snorlax", "boomburst", defender_ability="soundproof").move_blocked())
        self.assertTrue(make_calc("mew", "snorlax", "shadow-ball", defender_ability="bulletproof").move_blocked())

    # Wonder Guard only lets super-effective moves hit.
    def test_wonder_guard(self):
        self.assertFalse(make_calc("charizard", "shedinja", "flamethrower", defender_ability="wonder-guard").move_blocked())
        self.assertTrue(make_calc("scizor", "shedinja", "x-scissor", defender_ability="wonder-guard").move_blocked())

    # Queenly Majesty, Dazzling and Armor Tail block priority moves only.
    def test_priority_blockers(self):
        for ability in ("queenly-majesty", "dazzling", "armor-tail"):
            self.assertTrue(make_calc("snorlax", "machamp", "quick-attack", defender_ability=ability).move_blocked())
        self.assertFalse(make_calc("snorlax", "machamp", "tackle", defender_ability="queenly-majesty").move_blocked())

    # Psychic Terrain blocks priority moves on Pokémon that are on the ground.
    def test_psychic_terrain(self):
        grounded = DamageCalculator(Species.objects.get(name="snorlax"), Species.objects.get(name="machamp"), "normal", 40, "quick-attack", None, None, terrain="psychic-terrain")
        flying = DamageCalculator(Species.objects.get(name="snorlax"), Species.objects.get(name="pelipper"), "normal", 40, "quick-attack", None, None, terrain="psychic-terrain")
        self.assertTrue(grounded.move_blocked())
        self.assertFalse(flying.move_blocked())

    # Heavy rain stops Fire moves and extreme sun stops Water moves. Regular sun doesn't stop anything.
    def test_primal_weather(self):
        self.assertTrue(make_calc("charizard", "snorlax", "flamethrower", weather="heavy-rain").move_blocked())
        self.assertTrue(make_calc("blastoise", "snorlax", "surf", weather="extreme-sun").move_blocked())
        self.assertFalse(make_calc("blastoise", "snorlax", "surf", weather="sun").move_blocked())

    # Poltergeist needs the target to hold an item, Dream Eater needs it asleep and Steel Roller needs terrain.
    def test_moves_that_need_something(self):
        self.assertTrue(make_calc("gengar", "machamp", "poltergeist").move_blocked())
        self.assertFalse(make_calc("gengar", "machamp", "poltergeist", defender_item="leftovers").move_blocked())
        awake = DamageCalculator(Species.objects.get(name="gengar"), Species.objects.get(name="machamp"), "psychic", 100, "dream-eater", None, None)
        asleep = DamageCalculator(Species.objects.get(name="gengar"), Species.objects.get(name="machamp"), "psychic", 100, "dream-eater", None, "sleep")
        self.assertTrue(awake.move_blocked())
        self.assertFalse(asleep.move_blocked())
        self.assertTrue(make_calc("melmetal", "machamp", "steel-roller").move_blocked())

    # Synchronoise needs a shared type, Burn Up needs a Fire-type user, Double Shock needs an Electric-type user, and Sky Drop can't lift Flying types or anything 200 kg or heavier.
    def test_moves_that_need_types_or_weight(self):
        self.assertTrue(make_calc("alakazam", "machamp", "synchronoise").move_blocked())
        self.assertFalse(make_calc("alakazam", "espeon", "synchronoise").move_blocked())
        self.assertTrue(make_calc("snorlax", "machamp", "burn-up").move_blocked())
        self.assertFalse(make_calc("charizard", "machamp", "burn-up").move_blocked())
        self.assertTrue(make_calc("snorlax", "machamp", "double-shock").move_blocked())
        self.assertTrue(make_calc("charizard", "pelipper", "sky-drop").move_blocked())
        self.assertTrue(make_calc("charizard", "snorlax", "sky-drop").move_blocked())
        self.assertFalse(make_calc("charizard", "machamp", "sky-drop").move_blocked())