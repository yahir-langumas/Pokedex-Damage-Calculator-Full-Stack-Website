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

class FixedDamageTests(TestCase):
    fixtures = ["pokedata"]

    # Seismic Toss does dmg equal to the user's level.
    def test_seismic_toss(self):
        self.assertEqual(make_calc("machamp", "snorlax", "seismic-toss").fixed_damage(165, 235), 50)
        self.assertEqual(make_calc("machamp", "snorlax", "seismic-toss", attacker_build={"level": 37}).fixed_damage(165, 235), 37)

    # Night Shade works the same way.
    def test_night_shade(self):
        self.assertEqual(make_calc("gengar", "snorlax", "night-shade").fixed_damage(120, 235), 50)

    # Dragon Rage always does 40 and Sonic Boom always does 20.
    def test_dragon_rage_and_sonic_boom(self):
        self.assertEqual(make_calc("dragonite", "snorlax", "dragon-rage").fixed_damage(166, 235), 40)
        self.assertEqual(make_calc("magnezone", "snorlax", "sonic-boom").fixed_damage(130, 235), 20)

    # Super Fang does half the target's current HP, and always at least 1.
    def test_super_fang(self):
        self.assertEqual(make_calc("raticate", "snorlax", "super-fang").fixed_damage(115, 157), 78)
        self.assertEqual(make_calc("raticate", "snorlax", "super-fang").fixed_damage(115, 1), 1)

    # Ruination and Nature's Madness work the same way.
    def test_ruination_and_natures_madness(self):
        self.assertEqual(make_calc("chien-pao", "snorlax", "ruination").fixed_damage(155, 200), 100)
        self.assertEqual(make_calc("tapu-lele", "snorlax", "natures-madness").fixed_damage(130, 200), 100)

    # Final Gambit does dmg equal to the user's HP.
    def test_final_gambit(self):
        self.assertEqual(make_calc("machamp", "snorlax", "final-gambit").fixed_damage(120, 235), 120)

    # Endeavor brings the target down to the user's HP, and does nothing if the user has more HP.
    def test_endeavor(self):
        self.assertEqual(make_calc("machamp", "snorlax", "endeavor").fixed_damage(10, 150), 140)
        self.assertEqual(make_calc("machamp", "snorlax", "endeavor").fixed_damage(150, 10), 0)

    # One-hit KO moves do all the target's HP, unless it has Sturdy, is a higher level, or is an Ice type hit by Sheer Cold.
    def test_ohko_moves(self):
        self.assertEqual(make_calc("garchomp", "snorlax", "fissure").fixed_damage(183, 200), 200)
        self.assertEqual(make_calc("garchomp", "snorlax", "fissure", defender_ability="sturdy").fixed_damage(183, 200), 0)
        self.assertEqual(make_calc("garchomp", "snorlax", "fissure", attacker_build={"level": 40}).fixed_damage(150, 200), 0)
        self.assertEqual(make_calc("lapras", "lapras", "sheer-cold").fixed_damage(205, 205), 0)
        self.assertEqual(make_calc("lapras", "snorlax", "sheer-cold").fixed_damage(205, 235), 235)

    # Regular moves don't do set dmg.
    def test_regular_move(self):
        self.assertIsNone(make_calc("snorlax", "machamp", "tackle").fixed_damage(235, 165))


class KnockOffTests(TestCase):
    fixtures = ["pokedata"]

    # Knock Off gets its boost when the target is holding an item.
    def test_has_item(self):
        self.assertTrue(make_calc("weavile", "snorlax", "knock-off", defender_item="leftovers").knock_off_boost())

    # No item means no boost.
    def test_no_item(self):
        self.assertFalse(make_calc("weavile", "snorlax", "knock-off").knock_off_boost())

    # Groudon's Red Orb can't be knocked off, but anyone else's can.
    def test_primal_orbs(self):
        self.assertFalse(make_calc("weavile", "groudon", "knock-off", defender_item="red-orb").knock_off_boost())
        self.assertTrue(make_calc("weavile", "snorlax", "knock-off", defender_item="red-orb").knock_off_boost())

    # Arceus's Plates and Silvally's Memories can't be knocked off.
    def test_arceus_and_silvally(self):
        self.assertFalse(make_calc("weavile", "arceus", "knock-off", defender_item="flame-plate").knock_off_boost())
        self.assertTrue(make_calc("weavile", "snorlax", "knock-off", defender_item="flame-plate").knock_off_boost())
        self.assertFalse(make_calc("weavile", "silvally", "knock-off", defender_item="fire-memory").knock_off_boost())

    # Genesect's Drives can't be knocked off.
    def test_genesect_drives(self):
        self.assertFalse(make_calc("weavile", "genesect", "knock-off", defender_item="douse-drive").knock_off_boost())
        self.assertTrue(make_calc("weavile", "snorlax", "knock-off", defender_item="douse-drive").knock_off_boost())

    # The Origin Forme items and Ogerpon's masks can't be knocked off.
    def test_origin_items_and_masks(self):
        self.assertFalse(make_calc("weavile", "dialga", "knock-off", defender_item="adamant-crystal").knock_off_boost())
        self.assertFalse(make_calc("weavile", "ogerpon", "knock-off", defender_item="wellspring-mask").knock_off_boost())

    # Booster Energy can't be knocked off a Pokémon with Protosynthesis or Quark Drive.
    def test_booster_energy(self):
        self.assertFalse(make_calc("weavile", "great-tusk", "knock-off", defender_ability="protosynthesis", defender_item="booster-energy").knock_off_boost())
        self.assertTrue(make_calc("weavile", "snorlax", "knock-off", defender_item="booster-energy").knock_off_boost())


