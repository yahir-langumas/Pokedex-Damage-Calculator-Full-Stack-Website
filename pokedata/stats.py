# Stat Calculator

# Each nature's raised and lowered stat. Neutral natures don't change any stats.
NATURES = {
    "hardy": (None, None), "lonely": ("attack", "defense"), "brave": ("attack", "speed"), "adamant": ("attack", "special-attack"), "naughty": ("attack", "special-defense"),
    "bold": ("defense", "attack"), "docile": (None, None), "relaxed": ("defense", "speed"), "impish": ("defense", "special-attack"), "lax": ("defense", "special-defense"),
    "timid": ("speed", "attack"), "hasty": ("speed", "defense"), "serious": (None, None), "jolly": ("speed", "special-attack"), "naive": ("speed", "special-defense"),
    "modest": ("special-attack", "attack"), "mild": ("special-attack", "defense"), "quiet": ("special-attack", "speed"), "bashful": (None, None), "rash": ("special-attack", "special-defense"),
    "calm": ("special-defense", "attack"), "gentle": ("special-defense", "defense"), "sassy": ("special-defense", "speed"), "careful": ("special-defense", "special-attack"), "quirky": (None, None),
}

STAT_NAMES = ("hp", "attack", "defense", "special-attack", "special-defense", "speed")

# Level 50 is the default since most competitive formats use it (VCG, Singles). Level 50 is also the max for now. 
MIN_LEVEL = 1
MAX_LEVEL = 50
DEFAULT_LEVEL = 50
DEFAULT_NATURE = "serious"

# EVs go from 0 to 252 per stat, with 510 total. IVs go from 0 to 31.
MAX_EV = 252
MAX_TOTAL_EVS = 510
MAX_IV = 31


# Fills in anything missing from a build with the defaults (level 50, 0 EVs, 31 IVs, neutral nature) and checks the numbers are allowed.
# build = {"level": 50, "evs": {"attack": 252, "speed": 252}, "ivs": {"speed": 0}, "nature": "adamant"}. Every part is optional.
def make_build(build=None):
    build = build or {}
    level = build.get("level", DEFAULT_LEVEL)
    nature = build.get("nature", DEFAULT_NATURE)
    evs = {stat: build.get("evs", {}).get(stat, 0) for stat in STAT_NAMES}
    ivs = {stat: build.get("ivs", {}).get(stat, MAX_IV) for stat in STAT_NAMES}
    if not isinstance(level, int) or not MIN_LEVEL <= level <= MAX_LEVEL:
        raise ValueError(f"Level has to be between {MIN_LEVEL} and {MAX_LEVEL}.")
    if nature not in NATURES:
        raise ValueError(f"{nature} isn't a nature.")
    for stat in STAT_NAMES:
        if not isinstance(evs[stat], int) or not 0 <= evs[stat] <= MAX_EV:
            raise ValueError(f"{stat} EVs have to be between 0 and {MAX_EV}.")
        if not isinstance(ivs[stat], int) or not 0 <= ivs[stat] <= MAX_IV:
            raise ValueError(f"{stat} IVs have to be between 0 and {MAX_IV}.")
    if sum(evs.values()) > MAX_TOTAL_EVS:
        raise ValueError(f"EVs can't add up to more than {MAX_TOTAL_EVS}.")
    return {"level": level, "evs": evs, "ivs": ivs, "nature": nature}


# Turns base stats into real stats using the build's level, EVs, IVs and nature. Returns the real stats.
# Except for Shedinja, which always has 1 HP.
def calculate_stats(base_stats, build=None, pokedex_id=None):
    build = make_build(build)
    level = build["level"]
    raised, lowered = NATURES[build["nature"]]
    stats = {}
    for stat in STAT_NAMES:
        core = (2 * base_stats[stat] + build["ivs"][stat] + build["evs"][stat] // 4) * level // 100
        if stat == "hp":
            stats[stat] = 1 if pokedex_id == 292 else core + level + 10 # Shedinja 
        elif stat == raised:
            stats[stat] = (core + 5) * 11 // 10
        elif stat == lowered:
            stats[stat] = (core + 5) * 9 // 10
        else:
            stats[stat] = core + 5
    return stats