class VariablePowerTests(TestCase):
    fixtures = ["pokedata"]

    # Calls variable_move_power with full HP, no stat stages and equal Speed unless a test says otherwise.
    def power(self, calc, attacker_hp=None, defender_hp=None, attacker_boosts=None, defender_boosts=None, attacker_speed=100, defender_speed=100):
        attacker_hp = calc.attacker_stats["hp"] if attacker_hp is None else attacker_hp
        defender_hp = calc.defender_stats["hp"] if defender_hp is None else defender_hp
        return calc.variable_move_power(attacker_hp, defender_hp, attacker_boosts or {}, defender_boosts or {}, attacker_speed, defender_speed)

    # Regular moves keep their power.
    def test_regular_move(self):
        self.assertEqual(self.power(make_calc("snorlax", "machamp", "tackle")), 40)

    # Moves that do set dmg have no power.
    def test_set_damage_move(self):
        self.assertIsNone(self.power(make_calc("machamp", "snorlax", "seismic-toss")))

    # Low Kick gets stronger the heavier the target is. Float Stone and Heavy Metal change the target's weight.
    def test_low_kick(self):
        self.assertEqual(self.power(make_calc("machamp", "snorlax", "low-kick")), 120)
        self.assertEqual(self.power(make_calc("machamp", "machamp", "low-kick")), 100)
        self.assertEqual(self.power(make_calc("machamp", "pikachu", "low-kick")), 20)
        self.assertEqual(self.power(make_calc("machamp", "machamp", "low-kick", defender_item="float-stone")), 80)
        self.assertEqual(self.power(make_calc("machamp", "machamp", "low-kick", defender_ability="heavy-metal")), 120)

    # Heavy Slam gets stronger the heavier the user is compared to the target.
    def test_heavy_slam(self):
        self.assertEqual(self.power(make_calc("snorlax", "pikachu", "heavy-slam")), 120)
        self.assertEqual(self.power(make_calc("snorlax", "machamp", "heavy-slam")), 80)
        self.assertEqual(self.power(make_calc("snorlax", "snorlax", "heavy-slam")), 40)

    # Gyro Ball is stronger when the user is slower. Electro Ball is stronger when the user is faster.
    def test_speed_moves(self):
        self.assertEqual(self.power(make_calc("ferrothorn", "machamp", "gyro-ball"), attacker_speed=30, defender_speed=200), 150)
        self.assertEqual(self.power(make_calc("ferrothorn", "machamp", "gyro-ball")), 26)
        self.assertEqual(self.power(make_calc("pikachu", "machamp", "electro-ball"), attacker_speed=200, defender_speed=50), 150)
        self.assertEqual(self.power(make_calc("pikachu", "machamp", "electro-ball")), 60)
        self.assertEqual(self.power(make_calc("pikachu", "machamp", "electro-ball"), attacker_speed=50, defender_speed=100), 40)

    # Eruption gets weaker as the user loses HP.
    def test_eruption(self):
        calc = make_calc("typhlosion", "snorlax", "eruption")
        max_hp = calc.attacker_stats["hp"]
        self.assertEqual(self.power(calc), 150)
        self.assertEqual(self.power(calc, attacker_hp=max_hp // 2), 74)
        self.assertEqual(self.power(calc, attacker_hp=1), 1)

    # Flail gets stronger as the user loses HP.
    def test_flail(self):
        calc = make_calc("magikarp", "snorlax", "flail")
        self.assertEqual(self.power(calc, attacker_hp=1), 200)
        self.assertEqual(self.power(calc), 20)

    # Crush Grip and Hard Press get weaker as the target loses HP.
    def test_crush_grip_and_hard_press(self):
        crush_grip = make_calc("regigigas", "pikachu", "crush-grip")
        self.assertEqual(self.power(crush_grip), 120)
        self.assertEqual(self.power(crush_grip, defender_hp=crush_grip.defender_stats["hp"] // 2), 60)
        self.assertEqual(self.power(make_calc("regigigas", "snorlax", "hard-press")), 100)

    # Stored Power counts the user's stat boosts and Punishment counts the target's. Drops don't count.
    def test_stat_stage_moves(self):
        self.assertEqual(self.power(make_calc("espeon", "snorlax", "stored-power"), attacker_boosts={"attack": 2, "speed": 1}), 80)
        self.assertEqual(self.power(make_calc("espeon", "snorlax", "stored-power"), attacker_boosts={"attack": -2}), 20)
        self.assertEqual(self.power(make_calc("weavile", "snorlax", "punishment"), defender_boosts={"defense": 3}), 120)

    # Return and Frustration have 102 power at max friendship.
    def test_friendship_moves(self):
        self.assertEqual(self.power(make_calc("snorlax", "machamp", "return")), 102)
        self.assertEqual(self.power(make_calc("snorlax", "machamp", "frustration")), 102)

    # Weather Ball doubles in weather (not with Utility Umbrella in rain). Terrain Pulse, Rising Voltage and Psyblade get stronger in terrain.
    def test_weather_and_terrain(self):
        self.assertEqual(self.power(make_calc("castform", "snorlax", "weather-ball", weather="rain")), 100)
        self.assertEqual(self.power(make_calc("pelipper", "snorlax", "weather-ball", attacker_item="utility-umbrella", weather="rain")), 50)
        self.assertEqual(self.power(make_calc("castform", "snorlax", "weather-ball", weather="strong-winds")), 50)
        electric = DamageCalculator(Species.objects.get(name="pikachu"), Species.objects.get(name="snorlax"), "electric", 70, "rising-voltage", None, None, terrain="electric-terrain")
        self.assertEqual(self.power(electric), 140)
        terrain_pulse = DamageCalculator(Species.objects.get(name="pikachu"), Species.objects.get(name="snorlax"), "normal", 50, "terrain-pulse", None, None, terrain="electric-terrain")
        self.assertEqual(self.power(terrain_pulse), 100)
        psyblade = DamageCalculator(Species.objects.get(name="iron-leaves"), Species.objects.get(name="snorlax"), "psychic", 80, "psyblade", None, None, terrain="electric-terrain")
        self.assertEqual(self.power(psyblade), 120)

    # Hex doubles on a target with a status, Acrobatics doubles with no item, Payback doubles moving last and Bolt Beak doubles moving first.
    def test_doubled_power(self):
        burned = DamageCalculator(Species.objects.get(name="gengar"), Species.objects.get(name="machamp"), "ghost", 65, "hex", None, "burn")
        self.assertEqual(self.power(burned), 130)
        self.assertEqual(self.power(make_calc("gengar", "machamp", "hex")), 65)
        self.assertEqual(self.power(make_calc("hawlucha", "machamp", "acrobatics")), 110)
        self.assertEqual(self.power(make_calc("hawlucha", "machamp", "acrobatics", attacker_item="leftovers")), 55)
        self.assertEqual(self.power(make_calc("umbreon", "machamp", "payback"), attacker_speed=50, defender_speed=100), 100)
        self.assertEqual(self.power(make_calc("umbreon", "machamp", "payback"), attacker_speed=150, defender_speed=100), 50)
        self.assertEqual(self.power(make_calc("dracozolt", "machamp", "bolt-beak"), attacker_speed=150, defender_speed=100), 170)

class HitCountTests(TestCase):
    fixtures = ["pokedata"]

    # Most moves only hit once.
    def test_single_hit(self):
        self.assertEqual(make_calc("snorlax", "machamp", "tackle").damage_calc_hits(), 1)

    # Moves like Double Kick always hit the same number of times.
    def test_fixed_hits(self):
        self.assertEqual(make_calc("machamp", "snorlax", "double-kick").damage_calc_hits(), 2)

    # 2-5 hit moves count as 3 hits.
    def test_two_to_five_hits(self):
        self.assertEqual(make_calc("cinccino", "snorlax", "bullet-seed").damage_calc_hits(), 3)

    # Skill Link makes 2-5 hit moves always hit 5 times.
    def test_skill_link(self):
        self.assertEqual(make_calc("cinccino", "snorlax", "bullet-seed", attacker_ability="skill-link").damage_calc_hits(), 5)

    # Skill Link doesn't change moves that already hit a set number of times.
    def test_skill_link_fixed_hits(self):
        self.assertEqual(make_calc("machamp", "snorlax", "double-kick", attacker_ability="skill-link").damage_calc_hits(), 2)

    # Loaded Dice makes 2-5 hit moves count as 4 hits, but does nothing for single hit moves.
    def test_loaded_dice(self):
        self.assertEqual(make_calc("cinccino", "snorlax", "bullet-seed", attacker_item="loaded-dice").damage_calc_hits(), 4)
        self.assertEqual(make_calc("snorlax", "machamp", "tackle", attacker_item="loaded-dice").damage_calc_hits(), 1)

    # Klutz stops Loaded Dice from working.
    def test_klutz_loaded_dice(self):
        self.assertEqual(make_calc("lopunny", "snorlax", "bullet-seed", attacker_ability="klutz", attacker_item="loaded-dice").damage_calc_hits(), 3)

    # Newer moves PokeAPI is missing hit counts for.
    def test_missing_hit_counts(self):
        self.assertEqual(make_calc("maushold-family-of-four", "snorlax", "population-bomb").damage_calc_hits(), 10)
        self.assertEqual(make_calc("dondozo", "snorlax", "triple-dive").damage_calc_hits(), 3)
        self.assertEqual(make_calc("espeon", "snorlax", "twin-beam").damage_calc_hits(), 2)


class BasePowerTests(TestCase):
    fixtures = ["pokedata"]

    # Calls final_base_power as a physical, neutral, non-contact move at full HP unless a test says otherwise.
    def power(self, calc, physical=True, effectiveness=1, ate_changed=False, moves_last=False, makes_contact=False, attacker_boosts=None, defender_hp=None):
        defender_hp = calc.defender_stats["hp"] if defender_hp is None else defender_hp
        return calc.final_base_power(physical, effectiveness, ate_changed, moves_last, makes_contact, attacker_boosts or {}, defender_hp)

    # Regular moves keep their power.
    def test_regular_move(self):
        self.assertEqual(self.power(make_calc("snorlax", "machamp", "tackle")), 40)

    # Facade doubles when the user has a status and Brine doubles when the target is at half HP or less.
    def test_facade_and_brine(self):
        burned = DamageCalculator(Species.objects.get(name="snorlax"), Species.objects.get(name="machamp"), "normal", 70, "facade", "burn", None)
        self.assertEqual(self.power(burned), 140)
        self.assertEqual(self.power(make_calc("snorlax", "machamp", "facade")), 70)
        self.assertEqual(self.power(make_calc("pelipper", "snorlax", "brine"), physical=False, defender_hp=117), 130)
        self.assertEqual(self.power(make_calc("pelipper", "snorlax", "brine"), physical=False), 65)

    # Knock Off's 1.5x boost makes 97.5 power, and .5 rounds down.
    def test_knock_off(self):
        self.assertEqual(self.power(make_calc("weavile", "snorlax", "knock-off", defender_item="leftovers")), 97)
        self.assertEqual(self.power(make_calc("weavile", "snorlax", "knock-off")), 65)

    # Solar Beam is halved in rain, but not in sun or with Utility Umbrella.
    def test_solar_beam(self):
        self.assertEqual(self.power(make_calc("venusaur", "snorlax", "solar-beam", weather="rain"), physical=False), 60)
        self.assertEqual(self.power(make_calc("venusaur", "snorlax", "solar-beam", weather="sun"), physical=False), 120)
        self.assertEqual(self.power(make_calc("venusaur", "snorlax", "solar-beam", attacker_item="utility-umbrella", weather="rain"), physical=False), 120)

    # Collision Course gets 1.33x power when it's super effective.
    def test_collision_course(self):
        self.assertEqual(self.power(make_calc("koraidon", "snorlax", "collision-course"), effectiveness=2), 133)
        self.assertEqual(self.power(make_calc("koraidon", "snorlax", "collision-course")), 100)

    # Electric Terrain boosts Electric moves by 1.3x and Grassy Terrain halves Earthquake.
    def test_terrain(self):
        electric = DamageCalculator(Species.objects.get(name="pikachu"), Species.objects.get(name="machamp"), "electric", 90, "thunderbolt", None, None, terrain="electric-terrain")
        self.assertEqual(self.power(electric, physical=False), 117)
        grassy = DamageCalculator(Species.objects.get(name="garchomp"), Species.objects.get(name="snorlax"), "ground", 100, "earthquake", None, None, terrain="grassy-terrain")
        self.assertEqual(self.power(grassy), 50)

    # Technician boosts moves with 60 power or less by 1.5x.
    def test_technician(self):
        self.assertEqual(self.power(make_calc("scizor", "snorlax", "bullet-punch", attacker_ability="technician")), 60)
        self.assertEqual(self.power(make_calc("scizor", "snorlax", "iron-head", attacker_ability="technician")), 80)

    # Iron Fist boosts punches by 1.2x, Strong Jaw boosts bites by 1.5x and Sheer Force boosts moves with added effects by 1.3x.
    def test_boosting_abilities(self):
        self.assertEqual(self.power(make_calc("hitmonchan", "snorlax", "mach-punch", attacker_ability="iron-fist")), 48)
        self.assertEqual(self.power(make_calc("feraligatr", "snorlax", "crunch", attacker_ability="strong-jaw")), 120)
        self.assertEqual(self.power(make_calc("nidoking", "machamp", "flamethrower", attacker_ability="sheer-force"), physical=False), 117)

    # Tough Claws boosts contact moves by 1.3x and -ate abilities boost the moves they change by 1.2x.
    def test_tough_claws_and_ate(self):
        self.assertEqual(self.power(make_calc("barbaracle", "snorlax", "tackle", attacker_ability="tough-claws"), makes_contact=True), 52)
        self.assertEqual(self.power(make_calc("barbaracle", "snorlax", "tackle", attacker_ability="tough-claws")), 40)
        self.assertEqual(self.power(make_calc("sylveon", "snorlax", "hyper-voice"), physical=False, ate_changed=True), 108)

    # Type boosting items give 1.2x, Gems give 1.3x, Muscle Band boosts physical moves and Wise Glasses boosts special moves.
    def test_items(self):
        self.assertEqual(self.power(make_calc("charizard", "machamp", "flamethrower", attacker_item="charcoal"), physical=False), 108)
        self.assertEqual(self.power(make_calc("charizard", "machamp", "flamethrower", attacker_item="fire-gem"), physical=False), 117)
        self.assertEqual(self.power(make_calc("snorlax", "machamp", "tackle", attacker_item="muscle-band")), 44)
        self.assertEqual(self.power(make_calc("snorlax", "machamp", "tackle", attacker_item="wise-glasses")), 40)
        self.assertEqual(self.power(make_calc("charizard", "machamp", "flamethrower", attacker_item="wise-glasses"), physical=False), 99)

    # Abilities and items stack. Technician and Metal Coat on Bullet Punch is 40 x 1.5 x 1.2.
    def test_modifiers_stack(self):
        self.assertEqual(self.power(make_calc("scizor", "snorlax", "bullet-punch", attacker_ability="technician", attacker_item="metal-coat")), 72)


class AttackStatTests(TestCase):
    fixtures = ["pokedata"]

    # Calls final_attack as a physical, non-crit move at full HP with no stat stages unless a test says otherwise.
    def attack(self, calc, physical=True, critical_hit=False, attacker_boosts=None, defender_boosts=None, attacker_hp=None):
        attacker_hp = calc.attacker_stats["hp"] if attacker_hp is None else attacker_hp
        return calc.final_attack(physical, critical_hit, attacker_boosts or {}, defender_boosts or {}, attacker_hp)

    # Physical moves use Attack and special moves use Sp. Atk.
    def test_attack_and_special_attack(self):
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "earthquake")), 150)
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "draco-meteor"), physical=False), 100)

    # Stat stages raise or lower the stat. +2 doubles it and -1 makes it 2/3.
    def test_stat_stages(self):
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "earthquake"), attacker_boosts={"attack": 2}), 300)
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "earthquake"), attacker_boosts={"attack": -1}), 100)

    # Crits ignore the attacker's stat drops but keep its boosts.
    def test_critical_hit(self):
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "earthquake"), critical_hit=True, attacker_boosts={"attack": -1}), 150)
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "earthquake"), critical_hit=True, attacker_boosts={"attack": 1}), 225)

    # Unaware ignores the attacker's stat boosts.
    def test_unaware(self):
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "earthquake", defender_ability="unaware"), attacker_boosts={"attack": 2}), 150)

    # Foul Play uses the target's Attack and the target's stat stages.
    def test_foul_play(self):
        self.assertEqual(self.attack(make_calc("umbreon", "garchomp", "foul-play")), 150)
        self.assertEqual(self.attack(make_calc("umbreon", "garchomp", "foul-play"), defender_boosts={"attack": 1}), 225)
        self.assertEqual(self.attack(make_calc("umbreon", "garchomp", "foul-play"), attacker_boosts={"attack": 2}), 150)

    # Body Press uses the user's Defense and Defense stages.
    def test_body_press(self):
        self.assertEqual(self.attack(make_calc("snorlax", "machamp", "body-press")), 85)
        self.assertEqual(self.attack(make_calc("snorlax", "machamp", "body-press"), attacker_boosts={"defense": 1}), 127)

    # Huge Power doubles Attack. Hustle boosts Attack by 1.5x but not Sp. Atk.
    def test_huge_power_and_hustle(self):
        self.assertEqual(self.attack(make_calc("azumarill", "machamp", "aqua-tail", attacker_ability="huge-power")), 140)
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "earthquake", attacker_ability="hustle")), 225)
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "draco-meteor", attacker_ability="hustle"), physical=False), 100)

    # Choice Band and Choice Specs give 1.5x. Light Ball doubles Pikachu's Attack and Sp. Atk.
    def test_choice_items_and_light_ball(self):
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "earthquake", attacker_item="choice-band")), 225)
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "draco-meteor", attacker_item="choice-specs"), physical=False), 150)
        self.assertEqual(self.attack(make_calc("pikachu", "machamp", "volt-tackle", attacker_item="light-ball")), 150)
        self.assertEqual(self.attack(make_calc("pikachu", "machamp", "thunderbolt", attacker_item="light-ball"), physical=False), 140)

    # Blaze boosts Fire moves by 1.5x at 1/3 HP or less. 193.5 rounds down to 193.
    def test_blaze(self):
        calc = make_calc("charizard", "machamp", "flamethrower", attacker_ability="blaze")
        third = calc.attacker_stats["hp"] // 3
        self.assertEqual(self.attack(calc, physical=False, attacker_hp=third), 193)
        self.assertEqual(self.attack(calc, physical=False, attacker_hp=third + 1), 129)

    # Thick Fat halves Fire and Ice moves and Tablets of Ruin lowers the attacker's Attack to 0.75x.
    def test_defender_abilities(self):
        self.assertEqual(self.attack(make_calc("charizard", "snorlax", "flamethrower", defender_ability="thick-fat"), physical=False), 64)
        self.assertEqual(self.attack(make_calc("garchomp", "machamp", "earthquake", defender_ability="tablets-of-ruin")), 112)

class DefenseStatTests(TestCase):
    fixtures = ["pokedata"]

    # Calls final_defense as a physical, non-crit hit with no stat stages unless a test says otherwise.
    def defense(self, calc, physical_hit=True, critical_hit=False, attacker_boosts=None, defender_boosts=None):
        return calc.final_defense(physical_hit, critical_hit, attacker_boosts or {}, defender_boosts or {})

    # Physical hits use Defense and special hits use Sp. Def.
    def test_defense_and_special_defense(self):
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle")), 85)
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle"), physical_hit=False), 130)

    # Stat stages raise or lower the stat. +1 is 1.5x and -2 is 1/2.
    def test_stat_stages(self):
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle"), defender_boosts={"defense": 1}), 127)
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle"), defender_boosts={"defense": -2}), 42)

    # Crits ignore the defender's stat boosts but keep its drops.
    def test_critical_hit(self):
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle"), critical_hit=True, defender_boosts={"defense": 2}), 85)
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle"), critical_hit=True, defender_boosts={"defense": -1}), 56)

    # Unaware and Sacred Sword ignore the defender's stat changes.
    def test_unaware_and_sacred_sword(self):
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle", attacker_ability="unaware"), defender_boosts={"defense": 2}), 85)
        self.assertEqual(self.defense(make_calc("gallade", "snorlax", "sacred-sword"), defender_boosts={"defense": 2}), 85)
        self.assertEqual(self.defense(make_calc("gallade", "snorlax", "sacred-sword"), defender_boosts={"defense": -2}), 85)

    # Sandstorm boosts Rock types' Sp. Def by 1.5x, but not their Defense or anyone else's Sp. Def.
    def test_sandstorm(self):
        self.assertEqual(self.defense(make_calc("machamp", "tyranitar", "tackle", weather="sandstorm"), physical_hit=False), 180)
        self.assertEqual(self.defense(make_calc("machamp", "tyranitar", "tackle", weather="sandstorm")), 130)
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle", weather="sandstorm"), physical_hit=False), 130)

    # Snow boosts Ice types' Defense by 1.5x. 142.5 rounds down to 142.
    def test_snow(self):
        self.assertEqual(self.defense(make_calc("machamp", "abomasnow", "tackle", weather="snow")), 142)
        self.assertEqual(self.defense(make_calc("machamp", "abomasnow", "tackle")), 95)

    # Eviolite boosts both defenses by 1.5x, but only on Pokémon that can still evolve.
    def test_eviolite(self):
        self.assertEqual(self.defense(make_calc("machamp", "chansey", "tackle", defender_item="eviolite")), 37)
        self.assertEqual(self.defense(make_calc("machamp", "chansey", "tackle", defender_item="eviolite"), physical_hit=False), 187)
        self.assertEqual(self.defense(make_calc("machamp", "blissey", "tackle", defender_item="eviolite")), 30)

    # Assault Vest boosts Sp. Def by 1.5x but not Defense.
    def test_assault_vest(self):
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle", defender_item="assault-vest"), physical_hit=False), 195)
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle", defender_item="assault-vest")), 85)

    # Fur Coat doubles Defense and Marvel Scale boosts it by 1.5x when the defender has a status.
    def test_fur_coat_and_marvel_scale(self):
        self.assertEqual(self.defense(make_calc("machamp", "snorlax", "tackle", defender_ability="fur-coat")), 170)
        burned = DamageCalculator(Species.objects.get(name="machamp"), Species.objects.get(name="milotic"), "normal", 40, "tackle", None, "burn", defender_ability="marvel-scale")
        self.assertEqual(self.defense(burned), 148)
        self.assertEqual(self.defense(make_calc("machamp", "milotic", "tackle", defender_ability="marvel-scale")), 99)

    # Sword of Ruin lowers the defender's Defense and Beads of Ruin lowers its Sp. Def to 0.75x. 97.5 rounds down to 97.
    def test_ruin_abilities(self):
        self.assertEqual(self.defense(make_calc("chien-pao", "snorlax", "tackle", attacker_ability="sword-of-ruin")), 64)
        self.assertEqual(self.defense(make_calc("chi-yu", "snorlax", "tackle", attacker_ability="beads-of-ruin"), physical_hit=False), 97)


class FinalModifierTests(TestCase):
    fixtures = ["pokedata"]

    # Calls final_modifiers as a physical, non-crit, neutral, non-contact first hit at full HP with no screens unless a test says otherwise.
    def modifier(self, calc, physical=True, critical_hit=False, effectiveness=1, defender_hp=None, makes_contact=False, reflect=False, light_screen=False, aurora_veil=False, first_hit=True):
        defender_hp = calc.defender_stats["hp"] if defender_hp is None else defender_hp
        return calc.final_modifiers(physical, critical_hit, effectiveness, defender_hp, makes_contact, reflect, light_screen, aurora_veil, first_hit)

    # No modifiers means 4096 (1x).
    def test_no_modifiers(self):
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle")), 4096)

    # Reflect halves physical dmg and Light Screen halves special dmg. Aurora Veil halves both.
    def test_screens(self):
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle"), reflect=True), 2048)
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle"), physical=False, reflect=True), 4096)
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle"), physical=False, light_screen=True), 2048)
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle"), aurora_veil=True), 2048)
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle"), physical=False, aurora_veil=True), 2048)

    # Crits, Infiltrator and Brick Break go through screens.
    def test_ignoring_screens(self):
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle"), critical_hit=True, reflect=True), 4096)
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle", attacker_ability="infiltrator"), reflect=True), 4096)
        self.assertEqual(self.modifier(make_calc("machamp", "snorlax", "brick-break"), reflect=True), 4096)

    # Multiscale halves dmg at full HP, but only on the first hit.
    def test_multiscale(self):
        calc = make_calc("garchomp", "dragonite", "dragon-claw", defender_ability="multiscale")
        self.assertEqual(self.modifier(calc), 2048)
        self.assertEqual(self.modifier(calc, defender_hp=calc.defender_stats["hp"] - 1), 4096)
        self.assertEqual(self.modifier(calc, first_hit=False), 4096)

    # Filter takes 0.75x dmg from super effective moves.
    def test_filter(self):
        self.assertEqual(self.modifier(make_calc("machamp", "mr-mime", "tackle", defender_ability="filter"), effectiveness=2), 3072)
        self.assertEqual(self.modifier(make_calc("machamp", "mr-mime", "tackle", defender_ability="filter")), 4096)

    # Fluffy halves contact dmg but doubles Fire dmg. A Fire contact move cancels out.
    def test_fluffy(self):
        self.assertEqual(self.modifier(make_calc("machamp", "dubwool", "tackle", defender_ability="fluffy"), makes_contact=True), 2048)
        self.assertEqual(self.modifier(make_calc("charizard", "dubwool", "flamethrower", defender_ability="fluffy"), physical=False), 8192)
        self.assertEqual(self.modifier(make_calc("charizard", "dubwool", "fire-punch", defender_ability="fluffy"), makes_contact=True), 4096)

    # Ice Scales halves special dmg but not physical dmg.
    def test_ice_scales(self):
        self.assertEqual(self.modifier(make_calc("charizard", "frosmoth", "flamethrower", defender_ability="ice-scales"), physical=False), 2048)
        self.assertEqual(self.modifier(make_calc("machamp", "frosmoth", "tackle", defender_ability="ice-scales")), 4096)

    # Tinted Lens doubles not very effective dmg, Neuroforce gives 1.25x on super effective hits and Sniper gives 1.5x on crits.
    def test_attacker_abilities(self):
        self.assertEqual(self.modifier(make_calc("butterfree", "machamp", "bug-buzz", attacker_ability="tinted-lens"), physical=False, effectiveness=0.5), 8192)
        self.assertEqual(self.modifier(make_calc("necrozma", "machamp", "psychic", attacker_ability="neuroforce"), physical=False, effectiveness=2), 5120)
        self.assertEqual(self.modifier(make_calc("kingdra", "machamp", "surf", attacker_ability="sniper"), physical=False, critical_hit=True), 6144)

    # Expert Belt gives 1.2x on super effective hits and Life Orb gives 1.3x on everything.
    def test_expert_belt_and_life_orb(self):
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle", attacker_item="expert-belt"), effectiveness=2), 4915)
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle", attacker_item="expert-belt")), 4096)
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle", attacker_item="life-orb")), 5324)

    # Resist Berries halve super effective dmg of their type on the first hit. Ripen makes it 1/4 and Chilan Berry works on neutral Normal moves.
    def test_resist_berries(self):
        self.assertEqual(self.modifier(make_calc("charizard", "scizor", "flamethrower", defender_item="occa-berry"), physical=False, effectiveness=4), 2048)
        self.assertEqual(self.modifier(make_calc("charizard", "snorlax", "flamethrower", defender_item="occa-berry"), physical=False), 4096)
        self.assertEqual(self.modifier(make_calc("charizard", "scizor", "flamethrower", defender_ability="ripen", defender_item="occa-berry"), physical=False, effectiveness=4), 1024)
        self.assertEqual(self.modifier(make_calc("charizard", "scizor", "flamethrower", defender_item="occa-berry"), physical=False, effectiveness=4, first_hit=False), 4096)
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle", defender_item="chilan-berry")), 2048)

    # Unnerve stops the defender from eating its Berry.
    def test_unnerve(self):
        self.assertEqual(self.modifier(make_calc("charizard", "scizor", "flamethrower", attacker_ability="unnerve", defender_item="occa-berry"), physical=False, effectiveness=4), 4096)

    # Modifiers combine and round after each one. Reflect and Life Orb is 2662.5, which rounds down to 2662.
    def test_modifiers_stack(self):
        self.assertEqual(self.modifier(make_calc("snorlax", "machamp", "tackle", attacker_item="life-orb"), reflect=True), 2662)

class DamageCalcTests(TestCase):
    fixtures = ["pokedata"]

    # Calls calculate() and returns the lowest and highest dmg roll.
    def damage(self, calc, **options):
        result = calc.calculate(**options)
        return (result["min_damage"], result["max_damage"])

    # A level 50 Machamp's Close Combat on a level 50 Snorlax.
    def test_basic_damage(self):
        result = make_calc("machamp", "snorlax", "close-combat").calculate()
        self.assertEqual((result["min_damage"], result["max_damage"]), (240, 284))
        self.assertEqual(len(result["rolls"]), 16)
        self.assertEqual(result["ko_chance"], "Guaranteed OHKO")

    # 252 Atk Jolly Garchomp's Earthquake on 4 HP Heatran.
    def test_evs_and_nature(self):
        result = make_calc("garchomp", "heatran", "earthquake", attacker_build={"evs": {"hp": 4, "attack": 252, "speed": 252}, "nature": "jolly"}, defender_build={"evs": {"hp": 4}}).calculate()
        self.assertEqual((result["min_damage"], result["max_damage"]), (328, 388))

    # A crit at +2 Attack.
    def test_crit_and_boosts(self):
        result = make_calc("machamp", "snorlax", "close-combat").calculate(critical_hit=True, attacker_boosts={"attack": 2})
        self.assertEqual((result["min_damage"], result["max_damage"]), (716, 846))

    # Sun boosts Fire moves.
    def test_weather(self):
        result = make_calc("charizard", "venusaur", "flamethrower", weather="sun").calculate()
        self.assertEqual((result["min_damage"], result["max_damage"]), (168, 198))

    # Huge Power and Choice Band stack.
    def test_ability_and_item(self):
        result = make_calc("azumarill", "snorlax", "aqua-tail", attacker_ability="huge-power", attacker_item="choice-band").calculate()
        self.assertEqual((result["min_damage"], result["max_damage"]), (126, 148))

    # Multiscale halves the dmg at full HP.
    def test_multiscale(self):
        result = make_calc("dragonite", "dragonite", "outrage", attacker_ability="inner-focus", defender_ability="multiscale").calculate()
        self.assertEqual((result["min_damage"], result["max_damage"]), (91, 108))

    # A burned Pokémon's physical moves do half dmg.
    def test_burn(self):
        calc = DamageCalculator(Species.objects.get(name="snorlax"), Species.objects.get(name="machamp"), "normal", 85, "body-slam", "burn", None)
        result = calc.calculate()
        self.assertEqual((result["min_damage"], result["max_damage"]), (31, 37))

    # Skill Link makes Icicle Spear hit 5 times. Thick Fat halves each hit.
    def test_multi_hit(self):
        result = make_calc("cloyster", "snorlax", "icicle-spear", attacker_ability="skill-link", defender_ability="thick-fat").calculate()
        self.assertEqual(result["hits"], 5)
        self.assertEqual((result["min_damage"], result["max_damage"]), (50, 65))

    # Red Orb turns Groudon into Primal Groudon.
    def test_primal_groudon(self):
        result = make_calc("groudon", "snorlax", "precipice-blades", attacker_item="red-orb", weather="extreme-sun").calculate()
        self.assertEqual((result["min_damage"], result["max_damage"]), (160, 189))

    # Immunities do no dmg.
    def test_immunities(self):
        self.assertEqual(make_calc("snorlax", "gengar", "tackle").calculate()["max_damage"], 0)
        self.assertEqual(make_calc("garchomp", "heatran", "earthquake", defender_item="air-balloon").calculate()["max_damage"], 0)
        self.assertEqual(make_calc("garchomp", "rotom", "earthquake", defender_ability="levitate").calculate()["max_damage"], 0)

    # Seismic Toss does dmg equal to the user's level.
    def test_fixed_damage(self):
        result = make_calc("machamp", "snorlax", "seismic-toss", attacker_build={"level": 37}).calculate()
        self.assertEqual(result["rolls"], [37] * 16)

    # Status moves don't do dmg.
    def test_status_move(self):
        result = make_calc("machamp", "snorlax", "growl").calculate()
        self.assertEqual(result["max_damage"], 0)
        self.assertEqual(result["note"], "Status moves don't do damage.")

    # calculate() puts the calculator back how it was, so it can be run again.
    def test_calculate_twice(self):
        calc = make_calc("groudon", "snorlax", "precipice-blades", attacker_item="red-orb", weather="extreme-sun")
        first = calc.calculate()
        self.assertEqual(calc.attacker.name, "groudon")
        self.assertEqual(calc.calculate(), first)

    # Reflect halves physical dmg and Light Screen halves special dmg. Crits go through screens.
    def test_screens(self):
        reflect = make_calc("machamp", "snorlax", "close-combat").calculate(reflect=True)
        self.assertEqual((reflect["min_damage"], reflect["max_damage"]), (120, 142))
        light_screen = make_calc("charizard", "venusaur", "flamethrower").calculate(light_screen=True)
        self.assertEqual((light_screen["min_damage"], light_screen["max_damage"]), (55, 66))
        crit = make_calc("machamp", "snorlax", "close-combat").calculate(critical_hit=True, reflect=True)
        self.assertEqual((crit["min_damage"], crit["max_damage"]), (360, 426))

    # The % is out of the defender's max HP, but the KO chance goes by its current HP.
    def test_percent_and_ko_text(self):
        result = make_calc("garchomp", "snorlax", "earthquake").calculate()
        self.assertEqual((result["min_percent"], result["max_percent"]), (42.5, 50.2))
        self.assertEqual(result["ko_chance"], "Possible 2HKO")
        hurt = make_calc("garchomp", "snorlax", "earthquake").calculate(defender_hp=150)
        self.assertEqual((hurt["min_percent"], hurt["max_percent"]), (42.5, 50.2))
        self.assertEqual(hurt["ko_chance"], "Guaranteed 2HKO")

    # When only some rolls KO, it says the chance. 7 of the 16 rolls KO here.
    def test_ohko_chance(self):
        result = make_calc("gengar", "alakazam", "shadow-ball").calculate()
        self.assertEqual((result["min_damage"], result["max_damage"]), (116, 140))
        self.assertEqual(result["ko_chance"], "43.8% chance to OHKO")

    # Triple Axel hits 3 times with 20, 40 and 60 power.
    def test_triple_axel(self):
        result = make_calc("weavile", "garchomp", "triple-axel").calculate()
        self.assertEqual(result["hits"], 3)
        self.assertEqual((result["min_damage"], result["max_damage"]), (340, 412))

    # Moves that can't hit or can't be calculated yet say why in the note.
    def test_notes(self):
        self.assertEqual(make_calc("garchomp", "dragonite", "earthquake").calculate()["note"], "The move doesn't affect the target.")
        self.assertEqual(make_calc("machamp", "snorlax", "counter").calculate()["note"], "This move's damage can't be calculated yet.")
        self.assertIsNone(make_calc("machamp", "snorlax", "close-combat").calculate()["note"])

    # Adaptability makes STAB 2x instead of 1.5x. Technician boosts Bullet Punch to 60 power.
    def test_adaptability_and_technician(self):
        self.assertEqual(self.damage(make_calc("porygon-z", "snorlax", "hyper-beam", attacker_ability="adaptability")), (136, 160))
        result = make_calc("scizor", "gardevoir", "bullet-punch", attacker_ability="technician").calculate()
        self.assertEqual(result["base_power"], 60)
        self.assertEqual((result["min_damage"], result["max_damage"]), (120, 144))
        self.assertEqual(result["ko_chance"], "6.2% chance to OHKO")

    # 4x super effective and not very effective hits.
    def test_type_effectiveness(self):
        result = make_calc("lapras", "garchomp", "ice-beam").calculate()
        self.assertEqual(result["effectiveness"], 4)
        self.assertEqual((result["min_damage"], result["max_damage"]), (204, 244))
        resisted = make_calc("charizard", "blastoise", "flamethrower").calculate()
        self.assertEqual(resisted["effectiveness"], 0.5)
        self.assertEqual((resisted["min_damage"], resisted["max_damage"]), (26, 31))

    # Rain boosts Water moves and weakens Fire moves.
    def test_rain(self):
        surf = make_calc("blastoise", "charizard", "surf", weather="rain").calculate()
        self.assertEqual((surf["min_damage"], surf["max_damage"]), (152, 182))
        self.assertEqual(surf["ko_chance"], "93.8% chance to OHKO")
        self.assertEqual(self.damage(make_calc("charizard", "venusaur", "flamethrower", weather="rain")), (54, 66))

    # Electric Terrain boosts Electric moves and Grassy Terrain halves Earthquake.
    def test_terrain(self):
        electric = DamageCalculator(Species.objects.get(name="pikachu"), Species.objects.get(name="gyarados"), "electric", 90, "thunderbolt", None, None, terrain="electric-terrain")
        self.assertEqual(self.damage(electric), (160, 192))
        grassy = DamageCalculator(Species.objects.get(name="garchomp"), Species.objects.get(name="snorlax"), "ground", 100, "earthquake", None, None, terrain="grassy-terrain")
        self.assertEqual(self.damage(grassy), (51, 60))

    # Life Orb boosts everything, Expert Belt boosts super effective hits, and Sheer Force still gets the Life Orb boost.
    def test_life_orb_and_expert_belt(self):
        self.assertEqual(self.damage(make_calc("garchomp", "snorlax", "earthquake", attacker_item="life-orb")), (130, 153))
        self.assertEqual(self.damage(make_calc("garchomp", "heatran", "earthquake", attacker_item="expert-belt")), (322, 389))
        self.assertEqual(self.damage(make_calc("nidoking", "snorlax", "flamethrower", attacker_ability="sheer-force", attacker_item="life-orb")), (47, 56))

    # Yache Berry halves a super effective Ice move. On a multi-hit move it only halves the first hit.
    def test_resist_berries(self):
        self.assertEqual(self.damage(make_calc("lapras", "garchomp", "ice-beam", defender_item="yache-berry")), (102, 122))
        self.assertEqual(self.damage(make_calc("cloyster", "garchomp", "icicle-spear", attacker_ability="skill-link")), (320, 380))
        self.assertEqual(self.damage(make_calc("cloyster", "garchomp", "icicle-spear", attacker_ability="skill-link", defender_item="yache-berry")), (288, 342))

    # The defender's stat boosts lower the dmg.
    def test_defender_boosts(self):
        self.assertEqual(self.damage(make_calc("machamp", "snorlax", "close-combat"), defender_boosts={"defense": 1}), (162, 192))

    # Lower level, 0 IVs and a full EV spread on both sides all change the dmg.
    def test_level_ivs_and_evs(self):
        level_30 = make_calc("machamp", "snorlax", "close-combat", attacker_build={"level": 30}).calculate()
        self.assertEqual((level_30["min_damage"], level_30["max_damage"]), (96, 114))
        self.assertEqual(level_30["ko_chance"], "Guaranteed 3HKO")
        zero_ivs = make_calc("machamp", "snorlax", "close-combat", attacker_build={"ivs": {"hp": 0, "attack": 0, "defense": 0, "special-attack": 0, "special-defense": 0, "speed": 0}}).calculate()
        self.assertEqual((zero_ivs["min_damage"], zero_ivs["max_damage"]), (216, 254))
        self.assertEqual(zero_ivs["ko_chance"], "50.0% chance to OHKO")
        spread = make_calc("machamp", "snorlax", "close-combat", attacker_build={"evs": {"attack": 252}, "nature": "adamant"}, defender_build={"evs": {"hp": 252, "defense": 252}, "nature": "impish"})
        self.assertEqual(self.damage(spread), (212, 252))

    # Guts ignores the burn's dmg drop and boosts Attack. Facade doubles and also ignores the burn.
    def test_guts_and_facade(self):
        guts = DamageCalculator(Species.objects.get(name="machamp"), Species.objects.get(name="snorlax"), "fighting", 120, "close-combat", "burn", None, attacker_ability="guts")
        self.assertEqual(self.damage(guts), (356, 422))
        facade = DamageCalculator(Species.objects.get(name="snorlax"), Species.objects.get(name="machamp"), "normal", 70, "facade", "burn", None)
        self.assertEqual(self.damage(facade), (103, 123))

    # Assault Vest boosts Sp. Def and Eviolite boosts Chansey's Defense.
    def test_assault_vest_and_eviolite(self):
        self.assertEqual(self.damage(make_calc("gengar", "snorlax", "sludge-bomb", defender_item="assault-vest")), (40, 48))
        self.assertEqual(self.damage(make_calc("machamp", "chansey", "close-combat", defender_item="eviolite")), (548, 648))

    # Foul Play uses the target's Attack, Body Press uses Defense, and Psyshock hits Defense.
    def test_moves_that_use_other_stats(self):
        self.assertEqual(self.damage(make_calc("umbreon", "garchomp", "foul-play")), (70, 84))
        self.assertEqual(self.damage(make_calc("corviknight", "snorlax", "body-press")), (90, 106))
        self.assertEqual(self.damage(make_calc("alakazam", "blissey", "psyshock")), (232, 274))

    # Knock Off, Low Kick, Eruption and Gyro Ball get their power worked out before the dmg.
    def test_variable_power_moves(self):
        knock_off = make_calc("weavile", "alakazam", "knock-off", defender_item="leftovers").calculate()
        self.assertEqual((knock_off["base_power"], knock_off["min_damage"], knock_off["max_damage"]), (97, 236, 278))
        self.assertEqual(make_calc("machamp", "snorlax", "low-kick").calculate()["base_power"], 120)
        eruption = make_calc("typhlosion", "snorlax", "eruption").calculate(attacker_hp=50)
        self.assertEqual((eruption["base_power"], eruption["min_damage"], eruption["max_damage"]), (49, 28, 34))
        gyro_ball = make_calc("ferrothorn", "weavile", "gyro-ball").calculate()
        self.assertEqual((gyro_ball["base_power"], gyro_ball["min_damage"], gyro_ball["max_damage"]), (91, 138, 164))

    # Sandstorm boosts Tyranitar's Sp. Def.
    def test_sandstorm(self):
        self.assertEqual(self.damage(make_calc("gardevoir", "tyranitar", "moonblast", weather="sandstorm")), (86, 104))

    # Sacred Sword ignores the defender's Defense boosts and Unaware ignores the attacker's Attack boosts.
    def test_ignoring_stat_changes(self):
        self.assertEqual(self.damage(make_calc("gallade", "snorlax", "sacred-sword"), defender_boosts={"defense": 2}), (174, 206))
        self.assertEqual(self.damage(make_calc("machamp", "snorlax", "close-combat", defender_ability="unaware"), attacker_boosts={"attack": 2}), (240, 284))

    # Filter lowers super effective dmg and Fluffy doubles Fire dmg.
    def test_filter_and_fluffy(self):
        self.assertEqual(self.damage(make_calc("lapras", "garchomp", "ice-beam", defender_ability="filter")), (153, 183))
        self.assertEqual(self.damage(make_calc("charizard", "dubwool", "flamethrower", defender_ability="fluffy")), (120, 144))

    # Tinted Lens doubles a 1/4 effective hit and Sniper boosts crits.
    def test_tinted_lens_and_sniper(self):
        self.assertEqual(self.damage(make_calc("butterfree", "charizard", "bug-buzz", attacker_ability="tinted-lens")), (26, 32))
        self.assertEqual(self.damage(make_calc("kingdra", "snorlax", "surf", attacker_ability="sniper"), critical_hit=True), (103, 123))

    # Loaded Dice makes Bullet Seed hit 4 times.
    def test_loaded_dice(self):
        result = make_calc("cinccino", "snorlax", "bullet-seed", attacker_item="loaded-dice").calculate()
        self.assertEqual(result["hits"], 4)
        self.assertEqual((result["min_damage"], result["max_damage"]), (52, 64))

    # Spectral Thief steals the target's boosts, Meteor Beam raises Sp. Atk before hitting and Photon Geyser turns physical when Attack is higher.
    def test_stat_changing_moves(self):
        self.assertEqual(self.damage(make_calc("marshadow", "garchomp", "spectral-thief"), defender_boosts={"attack": 2}), (127, 151))
        self.assertEqual(self.damage(make_calc("gardevoir", "snorlax", "meteor-beam")), (76, 90))
        photon_geyser = make_calc("necrozma", "snorlax", "photon-geyser").calculate(attacker_boosts={"attack": 2})
        self.assertEqual(photon_geyser["category"], "physical")
        self.assertEqual((photon_geyser["min_damage"], photon_geyser["max_damage"]), (169, 199))

    # Freeze-Dry is super effective on Water types, Scrappy hits Ghost types with Normal moves and Mold Breaker ignores Levitate.
    def test_type_tricks(self):
        freeze_dry = make_calc("lapras", "gyarados", "freeze-dry").calculate()
        self.assertEqual(freeze_dry["effectiveness"], 4)
        self.assertEqual((freeze_dry["min_damage"], freeze_dry["max_damage"]), (136, 168))
        self.assertEqual(self.damage(make_calc("kangaskhan", "gengar", "body-slam", attacker_ability="scrappy")), (69, 82))
        self.assertEqual(self.damage(make_calc("excadrill", "rotom", "earthquake", attacker_ability="mold-breaker", defender_ability="levitate")), (182, 216))

    # Wonder Guard only lets super effective moves hit, and Fire moves fail in heavy rain.
    def test_moves_that_fail(self):
        blocked = make_calc("garchomp", "shedinja", "earthquake", defender_ability="wonder-guard").calculate()
        self.assertEqual(blocked["note"], "The move doesn't affect the target.")
        self.assertEqual(make_calc("garchomp", "shedinja", "fire-fang", defender_ability="wonder-guard").calculate()["ko_chance"], "Guaranteed OHKO")
        heavy_rain = make_calc("charizard", "snorlax", "flamethrower", weather="heavy-rain").calculate()
        self.assertEqual((heavy_rain["max_damage"], heavy_rain["note"]), (0, "The move doesn't affect the target."))

    # Battle Armor blocks crits and Frost Breath always crits.
    def test_crit_rules(self):
        blocked = make_calc("machamp", "snorlax", "close-combat", defender_ability="battle-armor").calculate(critical_hit=True)
        self.assertFalse(blocked["critical_hit"])
        self.assertEqual((blocked["min_damage"], blocked["max_damage"]), (240, 284))
        frost_breath = make_calc("lapras", "garchomp", "frost-breath").calculate()
        self.assertTrue(frost_breath["critical_hit"])
        self.assertEqual((frost_breath["min_damage"], frost_breath["max_damage"]), (208, 252))

    # Sword of Ruin lowers the target's Defense and Booster Energy boosts Great Tusk's Attack.
    def test_ruin_and_booster_energy(self):
        self.assertEqual(self.damage(make_calc("chien-pao", "garchomp", "icicle-crash")), (312, 372))
        self.assertEqual(self.damage(make_calc("great-tusk", "snorlax", "headlong-rush", attacker_item="booster-energy")), (156, 184))