# DMG Calculator
from pokedata.models import Species
from pokedata.models import Moves
from pokedata.models import Learnset
from pokedata.models import Type
from pokedata.stats import NATURES, calculate_stats, make_build
import random
import math
import copy

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
    "comatose": "all", "purifying-salt": "all", "thermal-exchange": "burn",
}

# Effects that aren't major statuses but some abilities still block. Since Gen 8, Oblivious, Own Tempo, and Inner Focus also block Intimidate.
VOLATILE_IMMUNITY_ABILITIES = {
    "oblivious": {"infatuation", "taunt", "intimidate"},
    "own-tempo": {"confusion", "intimidate"},
    "inner-focus": {"flinch", "intimidate"},
    "aroma-veil": {"infatuation", "taunt", "torment", "encore", "disable", "heal-block"},
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

# Moves Normalize doesn't change to Normal type. Refrigerate, Pixilate, Aerilate and Galvanize skip these too.
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
    "ability-shield", "macho-brace", "power-anklet", "power-band", "power-belt", "power-bracer", "power-lens", "power-weight",
}

# Recoil and crash moves Reckless boosts.
RECKLESS_MOVES = {
    "axe-kick", "brave-bird", "double-edge", "flare-blitz", "head-charge", "head-smash",
    "high-jump-kick", "jump-kick", "light-of-ruin", "submission", "supercell-slam",
    "take-down", "volt-tackle", "wave-crash", "wild-charge", "wood-hammer",
}

# Moves with added effects that Sheer Force boosts.
SHEER_FORCE_MOVES = {
    "acid", "acid-spray", "air-slash", "alluring-voice", "anchor-shot", "ancient-power",
    "apple-acid", "aqua-step", "astonish", "aura-wheel", "aurora-beam", "axe-kick",
    "barb-barrage", "bite", "bitter-malice", "blaze-kick", "blazing-torque",
    "bleakwind-storm", "blizzard", "blue-flare", "body-slam", "bolt-strike",
    "bone-club", "bounce", "breaking-swipe", "bubble", "bubble-beam", "bug-buzz",
    "bulldoze", "burning-jealousy", "ceaseless-edge", "charge-beam", "chatter",
    "chilling-water", "combat-torque", "confusion", "constrict", "cross-poison",
    "crunch", "crush-claw", "dark-pulse", "diamond-storm", "dire-claw", "discharge",
    "dizzy-punch", "double-iron-bash", "dragon-breath", "dragon-rush", "drum-beating",
    "dynamic-punch", "earth-power", "eerie-spell", "electro-shot", "electroweb",
    "ember", "energy-ball", "esper-wing", "extrasensory", "fake-out", "fiery-dance",
    "fiery-wrath", "fire-blast", "fire-fang", "fire-lash", "fire-punch", "flame-charge",
    "flame-wheel", "flamethrower", "flare-blitz", "flash-cannon", "focus-blast",
    "force-palm", "freeze-dry", "freeze-shock", "freezing-glare", "glaciate",
    "grav-apple", "gunk-shot", "headbutt", "heart-stamp", "heat-wave", "hurricane",
    "hyper-fang", "ice-beam", "ice-burn", "ice-fang", "ice-punch", "icicle-crash",
    "icy-wind", "infernal-parade", "inferno", "iron-head", "iron-tail", "lava-plume",
    "leaf-tornado", "lick", "liquidation", "low-sweep", "lumina-crash", "lunge",
    "luster-purge", "magical-torque", "malignant-chain", "matcha-gotcha", "metal-claw",
    "meteor-mash", "mirror-shot", "mist-ball", "moonblast", "mortal-spin",
    "mountain-gale", "mud-bomb", "mud-shot", "mud-slap", "muddy-water", "mystical-fire",
    "mystical-power", "needle-arm", "night-daze", "noxious-torque", "nuzzle",
    "octazooka", "ominous-wind", "order-up", "play-rough", "poison-fang", "poison-jab",
    "poison-sting", "poison-tail", "pounce", "powder-snow", "power-up-punch", "psybeam",
    "psychic", "psychic-noise", "psyshield-bash", "pyro-ball", "rapid-spin",
    "razor-shell", "relic-song", "rock-climb", "rock-slide", "rock-smash", "rock-tomb",
    "rolling-kick", "sacred-fire", "salt-cure", "sandsear-storm", "scald",
    "scorching-sands", "searing-shot", "secret-power", "seed-flare", "shadow-ball",
    "shadow-bone", "shell-side-arm", "signal-beam", "silver-wind", "skitter-smack",
    "sky-attack", "sludge", "sludge-bomb", "sludge-wave", "smog", "snarl", "snore",
    "spark", "sparkling-aria", "spirit-break", "spirit-shackle", "springtide-storm",
    "steam-eruption", "steamroller", "steel-wing", "stomp", "stone-axe",
    "strange-steam", "struggle-bug", "syrup-bomb", "throat-chop", "thunder",
    "thunder-fang", "thunder-punch", "thunder-shock", "thunderbolt", "thunderous-kick",
    "torch-song", "trailblaze", "tri-attack", "triple-arrows", "trop-kick", "twineedle",
    "twister", "upper-hand", "volt-tackle", "water-pulse", "waterfall", "wicked-torque",
    "wildbolt-storm", "zap-cannon", "zen-headbutt", "zing-zap",
}

# The type each Plate gives Arceus with Multitype.
PLATE_TYPES = {
    "draco-plate": "dragon", "dread-plate": "dark", "earth-plate": "ground", "fist-plate": "fighting",
    "flame-plate": "fire", "icicle-plate": "ice", "insect-plate": "bug", "iron-plate": "steel",
    "meadow-plate": "grass", "mind-plate": "psychic", "pixie-plate": "fairy", "sky-plate": "flying",
    "splash-plate": "water", "spooky-plate": "ghost", "stone-plate": "rock", "toxic-plate": "poison",
    "zap-plate": "electric",
}

# Abilities that can't be replaced or suppressed (Mummy can't change these).
CANT_SUPPRESS_ABILITIES = {
    "as-one-glastrier", "as-one-spectrier", "battle-bond", "comatose", "disguise", "gulp-missile",
    "ice-face", "multitype", "power-construct", "rks-system", "schooling", "shields-down",
    "stance-change", "tera-shift", "zen-mode", "zero-to-hero",
}

# Status moves Magic Bounce bounces back.
REFLECTABLE_MOVES = {
    "attract", "baby-doll-eyes", "block", "captivate", "charm", "confide",
    "confuse-ray", "corrosive-gas", "cotton-spore", "dark-void", "defog", "disable",
    "eerie-impulse", "embargo", "encore", "entrainment", "fake-tears", "feather-dance",
    "flash", "flatter", "floral-healing", "foresight", "forests-curse", "gastro-acid",
    "glare", "grass-whistle", "growl", "heal-block", "heal-pulse", "hypnosis",
    "kinesis", "leech-seed", "leer", "lovely-kiss", "magic-powder", "mean-look",
    "metal-sound", "miracle-eye", "noble-roar", "odor-sleuth", "parting-shot",
    "play-nice", "poison-gas", "poison-powder", "powder", "purify", "roar",
    "sand-attack", "scary-face", "screech", "simple-beam", "sing", "sleep-powder",
    "smokescreen", "soak", "spicy-extract", "spider-web", "spikes", "spite", "spore",
    "spotlight", "stealth-rock", "sticky-web", "strength-sap", "string-shot",
    "stun-spore", "supersonic", "swagger", "sweet-kiss", "sweet-scent", "tail-whip",
    "tar-shot", "taunt", "tearful-look", "telekinesis", "thunder-wave", "tickle",
    "topsy-turvy", "torment", "toxic", "toxic-spikes", "toxic-thread", "trick-or-treat",
    "venom-drench", "whirlwind", "will-o-wisp", "worry-seed", "yawn",
}

# Status moves aimed at the target (Dark types are immune to these when Prankster boosts them).
TARGETED_STATUS_MOVES = {
    "after-you", "attract", "baby-doll-eyes", "bestow", "block", "captivate", "charm",
    "confide", "confuse-ray", "conversion-2", "corrosive-gas", "cotton-spore", "curse",
    "dark-void", "decorate", "defog", "disable", "doodle", "eerie-impulse", "electrify",
    "embargo", "encore", "entrainment", "fake-tears", "feather-dance", "flash",
    "flatter", "floral-healing", "foresight", "forests-curse", "gastro-acid", "glare",
    "grass-whistle", "growl", "guard-split", "guard-swap", "heal-block", "heal-pulse",
    "heart-swap", "hypnosis", "instruct", "kinesis", "leech-seed", "leer", "lock-on",
    "lovely-kiss", "magic-powder", "me-first", "mean-look", "memento", "metal-sound",
    "mimic", "mind-reader", "miracle-eye", "mirror-move", "nature-power", "nightmare",
    "noble-roar", "octolock", "odor-sleuth", "pain-split", "parting-shot", "play-nice",
    "poison-gas", "poison-powder", "powder", "power-split", "power-swap", "psych-up",
    "psycho-shift", "purify", "quash", "reflect-type", "roar", "role-play",
    "sand-attack", "scary-face", "screech", "simple-beam", "sing", "sketch",
    "skill-swap", "sleep-powder", "smokescreen", "soak", "speed-swap", "spicy-extract",
    "spider-web", "spite", "spore", "spotlight", "strength-sap", "string-shot",
    "stun-spore", "supersonic", "swagger", "sweet-kiss", "sweet-scent", "switcheroo",
    "tail-whip", "tar-shot", "taunt", "tearful-look", "teeter-dance", "telekinesis",
    "thunder-wave", "tickle", "topsy-turvy", "torment", "toxic", "toxic-thread",
    "transform", "trick", "trick-or-treat", "venom-drench", "whirlwind", "will-o-wisp",
    "worry-seed", "yawn",
}

# Forms some Pokémon change into during battle. The database only has the default forms, so these are hard coded.
# These are base stats. Run them through calculate_stats to get the real stats.
BATTLE_FORMS = {
    "darmanitan-zen": {"types": ["fire", "psychic"], "stats": {"hp": 105, "attack": 30, "defense": 105, "special-attack": 140, "special-defense": 105, "speed": 55}},
    "aegislash-blade": {"types": ["steel", "ghost"], "stats": {"hp": 60, "attack": 140, "defense": 50, "special-attack": 140, "special-defense": 50, "speed": 60}},
    "minior-core": {"types": ["rock", "flying"], "stats": {"hp": 60, "attack": 100, "defense": 60, "special-attack": 100, "special-defense": 60, "speed": 120}},
    "wishiwashi-school": {"types": ["water"], "stats": {"hp": 45, "attack": 140, "defense": 130, "special-attack": 140, "special-defense": 135, "speed": 30}},
    "zygarde-complete": {"types": ["dragon", "ground"], "stats": {"hp": 216, "attack": 100, "defense": 121, "special-attack": 91, "special-defense": 95, "speed": 85}},
    "eiscue-noice": {"types": ["ice"], "stats": {"hp": 75, "attack": 80, "defense": 70, "special-attack": 65, "special-defense": 50, "speed": 130}},
    "palafin-hero": {"types": ["water"], "stats": {"hp": 100, "attack": 160, "defense": 97, "special-attack": 106, "special-defense": 87, "speed": 100}},
    "terapagos-terastal": {"types": ["normal"], "stats": {"hp": 95, "attack": 95, "defense": 110, "special-attack": 105, "special-defense": 110, "speed": 85}},
    "groudon-primal": {"types": ["ground", "fire"], "stats": {"hp": 100, "attack": 180, "defense": 160, "special-attack": 150, "special-defense": 90, "speed": 90}},
    "kyogre-primal": {"types": ["water"], "stats": {"hp": 100, "attack": 150, "defense": 90, "special-attack": 180, "special-defense": 160, "speed": 90}},
    "dialga-origin": {"types": ["steel", "dragon"], "stats": {"hp": 100, "attack": 100, "defense": 120, "special-attack": 150, "special-defense": 120, "speed": 90}},
    "palkia-origin": {"types": ["water", "dragon"], "stats": {"hp": 90, "attack": 100, "defense": 100, "special-attack": 150, "special-defense": 120, "speed": 120}},
    "giratina-origin": {"types": ["ghost", "dragon"], "stats": {"hp": 150, "attack": 120, "defense": 100, "special-attack": 120, "special-defense": 100, "speed": 90}},
}

# Moves Parental Bond doesn't make hit twice (charge moves, future moves and moves that only work once).
PARENTAL_BOND_EXCEPTIONS = {
    "bounce", "dig", "dive", "doom-desire", "dragon-darts", "dynamax-cannon", "electro-shot",
    "endeavor", "explosion", "final-gambit", "fling", "fly", "freeze-shock", "future-sight",
    "ice-ball", "ice-burn", "meteor-beam", "phantom-force", "razor-wind", "rollout",
    "self-destruct", "shadow-force", "skull-bash", "sky-attack", "sky-drop", "solar-beam",
    "solar-blade",
}

# Healing moves Triage gives +3 priority.
HEALING_MOVES = {
    "absorb", "bitter-blade", "drain-punch", "draining-kiss", "dream-eater",
    "floral-healing", "giga-drain", "heal-order", "heal-pulse", "healing-wish",
    "horn-leech", "jungle-healing", "leech-life", "life-dew", "lunar-blessing",
    "lunar-dance", "matcha-gotcha", "mega-drain", "milk-drink", "moonlight",
    "morning-sun", "oblivion-wing", "parabolic-charge", "purify", "recover", "rest",
    "revival-blessing", "roost", "shore-up", "slack-off", "soft-boiled", "strength-sap",
    "swallow", "synthesis", "wish",
}

# Dance moves Dancer copies.
DANCE_MOVES = {
    "aqua-step", "clangorous-soul", "dragon-dance", "feather-dance", "fiery-dance",
    "lunar-dance", "petal-dance", "quiver-dance", "revelation-dance", "swords-dance",
    "teeter-dance", "victory-dance",
}

# The type each Memory gives Silvally with RKS System.
MEMORY_TYPES = {
    "bug-memory": "bug", "dark-memory": "dark", "dragon-memory": "dragon", "electric-memory": "electric",
    "fairy-memory": "fairy", "fighting-memory": "fighting", "fire-memory": "fire", "flying-memory": "flying",
    "ghost-memory": "ghost", "grass-memory": "grass", "ground-memory": "ground", "ice-memory": "ice",
    "poison-memory": "poison", "psychic-memory": "psychic", "rock-memory": "rock", "steel-memory": "steel",
    "water-memory": "water",
}

# Abilities Receiver and Power of Alchemy can't copy. Same as Trace plus Wonder Guard.
RECEIVER_BANNED_ABILITIES = TRACE_BANNED_ABILITIES | {"wonder-guard"}

# Abilities that can't be swapped (Wandering Spirit and Skill Swap fail with these).
SKILL_SWAP_BANNED_ABILITIES = {
    "as-one-glastrier", "as-one-spectrier", "battle-bond", "comatose", "commander", "disguise",
    "embody-aspect", "hunger-switch", "ice-face", "illusion", "multitype", "neutralizing-gas",
    "poison-puppeteer", "power-construct", "protosynthesis", "quark-drive", "rks-system", "schooling",
    "shields-down", "stance-change", "tera-shell", "tera-shift", "teraform-zero", "wonder-guard",
    "zen-mode", "zero-to-hero",
}

# The type each terrain gives a Pokémon with Mimicry.
MIMICRY_TYPES = {
    "electric-terrain": "electric", "grassy-terrain": "grass", "misty-terrain": "fairy", "psychic-terrain": "psychic",
}

# The stat Embody Aspect raises for each of Ogerpon's masks. No mask (Teal) raises Speed.
EMBODY_ASPECT_STATS = {
    "teal-mask": "speed", "wellspring-mask": "special-defense", "hearthflame-mask": "attack", "cornerstone-mask": "defense",
}

# Healing Berries that also confuse the Pokémon if its nature lowers this stat (it dislikes the flavor).
CONFUSION_BERRIES = {
    "figy-berry": "attack", "wiki-berry": "special-attack", "mago-berry": "speed", "aguav-berry": "special-defense", "iapapa-berry": "defense",
}

# The move type each resist Berry weakens. Chilan Berry works on any Normal move, the rest only on super-effective hits.
RESIST_BERRIES = {
    "occa-berry": "fire", "passho-berry": "water", "wacan-berry": "electric", "rindo-berry": "grass", "yache-berry": "ice",
    "chople-berry": "fighting", "kebia-berry": "poison", "shuca-berry": "ground", "coba-berry": "flying", "payapa-berry": "psychic",
    "tanga-berry": "bug", "charti-berry": "rock", "kasib-berry": "ghost", "haban-berry": "dragon", "colbur-berry": "dark",
    "babiri-berry": "steel", "chilan-berry": "normal", "roseli-berry": "fairy",
}

# The stat each pinch Berry raises when the Pokémon's HP gets low.
PINCH_BERRIES = {
    "liechi-berry": "attack", "ganlon-berry": "defense", "salac-berry": "speed", "petaya-berry": "special-attack", "apicot-berry": "special-defense",
}

# The move type each type-boosting item powers up by 20%.
TYPE_BOOST_ITEMS = {
    "silver-powder": "bug", "metal-coat": "steel", "soft-sand": "ground", "hard-stone": "rock", "miracle-seed": "grass",
    "black-glasses": "dark", "black-belt": "fighting", "magnet": "electric", "mystic-water": "water", "sharp-beak": "flying",
    "poison-barb": "poison", "never-melt-ice": "ice", "spell-tag": "ghost", "twisted-spoon": "psychic", "charcoal": "fire",
    "dragon-fang": "dragon", "silk-scarf": "normal", "sea-incense": "water", "odd-incense": "psychic", "rock-incense": "rock",
    "wave-incense": "water", "rose-incense": "grass", "fairy-feather": "fairy",
}

# Choice items lock the Pokémon into the first move it uses.
CHOICE_ITEMS = {"choice-band", "choice-scarf", "choice-specs"}

# Two-turn moves that charge on the first turn. Power Herb skips the charging turn.
CHARGE_MOVES = {
    "bounce", "dig", "dive", "electro-shot", "fly", "freeze-shock", "geomancy", "ice-burn", "meteor-beam",
    "phantom-force", "razor-wind", "shadow-force", "skull-bash", "sky-attack", "solar-beam", "solar-blade",
}

# Power items halve the Pokémon's Speed. They still work with Klutz.
POWER_ITEMS = {"power-anklet", "power-band", "power-belt", "power-bracer", "power-lens", "power-weight"}

# The move type each Gem powers up by 30%. The Gem is used up after one move.
GEM_TYPES = {
    "fire-gem": "fire", "water-gem": "water", "electric-gem": "electric", "grass-gem": "grass", "ice-gem": "ice",
    "fighting-gem": "fighting", "poison-gem": "poison", "ground-gem": "ground", "flying-gem": "flying",
    "psychic-gem": "psychic", "bug-gem": "bug", "rock-gem": "rock", "ghost-gem": "ghost", "dragon-gem": "dragon",
    "dark-gem": "dark", "steel-gem": "steel", "normal-gem": "normal", "fairy-gem": "fairy",
}

# Moves that do a set amount of dmg. Weakness Policy doesn't activate from these.
FIXED_DAMAGE_MOVES = {
    "comeuppance", "counter", "dragon-rage", "endeavor", "final-gambit", "metal-burst", "mirror-coat",
    "natures-madness", "night-shade", "psywave", "ruination", "seismic-toss", "sonic-boom", "super-fang",
}

# The terrain each Terrain Seed activates in, and the stat it raises.
TERRAIN_SEEDS = {
    "electric-seed": ("electric-terrain", "defense"), "grassy-seed": ("grassy-terrain", "defense"),
    "misty-seed": ("misty-terrain", "special-defense"), "psychic-seed": ("psychic-terrain", "special-defense"),
}

# The Pokémon each Origin Forme item works on and the form it changes into.
ORIGIN_FORME_ITEMS = {
    "adamant-crystal": (483, "dialga-origin"), "lustrous-globe": (484, "palkia-origin"), "griseous-core": (487, "giratina-origin"),
}

# Ogerpon's masks: the type each one adds and the ability Ogerpon gets.
OGERPON_MASKS = {
    "wellspring-mask": ("water", "water-absorb"), "hearthflame-mask": ("fire", "mold-breaker"), "cornerstone-mask": ("rock", "sturdy"),
}

# Moves that always land a critical hit.
ALWAYS_CRIT_MOVES = {"flower-trick", "frost-breath", "storm-throw", "surging-strikes", "wicked-blow"}

# Moves that ignore the target's Defense and Sp. Def changes.
IGNORE_DEFENSE_STAGE_MOVES = {"chip-away", "darkest-lariat", "sacred-sword"}

# Special moves that hit the target's Defense instead of its Sp. Def.
PHYSICAL_DEFENSE_SPECIAL_MOVES = {"psyshock", "psystrike", "secret-sword"}

# Moves that ignore the target's ability, like Mold Breaker.
ABILITY_IGNORING_MOVES = {"moongeist-beam", "photon-geyser", "sunsteel-strike"}

# Moves calculate() can't work out yet, since they depend on things it doesn't track (dmg taken earlier, Stockpile, the party, random power, etc.).
UNSUPPORTED_DAMAGE_MOVES = {
    "beat-up", "bide", "comeuppance", "counter", "fling", "magnitude", "metal-burst", "mirror-coat",
    "natural-gift", "present", "psywave", "spit-up", "trump-card",
}

# Z-Moves and Max Moves. They need Z-Crystals or Dynamax, which aren't in the calc, so they're skipped. (The Z-Moves with -- in their names are skipped too.)
Z_AND_MAX_MOVES = {
    "10-000-000-volt-thunderbolt", "catastropika", "clangorous-soulblaze", "extreme-evoboost", "genesis-supernova", "guardian-of-alola",
    "lets-snuggle-forever", "light-that-burns-the-sky", "malicious-moonsault", "max-airstream", "max-darkness", "max-flare", "max-flutterby",
    "max-geyser", "max-guard", "max-hailstorm", "max-knuckle", "max-lightning", "max-mindstorm", "max-ooze", "max-overgrowth", "max-phantasm",
    "max-quake", "max-rockfall", "max-starfall", "max-steelspike", "max-strike", "max-wyrmwind", "menacing-moonraze-maelstrom", "oceanic-operetta",
    "pulverizing-pancake", "searing-sunraze-smash", "sinister-arrow-raid", "soul-stealing-7-star-strike", "splintered-stormshards", "stoked-sparksurfer",
}

# Newer multi-hit moves PokeAPI doesn't have hit counts for.
MISSING_HIT_COUNTS = {"population-bomb": 10, "tachyon-cutter": 2, "triple-dive": 3, "twin-beam": 2}

# Hidden Power's type comes from the Pokémon's IVs, in this order.
HIDDEN_POWER_TYPES = ["fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark"]

# Moves whose power is based on friendship. Max friendship gives 102 power.
FRIENDSHIP_MOVES = {"frustration", "pika-papow", "return", "veevee-volley"}

# Items Knock Off can't remove from these Pokémon, so it doesn't get its power boost. (item, pokedex number)
UNREMOVABLE_ITEMS = {
    "red-orb": 383, "blue-orb": 382, "adamant-crystal": 483, "lustrous-globe": 484, "griseous-core": 487,
    "wellspring-mask": 1017, "hearthflame-mask": 1017, "cornerstone-mask": 1017,
}

# Pokémon that can still evolve. Eviolite only works on these.
NOT_FULLY_EVOLVED = {
    "bulbasaur", "ivysaur", "charmander", "charmeleon", "squirtle", "wartortle", "caterpie", "metapod", "weedle",
    "kakuna", "pidgey", "pidgeotto", "rattata", "spearow", "ekans", "pikachu", "sandshrew", "nidoran-f", "nidorina",
    "nidoran-m", "nidorino", "clefairy", "vulpix", "jigglypuff", "zubat", "golbat", "oddish", "gloom", "paras",
    "venonat", "diglett", "meowth", "psyduck", "mankey", "primeape", "growlithe", "poliwag", "poliwhirl", "abra",
    "kadabra", "machop", "machoke", "bellsprout", "weepinbell", "tentacool", "geodude", "graveler", "ponyta",
    "slowpoke", "magnemite", "magneton", "doduo", "seel", "grimer", "shellder", "gastly", "haunter", "onix",
    "drowzee", "krabby", "voltorb", "exeggcute", "cubone", "lickitung", "koffing", "rhyhorn", "rhydon", "chansey",
    "tangela", "horsea", "seadra", "goldeen", "staryu", "scyther", "electabuzz", "magmar", "magikarp", "eevee",
    "porygon", "omanyte", "kabuto", "dratini", "dragonair", "chikorita", "bayleef", "cyndaquil", "quilava",
    "totodile", "croconaw", "sentret", "hoothoot", "ledyba", "spinarak", "chinchou", "pichu", "cleffa", "igglybuff",
    "togepi", "togetic", "natu", "mareep", "flaaffy", "marill", "hoppip", "skiploom", "aipom", "sunkern", "yanma",
    "wooper", "murkrow", "misdreavus", "girafarig", "pineco", "dunsparce", "gligar", "snubbull", "sneasel",
    "teddiursa", "ursaring", "slugma", "swinub", "piloswine", "remoraid", "houndour", "phanpy", "porygon2",
    "stantler", "tyrogue", "smoochum", "elekid", "magby", "larvitar", "pupitar", "treecko", "grovyle", "torchic",
    "combusken", "mudkip", "marshtomp", "poochyena", "zigzagoon", "wurmple", "silcoon", "cascoon", "lotad",
    "lombre", "seedot", "nuzleaf", "taillow", "wingull", "ralts", "kirlia", "surskit", "shroomish", "slakoth",
    "vigoroth", "nincada", "whismur", "loudred", "makuhita", "azurill", "nosepass", "skitty", "aron", "lairon",
    "meditite", "electrike", "roselia", "gulpin", "carvanha", "wailmer", "numel", "spoink", "trapinch", "vibrava",
    "cacnea", "swablu", "barboach", "corphish", "baltoy", "lileep", "anorith", "feebas", "shuppet", "duskull",
    "dusclops", "wynaut", "snorunt", "spheal", "sealeo", "clamperl", "bagon", "shelgon", "beldum", "metang",
    "turtwig", "grotle", "chimchar", "monferno", "piplup", "prinplup", "starly", "staravia", "bidoof", "kricketot",
    "shinx", "luxio", "budew", "cranidos", "shieldon", "burmy", "combee", "buizel", "cherubi", "shellos",
    "drifloon", "buneary", "glameow", "chingling", "stunky", "bronzor", "bonsly", "mime-jr", "happiny", "gible",
    "gabite", "munchlax", "riolu", "hippopotas", "skorupi", "croagunk", "finneon", "mantyke", "snover", "snivy",
    "servine", "tepig", "pignite", "oshawott", "dewott", "patrat", "lillipup", "herdier", "purrloin", "pansage",
    "pansear", "panpour", "munna", "pidove", "tranquill", "blitzle", "roggenrola", "boldore", "woobat", "drilbur",
    "timburr", "gurdurr", "tympole", "palpitoad", "sewaddle", "swadloon", "venipede", "whirlipede", "cottonee",
    "petilil", "sandile", "krokorok", "darumaka", "dwebble", "scraggy", "yamask", "tirtouga", "archen", "trubbish",
    "zorua", "minccino", "gothita", "gothorita", "solosis", "duosion", "ducklett", "vanillite", "vanillish",
    "deerling", "karrablast", "foongus", "frillish-male", "joltik", "ferroseed", "klink", "klang", "tynamo",
    "eelektrik", "elgyem", "litwick", "lampent", "axew", "fraxure", "cubchoo", "shelmet", "mienfoo", "golett",
    "pawniard", "bisharp", "rufflet", "vullaby", "deino", "zweilous", "larvesta", "chespin", "quilladin",
    "fennekin", "braixen", "froakie", "frogadier", "bunnelby", "fletchling", "fletchinder", "scatterbug", "spewpa",
    "litleo", "flabebe", "floette", "skiddo", "pancham", "espurr", "honedge", "doublade", "spritzee", "swirlix",
    "inkay", "binacle", "skrelp", "clauncher", "helioptile", "tyrunt", "amaura", "goomy", "sliggoo", "phantump",
    "pumpkaboo-average", "bergmite", "noibat", "rowlet", "dartrix", "litten", "torracat", "popplio", "brionne",
    "pikipek", "trumbeak", "yungoos", "grubbin", "charjabug", "crabrawler", "cutiefly", "rockruff", "mareanie",
    "mudbray", "dewpider", "fomantis", "morelull", "salandit", "stufful", "bounsweet", "steenee", "wimpod",
    "sandygast", "type-null", "jangmo-o", "hakamo-o", "cosmog", "cosmoem", "poipole", "grookey", "thwackey",
    "scorbunny", "raboot", "sobble", "drizzile", "skwovet", "rookidee", "corvisquire", "blipbug", "dottler",
    "nickit", "gossifleur", "wooloo", "chewtle", "yamper", "rolycoly", "carkol", "applin", "silicobra", "arrokuda",
    "toxel", "sizzlipede", "clobbopus", "sinistea", "hatenna", "hattrem", "impidimp", "morgrem", "milcery", "snom",
    "cufant", "duraludon", "dreepy", "drakloak", "kubfu", "sprigatito", "floragato", "fuecoco", "crocalor",
    "quaxly", "quaxwell", "lechonk", "tarountula", "nymble", "pawmi", "pawmo", "tandemaus", "fidough", "smoliv",
    "dolliv", "nacli", "naclstack", "charcadet", "tadbulb", "wattrel", "maschiff", "shroodle", "bramblin",
    "toedscool", "capsakid", "rellor", "flittle", "tinkatink", "tinkatuff", "wiglett", "finizen", "varoom",
    "glimmet", "greavard", "cetoddle", "frigibax", "arctibax", "gimmighoul", "dipplin", "poltchageist",
}


# -------- Damage math helpers --------
# The games do the damage math with whole numbers out of 4096 instead of decimals, so these copy how they round.

# Rounds like the games do. Exactly .5 rounds down and anything over .5 rounds up.
def poke_round(number):
    return math.ceil(number) if number % 1 > 0.5 else math.floor(number)

# Turns a multiplier like 1.5 into the out-of-4096 modifier the games use (6144).
def to_4096(multiplier):
    return round(multiplier * 4096)

# Combines modifiers (out of 4096) one at a time, rounding after each one like the games do. Returns the combined modifier.
def chain_modifiers(modifiers, lower_bound, upper_bound):
    total = 4096
    for modifier in modifiers:
        if modifier != 4096:
            total = (total * modifier + 2048) >> 12
    return max(min(total, upper_bound), lower_bound)

# Applies a stat stage (-6 to +6) to a stat. +1 = 1.5x, +2 = 2x, -1 = 2/3, -2 = 1/2, etc.
def apply_stage(stat, stage):
    stage = max(-6, min(6, stage))
    if stage >= 0:
        return stat * (2 + stage) // 2
    return stat * 2 // (2 - stage)

# Describes how many hits it takes to KO, like Smogon's calc. Ignores recovery and end-of-turn dmg.
# rolls = the 16 total dmg rolls. hp = the defender's current HP.
def ko_chance_text(rolls, hp):
    if max(rolls) == 0:
        return "No damage"
    if min(rolls) >= hp:
        return "Guaranteed OHKO"
    if max(rolls) >= hp:
        chance = sum(1 for roll in rolls if roll >= hp) / 16 * 100
        return f"{chance:.1f}% chance to OHKO"
    fewest_hits = math.ceil(hp / max(rolls))
    most_hits = math.ceil(hp / min(rolls))
    if fewest_hits == most_hits:
        return f"Guaranteed {fewest_hits}HKO"
    return f"Possible {fewest_hits}HKO"

# Turns a before and after value into a modifier out of 4096. Returns 4096 (no change) if nothing changed.
def modifier_from(new_value, old_value):
    if not old_value or new_value is None or new_value == old_value:
        return 4096
    return to_4096(new_value / old_value)

# The 16 random dmg rolls (85% to 100%) for one hit, with STAB, type effectiveness, burn and the final modifiers applied in the games' order.
def damage_rolls(base_damage, stab, effectiveness, burned, final_modifier):
    rolls = []
    for roll in range(85, 101):
        damage = base_damage * roll // 100
        if stab != 4096:
            damage = damage * stab / 4096
        damage = math.floor(poke_round(damage) * effectiveness)
        if burned:
            damage = damage // 2
        rolls.append(poke_round(max(1, damage * final_modifier / 4096)))
    return rolls


class DamageCalculator:
    # attacker_ability and defender_ability = the ability each Pokémon is using. If it's not given, it uses the Pokémon's first ability.
    # attacker_item and defender_item = the item each Pokémon is holding. If it's not given, the Pokémon isn't holding anything.
    # attacker_build and defender_build = each Pokémon's level, EVs, IVs and nature. Anything not given uses level 50, 0 EVs, 31 IVs and a neutral nature.
    def __init__(self, attacker: Species, defender: Species, move_type: str, move_power: int, move_name: str, status_effect_attacker: str, status_effect_defender: str, weather: str = None, terrain: str = None, attacker_ability: str = None, defender_ability: str = None, attacker_item: str = None, defender_item: str = None, attacker_build: dict = None, defender_build: dict = None):
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
        self.attacker_item = attacker_item
        self.defender_item = defender_item
        self.attacker_build = make_build(attacker_build)
        self.defender_build = make_build(defender_build)
        self.attacker_level = self.attacker_build["level"]
        self.defender_level = self.defender_build["level"]
        # Real stats from each Pokémon's base stats and build.
        self.attacker_stats = calculate_stats(self.attacker.stats, self.attacker_build, self.attacker.pokedex_id)
        self.defender_stats = calculate_stats(self.defender.stats, self.defender_build, self.defender.pokedex_id)

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

    # A Pokémon is grounded unless it is a Flying type or has Levitate or Eelevate. Terrain only affects grounded Pokémon.
    # Will add Air Balloon, Magnet Rise, and Gravity later once items and field moves are in.
    def grounded_attacker(self):
        if self.held_item_attacker() == "iron-ball":
            return True
        return "flying" not in self.attacker.types and "levitate" not in self.attacker_abilities and "eelevate" not in self.attacker_abilities and self.held_item_attacker() != "air-balloon"
    def grounded_defender(self):
        if self.held_item_defender() == "iron-ball":
            return True
        return "flying" not in self.defender.types and "levitate" not in self.defender_abilities and "eelevate" not in self.defender_abilities and self.held_item_defender() != "air-balloon"

    # Rain, sun, and their primal versions boost or weaken moves of certain types.
    def weather_move_power(self):
        if not self.move_power:
            return self.move_power
        effects = self.weather_effects()
        if effects.get("weakened_type") == self.move_type and effects["weaken_multiplier"] == 0:
            return 0
        # Utility Umbrella on the target cancels the sun and rain boost or drop.
        if self.utility_umbrella_item_defender() != self.current_weather():
            return self.move_power
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
        if "self_inflicted_dmg" not in effects or self.held_item_attacker() == "safety-goggles":
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
        if "self_inflicted_dmg" not in effects or self.held_item_defender() == "safety-goggles":
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
            return self.attacker_stats[stat] * effects["stat_multiplier"]
        return self.attacker_stats[stat]
    def weather_stat_defender(self, stat):
        effects = self.weather_effects()
        if effects.get("boosted_stat") == stat and effects.get("boosted_stat_type") in self.defender.types:
            return self.defender_stats[stat] * effects["stat_multiplier"]
        return self.defender_stats[stat]

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
            return self.attacker_stats["attack"]
        if self.status_effects_attacker():
            return self.attacker_stats["attack"] * 1.5
        else:
            return self.attacker_stats["attack"]
    def guts_ability_defender(self):
        if "guts" not in self.defender_abilities:
                return self.defender_stats["attack"]
        if self.status_effects_defender():
            return self.defender_stats["attack"] * 1.5
        else:
            return self.defender_stats["attack"]

    # Toxic boost increases the Pokémon's physical Attack stat by 1.5× when it is poisoned
    def toxic_boost_ability_attacker(self):
        if "toxic-boost" not in self.attacker_abilities:
            return self.attacker_stats["attack"]
        if self.status_attacker == "poison" or self.status_attacker == "badly-poison":
            return self.attacker_stats["attack"] * 1.5
        else:
            return self.attacker_stats["attack"]
    def toxic_boost_ability_defender(self):
        if "toxic-boost" not in self.defender_abilities:
           return self.defender_stats["attack"]
        if self.status_defender == "poison" or self.status_defender == "badly-poison":
            return self.defender_stats["attack"] * 1.5
        else:
            return self.defender_stats["attack"]

    # Flare boost multiplies the user's Special Attack stat by 1.5× when the Pokémon is burned
    def flare_boost_ability_attacker(self):
        if "flare-boost" not in self.attacker_abilities:
            return self.attacker_stats["special-attack"]
        if self.status_attacker == "burn":
            return self.attacker_stats["special-attack"] * 1.5
        else:
            return self.attacker_stats["special-attack"]
    def flare_boost_ability_defender(self):
        if "flare-boost" not in self.defender_abilities:
            return self.defender_stats["special-attack"]
        if self.status_defender == "burn":
            return self.defender_stats["special-attack"] * 1.5
        else:
            return self.defender_stats["special-attack"]

    # Quick feet increases a Pokémon's Speed stat by 50% when it is affected by a major status ailment like poison, burn, paralysis, freeze, or sleep
    def quick_feet_ability_attacker(self):
        if "quick-feet" not in self.attacker_abilities:
            return self.attacker_stats["speed"]
        if self.status_effects_attacker():
            return self.attacker_stats["speed"] * 1.5
        else:
            return self.attacker_stats["speed"]
    def quick_feet_ability_defender(self):
        if "quick-feet" not in self.defender_abilities:
            return self.defender_stats["speed"]
        if self.status_effects_defender():
            return self.defender_stats["speed"] * 1.5
        else:
            return self.defender_stats["speed"]

    # Marvel scale boosts the user's Defense stat by 50% (1.5×) whenever it is afflicted with a major status condition(poison, burn, paralysis, freeze, or sleep).
    def marvel_scale_ability_attacker(self):
        if "marvel-scale" not in self.attacker_abilities:
            return self.attacker_stats["defense"]
        if self.status_effects_attacker():
            return self.attacker_stats["defense"] * 1.5
        else:
            return self.attacker_stats["defense"]
    def marvel_scale_ability_defender(self):
        if "marvel-scale" not in self.defender_abilities:
            return self.defender_stats["defense"]
        if self.status_effects_defender():
            return self.defender_stats["defense"] * 1.5
        else:
            return self.defender_stats["defense"]


    # Pure Power doubles the user's total physical Attack stat in battle.
    def pure_power_ability_attacker(self):
        if "pure-power" not in self.attacker_abilities:
           return self.attacker_stats["attack"]
        return self.attacker_stats["attack"] * 2
    def pure_power_ability_defender(self):
        if "pure-power" not in self.defender_abilities:
           return self.defender_stats["attack"]
        return self.defender_stats["attack"] * 2

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
        if "levitate" not in self.attacker_abilities or self.held_item_attacker() == "iron-ball":
            return self.move_power
        if self.move_type == "ground" and not self.status_move():
            return 0
        else:
            return self.move_power
    def levitate_ability_defender(self):
        if "levitate" not in self.defender_abilities or self.held_item_defender() == "iron-ball":
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
            return self.attacker_stats["attack"]
        return self.attacker_stats["attack"] * 2
    def huge_power_ability_defender(self):
        if "huge-power" not in self.defender_abilities:
            return self.defender_stats["attack"]
        return self.defender_stats["attack"] * 2
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
            return self.attacker_stats["speed"]
        stage = min(turns_on_field, 6)
        return self.attacker_stats["speed"] * (2 + stage) / 2
    def speed_boost_ability_defender(self, turns_on_field):
        if "speed-boost" not in self.defender_abilities:
            return self.defender_stats["speed"]
        stage = min(turns_on_field, 6)
        return self.defender_stats["speed"] * (2 + stage) / 2

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
        if "sand-veil" not in self.attacker_abilities or self.current_weather() != "sandstorm" or self.ohko_move():
            return accuracy
        return accuracy * 0.8
    def sand_veil_ability_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "sand-veil" not in self.defender_abilities or self.current_weather() != "sandstorm" or self.ohko_move():
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
            return self.defender_stats["attack"]
        for ability in self.defender_abilities:
            if ability in INTIMIDATE_IMMUNITY_ABILITIES:
                return self.defender_stats["attack"]
        if self.held_item_defender() == "clear-amulet":
            return self.defender_stats["attack"]
        if "guard-dog" in self.defender_abilities:
            return self.defender_stats["attack"] * 1.5
        return self.defender_stats["attack"] * 2 / 3
    def intimidate_ability_defender(self):
        if "intimidate" not in self.defender_abilities:
            return self.attacker_stats["attack"]
        for ability in self.attacker_abilities:
            if ability in INTIMIDATE_IMMUNITY_ABILITIES:
                return self.attacker_stats["attack"]
        if self.held_item_attacker() == "clear-amulet":
            return self.attacker_stats["attack"]
        if "guard-dog" in self.attacker_abilities:
            return self.attacker_stats["attack"] * 1.5
        return self.attacker_stats["attack"] * 2 / 3

    # Shadow Tag: The opposing Pokémon can't switch out. Returns True if it's trapped.
    def shadow_tag_ability_attacker(self, switched_in_this_turn=False):
        if "shadow-tag" not in self.attacker_abilities or switched_in_this_turn:
            return False
        if "ghost" in self.defender.types or "shadow-tag" in self.defender_abilities:
            return False
        return self.shed_shell_item_defender(True)
    def shadow_tag_ability_defender(self, switched_in_this_turn=False):
        if "shadow-tag" not in self.defender_abilities or switched_in_this_turn:
            return False
        if "ghost" in self.attacker.types or "shadow-tag" in self.attacker_abilities:
            return False
        return self.shed_shell_item_attacker(True)

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
        if "grass" in self.defender.types or "overcoat" in self.defender_abilities or self.held_item_defender() == "safety-goggles" or self.status_effects_defender():
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
        if "grass" in self.attacker.types or "overcoat" in self.attacker_abilities or self.held_item_attacker() == "safety-goggles" or self.status_effects_attacker():
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
            return self.attacker_stats["speed"]
        if self.utility_umbrella_item_attacker() in ("rain", "heavy-rain"):
            return self.attacker_stats["speed"] * 2
        return self.attacker_stats["speed"]
    def swift_swim_ability_defender(self):
        if "swift-swim" not in self.defender_abilities:
            return self.defender_stats["speed"]
        if self.utility_umbrella_item_defender() in ("rain", "heavy-rain"):
            return self.defender_stats["speed"] * 2
        return self.defender_stats["speed"]

    # Chlorophyll: Doubles the Pokémon's Speed in harsh sunlight.
    def chlorophyll_ability_attacker(self):
        if "chlorophyll" not in self.attacker_abilities:
            return self.attacker_stats["speed"]
        if self.utility_umbrella_item_attacker() in ("sun", "extreme-sun"):
            return self.attacker_stats["speed"] * 2
        return self.attacker_stats["speed"]
    def chlorophyll_ability_defender(self):
        if "chlorophyll" not in self.defender_abilities:
            return self.defender_stats["speed"]
        if self.utility_umbrella_item_defender() in ("sun", "extreme-sun"):
            return self.defender_stats["speed"] * 2
        return self.defender_stats["speed"]

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
        return self.shed_shell_item_defender(True)
    def magnet_pull_ability_defender(self, switched_in_this_turn=False):
        if "magnet-pull" not in self.defender_abilities or switched_in_this_turn:
            return False
        if "steel" not in self.attacker.types or "ghost" in self.attacker.types:
            return False
        return self.shed_shell_item_attacker(True)

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
        if self.utility_umbrella_item_attacker() in ("rain", "heavy-rain"):
            return 0.0625
        return 0
    def rain_dish_ability_defender(self):
        if "rain-dish" not in self.defender_abilities:
            return 0
        if self.utility_umbrella_item_defender() in ("rain", "heavy-rain"):
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
        if accuracy is None or self.ohko_move():
            return accuracy
        if "keen-eye" in self.attacker_abilities:
            target_evasion_stage = 0
        stage = max(-6, min(6, accuracy_stage - target_evasion_stage))
        if stage >= 0:
            return accuracy * (3 + stage) / 3
        return accuracy * 3 / (3 - stage)
    def keen_eye_ability_defender(self, accuracy_stage=0, target_evasion_stage=0):
        accuracy = self.move_data.accuracy
        if accuracy is None or self.ohko_move():
            return accuracy
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
            return self.attacker_stats["attack"]
        return self.attacker_stats["attack"] * 1.5
    def hustle_ability_defender(self):
        if "hustle" not in self.defender_abilities:
            return self.defender_stats["attack"]
        return self.defender_stats["attack"] * 1.5

    # Hustle: The Pokémon's physical moves are 20% less accurate. Returns the move's accuracy when this Pokémon uses it.
    def hustle_accuracy_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "hustle" not in self.attacker_abilities or self.move_data.damage_class != "physical" or self.ohko_move():
            return accuracy
        return accuracy * 0.8
    def hustle_accuracy_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "hustle" not in self.defender_abilities or self.move_data.damage_class != "physical" or self.ohko_move():
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
            return self.attacker_stats["special-attack"]
        if "plus" in ally_abilities or "minus" in ally_abilities:
            return self.attacker_stats["special-attack"] * 1.5
        return self.attacker_stats["special-attack"]
    def plus_ability_defender(self, ally_abilities=None):
        if "plus" not in self.defender_abilities or not ally_abilities:
            return self.defender_stats["special-attack"]
        if "plus" in ally_abilities or "minus" in ally_abilities:
            return self.defender_stats["special-attack"] * 1.5
        return self.defender_stats["special-attack"]

    # Minus: Boosts the Pokémon's Sp. Atk by 50% if an ally has Plus or Minus. ally_abilities = the ally's abilities.
    def minus_ability_attacker(self, ally_abilities=None):
        if "minus" not in self.attacker_abilities or not ally_abilities:
            return self.attacker_stats["special-attack"]
        if "plus" in ally_abilities or "minus" in ally_abilities:
            return self.attacker_stats["special-attack"] * 1.5
        return self.attacker_stats["special-attack"]
    def minus_ability_defender(self, ally_abilities=None):
        if "minus" not in self.defender_abilities or not ally_abilities:
            return self.defender_stats["special-attack"]
        if "plus" in ally_abilities or "minus" in ally_abilities:
            return self.defender_stats["special-attack"] * 1.5
        return self.defender_stats["special-attack"]

    # Forecast: The Pokémon becomes Fire type in sun, Water type in rain, and Ice type in snow. Returns the Pokémon's types.
    def forecast_ability_attacker(self):
        if "forecast" not in self.attacker_abilities:
            return self.attacker.types
        weather = self.utility_umbrella_item_attacker()
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
        weather = self.utility_umbrella_item_defender()
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
        return self.shed_shell_item_defender(True)
    def arena_trap_ability_defender(self, switched_in_this_turn=False):
        if "arena-trap" not in self.defender_abilities or switched_in_this_turn:
            return False
        if not self.grounded_attacker() or "ghost" in self.attacker.types:
            return False
        return self.shed_shell_item_attacker(True)

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
        if "tangled-feet" not in self.attacker_abilities or not confused or self.ohko_move():
            return accuracy
        return accuracy * 0.5
    def tangled_feet_ability_defender(self, confused):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "tangled-feet" not in self.defender_abilities or not confused or self.ohko_move():
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
        if "snow-cloak" not in self.attacker_abilities or self.current_weather() not in ("snow", "hail") or self.ohko_move():
            return accuracy
        return accuracy * 0.8
    def snow_cloak_ability_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "snow-cloak" not in self.defender_abilities or self.current_weather() not in ("snow", "hail") or self.ohko_move():
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
            return self.attacker_stats["speed"]
        return self.attacker_stats["speed"] * 2
    def unburden_ability_defender(self, item_lost):
        if "unburden" not in self.defender_abilities or not item_lost:
            return self.defender_stats["speed"]
        return self.defender_stats["speed"] * 2

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
        if self.utility_umbrella_item_attacker() in ("rain", "heavy-rain"):
            return 0.125
        if self.utility_umbrella_item_attacker() in ("sun", "extreme-sun"):
            return -0.125
        return 0
    def dry_skin_weather_defender(self):
        if "dry-skin" not in self.defender_abilities:
            return 0
        if self.utility_umbrella_item_defender() in ("rain", "heavy-rain"):
            return 0.125
        if self.utility_umbrella_item_defender() in ("sun", "extreme-sun"):
            return -0.125
        return 0

    # Download: When the Pokémon enters battle, it raises Sp. Atk if the opponent's Defense is higher, or Attack if its Sp. Def is higher. Returns the stat that goes up 1 stage.
    def download_ability_attacker(self):
        if "download" not in self.attacker_abilities:
            return None
        if self.defender_stats["defense"] >= self.defender_stats["special-defense"]:
            return "special-attack"
        return "attack"
    def download_ability_defender(self):
        if "download" not in self.defender_abilities:
            return None
        if self.attacker_stats["defense"] >= self.attacker_stats["special-defense"]:
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
        if self.utility_umbrella_item_attacker() in ("rain", "heavy-rain"):
            return None
        return self.status_attacker
    def hydration_ability_defender(self):
        if "hydration" not in self.defender_abilities:
            return self.status_defender
        if self.utility_umbrella_item_defender() in ("rain", "heavy-rain"):
            return None
        return self.status_defender

    # Solar Power: Boosts the Pokémon's Sp. Atk by 50% in harsh sunlight.
    def solar_power_ability_attacker(self):
        if "solar-power" not in self.attacker_abilities:
            return self.attacker_stats["special-attack"]
        if self.utility_umbrella_item_attacker() in ("sun", "extreme-sun"):
            return self.attacker_stats["special-attack"] * 1.5
        return self.attacker_stats["special-attack"]
    def solar_power_ability_defender(self):
        if "solar-power" not in self.defender_abilities:
            return self.defender_stats["special-attack"]
        if self.utility_umbrella_item_defender() in ("sun", "extreme-sun"):
            return self.defender_stats["special-attack"] * 1.5
        return self.defender_stats["special-attack"]

    # Solar Power: The Pokémon loses 1/8 of its max HP each turn in harsh sunlight.
    def solar_power_damage_attacker(self):
        if "solar-power" not in self.attacker_abilities:
            return 0
        if self.utility_umbrella_item_attacker() in ("sun", "extreme-sun"):
            return 0.125
        return 0
    def solar_power_damage_defender(self):
        if "solar-power" not in self.defender_abilities:
            return 0
        if self.utility_umbrella_item_defender() in ("sun", "extreme-sun"):
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
        if self.utility_umbrella_item_attacker() in ("sun", "extreme-sun"):
            return None
        return self.status_attacker
    def leaf_guard_ability_defender(self):
        if "leaf-guard" not in self.defender_abilities:
            return self.status_defender
        if self.utility_umbrella_item_defender() in ("sun", "extreme-sun"):
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
        if "mold-breaker" not in self.attacker_abilities or self.ability_shield_item_defender():
            return self.defender_abilities
        return [ability for ability in self.defender_abilities if ability not in BREAKABLE_ABILITIES]
    def mold_breaker_ability_defender(self):
        if "mold-breaker" not in self.defender_abilities or self.ability_shield_item_attacker():
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
        attack = self.attacker_stats["attack"]
        speed = self.attacker_stats["speed"]
        if "slow-start" not in self.attacker_abilities or turns_on_field >= 5:
            return attack, speed
        return attack * 0.5, speed * 0.5
    def slow_start_ability_defender(self, turns_on_field):
        attack = self.defender_stats["attack"]
        speed = self.defender_stats["speed"]
        if "slow-start" not in self.defender_abilities or turns_on_field >= 5:
            return attack, speed
        return attack * 0.5, speed * 0.5

    # Scrappy: The Pokémon's Normal and Fighting moves can hit Ghost types. Returns the type effectiveness against the target.
    # Scrappy also blocks Intimidate, which is handled in INTIMIDATE_IMMUNITY_ABILITIES.
    def scrappy_ability_attacker(self):
        if "scrappy" not in self.attacker_abilities or self.move_type not in ("normal", "fighting"):
            return self.type_effectiveness_defender()
        removes_flying_weaknesses = self.weather_effects().get("removes_flying_weaknesses", False)
        multiplier = 1
        for type_name, type_data in zip(self.defender.types, self.defender_types_data):
            if type_name == "ghost":
                continue
            if self.move_type in type_data["double_damage_from"]:
                if not (removes_flying_weaknesses and type_name == "flying"):
                    multiplier *= 2
            elif self.move_type in type_data["half_damage_from"]:
                multiplier *= 0.5
            elif self.move_type in type_data["no_damage_from"]:
                multiplier *= 0
        return multiplier
    def scrappy_ability_defender(self):
        if "scrappy" not in self.defender_abilities or self.move_type not in ("normal", "fighting"):
            return self.type_effectiveness_attacker()
        removes_flying_weaknesses = self.weather_effects().get("removes_flying_weaknesses", False)
        multiplier = 1
        for type_name, type_data in zip(self.attacker.types, self.attacker_types_data):
            if type_name == "ghost":
                continue
            if self.move_type in type_data["double_damage_from"]:
                if not (removes_flying_weaknesses and type_name == "flying"):
                    multiplier *= 2
            elif self.move_type in type_data["half_damage_from"]:
                multiplier *= 0.5
            elif self.move_type in type_data["no_damage_from"]:
                multiplier *= 0
        return multiplier

    # Storm Drain: Water moves don't affect the Pokémon. Instead they raise its Sp. Atk by 1 stage.
    def storm_drain_ability_attacker(self):
        if "storm-drain" not in self.attacker_abilities or self.move_type != "water":
            return self.move_power, 0
        if self.weather_move_power() == 0:
            return 0, 0
        return 0, 1
    def storm_drain_ability_defender(self):
        if "storm-drain" not in self.defender_abilities or self.move_type != "water":
            return self.move_power, 0
        if self.weather_move_power() == 0:
            return 0, 0
        return 0, 1

    # Ice Body: Heals 1/16 of the Pokémon's max HP at the end of each turn in snow.
    def ice_body_ability_attacker(self):
        if "ice-body" not in self.attacker_abilities:
            return 0
        if self.current_weather() in ("snow", "hail"):
            return 0.0625
        return 0
    def ice_body_ability_defender(self):
        if "ice-body" not in self.defender_abilities:
            return 0
        if self.current_weather() in ("snow", "hail"):
            return 0.0625
        return 0

    # Snow Warning: Summons snow for 5 turns when the Pokémon enters battle.
    def snow_warning_ability_attacker(self):
        if "snow-warning" not in self.attacker_abilities:
            return self.weather
        if self.weather == "snow" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "snow"
        self.weather_turns = WEATHER_EFFECTS["snow"]["turns"]
        return self.weather
    def snow_warning_ability_defender(self):
        if "snow-warning" not in self.defender_abilities:
            return self.weather
        if self.weather == "snow" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "snow"
        self.weather_turns = WEATHER_EFFECTS["snow"]["turns"]
        return self.weather

    # Honey Gather: The Pokémon may pick up Honey after a battle.
    # This ability currently has no effect on the dmg calc and will be implemented at a later date.
    # def honey_gather_ability_attacker(self):
    #     return "honey-gather" in self.attacker_abilities
    # def honey_gather_ability_defender(self):
    #     return "honey-gather" in self.defender_abilities

    # Frisk: When the Pokémon enters battle, it checks the opposing Pokémon's held item. Returns the item it finds.
    def frisk_ability_attacker(self, opponent_item):
        if "frisk" not in self.attacker_abilities:
            return None
        return opponent_item
    def frisk_ability_defender(self, opponent_item):
        if "frisk" not in self.defender_abilities:
            return None
        return opponent_item

    # Reckless: Boosts the power of the Pokémon's recoil and crash moves by 20%.
    def reckless_ability_attacker(self):
        if "reckless" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_name in RECKLESS_MOVES:
            return self.move_power * 1.2
        return self.move_power
    def reckless_ability_defender(self):
        if "reckless" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_name in RECKLESS_MOVES:
            return self.move_power * 1.2
        return self.move_power

    # Multitype: Arceus's type changes to match the Plate it's holding. Returns the Pokémon's types.
    def multitype_ability_attacker(self, held_item):
        if "multitype" not in self.attacker_abilities:
            return self.attacker.types
        return [PLATE_TYPES.get(held_item, "normal")]
    def multitype_ability_defender(self, held_item):
        if "multitype" not in self.defender_abilities:
            return self.defender.types
        return [PLATE_TYPES.get(held_item, "normal")]

    # Flower Gift: In harsh sunlight, Cherrim's Attack and Sp. Def go up by 50%. Returns its Attack and Sp. Def.
    def flower_gift_ability_attacker(self):
        attack = self.attacker_stats["attack"]
        special_defense = self.attacker_stats["special-defense"]
        if "flower-gift" not in self.attacker_abilities or not self.attacker.name.startswith("cherrim"):
            return attack, special_defense
        if self.utility_umbrella_item_attacker() in ("sun", "extreme-sun"):
            return attack * 1.5, special_defense * 1.5
        return attack, special_defense
    def flower_gift_ability_defender(self):
        attack = self.defender_stats["attack"]
        special_defense = self.defender_stats["special-defense"]
        if "flower-gift" not in self.defender_abilities or not self.defender.name.startswith("cherrim"):
            return attack, special_defense
        if self.utility_umbrella_item_defender() in ("sun", "extreme-sun"):
            return attack * 1.5, special_defense * 1.5
        return attack, special_defense
        # Will add the boost for allies later for doubles.

    # Bad Dreams: The opposing Pokémon loses 1/8 of its max HP each turn while it's asleep.
    def bad_dreams_ability_attacker(self):
        if "bad-dreams" not in self.attacker_abilities:
            return 0
        if self.status_defender != "sleep" and "comatose" not in self.defender_abilities:
            return 0
        if "magic-guard" in self.defender_abilities:
            return 0
        return 0.125
    def bad_dreams_ability_defender(self):
        if "bad-dreams" not in self.defender_abilities:
            return 0
        if self.status_attacker != "sleep" and "comatose" not in self.attacker_abilities:
            return 0
        if "magic-guard" in self.attacker_abilities:
            return 0
        return 0.125

    # Pickpocket: When the Pokémon is hit by a contact move, it steals the attacker's item if it isn't holding one. Returns the item it's holding after.
    def pickpocket_ability_attacker(self, held_item, opponent_item):
        if "pickpocket" not in self.attacker_abilities or held_item or not self.contact_move():
            return held_item
        if "sticky-hold" in self.defender_abilities:
            return held_item
        return opponent_item
    def pickpocket_ability_defender(self, held_item, opponent_item):
        if "pickpocket" not in self.defender_abilities or held_item or not self.contact_move():
            return held_item
        if "sticky-hold" in self.attacker_abilities:
            return held_item
        return opponent_item

    # Sheer Force: Boosts the power of the Pokémon's moves with added effects by 30%.
    def sheer_force_ability_attacker(self):
        if "sheer-force" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_name in SHEER_FORCE_MOVES:
            return self.move_power * 1.3
        return self.move_power
    def sheer_force_ability_defender(self):
        if "sheer-force" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_name in SHEER_FORCE_MOVES:
            return self.move_power * 1.3
        return self.move_power

    # Sheer Force: The move's added effects (status, flinch, stat changes) don't happen. Returns True if they're removed.
    def sheer_force_effects_attacker(self):
        return "sheer-force" in self.attacker_abilities and self.move_name in SHEER_FORCE_MOVES
    def sheer_force_effects_defender(self):
        return "sheer-force" in self.defender_abilities and self.move_name in SHEER_FORCE_MOVES

    # Contrary: The Pokémon's stat changes are reversed. Returns the stage change that actually happens.
    def contrary_ability_attacker(self, stage_change):
        if "contrary" not in self.attacker_abilities:
            return stage_change
        return -stage_change
    def contrary_ability_defender(self, stage_change):
        if "contrary" not in self.defender_abilities:
            return stage_change
        return -stage_change

    # Unnerve: The opposing Pokémon can't eat Berries. Returns the opposing Pokémon's item that still works.
    def unnerve_ability_attacker(self, opponent_item):
        if "unnerve" not in self.attacker_abilities or not opponent_item or not opponent_item.endswith("-berry"):
            return opponent_item
        return None
    def unnerve_ability_defender(self, opponent_item):
        if "unnerve" not in self.defender_abilities or not opponent_item or not opponent_item.endswith("-berry"):
            return opponent_item
        return None

    # Defiant: When an opposing Pokémon lowers one of its stats, its Attack goes up 2 stages. Returns the Attack stage change.
    def defiant_ability_attacker(self, stage_change, from_opponent=True):
        if "defiant" not in self.attacker_abilities or stage_change >= 0 or not from_opponent:
            return 0
        return 2
    def defiant_ability_defender(self, stage_change, from_opponent=True):
        if "defiant" not in self.defender_abilities or stage_change >= 0 or not from_opponent:
            return 0
        return 2

    # Defeatist: The Pokémon's Attack and Sp. Atk are halved when its HP is 1/2 or less. Returns its Attack and Sp. Atk.
    def defeatist_ability_attacker(self, current_hp, max_hp):
        attack = self.attacker_stats["attack"]
        special_attack = self.attacker_stats["special-attack"]
        if "defeatist" not in self.attacker_abilities or current_hp > max_hp / 2:
            return attack, special_attack
        return attack * 0.5, special_attack * 0.5
    def defeatist_ability_defender(self, current_hp, max_hp):
        attack = self.defender_stats["attack"]
        special_attack = self.defender_stats["special-attack"]
        if "defeatist" not in self.defender_abilities or current_hp > max_hp / 2:
            return attack, special_attack
        return attack * 0.5, special_attack * 0.5

    # Cursed Body: When the Pokémon is hit by a move, there's a 30% chance that move gets disabled. Returns True if the move gets disabled.
    def cursed_body_ability_attacker(self):
        if "cursed-body" not in self.attacker_abilities or self.status_move():
            return False
        if self.move_name in ("struggle", "future-sight", "doom-desire"):
            return False
        return random.random() < 0.30
    def cursed_body_ability_defender(self):
        if "cursed-body" not in self.defender_abilities or self.status_move():
            return False
        if self.move_name in ("struggle", "future-sight", "doom-desire"):
            return False
        return random.random() < 0.30

    # Healer: Each turn, there's a 30% chance the Pokémon cures its ally's status. ally_status = the ally's status. Returns the ally's status after.
    def healer_ability_attacker(self, ally_status=None):
        if "healer" not in self.attacker_abilities or not ally_status:
            return ally_status
        if random.random() < 0.30:
            return None
        return ally_status
    def healer_ability_defender(self, ally_status=None):
        if "healer" not in self.defender_abilities or not ally_status:
            return ally_status
        if random.random() < 0.30:
            return None
        return ally_status

    # Friend Guard: The Pokémon's allies take 25% less damage. ally_abilities = the abilities of the ally next to the Pokémon getting hit.
    def friend_guard_ability_attacker(self, ally_abilities=None):
        if not ally_abilities or "friend-guard" not in ally_abilities or not self.move_power:
            return self.move_power
        return self.move_power * 0.75
    def friend_guard_ability_defender(self, ally_abilities=None):
        if not ally_abilities or "friend-guard" not in ally_abilities or not self.move_power:
            return self.move_power
        return self.move_power * 0.75

    # Weak Armor: When the Pokémon is hit by a physical move, its Defense goes down 1 stage and its Speed goes up 2 stages. Returns the Defense and Speed stage changes.
    def weak_armor_ability_attacker(self):
        if "weak-armor" not in self.attacker_abilities or self.move_data.damage_class != "physical":
            return 0, 0
        return -1, 2
    def weak_armor_ability_defender(self):
        if "weak-armor" not in self.defender_abilities or self.move_data.damage_class != "physical":
            return 0, 0
        return -1, 2

    # Heavy Metal: Doubles the Pokémon's weight. Returns its weight.
    def heavy_metal_ability_attacker(self):
        if "heavy-metal" not in self.attacker_abilities:
            return self.attacker.weight
        return self.attacker.weight * 2
    def heavy_metal_ability_defender(self):
        if "heavy-metal" not in self.defender_abilities:
            return self.defender.weight
        return self.defender.weight * 2

    # Light Metal: Halves the Pokémon's weight. Returns its weight.
    def light_metal_ability_attacker(self):
        if "light-metal" not in self.attacker_abilities:
            return self.attacker.weight
        return max(1, self.attacker.weight // 2)
    def light_metal_ability_defender(self):
        if "light-metal" not in self.defender_abilities:
            return self.defender.weight
        return max(1, self.defender.weight // 2)

    # Multiscale: Halves the damage the Pokémon takes when its HP is full.
    def multiscale_ability_attacker(self, current_hp, max_hp):
        if "multiscale" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if current_hp >= max_hp:
            return self.move_power * 0.5
        return self.move_power
    def multiscale_ability_defender(self, current_hp, max_hp):
        if "multiscale" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if current_hp >= max_hp:
            return self.move_power * 0.5
        return self.move_power

    # Harvest: At the end of each turn, there's a 50% chance the Pokémon gets back the Berry it used. It always works in harsh sunlight. Returns the item it's holding after.
    def harvest_ability_attacker(self, held_item, used_item):
        if "harvest" not in self.attacker_abilities or held_item or not used_item or not used_item.endswith("-berry"):
            return held_item
        if self.current_weather() in ("sun", "extreme-sun") or random.random() < 0.5:
            return used_item
        return held_item
    def harvest_ability_defender(self, held_item, used_item):
        if "harvest" not in self.defender_abilities or held_item or not used_item or not used_item.endswith("-berry"):
            return held_item
        if self.current_weather() in ("sun", "extreme-sun") or random.random() < 0.5:
            return used_item
        return held_item

    # Telepathy: The Pokémon doesn't get hit by its ally's damaging moves. from_ally = True if the move came from its ally.
    def telepathy_ability_attacker(self, from_ally=False):
        if "telepathy" not in self.attacker_abilities or not from_ally or self.status_move():
            return self.move_power
        return 0
    def telepathy_ability_defender(self, from_ally=False):
        if "telepathy" not in self.defender_abilities or not from_ally or self.status_move():
            return self.move_power
        return 0

    # Moody: At the end of each turn, one random stat goes up 2 stages and a different one goes down 1 stage. Returns the stat that goes up and the stat that goes down.
    # stat_stages = the Pokémon's current stat stages. A stat already at +6 can't go up and a stat at -6 can't go down.
    def moody_ability_attacker(self, stat_stages=None):
        if "moody" not in self.attacker_abilities:
            return None, None
        stat_stages = stat_stages or {}
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        can_raise = [stat for stat in stats if stat_stages.get(stat, 0) < 6]
        raised = random.choice(can_raise) if can_raise else None
        can_lower = [stat for stat in stats if stat_stages.get(stat, 0) > -6 and stat != raised]
        lowered = random.choice(can_lower) if can_lower else None
        return raised, lowered
    def moody_ability_defender(self, stat_stages=None):
        if "moody" not in self.defender_abilities:
            return None, None
        stat_stages = stat_stages or {}
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        can_raise = [stat for stat in stats if stat_stages.get(stat, 0) < 6]
        raised = random.choice(can_raise) if can_raise else None
        can_lower = [stat for stat in stats if stat_stages.get(stat, 0) > -6 and stat != raised]
        lowered = random.choice(can_lower) if can_lower else None
        return raised, lowered

    # Overcoat: The Pokémon is immune to powder and spore moves. Returns True if the move is blocked.
    # Overcoat's immunity to sandstorm and hail dmg is in WEATHER_EFFECTS.
    def overcoat_ability_attacker(self):
        if "overcoat" not in self.attacker_abilities:
            return False
        return self.powder_and_spore_move() and self.move_name != "rage-powder"
    def overcoat_ability_defender(self):
        if "overcoat" not in self.defender_abilities:
            return False
        return self.powder_and_spore_move() and self.move_name != "rage-powder"

    # Poison Touch: The Pokémon's contact moves have a 30% chance of poisoning the target. Returns the status that actually sticks.
    def poison_touch_ability_attacker(self):
        if "poison-touch" not in self.attacker_abilities or not self.contact_move():
            return self.status_defender
        if "shield-dust" in self.defender_abilities or self.held_item_defender() == "covert-cloak":
            return self.status_defender
        if self.status_effects_defender() or self.status_immune_defender("poison"):
            return self.status_defender
        if random.random() < 0.30:
            return "poison"
        return self.status_defender
    def poison_touch_ability_defender(self):
        if "poison-touch" not in self.defender_abilities or not self.contact_move():
            return self.status_attacker
        if "shield-dust" in self.attacker_abilities or self.held_item_attacker() == "covert-cloak":
            return self.status_attacker
        if self.status_effects_attacker() or self.status_immune_attacker("poison"):
            return self.status_attacker
        if random.random() < 0.30:
            return "poison"
        return self.status_attacker

    # Regenerator: The Pokémon heals 1/3 of its max HP when it switches out.
    def regenerator_ability_attacker(self):
        if "regenerator" not in self.attacker_abilities:
            return 0
        return 1 / 3
    def regenerator_ability_defender(self):
        if "regenerator" not in self.defender_abilities:
            return 0
        return 1 / 3

    # Big Pecks: Other Pokémon's moves and abilities can't lower this Pokémon's Defense.
    # stat = the stat that's changing. Returns the stage change that actually happens.
    def big_pecks_ability_attacker(self, stat, stage_change, from_opponent=True):
        if "big-pecks" not in self.attacker_abilities:
            return stage_change
        if stat == "defense" and stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def big_pecks_ability_defender(self, stat, stage_change, from_opponent=True):
        if "big-pecks" not in self.defender_abilities:
            return stage_change
        if stat == "defense" and stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Sand Rush: Doubles the Pokémon's Speed in a sandstorm.
    # Sand Rush's immunity to sandstorm dmg is in WEATHER_EFFECTS.
    def sand_rush_ability_attacker(self):
        if "sand-rush" not in self.attacker_abilities:
            return self.attacker_stats["speed"]
        if self.current_weather() == "sandstorm":
            return self.attacker_stats["speed"] * 2
        return self.attacker_stats["speed"]
    def sand_rush_ability_defender(self):
        if "sand-rush" not in self.defender_abilities:
            return self.defender_stats["speed"]
        if self.current_weather() == "sandstorm":
            return self.defender_stats["speed"] * 2
        return self.defender_stats["speed"]

    # Wonder Skin: Status moves aimed at the Pokémon only have 50% accuracy. Returns the move's accuracy. None means the move never misses.
    def wonder_skin_ability_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "wonder-skin" not in self.attacker_abilities or not self.status_move():
            return accuracy
        return 50
    def wonder_skin_ability_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "wonder-skin" not in self.defender_abilities or not self.status_move():
            return accuracy
        return 50

    # Analytic: Boosts the power of the Pokémon's moves by 30% if it moves last. moves_last = True if it moves after the other Pokémon.
    def analytic_ability_attacker(self, moves_last):
        if "analytic" not in self.attacker_abilities or not self.move_power or not moves_last:
            return self.move_power
        return self.move_power * 1.3
    def analytic_ability_defender(self, moves_last):
        if "analytic" not in self.defender_abilities or not self.move_power or not moves_last:
            return self.move_power
        return self.move_power * 1.3

    # Illusion: The Pokémon enters battle disguised as the last Pokémon in its party. The disguise breaks when it's hit by a damaging move.
    # disguised_as = the name of the Pokémon it's disguised as. Returns the name the opponent sees after the move.
    def illusion_ability_attacker(self, disguised_as=None):
        if "illusion" not in self.attacker_abilities or not disguised_as:
            return self.attacker.name
        if not self.status_move() and self.type_effectiveness_attacker() > 0:
            return self.attacker.name
        return disguised_as
    def illusion_ability_defender(self, disguised_as=None):
        if "illusion" not in self.defender_abilities or not disguised_as:
            return self.defender.name
        if not self.status_move() and self.type_effectiveness_defender() > 0:
            return self.defender.name
        return disguised_as

    # Imposter: When the Pokémon enters battle, it transforms into the opposing Pokémon and copies its types, stats (except HP) and ability. Returns its types, stats and abilities after.
    # The copied stats are the target's real stats, so they don't go through calculate_stats again.
    def imposter_ability_attacker(self):
        if "imposter" not in self.attacker_abilities:
            return self.attacker.types, self.attacker_stats, self.attacker_abilities
        stats = dict(self.defender_stats)
        stats["hp"] = self.attacker_stats["hp"]
        return self.defender.types, stats, self.defender_abilities
    def imposter_ability_defender(self):
        if "imposter" not in self.defender_abilities:
            return self.defender.types, self.defender_stats, self.defender_abilities
        stats = dict(self.attacker_stats)
        stats["hp"] = self.defender_stats["hp"]
        return self.attacker.types, stats, self.attacker_abilities

    # Infiltrator: The Pokémon's moves ignore the target's Reflect, Light Screen and Aurora Veil. Returns the screen dmg multiplier.
    # screen_active = True if a screen is up that weakens this move.
    def infiltrator_ability_attacker(self, screen_active=False):
        if not screen_active or self.status_move():
            return 1
        if "infiltrator" in self.attacker_abilities:
            return 1
        return 0.5
    def infiltrator_ability_defender(self, screen_active=False):
        if not screen_active or self.status_move():
            return 1
        if "infiltrator" in self.defender_abilities:
            return 1
        return 0.5
        # Will add Substitute, Safeguard and Mist later once those moves are in.

    # Mummy: When the Pokémon is hit by a contact move, the attacker's ability becomes Mummy. Returns the attacker's abilities after.
    def mummy_ability_attacker(self):
        if "mummy" not in self.attacker_abilities or not self.contact_move() or self.ability_shield_item_defender():
            return self.defender_abilities
        for ability in self.defender_abilities:
            if ability in CANT_SUPPRESS_ABILITIES or ability == "mummy":
                return self.defender_abilities
        return ["mummy"]
    def mummy_ability_defender(self):
        if "mummy" not in self.defender_abilities or not self.contact_move() or self.ability_shield_item_attacker():
            return self.attacker_abilities
        for ability in self.attacker_abilities:
            if ability in CANT_SUPPRESS_ABILITIES or ability == "mummy":
                return self.attacker_abilities
        return ["mummy"]

    # Moxie: When the Pokémon knocks out another Pokémon with a move, its Attack goes up 1 stage. Returns the Attack stage change.
    def moxie_ability_attacker(self, knocked_out):
        if "moxie" not in self.attacker_abilities or not knocked_out:
            return 0
        return 1
    def moxie_ability_defender(self, knocked_out):
        if "moxie" not in self.defender_abilities or not knocked_out:
            return 0
        return 1

    # Justified: When the Pokémon is hit by a Dark-type move, its Attack goes up 1 stage. Returns the Attack stage change.
    def justified_ability_attacker(self):
        if "justified" not in self.attacker_abilities or self.move_type != "dark" or self.status_move():
            return 0
        if self.type_effectiveness_attacker() == 0:
            return 0
        return 1
    def justified_ability_defender(self):
        if "justified" not in self.defender_abilities or self.move_type != "dark" or self.status_move():
            return 0
        if self.type_effectiveness_defender() == 0:
            return 0
        return 1

    # Rattled: When the Pokémon is hit by a Dark, Bug or Ghost-type move or gets Intimidated, its Speed goes up 1 stage. Returns the Speed stage change.
    def rattled_ability_attacker(self, intimidated=False):
        if "rattled" not in self.attacker_abilities:
            return 0
        if intimidated:
            return 1
        if self.move_type not in ("dark", "bug", "ghost") or self.status_move():
            return 0
        if self.type_effectiveness_attacker() == 0:
            return 0
        return 1
    def rattled_ability_defender(self, intimidated=False):
        if "rattled" not in self.defender_abilities:
            return 0
        if intimidated:
            return 1
        if self.move_type not in ("dark", "bug", "ghost") or self.status_move():
            return 0
        if self.type_effectiveness_defender() == 0:
            return 0
        return 1

    # Magic Bounce: Status moves like Taunt, Toxic and Stealth Rock get bounced back at the Pokémon that used them. Returns True if the move bounces back.
    def magic_bounce_ability_attacker(self):
        if "magic-bounce" not in self.attacker_abilities:
            return False
        return self.move_name in REFLECTABLE_MOVES
    def magic_bounce_ability_defender(self):
        if "magic-bounce" not in self.defender_abilities:
            return False
        return self.move_name in REFLECTABLE_MOVES

    # Sap Sipper: Grass moves don't affect the Pokémon. Instead they raise its Attack by 1 stage.
    def sap_sipper_ability_attacker(self):
        if "sap-sipper" not in self.attacker_abilities or self.move_type != "grass":
            return self.move_power, 0
        return 0, 1
    def sap_sipper_ability_defender(self):
        if "sap-sipper" not in self.defender_abilities or self.move_type != "grass":
            return self.move_power, 0
        return 0, 1

    # Prankster: The Pokémon's status moves get +1 priority. Returns the move's priority.
    def prankster_ability_attacker(self):
        if "prankster" not in self.attacker_abilities or not self.status_move():
            return self.move_data.priority
        return self.move_data.priority + 1
    def prankster_ability_defender(self):
        if "prankster" not in self.defender_abilities or not self.status_move():
            return self.move_data.priority
        return self.move_data.priority + 1

    # Prankster: Dark types are immune to status moves boosted by Prankster. Returns True if the move fails.
    def prankster_dark_immunity_attacker(self):
        if "prankster" not in self.attacker_abilities or self.move_name not in TARGETED_STATUS_MOVES:
            return False
        return "dark" in self.defender.types
    def prankster_dark_immunity_defender(self):
        if "prankster" not in self.defender_abilities or self.move_name not in TARGETED_STATUS_MOVES:
            return False
        return "dark" in self.attacker.types

    # Sand Force: Boosts the power of the Pokémon's Rock, Ground and Steel-type moves by 30% in a sandstorm.
    # Sand Force's immunity to sandstorm dmg is in WEATHER_EFFECTS.
    def sand_force_ability_attacker(self):
        if "sand-force" not in self.attacker_abilities or not self.move_power or self.current_weather() != "sandstorm":
            return self.move_power
        if self.move_type in ("rock", "ground", "steel"):
            return self.move_power * 1.3
        return self.move_power
    def sand_force_ability_defender(self):
        if "sand-force" not in self.defender_abilities or not self.move_power or self.current_weather() != "sandstorm":
            return self.move_power
        if self.move_type in ("rock", "ground", "steel"):
            return self.move_power * 1.3
        return self.move_power

    # Iron Barbs: Same as Rough Skin. When the Pokémon is hit by a contact move, the attacker takes 1/8 of its max HP as dmg.
    def iron_barbs_ability_attacker(self):
        if "iron-barbs" not in self.attacker_abilities or not self.contact_move():
            return 0
        if "magic-guard" in self.defender_abilities:
            return 0
        return 0.125
    def iron_barbs_ability_defender(self):
        if "iron-barbs" not in self.defender_abilities or not self.contact_move():
            return 0
        if "magic-guard" in self.attacker_abilities:
            return 0
        return 0.125

    # Zen Mode: When Darmanitan's HP is 1/2 or less at the end of a turn, it changes to Zen Mode. Returns its form name, types and stats.
    def zen_mode_ability_attacker(self, current_hp, max_hp):
        if "zen-mode" not in self.attacker_abilities or not self.attacker.name.startswith("darmanitan") or current_hp > max_hp / 2:
            return self.attacker.name, self.attacker.types, self.attacker.stats
        form = BATTLE_FORMS["darmanitan-zen"]
        return "darmanitan-zen", form["types"], form["stats"]
    def zen_mode_ability_defender(self, current_hp, max_hp):
        if "zen-mode" not in self.defender_abilities or not self.defender.name.startswith("darmanitan") or current_hp > max_hp / 2:
            return self.defender.name, self.defender.types, self.defender.stats
        form = BATTLE_FORMS["darmanitan-zen"]
        return "darmanitan-zen", form["types"], form["stats"]

    # Victory Star: Boosts the accuracy of the Pokémon's moves (and its allies' moves) by 10%. Returns the move's accuracy. None means the move never misses.
    def victory_star_ability_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "victory-star" not in self.attacker_abilities or self.ohko_move():
            return accuracy
        return accuracy * 1.1
    def victory_star_ability_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "victory-star" not in self.defender_abilities or self.ohko_move():
            return accuracy
        return accuracy * 1.1

    # Turboblaze: Same as Mold Breaker. The Pokémon's moves ignore abilities that would block or weaken them. Returns the target's abilities that still work.
    def turboblaze_ability_attacker(self):
        if "turboblaze" not in self.attacker_abilities or self.ability_shield_item_defender():
            return self.defender_abilities
        return [ability for ability in self.defender_abilities if ability not in BREAKABLE_ABILITIES]
    def turboblaze_ability_defender(self):
        if "turboblaze" not in self.defender_abilities or self.ability_shield_item_attacker():
            return self.attacker_abilities
        return [ability for ability in self.attacker_abilities if ability not in BREAKABLE_ABILITIES]

    # Teravolt: Same as Mold Breaker. The Pokémon's moves ignore abilities that would block or weaken them. Returns the target's abilities that still work.
    def teravolt_ability_attacker(self):
        if "teravolt" not in self.attacker_abilities or self.ability_shield_item_defender():
            return self.defender_abilities
        return [ability for ability in self.defender_abilities if ability not in BREAKABLE_ABILITIES]
    def teravolt_ability_defender(self):
        if "teravolt" not in self.defender_abilities or self.ability_shield_item_attacker():
            return self.attacker_abilities
        return [ability for ability in self.attacker_abilities if ability not in BREAKABLE_ABILITIES]

    # Aroma Veil: The Pokémon and its allies can't be infatuated, taunted, tormented, encored, disabled or heal blocked.
    # incoming_effect = the effect a move or ability is trying to give. Returns True if Aroma Veil blocks it.
    def aroma_veil_ability_attacker(self, incoming_effect):
        if "aroma-veil" not in self.attacker_abilities:
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["aroma-veil"]
    def aroma_veil_ability_defender(self, incoming_effect):
        if "aroma-veil" not in self.defender_abilities:
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["aroma-veil"]

    # Flower Veil: Other Pokémon can't lower the stats of its Grass-type allies, or its own if it's Grass type. Returns the stage change that actually happens.
    def flower_veil_ability_attacker(self, stage_change, from_opponent=True):
        if "flower-veil" not in self.attacker_abilities or "grass" not in self.attacker.types:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def flower_veil_ability_defender(self, stage_change, from_opponent=True):
        if "flower-veil" not in self.defender_abilities or "grass" not in self.defender.types:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Flower Veil: Its Grass-type allies, and itself if it's Grass type, can't get a status from other Pokémon. Returns the status that actually sticks.
    def flower_veil_status_attacker(self):
        if "flower-veil" not in self.attacker_abilities or "grass" not in self.attacker.types:
            return self.status_attacker
        return None
    def flower_veil_status_defender(self):
        if "flower-veil" not in self.defender_abilities or "grass" not in self.defender.types:
            return self.status_defender
        return None
        # Will add the ally part later for doubles.

    # Cheek Pouch: When the Pokémon eats a Berry, it also heals 1/3 of its max HP. ate_berry = True if it ate a Berry this turn.
    def cheek_pouch_ability_attacker(self, ate_berry):
        if "cheek-pouch" not in self.attacker_abilities or not ate_berry:
            return 0
        return 1 / 3
    def cheek_pouch_ability_defender(self, ate_berry):
        if "cheek-pouch" not in self.defender_abilities or not ate_berry:
            return 0
        return 1 / 3

    # Protean: The Pokémon's type changes to the type of the move it's about to use. It only works once each time it enters battle. Returns its types.
    # already_used = True if Protean already changed its type since it came in.
    def protean_ability_attacker(self, already_used=False):
        if "protean" not in self.attacker_abilities or already_used:
            return self.attacker.types
        return [self.move_type]
    def protean_ability_defender(self, already_used=False):
        if "protean" not in self.defender_abilities or already_used:
            return self.defender.types
        return [self.move_type]

    # Fur Coat: Doubles the Pokémon's Defense.
    def fur_coat_ability_attacker(self):
        if "fur-coat" not in self.attacker_abilities:
            return self.attacker_stats["defense"]
        return self.attacker_stats["defense"] * 2
    def fur_coat_ability_defender(self):
        if "fur-coat" not in self.defender_abilities:
            return self.defender_stats["defense"]
        return self.defender_stats["defense"] * 2

    # Magician: When the Pokémon hits a target with a damaging move, it steals the target's item if it isn't holding one. Returns the item it's holding after.
    def magician_ability_attacker(self, held_item, opponent_item):
        if "magician" not in self.attacker_abilities or held_item or self.status_move() or self.move_name == "fling":
            return held_item
        if "sticky-hold" in self.defender_abilities or self.type_effectiveness_defender() == 0:
            return held_item
        return opponent_item
    def magician_ability_defender(self, held_item, opponent_item):
        if "magician" not in self.defender_abilities or held_item or self.status_move() or self.move_name == "fling":
            return held_item
        if "sticky-hold" in self.attacker_abilities or self.type_effectiveness_attacker() == 0:
            return held_item
        return opponent_item

    # Competitive: When an opposing Pokémon lowers one of its stats, its Sp. Atk goes up 2 stages. Returns the Sp. Atk stage change.
    def competitive_ability_attacker(self, stage_change, from_opponent=True):
        if "competitive" not in self.attacker_abilities or stage_change >= 0 or not from_opponent:
            return 0
        return 2
    def competitive_ability_defender(self, stage_change, from_opponent=True):
        if "competitive" not in self.defender_abilities or stage_change >= 0 or not from_opponent:
            return 0
        return 2

    # Strong Jaw: Boosts the power of the Pokémon's biting moves by 50%.
    def strong_jaw_ability_attacker(self):
        if "strong-jaw" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.bite_move():
            return self.move_power * 1.5
        return self.move_power
    def strong_jaw_ability_defender(self):
        if "strong-jaw" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.bite_move():
            return self.move_power * 1.5
        return self.move_power

    # Refrigerate: The Pokémon's Normal-type moves become Ice type and do 20% more damage. Returns the move's type and power.
    def refrigerate_ability_attacker(self):
        if "refrigerate" not in self.attacker_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "ice", self.move_power
        return "ice", self.move_power * 1.2
    def refrigerate_ability_defender(self):
        if "refrigerate" not in self.defender_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "ice", self.move_power
        return "ice", self.move_power * 1.2

    # Sweet Veil: The Pokémon and its allies can't fall asleep. Returns the status that actually sticks.
    def sweet_veil_ability_attacker(self):
        if "sweet-veil" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker == "sleep":
            return None
        return self.status_attacker
    def sweet_veil_ability_defender(self):
        if "sweet-veil" not in self.defender_abilities:
            return self.status_defender
        if self.status_defender == "sleep":
            return None
        return self.status_defender
        # Will add the ally part later for doubles.

    # Stance Change: Aegislash changes to Blade Forme when it uses a damaging move and back to Shield Forme when it uses King's Shield. Returns its form name, types and stats.
    # blade_forme = True if it's already in Blade Forme.
    def stance_change_ability_attacker(self, blade_forme=False):
        shield = (self.attacker.name, self.attacker.types, self.attacker.stats)
        blade = ("aegislash-blade", BATTLE_FORMS["aegislash-blade"]["types"], BATTLE_FORMS["aegislash-blade"]["stats"])
        if "stance-change" not in self.attacker_abilities or not self.attacker.name.startswith("aegislash"):
            return shield
        if self.move_name == "kings-shield":
            return shield
        if self.status_move():
            return blade if blade_forme else shield
        return blade
    def stance_change_ability_defender(self, blade_forme=False):
        shield = (self.defender.name, self.defender.types, self.defender.stats)
        blade = ("aegislash-blade", BATTLE_FORMS["aegislash-blade"]["types"], BATTLE_FORMS["aegislash-blade"]["stats"])
        if "stance-change" not in self.defender_abilities or not self.defender.name.startswith("aegislash"):
            return shield
        if self.move_name == "kings-shield":
            return shield
        if self.status_move():
            return blade if blade_forme else shield
        return blade

    # Gale Wings: The Pokémon's Flying-type moves get +1 priority when its HP is full. Returns the move's priority.
    def gale_wings_ability_attacker(self, current_hp, max_hp):
        if "gale-wings" not in self.attacker_abilities or self.move_type != "flying" or current_hp < max_hp:
            return self.move_data.priority
        return self.move_data.priority + 1
    def gale_wings_ability_defender(self, current_hp, max_hp):
        if "gale-wings" not in self.defender_abilities or self.move_type != "flying" or current_hp < max_hp:
            return self.move_data.priority
        return self.move_data.priority + 1

    # Mega Launcher: Boosts the power of the Pokémon's pulse moves by 50%.
    def mega_launcher_ability_attacker(self):
        if "mega-launcher" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.pulse_move():
            return self.move_power * 1.5
        return self.move_power
    def mega_launcher_ability_defender(self):
        if "mega-launcher" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.pulse_move():
            return self.move_power * 1.5
        return self.move_power
        # Will add Heal Pulse healing 3/4 instead of 1/2 later.

    # Grass Pelt: Boosts the Pokémon's Defense by 50% in Grassy Terrain.
    def grass_pelt_ability_attacker(self):
        if "grass-pelt" not in self.attacker_abilities or self.terrain != "grassy-terrain":
            return self.attacker_stats["defense"]
        return self.attacker_stats["defense"] * 1.5
    def grass_pelt_ability_defender(self):
        if "grass-pelt" not in self.defender_abilities or self.terrain != "grassy-terrain":
            return self.defender_stats["defense"]
        return self.defender_stats["defense"] * 1.5

    # Symbiosis: When the Pokémon's ally uses up its item, the Pokémon passes its own item to the ally. Returns the item the ally gets.
    # ally_used_item = True if the ally just used up its item.
    def symbiosis_ability_attacker(self, held_item, ally_used_item=False):
        if "symbiosis" not in self.attacker_abilities or not ally_used_item or not held_item:
            return None
        return held_item
    def symbiosis_ability_defender(self, held_item, ally_used_item=False):
        if "symbiosis" not in self.defender_abilities or not ally_used_item or not held_item:
            return None
        return held_item

    # Tough Claws: Boosts the power of the Pokémon's contact moves by 30%.
    def tough_claws_ability_attacker(self):
        if "tough-claws" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.contact_move():
            return self.move_power * 1.3
        return self.move_power
    def tough_claws_ability_defender(self):
        if "tough-claws" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.contact_move():
            return self.move_power * 1.3
        return self.move_power

    # Pixilate: The Pokémon's Normal-type moves become Fairy type and do 20% more damage. Returns the move's type and power.
    def pixilate_ability_attacker(self):
        if "pixilate" not in self.attacker_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "fairy", self.move_power
        return "fairy", self.move_power * 1.2
    def pixilate_ability_defender(self):
        if "pixilate" not in self.defender_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "fairy", self.move_power
        return "fairy", self.move_power * 1.2

    # Gooey: When the Pokémon is hit by a contact move, the attacker's Speed goes down 1 stage. Returns the attacker's Speed stage change.
    def gooey_ability_attacker(self):
        if "gooey" not in self.attacker_abilities or not self.contact_move():
            return 0
        return -1
    def gooey_ability_defender(self):
        if "gooey" not in self.defender_abilities or not self.contact_move():
            return 0
        return -1

    # Aerilate: The Pokémon's Normal-type moves become Flying type and do 20% more damage. Returns the move's type and power.
    def aerilate_ability_attacker(self):
        if "aerilate" not in self.attacker_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "flying", self.move_power
        return "flying", self.move_power * 1.2
    def aerilate_ability_defender(self):
        if "aerilate" not in self.defender_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "flying", self.move_power
        return "flying", self.move_power * 1.2

    # Parental Bond: The Pokémon's damaging moves hit twice. The second hit does 1/4 of the damage. Returns the power of each hit.
    def parental_bond_ability_attacker(self):
        if "parental-bond" not in self.attacker_abilities or not self.move_power or self.move_name in PARENTAL_BOND_EXCEPTIONS:
            return (self.move_power,)
        if self.move_data.meta is not None and self.move_data.meta.get("max_hits"):
            return (self.move_power,)
        return self.move_power, self.move_power * 0.25
    def parental_bond_ability_defender(self):
        if "parental-bond" not in self.defender_abilities or not self.move_power or self.move_name in PARENTAL_BOND_EXCEPTIONS:
            return (self.move_power,)
        if self.move_data.meta is not None and self.move_data.meta.get("max_hits"):
            return (self.move_power,)
        return self.move_power, self.move_power * 0.25

    # Dark Aura: Boosts the power of every Pokémon's Dark-type moves by 33%. With Aura Break out, they do 25% less instead.
    # Dark Aura affects the whole field, so it's one check instead of attacker/defender versions.
    def dark_aura_on_field(self):
        return "dark-aura" in self.attacker_abilities or "dark-aura" in self.defender_abilities
    def dark_aura_ability(self):
        if not self.dark_aura_on_field() or self.move_type != "dark" or not self.move_power:
            return self.move_power
        if self.aura_break_on_field():
            return self.move_power * 0.75
        return self.move_power * 1.33

    # Fairy Aura: Boosts the power of every Pokémon's Fairy-type moves by 33%. With Aura Break out, they do 25% less instead.
    # Fairy Aura affects the whole field, so it's one check instead of attacker/defender versions.
    def fairy_aura_on_field(self):
        return "fairy-aura" in self.attacker_abilities or "fairy-aura" in self.defender_abilities
    def fairy_aura_ability(self):
        if not self.fairy_aura_on_field() or self.move_type != "fairy" or not self.move_power:
            return self.move_power
        if self.aura_break_on_field():
            return self.move_power * 0.75
        return self.move_power * 1.33

    # Aura Break: Reverses Dark Aura and Fairy Aura, so those moves do 25% less damage instead of 33% more.
    # Aura Break affects the whole field, so it's one check instead of attacker/defender versions.
    def aura_break_on_field(self):
        return "aura-break" in self.attacker_abilities or "aura-break" in self.defender_abilities

    # Primordial Sea: Summons heavy rain when the Pokémon enters battle. It lasts until the Pokémon leaves the field.
    def primordial_sea_ability_attacker(self):
        if "primordial-sea" not in self.attacker_abilities:
            return self.weather
        self.weather = "heavy-rain"
        self.weather_turns = WEATHER_EFFECTS["heavy-rain"]["turns"]
        return self.weather
    def primordial_sea_ability_defender(self):
        if "primordial-sea" not in self.defender_abilities:
            return self.weather
        self.weather = "heavy-rain"
        self.weather_turns = WEATHER_EFFECTS["heavy-rain"]["turns"]
        return self.weather

    # Desolate Land: Summons extreme sunlight when the Pokémon enters battle. It lasts until the Pokémon leaves the field.
    def desolate_land_ability_attacker(self):
        if "desolate-land" not in self.attacker_abilities:
            return self.weather
        self.weather = "extreme-sun"
        self.weather_turns = WEATHER_EFFECTS["extreme-sun"]["turns"]
        return self.weather
    def desolate_land_ability_defender(self):
        if "desolate-land" not in self.defender_abilities:
            return self.weather
        self.weather = "extreme-sun"
        self.weather_turns = WEATHER_EFFECTS["extreme-sun"]["turns"]
        return self.weather

    # Delta Stream: Summons strong winds when the Pokémon enters battle. It lasts until the Pokémon leaves the field.
    def delta_stream_ability_attacker(self):
        if "delta-stream" not in self.attacker_abilities:
            return self.weather
        self.weather = "strong-winds"
        self.weather_turns = WEATHER_EFFECTS["strong-winds"]["turns"]
        return self.weather
    def delta_stream_ability_defender(self):
        if "delta-stream" not in self.defender_abilities:
            return self.weather
        self.weather = "strong-winds"
        self.weather_turns = WEATHER_EFFECTS["strong-winds"]["turns"]
        return self.weather

    # Stamina: When the Pokémon is hit by a damaging move, its Defense goes up 1 stage. Returns the Defense stage change.
    def stamina_ability_attacker(self):
        if "stamina" not in self.attacker_abilities or self.status_move():
            return 0
        if self.type_effectiveness_attacker() == 0:
            return 0
        return 1
    def stamina_ability_defender(self):
        if "stamina" not in self.defender_abilities or self.status_move():
            return 0
        if self.type_effectiveness_defender() == 0:
            return 0
        return 1

    # Wimp Out: When a hit drops the Pokémon's HP to 1/2 or less, it switches out. Returns True if it switches out.
    # damage = the dmg from the hit. current_hp = its HP before the hit.
    def wimp_out_ability_attacker(self, damage, current_hp, max_hp):
        if "wimp-out" not in self.attacker_abilities:
            return False
        hp_after = current_hp - damage
        return 0 < hp_after <= max_hp / 2 and current_hp > max_hp / 2
    def wimp_out_ability_defender(self, damage, current_hp, max_hp):
        if "wimp-out" not in self.defender_abilities:
            return False
        hp_after = current_hp - damage
        return 0 < hp_after <= max_hp / 2 and current_hp > max_hp / 2

    # Emergency Exit: Same as Wimp Out. When a hit drops the Pokémon's HP to 1/2 or less, it switches out. Returns True if it switches out.
    def emergency_exit_ability_attacker(self, damage, current_hp, max_hp):
        if "emergency-exit" not in self.attacker_abilities:
            return False
        hp_after = current_hp - damage
        return 0 < hp_after <= max_hp / 2 and current_hp > max_hp / 2
    def emergency_exit_ability_defender(self, damage, current_hp, max_hp):
        if "emergency-exit" not in self.defender_abilities:
            return False
        hp_after = current_hp - damage
        return 0 < hp_after <= max_hp / 2 and current_hp > max_hp / 2

    # Water Compaction: When the Pokémon is hit by a Water-type move, its Defense goes up 2 stages. Returns the Defense stage change.
    def water_compaction_ability_attacker(self):
        if "water-compaction" not in self.attacker_abilities or self.move_type != "water" or self.status_move():
            return 0
        return 2
    def water_compaction_ability_defender(self):
        if "water-compaction" not in self.defender_abilities or self.move_type != "water" or self.status_move():
            return 0
        return 2

    # Merciless: The Pokémon's moves always land a critical hit on a poisoned target. Returns the move's crit stage.
    def merciless_ability_attacker(self):
        crit_stage = 0
        if self.move_data.meta is not None:
            crit_stage = self.move_data.meta.get("crit_rate") or 0
        if "merciless" in self.attacker_abilities and self.status_defender in ("poison", "badly-poison"):
            return 3
        return min(crit_stage, 3)
    def merciless_ability_defender(self):
        crit_stage = 0
        if self.move_data.meta is not None:
            crit_stage = self.move_data.meta.get("crit_rate") or 0
        if "merciless" in self.defender_abilities and self.status_attacker in ("poison", "badly-poison"):
            return 3
        return min(crit_stage, 3)

    # Shields Down: Minior is in Meteor Form above 1/2 HP and changes to Core Form at 1/2 HP or less. Returns its form name, types and stats.
    def shields_down_ability_attacker(self, current_hp, max_hp):
        if "shields-down" not in self.attacker_abilities or not self.attacker.name.startswith("minior") or current_hp > max_hp / 2:
            return self.attacker.name, self.attacker.types, self.attacker.stats
        form = BATTLE_FORMS["minior-core"]
        return "minior-core", form["types"], form["stats"]
    def shields_down_ability_defender(self, current_hp, max_hp):
        if "shields-down" not in self.defender_abilities or not self.defender.name.startswith("minior") or current_hp > max_hp / 2:
            return self.defender.name, self.defender.types, self.defender.stats
        form = BATTLE_FORMS["minior-core"]
        return "minior-core", form["types"], form["stats"]

    # Shields Down: In Meteor Form, Minior can't get a status. Returns the status that actually sticks.
    def shields_down_status_attacker(self, current_hp, max_hp):
        if "shields-down" not in self.attacker_abilities or not self.attacker.name.startswith("minior") or current_hp <= max_hp / 2:
            return self.status_attacker
        return None
    def shields_down_status_defender(self, current_hp, max_hp):
        if "shields-down" not in self.defender_abilities or not self.defender.name.startswith("minior") or current_hp <= max_hp / 2:
            return self.status_defender
        return None

    # Stakeout: The Pokémon's Attack and Sp. Atk are doubled against a target that just switched in. Returns its Attack and Sp. Atk.
    # target_switched_in = True if the target switched in this turn.
    def stakeout_ability_attacker(self, target_switched_in=False):
        attack = self.attacker_stats["attack"]
        special_attack = self.attacker_stats["special-attack"]
        if "stakeout" not in self.attacker_abilities or not target_switched_in:
            return attack, special_attack
        return attack * 2, special_attack * 2
    def stakeout_ability_defender(self, target_switched_in=False):
        attack = self.defender_stats["attack"]
        special_attack = self.defender_stats["special-attack"]
        if "stakeout" not in self.defender_abilities or not target_switched_in:
            return attack, special_attack
        return attack * 2, special_attack * 2

    # Water Bubble: Fire-type moves do half damage to the Pokémon.
    def water_bubble_ability_attacker(self):
        if "water-bubble" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire":
            return self.move_power * 0.5
        return self.move_power
    def water_bubble_ability_defender(self):
        if "water-bubble" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire":
            return self.move_power * 0.5
        return self.move_power

    # Water Bubble: The Pokémon's Water-type moves do double damage.
    def water_bubble_power_attacker(self):
        if "water-bubble" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "water":
            return self.move_power * 2
        return self.move_power
    def water_bubble_power_defender(self):
        if "water-bubble" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "water":
            return self.move_power * 2
        return self.move_power

    # Water Bubble: The Pokémon can't be burned. Returns the status that actually sticks.
    def water_bubble_status_attacker(self):
        if "water-bubble" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker == STATUS_IMMUNITY_ABILITIES["water-bubble"]:
            return None
        return self.status_attacker
    def water_bubble_status_defender(self):
        if "water-bubble" not in self.defender_abilities:
            return self.status_defender
        if self.status_defender == STATUS_IMMUNITY_ABILITIES["water-bubble"]:
            return None
        return self.status_defender

    # Steelworker: Boosts the power of the Pokémon's Steel-type moves by 50%.
    def steelworker_ability_attacker(self):
        if "steelworker" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "steel":
            return self.move_power * 1.5
        return self.move_power
    def steelworker_ability_defender(self):
        if "steelworker" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "steel":
            return self.move_power * 1.5
        return self.move_power

    # Berserk: When a hit drops the Pokémon's HP to 1/2 or less, its Sp. Atk goes up 1 stage. Returns the Sp. Atk stage change.
    # damage = the dmg from the hit. current_hp = its HP before the hit.
    def berserk_ability_attacker(self, damage, current_hp, max_hp):
        if "berserk" not in self.attacker_abilities:
            return 0
        hp_after = current_hp - damage
        if 0 < hp_after <= max_hp / 2 and current_hp > max_hp / 2:
            return 1
        return 0
    def berserk_ability_defender(self, damage, current_hp, max_hp):
        if "berserk" not in self.defender_abilities:
            return 0
        hp_after = current_hp - damage
        if 0 < hp_after <= max_hp / 2 and current_hp > max_hp / 2:
            return 1
        return 0

    # Slush Rush: Doubles the Pokémon's Speed in snow.
    def slush_rush_ability_attacker(self):
        if "slush-rush" not in self.attacker_abilities:
            return self.attacker_stats["speed"]
        if self.current_weather() in ("snow", "hail"):
            return self.attacker_stats["speed"] * 2
        return self.attacker_stats["speed"]
    def slush_rush_ability_defender(self):
        if "slush-rush" not in self.defender_abilities:
            return self.defender_stats["speed"]
        if self.current_weather() in ("snow", "hail"):
            return self.defender_stats["speed"] * 2
        return self.defender_stats["speed"]

    # Long Reach: The Pokémon's moves don't make contact. Returns True if the move makes contact.
    def long_reach_ability_attacker(self):
        if not self.contact_move():
            return False
        return "long-reach" not in self.attacker_abilities
    def long_reach_ability_defender(self):
        if not self.contact_move():
            return False
        return "long-reach" not in self.defender_abilities
        # Will have the contact abilities (Rough Skin, Static, etc.) check this later.

    # Liquid Voice: The Pokémon's sound moves become Water type. Returns the move's type.
    def liquid_voice_ability_attacker(self):
        if "liquid-voice" not in self.attacker_abilities or not self.sound_move():
            return self.move_type
        return "water"
    def liquid_voice_ability_defender(self):
        if "liquid-voice" not in self.defender_abilities or not self.sound_move():
            return self.move_type
        return "water"

    # Triage: The Pokémon's healing moves get +3 priority. Returns the move's priority.
    def triage_ability_attacker(self):
        if "triage" not in self.attacker_abilities or self.move_name not in HEALING_MOVES:
            return self.move_data.priority
        return self.move_data.priority + 3
    def triage_ability_defender(self):
        if "triage" not in self.defender_abilities or self.move_name not in HEALING_MOVES:
            return self.move_data.priority
        return self.move_data.priority + 3

    # Galvanize: The Pokémon's Normal-type moves become Electric type and do 20% more damage. Returns the move's type and power.
    def galvanize_ability_attacker(self):
        if "galvanize" not in self.attacker_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "electric", self.move_power
        return "electric", self.move_power * 1.2
    def galvanize_ability_defender(self):
        if "galvanize" not in self.defender_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "electric", self.move_power
        return "electric", self.move_power * 1.2

    # Surge Surfer: Doubles the Pokémon's Speed in Electric Terrain.
    def surge_surfer_ability_attacker(self):
        if "surge-surfer" not in self.attacker_abilities or self.terrain != "electric-terrain":
            return self.attacker_stats["speed"]
        return self.attacker_stats["speed"] * 2
    def surge_surfer_ability_defender(self):
        if "surge-surfer" not in self.defender_abilities or self.terrain != "electric-terrain":
            return self.defender_stats["speed"]
        return self.defender_stats["speed"] * 2

    # Schooling: Wishiwashi is in School Form above 1/4 HP and goes back to Solo Form at 1/4 HP or less. Returns its form name, types and stats.
    def schooling_ability_attacker(self, current_hp, max_hp):
        if "schooling" not in self.attacker_abilities or not self.attacker.name.startswith("wishiwashi") or current_hp <= max_hp / 4:
            return self.attacker.name, self.attacker.types, self.attacker.stats
        form = BATTLE_FORMS["wishiwashi-school"]
        return "wishiwashi-school", form["types"], form["stats"]
    def schooling_ability_defender(self, current_hp, max_hp):
        if "schooling" not in self.defender_abilities or not self.defender.name.startswith("wishiwashi") or current_hp <= max_hp / 4:
            return self.defender.name, self.defender.types, self.defender.stats
        form = BATTLE_FORMS["wishiwashi-school"]
        return "wishiwashi-school", form["types"], form["stats"]

    # Disguise: The first damaging hit Mimikyu takes does no damage. It busts the disguise and Mimikyu loses 1/8 of its max HP instead. Returns the move's power and the HP Mimikyu loses.
    # busted = True if the disguise is already broken.
    def disguise_ability_attacker(self, busted=False):
        if "disguise" not in self.attacker_abilities or not self.attacker.name.startswith("mimikyu") or busted:
            return self.move_power, 0
        if self.status_move() or self.type_effectiveness_attacker() == 0:
            return self.move_power, 0
        return 0, 0.125
    def disguise_ability_defender(self, busted=False):
        if "disguise" not in self.defender_abilities or not self.defender.name.startswith("mimikyu") or busted:
            return self.move_power, 0
        if self.status_move() or self.type_effectiveness_defender() == 0:
            return self.move_power, 0
        return 0, 0.125

    # Battle Bond: The first time Greninja knocks out a Pokémon, its Attack, Sp. Atk and Speed go up 1 stage. Returns the Attack, Sp. Atk and Speed stage changes.
    # already_used = True if Battle Bond already went off this battle.
    def battle_bond_ability_attacker(self, knocked_out, already_used=False):
        if "battle-bond" not in self.attacker_abilities or not self.attacker.name.startswith("greninja"):
            return 0, 0, 0
        if not knocked_out or already_used:
            return 0, 0, 0
        return 1, 1, 1
    def battle_bond_ability_defender(self, knocked_out, already_used=False):
        if "battle-bond" not in self.defender_abilities or not self.defender.name.startswith("greninja"):
            return 0, 0, 0
        if not knocked_out or already_used:
            return 0, 0, 0
        return 1, 1, 1

    # Power Construct: When Zygarde's HP is 1/2 or less at the end of a turn, it changes to Complete Forme. Returns its form name, types and stats.
    def power_construct_ability_attacker(self, current_hp, max_hp):
        if "power-construct" not in self.attacker_abilities or not self.attacker.name.startswith("zygarde") or current_hp > max_hp / 2:
            return self.attacker.name, self.attacker.types, self.attacker.stats
        form = BATTLE_FORMS["zygarde-complete"]
        return "zygarde-complete", form["types"], form["stats"]
    def power_construct_ability_defender(self, current_hp, max_hp):
        if "power-construct" not in self.defender_abilities or not self.defender.name.startswith("zygarde") or current_hp > max_hp / 2:
            return self.defender.name, self.defender.types, self.defender.stats
        form = BATTLE_FORMS["zygarde-complete"]
        return "zygarde-complete", form["types"], form["stats"]

    # Corrosion: The Pokémon can poison Steel and Poison types. Returns True if the target still can't be poisoned.
    def corrosion_ability_attacker(self, incoming_status):
        if "corrosion" not in self.attacker_abilities or incoming_status not in ("poison", "badly-poison"):
            return self.status_immune_defender(incoming_status)
        for ability in self.defender_abilities:
            if STATUS_IMMUNITY_ABILITIES.get(ability) in ("all", "poison"):
                return True
        return self.field_blocks_status_defender(incoming_status)
    def corrosion_ability_defender(self, incoming_status):
        if "corrosion" not in self.defender_abilities or incoming_status not in ("poison", "badly-poison"):
            return self.status_immune_attacker(incoming_status)
        for ability in self.attacker_abilities:
            if STATUS_IMMUNITY_ABILITIES.get(ability) in ("all", "poison"):
                return True
        return self.field_blocks_status_attacker(incoming_status)

    # Comatose: The Pokémon is always drowsy, so moves like Hex and Wake-Up Slap treat it as asleep. Returns True if it counts as asleep.
    # Comatose's status immunity is in STATUS_IMMUNITY_ABILITIES.
    def comatose_ability_attacker(self):
        return "comatose" in self.attacker_abilities
    def comatose_ability_defender(self):
        return "comatose" in self.defender_abilities

    # Queenly Majesty: Opposing Pokémon can't use priority moves on the Pokémon. Returns True if the move is blocked.
    # priority = the move's priority after abilities like Prankster.
    def queenly_majesty_ability_attacker(self, priority=None):
        if "queenly-majesty" not in self.attacker_abilities:
            return False
        if priority is None:
            priority = self.move_data.priority
        if priority <= 0:
            return False
        return not self.status_move() or self.move_name in TARGETED_STATUS_MOVES
    def queenly_majesty_ability_defender(self, priority=None):
        if "queenly-majesty" not in self.defender_abilities:
            return False
        if priority is None:
            priority = self.move_data.priority
        if priority <= 0:
            return False
        return not self.status_move() or self.move_name in TARGETED_STATUS_MOVES

    # Innards Out: When the Pokémon is knocked out, the attacker takes dmg equal to the HP the Pokémon had left. Returns that dmg.
    # damage = the dmg from the hit. current_hp = its HP before the hit.
    def innards_out_ability_attacker(self, damage, current_hp):
        if "innards-out" not in self.attacker_abilities or damage < current_hp:
            return 0
        if "magic-guard" in self.defender_abilities:
            return 0
        return current_hp
    def innards_out_ability_defender(self, damage, current_hp):
        if "innards-out" not in self.defender_abilities or damage < current_hp:
            return 0
        if "magic-guard" in self.attacker_abilities:
            return 0
        return current_hp

    # Dancer: When another Pokémon uses a dance move, the Pokémon copies it right after. Returns True if it copies the move.
    def dancer_ability_attacker(self):
        if "dancer" not in self.attacker_abilities:
            return False
        return self.move_name in DANCE_MOVES
    def dancer_ability_defender(self):
        if "dancer" not in self.defender_abilities:
            return False
        return self.move_name in DANCE_MOVES

    # Battery: Boosts the power of its allies' special moves by 30%. ally_abilities = the abilities of the attacker's ally.
    def battery_ability_attacker(self, ally_abilities=None):
        if not ally_abilities or "battery" not in ally_abilities or not self.move_power:
            return self.move_power
        if self.move_data.damage_class == "special":
            return self.move_power * 1.3
        return self.move_power
    def battery_ability_defender(self, ally_abilities=None):
        if not ally_abilities or "battery" not in ally_abilities or not self.move_power:
            return self.move_power
        if self.move_data.damage_class == "special":
            return self.move_power * 1.3
        return self.move_power

    # Fluffy: Contact moves do half damage to the Pokémon, but Fire-type moves do double.
    def fluffy_ability_attacker(self):
        if "fluffy" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        power = self.move_power
        if self.move_type == "fire":
            power *= 2
        if self.contact_move():
            power *= 0.5
        return power
    def fluffy_ability_defender(self):
        if "fluffy" not in self.defender_abilities or not self.move_power:
            return self.move_power
        power = self.move_power
        if self.move_type == "fire":
            power *= 2
        if self.contact_move():
            power *= 0.5
        return power

    # Dazzling: Same as Queenly Majesty. Opposing Pokémon can't use priority moves on the Pokémon. Returns True if the move is blocked.
    def dazzling_ability_attacker(self, priority=None):
        if "dazzling" not in self.attacker_abilities:
            return False
        if priority is None:
            priority = self.move_data.priority
        if priority <= 0:
            return False
        return not self.status_move() or self.move_name in TARGETED_STATUS_MOVES
    def dazzling_ability_defender(self, priority=None):
        if "dazzling" not in self.defender_abilities:
            return False
        if priority is None:
            priority = self.move_data.priority
        if priority <= 0:
            return False
        return not self.status_move() or self.move_name in TARGETED_STATUS_MOVES

    # Soul-Heart: Every time another Pokémon faints, the Pokémon's Sp. Atk goes up 1 stage. Returns the Sp. Atk stage change.
    # fainted_count = how many other Pokémon just fainted.
    def soul_heart_ability_attacker(self, fainted_count=0):
        if "soul-heart" not in self.attacker_abilities:
            return 0
        return fainted_count
    def soul_heart_ability_defender(self, fainted_count=0):
        if "soul-heart" not in self.defender_abilities:
            return 0
        return fainted_count

    # Tangling Hair: Same as Gooey. When the Pokémon is hit by a contact move, the attacker's Speed goes down 1 stage. Returns the attacker's Speed stage change.
    def tangling_hair_ability_attacker(self):
        if "tangling-hair" not in self.attacker_abilities or not self.contact_move():
            return 0
        return -1
    def tangling_hair_ability_defender(self):
        if "tangling-hair" not in self.defender_abilities or not self.contact_move():
            return 0
        return -1

    # Receiver: When the Pokémon's ally faints, it copies the ally's ability. Returns the Pokémon's abilities after.
    # fainted_ally_abilities = the abilities of the ally that fainted.
    def receiver_ability_attacker(self, fainted_ally_abilities=None):
        if "receiver" not in self.attacker_abilities or not fainted_ally_abilities:
            return self.attacker_abilities
        copied = [ability for ability in fainted_ally_abilities if ability not in RECEIVER_BANNED_ABILITIES]
        if not copied:
            return self.attacker_abilities
        return copied
    def receiver_ability_defender(self, fainted_ally_abilities=None):
        if "receiver" not in self.defender_abilities or not fainted_ally_abilities:
            return self.defender_abilities
        copied = [ability for ability in fainted_ally_abilities if ability not in RECEIVER_BANNED_ABILITIES]
        if not copied:
            return self.defender_abilities
        return copied

    # Power of Alchemy: Same as Receiver. When the Pokémon's ally faints, it copies the ally's ability. Returns the Pokémon's abilities after.
    def power_of_alchemy_ability_attacker(self, fainted_ally_abilities=None):
        if "power-of-alchemy" not in self.attacker_abilities or not fainted_ally_abilities:
            return self.attacker_abilities
        copied = [ability for ability in fainted_ally_abilities if ability not in RECEIVER_BANNED_ABILITIES]
        if not copied:
            return self.attacker_abilities
        return copied
    def power_of_alchemy_ability_defender(self, fainted_ally_abilities=None):
        if "power-of-alchemy" not in self.defender_abilities or not fainted_ally_abilities:
            return self.defender_abilities
        copied = [ability for ability in fainted_ally_abilities if ability not in RECEIVER_BANNED_ABILITIES]
        if not copied:
            return self.defender_abilities
        return copied

    # Beast Boost: When the Pokémon knocks out another Pokémon with a move, its highest stat goes up 1 stage. Returns the stat that goes up.
    def beast_boost_ability_attacker(self, knocked_out):
        if "beast-boost" not in self.attacker_abilities or not knocked_out:
            return None
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        return max(stats, key=lambda stat: self.attacker_stats[stat])
    def beast_boost_ability_defender(self, knocked_out):
        if "beast-boost" not in self.defender_abilities or not knocked_out:
            return None
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        return max(stats, key=lambda stat: self.defender_stats[stat])

    # RKS System: Silvally's type changes to match the Memory it's holding. Returns the Pokémon's types.
    def rks_system_ability_attacker(self, held_item):
        if "rks-system" not in self.attacker_abilities:
            return self.attacker.types
        return [MEMORY_TYPES.get(held_item, "normal")]
    def rks_system_ability_defender(self, held_item):
        if "rks-system" not in self.defender_abilities:
            return self.defender.types
        return [MEMORY_TYPES.get(held_item, "normal")]

    # Electric Surge: Sets Electric Terrain for 5 turns when the Pokémon enters battle. Returns the terrain.
    def electric_surge_ability_attacker(self):
        if "electric-surge" not in self.attacker_abilities or self.terrain == "electric-terrain":
            return self.terrain
        self.terrain = "electric-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["electric-terrain"]["turns"]
        return self.terrain
    def electric_surge_ability_defender(self):
        if "electric-surge" not in self.defender_abilities or self.terrain == "electric-terrain":
            return self.terrain
        self.terrain = "electric-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["electric-terrain"]["turns"]
        return self.terrain

    # Psychic Surge: Sets Psychic Terrain for 5 turns when the Pokémon enters battle. Returns the terrain.
    def psychic_surge_ability_attacker(self):
        if "psychic-surge" not in self.attacker_abilities or self.terrain == "psychic-terrain":
            return self.terrain
        self.terrain = "psychic-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["psychic-terrain"]["turns"]
        return self.terrain
    def psychic_surge_ability_defender(self):
        if "psychic-surge" not in self.defender_abilities or self.terrain == "psychic-terrain":
            return self.terrain
        self.terrain = "psychic-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["psychic-terrain"]["turns"]
        return self.terrain

    # Misty Surge: Sets Misty Terrain for 5 turns when the Pokémon enters battle. Returns the terrain.
    def misty_surge_ability_attacker(self):
        if "misty-surge" not in self.attacker_abilities or self.terrain == "misty-terrain":
            return self.terrain
        self.terrain = "misty-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["misty-terrain"]["turns"]
        return self.terrain
    def misty_surge_ability_defender(self):
        if "misty-surge" not in self.defender_abilities or self.terrain == "misty-terrain":
            return self.terrain
        self.terrain = "misty-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["misty-terrain"]["turns"]
        return self.terrain

    # Grassy Surge: Sets Grassy Terrain for 5 turns when the Pokémon enters battle. Returns the terrain.
    def grassy_surge_ability_attacker(self):
        if "grassy-surge" not in self.attacker_abilities or self.terrain == "grassy-terrain":
            return self.terrain
        self.terrain = "grassy-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["grassy-terrain"]["turns"]
        return self.terrain
    def grassy_surge_ability_defender(self):
        if "grassy-surge" not in self.defender_abilities or self.terrain == "grassy-terrain":
            return self.terrain
        self.terrain = "grassy-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["grassy-terrain"]["turns"]
        return self.terrain

    # Full Metal Body: Same as Clear Body, but Mold Breaker can't ignore it. Other Pokémon's moves and abilities can't lower this Pokémon's stats.
    # stage_change = how many stages the stat is changing. Returns the stage change that actually happens.
    def full_metal_body_ability_attacker(self, stage_change, from_opponent=True):
        if "full-metal-body" not in self.attacker_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def full_metal_body_ability_defender(self, stage_change, from_opponent=True):
        if "full-metal-body" not in self.defender_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Shadow Shield: Same as Multiscale, but Mold Breaker can't ignore it. Halves the damage the Pokémon takes when its HP is full.
    def shadow_shield_ability_attacker(self, current_hp, max_hp):
        if "shadow-shield" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if current_hp >= max_hp:
            return self.move_power * 0.5
        return self.move_power
    def shadow_shield_ability_defender(self, current_hp, max_hp):
        if "shadow-shield" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if current_hp >= max_hp:
            return self.move_power * 0.5
        return self.move_power

    # Prism Armor: Same as Filter, but Mold Breaker can't ignore it. Reduces the damage taken from super-effective moves to 75%.
    def prism_armor_ability_attacker(self):
        if "prism-armor" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.type_effectiveness_attacker() > 1:
            return self.move_power * 0.75
        return self.move_power
    def prism_armor_ability_defender(self):
        if "prism-armor" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.type_effectiveness_defender() > 1:
            return self.move_power * 0.75
        return self.move_power

    # Neuroforce: The Pokémon's super-effective moves do 25% more damage.
    def neuroforce_ability_attacker(self):
        if "neuroforce" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.type_effectiveness_defender() > 1:
            return self.move_power * 1.25
        return self.move_power
    def neuroforce_ability_defender(self):
        if "neuroforce" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.type_effectiveness_attacker() > 1:
            return self.move_power * 1.25
        return self.move_power

    # Intrepid Sword: The first time the Pokémon enters battle, its Attack goes up 1 stage. Returns the Attack stage change.
    # already_used = True if it already went off this battle.
    def intrepid_sword_ability_attacker(self, already_used=False):
        if "intrepid-sword" not in self.attacker_abilities or already_used:
            return 0
        return 1
    def intrepid_sword_ability_defender(self, already_used=False):
        if "intrepid-sword" not in self.defender_abilities or already_used:
            return 0
        return 1

    # Dauntless Shield: The first time the Pokémon enters battle, its Defense goes up 1 stage. Returns the Defense stage change.
    # already_used = True if it already went off this battle.
    def dauntless_shield_ability_attacker(self, already_used=False):
        if "dauntless-shield" not in self.attacker_abilities or already_used:
            return 0
        return 1
    def dauntless_shield_ability_defender(self, already_used=False):
        if "dauntless-shield" not in self.defender_abilities or already_used:
            return 0
        return 1

    # Libero: Same as Protean. The Pokémon's type changes to the type of the move it's about to use. It only works once each time it enters battle. Returns its types.
    # already_used = True if Libero already changed its type since it came in.
    def libero_ability_attacker(self, already_used=False):
        if "libero" not in self.attacker_abilities or already_used:
            return self.attacker.types
        return [self.move_type]
    def libero_ability_defender(self, already_used=False):
        if "libero" not in self.defender_abilities or already_used:
            return self.defender.types
        return [self.move_type]

    # Ball Fetch: If the Pokémon isn't holding an item, it picks up the first Poké Ball that fails to catch a wild Pokémon.
    # This ability currently has no effect on the dmg calc and will be implemented at a later date.
    # def ball_fetch_ability_attacker(self):
    #     return "ball-fetch" in self.attacker_abilities
    # def ball_fetch_ability_defender(self):
    #     return "ball-fetch" in self.defender_abilities

    # Cotton Down: When the Pokémon is hit by a damaging move, every other Pokémon's Speed goes down 1 stage. Returns the attacker's Speed stage change.
    def cotton_down_ability_attacker(self):
        if "cotton-down" not in self.attacker_abilities or self.status_move():
            return 0
        if self.type_effectiveness_attacker() == 0:
            return 0
        return -1
    def cotton_down_ability_defender(self):
        if "cotton-down" not in self.defender_abilities or self.status_move():
            return 0
        if self.type_effectiveness_defender() == 0:
            return 0
        return -1

    # Propeller Tail: The Pokémon's moves can't be pulled to another target by moves and abilities like Follow Me and Storm Drain. Returns True if the move can't be redirected.
    def propeller_tail_ability_attacker(self):
        return "propeller-tail" in self.attacker_abilities
    def propeller_tail_ability_defender(self):
        return "propeller-tail" in self.defender_abilities

    # Mirror Armor: When another Pokémon tries to lower the Pokémon's stats, the drop bounces back to that Pokémon instead. Returns the stage change it takes and the stage change bounced back.
    def mirror_armor_ability_attacker(self, stage_change, from_opponent=True):
        if "mirror-armor" not in self.attacker_abilities or stage_change >= 0 or not from_opponent:
            return stage_change, 0
        return 0, stage_change
    def mirror_armor_ability_defender(self, stage_change, from_opponent=True):
        if "mirror-armor" not in self.defender_abilities or stage_change >= 0 or not from_opponent:
            return stage_change, 0
        return 0, stage_change

    # Gulp Missile: When Cramorant uses Surf or Dive, it catches prey. Above 1/2 HP it's Gulping, at 1/2 HP or less it's Gorging. Returns its form name.
    def gulp_missile_form_attacker(self, current_hp, max_hp):
        if "gulp-missile" not in self.attacker_abilities or not self.attacker.name.startswith("cramorant"):
            return self.attacker.name
        if self.move_name not in ("surf", "dive"):
            return self.attacker.name
        if current_hp <= max_hp / 2:
            return "cramorant-gorging"
        return "cramorant-gulping"
    def gulp_missile_form_defender(self, current_hp, max_hp):
        if "gulp-missile" not in self.defender_abilities or not self.defender.name.startswith("cramorant"):
            return self.defender.name
        if self.move_name not in ("surf", "dive"):
            return self.defender.name
        if current_hp <= max_hp / 2:
            return "cramorant-gorging"
        return "cramorant-gulping"

    # Gulp Missile: When Cramorant is hit while it has prey, it spits it at the attacker. The attacker loses 1/4 of its max HP. Gulping also lowers its Defense 1 stage and Gorging paralyzes it.
    # form = Cramorant's current form. Returns the HP the attacker loses, its Defense stage change and its status.
    def gulp_missile_ability_attacker(self, form):
        if "gulp-missile" not in self.attacker_abilities or form not in ("cramorant-gulping", "cramorant-gorging"):
            return 0, 0, self.status_defender
        if self.status_move() or self.type_effectiveness_attacker() == 0:
            return 0, 0, self.status_defender
        damage = 0 if "magic-guard" in self.defender_abilities else 0.25
        if form == "cramorant-gulping":
            return damage, -1, self.status_defender
        if self.status_effects_defender() or self.status_immune_defender("paralysis"):
            return damage, 0, self.status_defender
        return damage, 0, "paralysis"
    def gulp_missile_ability_defender(self, form):
        if "gulp-missile" not in self.defender_abilities or form not in ("cramorant-gulping", "cramorant-gorging"):
            return 0, 0, self.status_attacker
        if self.status_move() or self.type_effectiveness_defender() == 0:
            return 0, 0, self.status_attacker
        damage = 0 if "magic-guard" in self.attacker_abilities else 0.25
        if form == "cramorant-gulping":
            return damage, -1, self.status_attacker
        if self.status_effects_attacker() or self.status_immune_attacker("paralysis"):
            return damage, 0, self.status_attacker
        return damage, 0, "paralysis"

    # Stalwart: Same as Propeller Tail. The Pokémon's moves can't be pulled to another target. Returns True if the move can't be redirected.
    def stalwart_ability_attacker(self):
        return "stalwart" in self.attacker_abilities
    def stalwart_ability_defender(self):
        return "stalwart" in self.defender_abilities

    # Steam Engine: When the Pokémon is hit by a Fire or Water-type move, its Speed goes up 6 stages. Returns the Speed stage change.
    def steam_engine_ability_attacker(self):
        if "steam-engine" not in self.attacker_abilities or self.move_type not in ("fire", "water") or self.status_move():
            return 0
        return 6
    def steam_engine_ability_defender(self):
        if "steam-engine" not in self.defender_abilities or self.move_type not in ("fire", "water") or self.status_move():
            return 0
        return 6

    # Punk Rock: Sound moves do half damage to the Pokémon.
    def punk_rock_ability_attacker(self):
        if "punk-rock" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.sound_move():
            return self.move_power * 0.5
        return self.move_power
    def punk_rock_ability_defender(self):
        if "punk-rock" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.sound_move():
            return self.move_power * 0.5
        return self.move_power

    # Punk Rock: Boosts the power of the Pokémon's sound moves by 30%.
    def punk_rock_power_attacker(self):
        if "punk-rock" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.sound_move():
            return self.move_power * 1.3
        return self.move_power
    def punk_rock_power_defender(self):
        if "punk-rock" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.sound_move():
            return self.move_power * 1.3
        return self.move_power

    # Sand Spit: When the Pokémon is hit by a damaging move, it summons a sandstorm for 5 turns. Returns the weather.
    def sand_spit_ability_attacker(self):
        if "sand-spit" not in self.attacker_abilities or self.status_move() or self.type_effectiveness_attacker() == 0:
            return self.weather
        if self.weather == "sandstorm" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "sandstorm"
        self.weather_turns = WEATHER_EFFECTS["sandstorm"]["turns"]
        return self.weather
    def sand_spit_ability_defender(self):
        if "sand-spit" not in self.defender_abilities or self.status_move() or self.type_effectiveness_defender() == 0:
            return self.weather
        if self.weather == "sandstorm" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "sandstorm"
        self.weather_turns = WEATHER_EFFECTS["sandstorm"]["turns"]
        return self.weather

    # Ice Scales: Special moves do half damage to the Pokémon.
    def ice_scales_ability_attacker(self):
        if "ice-scales" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_data.damage_class == "special":
            return self.move_power * 0.5
        return self.move_power
    def ice_scales_ability_defender(self):
        if "ice-scales" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_data.damage_class == "special":
            return self.move_power * 0.5
        return self.move_power

    # Ripen: Doubles the effect of Berries the Pokémon eats. berry_effect = how much the Berry heals or how many stages it raises. Returns the effect after Ripen.
    def ripen_ability_attacker(self, berry_effect):
        if "ripen" not in self.attacker_abilities:
            return berry_effect
        return berry_effect * 2
    def ripen_ability_defender(self, berry_effect):
        if "ripen" not in self.defender_abilities:
            return berry_effect
        return berry_effect * 2
        # Resist Berries check for Ripen in resist_berry_item.

    # Ice Face: The first physical hit Eiscue takes does no damage and breaks its ice face. Returns the move's power.
    # busted = True if the ice face is already broken.
    def ice_face_ability_attacker(self, busted=False):
        if "ice-face" not in self.attacker_abilities or not self.attacker.name.startswith("eiscue") or busted:
            return self.move_power
        if self.move_data.damage_class != "physical" or self.type_effectiveness_attacker() == 0:
            return self.move_power
        return 0
    def ice_face_ability_defender(self, busted=False):
        if "ice-face" not in self.defender_abilities or not self.defender.name.startswith("eiscue") or busted:
            return self.move_power
        if self.move_data.damage_class != "physical" or self.type_effectiveness_defender() == 0:
            return self.move_power
        return 0

    # Ice Face: With its ice face broken, Eiscue is in Noice Face until snow brings it back. Returns its form name, types and stats.
    def ice_face_form_attacker(self, busted=False):
        if "ice-face" not in self.attacker_abilities or not self.attacker.name.startswith("eiscue") or not busted:
            return self.attacker.name, self.attacker.types, self.attacker.stats
        if self.current_weather() in ("snow", "hail"):
            return self.attacker.name, self.attacker.types, self.attacker.stats
        form = BATTLE_FORMS["eiscue-noice"]
        return "eiscue-noice", form["types"], form["stats"]
    def ice_face_form_defender(self, busted=False):
        if "ice-face" not in self.defender_abilities or not self.defender.name.startswith("eiscue") or not busted:
            return self.defender.name, self.defender.types, self.defender.stats
        if self.current_weather() in ("snow", "hail"):
            return self.defender.name, self.defender.types, self.defender.stats
        form = BATTLE_FORMS["eiscue-noice"]
        return "eiscue-noice", form["types"], form["stats"]

    # Power Spot: Boosts the power of its allies' moves by 30%. ally_abilities = the abilities of the attacker's ally.
    def power_spot_ability_attacker(self, ally_abilities=None):
        if not ally_abilities or "power-spot" not in ally_abilities or not self.move_power:
            return self.move_power
        return self.move_power * 1.3
    def power_spot_ability_defender(self, ally_abilities=None):
        if not ally_abilities or "power-spot" not in ally_abilities or not self.move_power:
            return self.move_power
        return self.move_power * 1.3

    # Mimicry: The Pokémon's type changes to match the terrain. Returns its types.
    def mimicry_ability_attacker(self):
        if "mimicry" not in self.attacker_abilities or self.terrain not in MIMICRY_TYPES:
            return self.attacker.types
        return [MIMICRY_TYPES[self.terrain]]
    def mimicry_ability_defender(self):
        if "mimicry" not in self.defender_abilities or self.terrain not in MIMICRY_TYPES:
            return self.defender.types
        return [MIMICRY_TYPES[self.terrain]]

    # Screen Cleaner: When the Pokémon enters battle, it removes Reflect, Light Screen and Aurora Veil from both sides. Returns True if a screen is still up.
    def screen_cleaner_ability_attacker(self, screen_active=False):
        if "screen-cleaner" not in self.attacker_abilities:
            return screen_active
        return False
    def screen_cleaner_ability_defender(self, screen_active=False):
        if "screen-cleaner" not in self.defender_abilities:
            return screen_active
        return False

    # Steely Spirit: Boosts the power of Steel-type moves used by the Pokémon and its allies by 50%. ally_abilities = the abilities of the attacker's ally.
    def steely_spirit_ability_attacker(self, ally_abilities=None):
        if not self.move_power or self.move_type != "steel":
            return self.move_power
        power = self.move_power
        if "steely-spirit" in self.attacker_abilities:
            power *= 1.5
        if ally_abilities and "steely-spirit" in ally_abilities:
            power *= 1.5
        return power
    def steely_spirit_ability_defender(self, ally_abilities=None):
        if not self.move_power or self.move_type != "steel":
            return self.move_power
        power = self.move_power
        if "steely-spirit" in self.defender_abilities:
            power *= 1.5
        if ally_abilities and "steely-spirit" in ally_abilities:
            power *= 1.5
        return power

    # Perish Body: When the Pokémon is hit by a contact move, it and the attacker will both faint in 3 turns, like Perish Song. Returns True if Perish Body goes off.
    # already_perishing = True if the attacker already has a Perish Song count.
    def perish_body_ability_attacker(self, already_perishing=False):
        if "perish-body" not in self.attacker_abilities or not self.contact_move() or already_perishing:
            return False
        return True
    def perish_body_ability_defender(self, already_perishing=False):
        if "perish-body" not in self.defender_abilities or not self.contact_move() or already_perishing:
            return False
        return True

    # Wandering Spirit: When the Pokémon is hit by a contact move, it swaps abilities with the attacker. Returns its abilities and the attacker's abilities after.
    def wandering_spirit_ability_attacker(self):
        if "wandering-spirit" not in self.attacker_abilities or not self.contact_move() or self.type_effectiveness_attacker() == 0 or self.ability_shield_item_defender():
            return self.attacker_abilities, self.defender_abilities
        for ability in self.defender_abilities:
            if ability in SKILL_SWAP_BANNED_ABILITIES:
                return self.attacker_abilities, self.defender_abilities
        return self.defender_abilities, self.attacker_abilities
    def wandering_spirit_ability_defender(self):
        if "wandering-spirit" not in self.defender_abilities or not self.contact_move() or self.type_effectiveness_defender() == 0 or self.ability_shield_item_attacker():
            return self.defender_abilities, self.attacker_abilities
        for ability in self.attacker_abilities:
            if ability in SKILL_SWAP_BANNED_ABILITIES:
                return self.defender_abilities, self.attacker_abilities
        return self.attacker_abilities, self.defender_abilities

    # Gorilla Tactics: Boosts the Pokémon's Attack by 50%, but it can only use the first move it picks.
    def gorilla_tactics_ability_attacker(self):
        if "gorilla-tactics" not in self.attacker_abilities:
            return self.attacker_stats["attack"]
        return self.attacker_stats["attack"] * 1.5
    def gorilla_tactics_ability_defender(self):
        if "gorilla-tactics" not in self.defender_abilities:
            return self.defender_stats["attack"]
        return self.defender_stats["attack"] * 1.5
        # The move lock is in choice_lock_item.

    # Neutralizing Gas: While the Pokémon is out, the other Pokémon's abilities don't work. Returns the other Pokémon's abilities that still work.
    def neutralizing_gas_ability_attacker(self):
        if "neutralizing-gas" not in self.attacker_abilities or self.ability_shield_item_defender():
            return self.defender_abilities
        return [ability for ability in self.defender_abilities if ability in CANT_SUPPRESS_ABILITIES or ability == "neutralizing-gas"]
    def neutralizing_gas_ability_defender(self):
        if "neutralizing-gas" not in self.defender_abilities or self.ability_shield_item_attacker():
            return self.attacker_abilities
        return [ability for ability in self.attacker_abilities if ability in CANT_SUPPRESS_ABILITIES or ability == "neutralizing-gas"]

    # Pastel Veil: The Pokémon and its allies can't be poisoned. Returns the status that actually sticks.
    def pastel_veil_ability_attacker(self):
        if "pastel-veil" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker in ("poison", "badly-poison"):
            return None
        return self.status_attacker
    def pastel_veil_ability_defender(self):
        if "pastel-veil" not in self.defender_abilities:
            return self.status_defender
        if self.status_defender in ("poison", "badly-poison"):
            return None
        return self.status_defender
        # Will add the ally part later for doubles.

    # Hunger Switch: At the end of each turn, Morpeko switches between Full Belly Mode and Hangry Mode. Returns its form after the turn.
    # hangry = True if it's in Hangry Mode right now.
    def hunger_switch_ability_attacker(self, hangry=False):
        if "hunger-switch" not in self.attacker_abilities or not self.attacker.name.startswith("morpeko"):
            return self.attacker.name
        if hangry:
            return "morpeko-full-belly"
        return "morpeko-hangry"
    def hunger_switch_ability_defender(self, hangry=False):
        if "hunger-switch" not in self.defender_abilities or not self.defender.name.startswith("morpeko"):
            return self.defender.name
        if hangry:
            return "morpeko-full-belly"
        return "morpeko-hangry"

    # Hunger Switch: Aura Wheel is Electric type in Full Belly Mode and Dark type in Hangry Mode. Returns the move's type.
    def hunger_switch_move_type_attacker(self, hangry=False):
        if self.move_name != "aura-wheel" or not self.attacker.name.startswith("morpeko"):
            return self.move_type
        if hangry:
            return "dark"
        return "electric"
    def hunger_switch_move_type_defender(self, hangry=False):
        if self.move_name != "aura-wheel" or not self.defender.name.startswith("morpeko"):
            return self.move_type
        if hangry:
            return "dark"
        return "electric"

    # Quick Draw: The Pokémon's damaging moves have a 30% chance to go first among moves with the same priority. Returns the move's priority.
    def quick_draw_ability_attacker(self):
        if "quick-draw" not in self.attacker_abilities or self.status_move():
            return self.move_data.priority
        if random.random() < 0.30:
            return self.move_data.priority + 0.1
        return self.move_data.priority
    def quick_draw_ability_defender(self):
        if "quick-draw" not in self.defender_abilities or self.status_move():
            return self.move_data.priority
        if random.random() < 0.30:
            return self.move_data.priority + 0.1
        return self.move_data.priority

    # Unseen Fist: The Pokémon's contact moves hit through Protect and moves like it. Returns True if the move goes through Protect.
    def unseen_fist_ability_attacker(self):
        if "unseen-fist" not in self.attacker_abilities:
            return False
        return self.contact_move()
    def unseen_fist_ability_defender(self):
        if "unseen-fist" not in self.defender_abilities:
            return False
        return self.contact_move()

    # Curious Medicine: When the Pokémon enters battle, its allies' stat changes are reset. Returns the ally's stat stages after.
    # ally_stat_stages = the ally's current stat stages.
    def curious_medicine_ability_attacker(self, ally_stat_stages=None):
        if "curious-medicine" not in self.attacker_abilities:
            return ally_stat_stages
        return {}
    def curious_medicine_ability_defender(self, ally_stat_stages=None):
        if "curious-medicine" not in self.defender_abilities:
            return ally_stat_stages
        return {}

    # Transistor: Boosts the power of the Pokémon's Electric-type moves by 30%.
    def transistor_ability_attacker(self):
        if "transistor" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "electric":
            return self.move_power * 1.3
        return self.move_power
    def transistor_ability_defender(self):
        if "transistor" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "electric":
            return self.move_power * 1.3
        return self.move_power

    # Dragon's Maw: Boosts the power of the Pokémon's Dragon-type moves by 50%.
    def dragons_maw_ability_attacker(self):
        if "dragons-maw" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "dragon":
            return self.move_power * 1.5
        return self.move_power
    def dragons_maw_ability_defender(self):
        if "dragons-maw" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "dragon":
            return self.move_power * 1.5
        return self.move_power

    # Chilling Neigh: When the Pokémon knocks out another Pokémon with a move, its Attack goes up 1 stage. Returns the Attack stage change.
    def chilling_neigh_ability_attacker(self, knocked_out):
        if "chilling-neigh" not in self.attacker_abilities or not knocked_out:
            return 0
        return 1
    def chilling_neigh_ability_defender(self, knocked_out):
        if "chilling-neigh" not in self.defender_abilities or not knocked_out:
            return 0
        return 1

    # Grim Neigh: When the Pokémon knocks out another Pokémon with a move, its Sp. Atk goes up 1 stage. Returns the Sp. Atk stage change.
    def grim_neigh_ability_attacker(self, knocked_out):
        if "grim-neigh" not in self.attacker_abilities or not knocked_out:
            return 0
        return 1
    def grim_neigh_ability_defender(self, knocked_out):
        if "grim-neigh" not in self.defender_abilities or not knocked_out:
            return 0
        return 1

    # As One (Glastrier): Unnerve and Chilling Neigh together. When the Pokémon knocks out another Pokémon with a move, its Attack goes up 1 stage. Returns the Attack stage change.
    def as_one_glastrier_ability_attacker(self, knocked_out):
        if "as-one-glastrier" not in self.attacker_abilities or not knocked_out:
            return 0
        return 1
    def as_one_glastrier_ability_defender(self, knocked_out):
        if "as-one-glastrier" not in self.defender_abilities or not knocked_out:
            return 0
        return 1

    # As One (Glastrier): The opposing Pokémon can't eat Berries. Returns the opposing Pokémon's item that still works.
    def as_one_glastrier_unnerve_attacker(self, opponent_item):
        if "as-one-glastrier" not in self.attacker_abilities or not opponent_item or not opponent_item.endswith("-berry"):
            return opponent_item
        return None
    def as_one_glastrier_unnerve_defender(self, opponent_item):
        if "as-one-glastrier" not in self.defender_abilities or not opponent_item or not opponent_item.endswith("-berry"):
            return opponent_item
        return None

    # As One (Spectrier): Unnerve and Grim Neigh together. When the Pokémon knocks out another Pokémon with a move, its Sp. Atk goes up 1 stage. Returns the Sp. Atk stage change.
    def as_one_spectrier_ability_attacker(self, knocked_out):
        if "as-one-spectrier" not in self.attacker_abilities or not knocked_out:
            return 0
        return 1
    def as_one_spectrier_ability_defender(self, knocked_out):
        if "as-one-spectrier" not in self.defender_abilities or not knocked_out:
            return 0
        return 1

    # As One (Spectrier): The opposing Pokémon can't eat Berries. Returns the opposing Pokémon's item that still works.
    def as_one_spectrier_unnerve_attacker(self, opponent_item):
        if "as-one-spectrier" not in self.attacker_abilities or not opponent_item or not opponent_item.endswith("-berry"):
            return opponent_item
        return None
    def as_one_spectrier_unnerve_defender(self, opponent_item):
        if "as-one-spectrier" not in self.defender_abilities or not opponent_item or not opponent_item.endswith("-berry"):
            return opponent_item
        return None

    # Lingering Aroma: Same as Mummy. When the Pokémon is hit by a contact move, the attacker's ability becomes Lingering Aroma. Returns the attacker's abilities after.
    def lingering_aroma_ability_attacker(self):
        if "lingering-aroma" not in self.attacker_abilities or not self.contact_move() or self.ability_shield_item_defender():
            return self.defender_abilities
        for ability in self.defender_abilities:
            if ability in CANT_SUPPRESS_ABILITIES or ability == "lingering-aroma":
                return self.defender_abilities
        return ["lingering-aroma"]
    def lingering_aroma_ability_defender(self):
        if "lingering-aroma" not in self.defender_abilities or not self.contact_move() or self.ability_shield_item_attacker():
            return self.attacker_abilities
        for ability in self.attacker_abilities:
            if ability in CANT_SUPPRESS_ABILITIES or ability == "lingering-aroma":
                return self.attacker_abilities
        return ["lingering-aroma"]

    # Seed Sower: When the Pokémon is hit by a damaging move, it sets Grassy Terrain for 5 turns. Returns the terrain.
    def seed_sower_ability_attacker(self):
        if "seed-sower" not in self.attacker_abilities or self.status_move() or self.type_effectiveness_attacker() == 0:
            return self.terrain
        if self.terrain == "grassy-terrain":
            return self.terrain
        self.terrain = "grassy-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["grassy-terrain"]["turns"]
        return self.terrain
    def seed_sower_ability_defender(self):
        if "seed-sower" not in self.defender_abilities or self.status_move() or self.type_effectiveness_defender() == 0:
            return self.terrain
        if self.terrain == "grassy-terrain":
            return self.terrain
        self.terrain = "grassy-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["grassy-terrain"]["turns"]
        return self.terrain

    # Thermal Exchange: When the Pokémon is hit by a Fire-type move, its Attack goes up 1 stage. Returns the Attack stage change.
    def thermal_exchange_ability_attacker(self):
        if "thermal-exchange" not in self.attacker_abilities or self.move_type != "fire" or self.status_move():
            return 0
        return 1
    def thermal_exchange_ability_defender(self):
        if "thermal-exchange" not in self.defender_abilities or self.move_type != "fire" or self.status_move():
            return 0
        return 1

    # Thermal Exchange: The Pokémon can't be burned. Returns the status that actually sticks.
    def thermal_exchange_status_attacker(self):
        if "thermal-exchange" not in self.attacker_abilities:
            return self.status_attacker
        if self.status_attacker == STATUS_IMMUNITY_ABILITIES["thermal-exchange"]:
            return None
        return self.status_attacker
    def thermal_exchange_status_defender(self):
        if "thermal-exchange" not in self.defender_abilities:
            return self.status_defender
        if self.status_defender == STATUS_IMMUNITY_ABILITIES["thermal-exchange"]:
            return None
        return self.status_defender

    # Anger Shell: When a hit drops the Pokémon's HP to 1/2 or less, its Attack, Sp. Atk and Speed go up 1 stage, but its Defense and Sp. Def go down 1 stage. Returns the stage changes.
    # damage = the dmg from the hit. current_hp = its HP before the hit.
    def anger_shell_ability_attacker(self, damage, current_hp, max_hp):
        if "anger-shell" not in self.attacker_abilities:
            return {}
        hp_after = current_hp - damage
        if 0 < hp_after <= max_hp / 2 and current_hp > max_hp / 2:
            return {"attack": 1, "special-attack": 1, "speed": 1, "defense": -1, "special-defense": -1}
        return {}
    def anger_shell_ability_defender(self, damage, current_hp, max_hp):
        if "anger-shell" not in self.defender_abilities:
            return {}
        hp_after = current_hp - damage
        if 0 < hp_after <= max_hp / 2 and current_hp > max_hp / 2:
            return {"attack": 1, "special-attack": 1, "speed": 1, "defense": -1, "special-defense": -1}
        return {}

    # Purifying Salt: Ghost-type moves do half damage to the Pokémon.
    # Purifying Salt's status immunity is in STATUS_IMMUNITY_ABILITIES.
    def purifying_salt_ability_attacker(self):
        if "purifying-salt" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "ghost":
            return self.move_power * 0.5
        return self.move_power
    def purifying_salt_ability_defender(self):
        if "purifying-salt" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "ghost":
            return self.move_power * 0.5
        return self.move_power

    # Well-Baked Body: Fire moves don't affect the Pokémon. Instead they raise its Defense by 2 stages.
    def well_baked_body_ability_attacker(self):
        if "well-baked-body" not in self.attacker_abilities or self.move_type != "fire":
            return self.move_power, 0
        return 0, 2
    def well_baked_body_ability_defender(self):
        if "well-baked-body" not in self.defender_abilities or self.move_type != "fire":
            return self.move_power, 0
        return 0, 2

    # Wind Rider: Wind moves don't affect the Pokémon. Instead they raise its Attack by 1 stage.
    def wind_rider_ability_attacker(self):
        if "wind-rider" not in self.attacker_abilities or not self.wind_move():
            return self.move_power, 0
        return 0, 1
    def wind_rider_ability_defender(self):
        if "wind-rider" not in self.defender_abilities or not self.wind_move():
            return self.move_power, 0
        return 0, 1
        # Will add the Attack boost from Tailwind later once Tailwind is in.

    # Guard Dog: The Pokémon can't be forced out by Roar, Whirlwind, Dragon Tail or Circle Throw. Returns True if the move forces this Pokémon out.
    # Guard Dog's Intimidate boost is in intimidate_ability.
    def guard_dog_ability_attacker(self):
        if not self.force_switch_move():
            return False
        return "guard-dog" not in self.attacker_abilities
    def guard_dog_ability_defender(self):
        if not self.force_switch_move():
            return False
        return "guard-dog" not in self.defender_abilities

    # Rocky Payload: Boosts the power of the Pokémon's Rock-type moves by 50%.
    def rocky_payload_ability_attacker(self):
        if "rocky-payload" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "rock":
            return self.move_power * 1.5
        return self.move_power
    def rocky_payload_ability_defender(self):
        if "rocky-payload" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "rock":
            return self.move_power * 1.5
        return self.move_power

    # Wind Power: When the Pokémon is hit by a wind move, it becomes charged. Returns True if it becomes charged.
    def wind_power_ability_attacker(self):
        if "wind-power" not in self.attacker_abilities or not self.wind_move() or self.status_move():
            return False
        return True
    def wind_power_ability_defender(self):
        if "wind-power" not in self.defender_abilities or not self.wind_move() or self.status_move():
            return False
        return True
        # Will add getting charged from Tailwind later once Tailwind is in.

    # Charge: Once the Pokémon is charged (from Wind Power, Electromorphosis or the move Charge), its next Electric-type move does double damage.
    # charged = True if the Pokémon is charged.
    def charge_move_power_attacker(self, charged=False):
        if not charged or not self.move_power or self.move_type != "electric":
            return self.move_power
        return self.move_power * 2
    def charge_move_power_defender(self, charged=False):
        if not charged or not self.move_power or self.move_type != "electric":
            return self.move_power
        return self.move_power * 2

    # Zero to Hero: When Palafin switches out, it changes to Hero Form and stays that way for the rest of the battle. Returns its form name, types and stats.
    # switched_out_before = True if it already switched out once this battle.
    def zero_to_hero_ability_attacker(self, switched_out_before=False):
        if "zero-to-hero" not in self.attacker_abilities or not self.attacker.name.startswith("palafin") or not switched_out_before:
            return self.attacker.name, self.attacker.types, self.attacker.stats
        form = BATTLE_FORMS["palafin-hero"]
        return "palafin-hero", form["types"], form["stats"]
    def zero_to_hero_ability_defender(self, switched_out_before=False):
        if "zero-to-hero" not in self.defender_abilities or not self.defender.name.startswith("palafin") or not switched_out_before:
            return self.defender.name, self.defender.types, self.defender.stats
        form = BATTLE_FORMS["palafin-hero"]
        return "palafin-hero", form["types"], form["stats"]

    # Commander: In a double battle, Tatsugiri jumps into its ally Dondozo's mouth and Dondozo's stats all go up 2 stages. Returns Dondozo's stage changes.
    # ally_name = the name of the Pokémon's ally.
    def commander_ability_attacker(self, ally_name=None):
        if "commander" not in self.attacker_abilities or not self.attacker.name.startswith("tatsugiri"):
            return {}
        if not ally_name or not ally_name.startswith("dondozo"):
            return {}
        return {"attack": 2, "defense": 2, "special-attack": 2, "special-defense": 2, "speed": 2}
    def commander_ability_defender(self, ally_name=None):
        if "commander" not in self.defender_abilities or not self.defender.name.startswith("tatsugiri"):
            return {}
        if not ally_name or not ally_name.startswith("dondozo"):
            return {}
        return {"attack": 2, "defense": 2, "special-attack": 2, "special-defense": 2, "speed": 2}

    # Electromorphosis: When the Pokémon is hit by a damaging move, it becomes charged. Returns True if it becomes charged.
    def electromorphosis_ability_attacker(self):
        if "electromorphosis" not in self.attacker_abilities or self.status_move():
            return False
        return self.type_effectiveness_attacker() > 0
    def electromorphosis_ability_defender(self):
        if "electromorphosis" not in self.defender_abilities or self.status_move():
            return False
        return self.type_effectiveness_defender() > 0

    # Protosynthesis: In harsh sunlight or with Booster Energy, the Pokémon's highest stat goes up 30% (50% if it's Speed). Returns the stat that goes up and how much.
    # booster_energy = True if it used Booster Energy.
    def protosynthesis_ability_attacker(self, booster_energy=False):
        if "protosynthesis" not in self.attacker_abilities:
            return None, 1
        if self.current_weather() != "sun" and not booster_energy:
            return None, 1
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        best_stat = max(stats, key=lambda stat: self.attacker_stats[stat])
        if best_stat == "speed":
            return best_stat, 1.5
        return best_stat, 1.3
    def protosynthesis_ability_defender(self, booster_energy=False):
        if "protosynthesis" not in self.defender_abilities:
            return None, 1
        if self.current_weather() != "sun" and not booster_energy:
            return None, 1
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        best_stat = max(stats, key=lambda stat: self.defender_stats[stat])
        if best_stat == "speed":
            return best_stat, 1.5
        return best_stat, 1.3

    # Quark Drive: In Electric Terrain or with Booster Energy, the Pokémon's highest stat goes up 30% (50% if it's Speed). Returns the stat that goes up and how much.
    # booster_energy = True if it used Booster Energy.
    def quark_drive_ability_attacker(self, booster_energy=False):
        if "quark-drive" not in self.attacker_abilities:
            return None, 1
        if self.terrain != "electric-terrain" and not booster_energy:
            return None, 1
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        best_stat = max(stats, key=lambda stat: self.attacker_stats[stat])
        if best_stat == "speed":
            return best_stat, 1.5
        return best_stat, 1.3
    def quark_drive_ability_defender(self, booster_energy=False):
        if "quark-drive" not in self.defender_abilities:
            return None, 1
        if self.terrain != "electric-terrain" and not booster_energy:
            return None, 1
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        best_stat = max(stats, key=lambda stat: self.defender_stats[stat])
        if best_stat == "speed":
            return best_stat, 1.5
        return best_stat, 1.3

    # Good as Gold: Status moves from other Pokémon don't affect the Pokémon. Returns True if the move is blocked.
    def good_as_gold_ability_attacker(self):
        if "good-as-gold" not in self.attacker_abilities:
            return False
        return self.move_name in TARGETED_STATUS_MOVES
    def good_as_gold_ability_defender(self):
        if "good-as-gold" not in self.defender_abilities:
            return False
        return self.move_name in TARGETED_STATUS_MOVES

    # Vessel of Ruin: Lowers the Sp. Atk of every other Pokémon by 25%. Returns the opposing Pokémon's Sp. Atk.
    def vessel_of_ruin_ability_attacker(self):
        if "vessel-of-ruin" not in self.attacker_abilities or "vessel-of-ruin" in self.defender_abilities:
            return self.defender_stats["special-attack"]
        return self.defender_stats["special-attack"] * 0.75
    def vessel_of_ruin_ability_defender(self):
        if "vessel-of-ruin" not in self.defender_abilities or "vessel-of-ruin" in self.attacker_abilities:
            return self.attacker_stats["special-attack"]
        return self.attacker_stats["special-attack"] * 0.75

    # Sword of Ruin: Lowers the Defense of every other Pokémon by 25%. Returns the opposing Pokémon's Defense.
    def sword_of_ruin_ability_attacker(self):
        if "sword-of-ruin" not in self.attacker_abilities or "sword-of-ruin" in self.defender_abilities:
            return self.defender_stats["defense"]
        return self.defender_stats["defense"] * 0.75
    def sword_of_ruin_ability_defender(self):
        if "sword-of-ruin" not in self.defender_abilities or "sword-of-ruin" in self.attacker_abilities:
            return self.attacker_stats["defense"]
        return self.attacker_stats["defense"] * 0.75

    # Tablets of Ruin: Lowers the Attack of every other Pokémon by 25%. Returns the opposing Pokémon's Attack.
    def tablets_of_ruin_ability_attacker(self):
        if "tablets-of-ruin" not in self.attacker_abilities or "tablets-of-ruin" in self.defender_abilities:
            return self.defender_stats["attack"]
        return self.defender_stats["attack"] * 0.75
    def tablets_of_ruin_ability_defender(self):
        if "tablets-of-ruin" not in self.defender_abilities or "tablets-of-ruin" in self.attacker_abilities:
            return self.attacker_stats["attack"]
        return self.attacker_stats["attack"] * 0.75

    # Beads of Ruin: Lowers the Sp. Def of every other Pokémon by 25%. Returns the opposing Pokémon's Sp. Def.
    def beads_of_ruin_ability_attacker(self):
        if "beads-of-ruin" not in self.attacker_abilities or "beads-of-ruin" in self.defender_abilities:
            return self.defender_stats["special-defense"]
        return self.defender_stats["special-defense"] * 0.75
    def beads_of_ruin_ability_defender(self):
        if "beads-of-ruin" not in self.defender_abilities or "beads-of-ruin" in self.attacker_abilities:
            return self.attacker_stats["special-defense"]
        return self.attacker_stats["special-defense"] * 0.75

    # Orichalcum Pulse: Summons harsh sunlight for 5 turns when the Pokémon enters battle. Returns the weather.
    def orichalcum_pulse_ability_attacker(self):
        if "orichalcum-pulse" not in self.attacker_abilities:
            return self.weather
        if self.weather == "sun" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "sun"
        self.weather_turns = WEATHER_EFFECTS["sun"]["turns"]
        return self.weather
    def orichalcum_pulse_ability_defender(self):
        if "orichalcum-pulse" not in self.defender_abilities:
            return self.weather
        if self.weather == "sun" or WEATHER_EFFECTS.get(self.weather, {}).get("primal"):
            return self.weather
        self.weather = "sun"
        self.weather_turns = WEATHER_EFFECTS["sun"]["turns"]
        return self.weather

    # Orichalcum Pulse: Boosts the Pokémon's Attack by 33% in harsh sunlight.
    def orichalcum_pulse_attack_attacker(self):
        if "orichalcum-pulse" not in self.attacker_abilities:
            return self.attacker_stats["attack"]
        if self.utility_umbrella_item_attacker() in ("sun", "extreme-sun"):
            return self.attacker_stats["attack"] * 4 / 3
        return self.attacker_stats["attack"]
    def orichalcum_pulse_attack_defender(self):
        if "orichalcum-pulse" not in self.defender_abilities:
            return self.defender_stats["attack"]
        if self.utility_umbrella_item_defender() in ("sun", "extreme-sun"):
            return self.defender_stats["attack"] * 4 / 3
        return self.defender_stats["attack"]

    # Hadron Engine: Sets Electric Terrain for 5 turns when the Pokémon enters battle. Returns the terrain.
    def hadron_engine_ability_attacker(self):
        if "hadron-engine" not in self.attacker_abilities or self.terrain == "electric-terrain":
            return self.terrain
        self.terrain = "electric-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["electric-terrain"]["turns"]
        return self.terrain
    def hadron_engine_ability_defender(self):
        if "hadron-engine" not in self.defender_abilities or self.terrain == "electric-terrain":
            return self.terrain
        self.terrain = "electric-terrain"
        self.terrain_turns = TERRAIN_EFFECTS["electric-terrain"]["turns"]
        return self.terrain

    # Hadron Engine: Boosts the Pokémon's Sp. Atk by 33% in Electric Terrain.
    def hadron_engine_special_attack_attacker(self):
        if "hadron-engine" not in self.attacker_abilities or self.terrain != "electric-terrain":
            return self.attacker_stats["special-attack"]
        return self.attacker_stats["special-attack"] * 4 / 3
    def hadron_engine_special_attack_defender(self):
        if "hadron-engine" not in self.defender_abilities or self.terrain != "electric-terrain":
            return self.defender_stats["special-attack"]
        return self.defender_stats["special-attack"] * 4 / 3

    # Opportunist: When an opposing Pokémon's stats go up, the Pokémon copies the boost. Returns the stage change it copies.
    # stage_change = how many stages the opposing Pokémon's stat changed.
    def opportunist_ability_attacker(self, stage_change):
        if "opportunist" not in self.attacker_abilities or stage_change <= 0:
            return 0
        return stage_change
    def opportunist_ability_defender(self, stage_change):
        if "opportunist" not in self.defender_abilities or stage_change <= 0:
            return 0
        return stage_change

    # Cud Chew: When the Pokémon eats a Berry, it eats it again at the end of the next turn. Returns the Berry it eats again.
    # berry_eaten_last_turn = the Berry it ate last turn.
    def cud_chew_ability_attacker(self, berry_eaten_last_turn=None):
        if "cud-chew" not in self.attacker_abilities or not berry_eaten_last_turn or not berry_eaten_last_turn.endswith("-berry"):
            return None
        return berry_eaten_last_turn
    def cud_chew_ability_defender(self, berry_eaten_last_turn=None):
        if "cud-chew" not in self.defender_abilities or not berry_eaten_last_turn or not berry_eaten_last_turn.endswith("-berry"):
            return None
        return berry_eaten_last_turn

    # Sharpness: Boosts the power of the Pokémon's slicing moves by 50%.
    def sharpness_ability_attacker(self):
        if "sharpness" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.cut_move():
            return self.move_power * 1.5
        return self.move_power
    def sharpness_ability_defender(self):
        if "sharpness" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.cut_move():
            return self.move_power * 1.5
        return self.move_power

    # Supreme Overlord: Boosts the power of the Pokémon's moves by 10% for each ally that fainted, up to 50%.
    # fainted_allies = how many Pokémon on its team have fainted.
    def supreme_overlord_ability_attacker(self, fainted_allies=0):
        if "supreme-overlord" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        return self.move_power * (1 + 0.1 * min(fainted_allies, 5))
    def supreme_overlord_ability_defender(self, fainted_allies=0):
        if "supreme-overlord" not in self.defender_abilities or not self.move_power:
            return self.move_power
        return self.move_power * (1 + 0.1 * min(fainted_allies, 5))

    # Costar: When the Pokémon enters battle, it copies its ally's stat changes. Returns its stat stages after.
    # ally_stat_stages = the ally's current stat stages.
    def costar_ability_attacker(self, ally_stat_stages=None):
        if "costar" not in self.attacker_abilities or not ally_stat_stages:
            return {}
        return dict(ally_stat_stages)
    def costar_ability_defender(self, ally_stat_stages=None):
        if "costar" not in self.defender_abilities or not ally_stat_stages:
            return {}
        return dict(ally_stat_stages)

    # Toxic Debris: When the Pokémon is hit by a physical move, it scatters Toxic Spikes on the attacker's side (up to 2 layers). Returns the layers after.
    # toxic_spikes_layers = how many layers are already on the attacker's side.
    def toxic_debris_ability_attacker(self, toxic_spikes_layers=0):
        if "toxic-debris" not in self.attacker_abilities or self.move_data.damage_class != "physical":
            return toxic_spikes_layers
        if self.type_effectiveness_attacker() == 0:
            return toxic_spikes_layers
        return min(toxic_spikes_layers + 1, 2)
    def toxic_debris_ability_defender(self, toxic_spikes_layers=0):
        if "toxic-debris" not in self.defender_abilities or self.move_data.damage_class != "physical":
            return toxic_spikes_layers
        if self.type_effectiveness_defender() == 0:
            return toxic_spikes_layers
        return min(toxic_spikes_layers + 1, 2)

    # Armor Tail: Same as Queenly Majesty. Opposing Pokémon can't use priority moves on the Pokémon. Returns True if the move is blocked.
    def armor_tail_ability_attacker(self, priority=None):
        if "armor-tail" not in self.attacker_abilities:
            return False
        if priority is None:
            priority = self.move_data.priority
        if priority <= 0:
            return False
        return not self.status_move() or self.move_name in TARGETED_STATUS_MOVES
    def armor_tail_ability_defender(self, priority=None):
        if "armor-tail" not in self.defender_abilities:
            return False
        if priority is None:
            priority = self.move_data.priority
        if priority <= 0:
            return False
        return not self.status_move() or self.move_name in TARGETED_STATUS_MOVES

    # Earth Eater: Ground moves don't affect the Pokémon. Instead they heal 1/4 of its max HP.
    def earth_eater_ability_attacker(self):
        if "earth-eater" not in self.attacker_abilities or self.move_type != "ground":
            return self.move_power, 0
        return 0, 0.25
    def earth_eater_ability_defender(self):
        if "earth-eater" not in self.defender_abilities or self.move_type != "ground":
            return self.move_power, 0
        return 0, 0.25

    # Mycelium Might: The Pokémon's status moves always go last among moves with the same priority. Returns the move's priority.
    def mycelium_might_ability_attacker(self):
        if "mycelium-might" not in self.attacker_abilities or not self.status_move():
            return self.move_data.priority
        return self.move_data.priority - 0.1
    def mycelium_might_ability_defender(self):
        if "mycelium-might" not in self.defender_abilities or not self.status_move():
            return self.move_data.priority
        return self.move_data.priority - 0.1

    # Mycelium Might: The Pokémon's status moves ignore the target's ability. Returns the target's abilities that still work.
    def mycelium_might_abilities_attacker(self):
        if "mycelium-might" not in self.attacker_abilities or not self.status_move() or self.ability_shield_item_defender():
            return self.defender_abilities
        return [ability for ability in self.defender_abilities if ability not in BREAKABLE_ABILITIES]
    def mycelium_might_abilities_defender(self):
        if "mycelium-might" not in self.defender_abilities or not self.status_move() or self.ability_shield_item_attacker():
            return self.attacker_abilities
        return [ability for ability in self.attacker_abilities if ability not in BREAKABLE_ABILITIES]

    # Mind's Eye: The Pokémon's Normal and Fighting moves can hit Ghost types. Returns the type effectiveness against the target.
    def minds_eye_ability_attacker(self):
        if "minds-eye" not in self.attacker_abilities or self.move_type not in ("normal", "fighting"):
            return self.type_effectiveness_defender()
        removes_flying_weaknesses = self.weather_effects().get("removes_flying_weaknesses", False)
        multiplier = 1
        for type_name, type_data in zip(self.defender.types, self.defender_types_data):
            if type_name == "ghost":
                continue
            if self.move_type in type_data["double_damage_from"]:
                if not (removes_flying_weaknesses and type_name == "flying"):
                    multiplier *= 2
            elif self.move_type in type_data["half_damage_from"]:
                multiplier *= 0.5
            elif self.move_type in type_data["no_damage_from"]:
                multiplier *= 0
        return multiplier
    def minds_eye_ability_defender(self):
        if "minds-eye" not in self.defender_abilities or self.move_type not in ("normal", "fighting"):
            return self.type_effectiveness_attacker()
        removes_flying_weaknesses = self.weather_effects().get("removes_flying_weaknesses", False)
        multiplier = 1
        for type_name, type_data in zip(self.attacker.types, self.attacker_types_data):
            if type_name == "ghost":
                continue
            if self.move_type in type_data["double_damage_from"]:
                if not (removes_flying_weaknesses and type_name == "flying"):
                    multiplier *= 2
            elif self.move_type in type_data["half_damage_from"]:
                multiplier *= 0.5
            elif self.move_type in type_data["no_damage_from"]:
                multiplier *= 0
        return multiplier

    # Mind's Eye: Same as Keen Eye. The Pokémon's moves ignore the target's evasion changes. Returns the move's accuracy. None means the move never misses.
    def minds_eye_accuracy_attacker(self, accuracy_stage=0, target_evasion_stage=0):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "minds-eye" in self.attacker_abilities:
            target_evasion_stage = 0
        stage = max(-6, min(6, accuracy_stage - target_evasion_stage))
        if stage >= 0:
            return accuracy * (3 + stage) / 3
        return accuracy * 3 / (3 - stage)
    def minds_eye_accuracy_defender(self, accuracy_stage=0, target_evasion_stage=0):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "minds-eye" in self.defender_abilities:
            target_evasion_stage = 0
        stage = max(-6, min(6, accuracy_stage - target_evasion_stage))
        if stage >= 0:
            return accuracy * (3 + stage) / 3
        return accuracy * 3 / (3 - stage)

    # Mind's Eye: Other Pokémon can't lower this Pokémon's accuracy. Returns the stage change that actually happens.
    def minds_eye_accuracy_drop_attacker(self, stage_change, from_opponent=True):
        if "minds-eye" not in self.attacker_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def minds_eye_accuracy_drop_defender(self, stage_change, from_opponent=True):
        if "minds-eye" not in self.defender_abilities:
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Supersweet Syrup: The first time the Pokémon enters battle, the opposing Pokémon's evasion goes down 1 stage. Returns the opposing Pokémon's evasion stage change.
    # already_used = True if it already went off this battle.
    def supersweet_syrup_ability_attacker(self, already_used=False):
        if "supersweet-syrup" not in self.attacker_abilities or already_used:
            return 0
        return -1
    def supersweet_syrup_ability_defender(self, already_used=False):
        if "supersweet-syrup" not in self.defender_abilities or already_used:
            return 0
        return -1

    # Hospitality: When the Pokémon enters battle, its ally heals 1/4 of its max HP. Returns how much the ally heals.
    # has_ally = True if the Pokémon has an ally next to it.
    def hospitality_ability_attacker(self, has_ally=False):
        if "hospitality" not in self.attacker_abilities or not has_ally:
            return 0
        return 0.25
    def hospitality_ability_defender(self, has_ally=False):
        if "hospitality" not in self.defender_abilities or not has_ally:
            return 0
        return 0.25

    # Toxic Chain: The Pokémon's damaging moves have a 30% chance of badly poisoning the target. Returns the status that actually sticks.
    def toxic_chain_ability_attacker(self):
        if "toxic-chain" not in self.attacker_abilities or self.status_move():
            return self.status_defender
        if "shield-dust" in self.defender_abilities or self.held_item_defender() == "covert-cloak" or self.type_effectiveness_defender() == 0:
            return self.status_defender
        if self.status_effects_defender() or self.status_immune_defender("badly-poison"):
            return self.status_defender
        if random.random() < 0.30:
            return "badly-poison"
        return self.status_defender
    def toxic_chain_ability_defender(self):
        if "toxic-chain" not in self.defender_abilities or self.status_move():
            return self.status_attacker
        if "shield-dust" in self.attacker_abilities or self.held_item_attacker() == "covert-cloak" or self.type_effectiveness_attacker() == 0:
            return self.status_attacker
        if self.status_effects_attacker() or self.status_immune_attacker("badly-poison"):
            return self.status_attacker
        if random.random() < 0.30:
            return "badly-poison"
        return self.status_attacker

    # Embody Aspect: When a Terastallized Ogerpon enters battle, one of its stats goes up 1 stage depending on its mask. Returns the stat that goes up.
    # held_item = Ogerpon's mask. terastallized = True if it's Terastallized.
    def embody_aspect_ability_attacker(self, held_item=None, terastallized=False):
        if "embody-aspect" not in self.attacker_abilities or not self.attacker.name.startswith("ogerpon") or not terastallized:
            return None
        return EMBODY_ASPECT_STATS.get(held_item, "speed")
    def embody_aspect_ability_defender(self, held_item=None, terastallized=False):
        if "embody-aspect" not in self.defender_abilities or not self.defender.name.startswith("ogerpon") or not terastallized:
            return None
        return EMBODY_ASPECT_STATS.get(held_item, "speed")

    # Tera Shift: When Terapagos enters battle, it changes to its Terastal Form. Returns its form name, types and stats.
    def tera_shift_ability_attacker(self):
        if "tera-shift" not in self.attacker_abilities or not self.attacker.name.startswith("terapagos"):
            return self.attacker.name, self.attacker.types, self.attacker.stats
        form = BATTLE_FORMS["terapagos-terastal"]
        return "terapagos-terastal", form["types"], form["stats"]
    def tera_shift_ability_defender(self):
        if "tera-shift" not in self.defender_abilities or not self.defender.name.startswith("terapagos"):
            return self.defender.name, self.defender.types, self.defender.stats
        form = BATTLE_FORMS["terapagos-terastal"]
        return "terapagos-terastal", form["types"], form["stats"]

    # Tera Shell: When the Pokémon's HP is full, every damaging move that hits it is not very effective. Returns the type effectiveness against it.
    # first_hit_resisted = True if Tera Shell already resisted the first hit of this multi-hit move. The rest of the hits are resisted too.
    def tera_shell_ability_attacker(self, current_hp, max_hp, first_hit_resisted=False):
        effectiveness = self.type_effectiveness_attacker()
        if "tera-shell" not in self.attacker_abilities or not self.attacker.name.startswith("terapagos"):
            return effectiveness
        if self.status_move() or self.move_name == "struggle":
            return effectiveness
        if first_hit_resisted:
            return 0.5
        if current_hp < max_hp:
            return effectiveness
        if effectiveness < 1:
            return effectiveness
        return 0.5
    def tera_shell_ability_defender(self, current_hp, max_hp, first_hit_resisted=False):
        effectiveness = self.type_effectiveness_defender()
        if "tera-shell" not in self.defender_abilities or not self.defender.name.startswith("terapagos"):
            return effectiveness
        if self.status_move() or self.move_name == "struggle":
            return effectiveness
        if first_hit_resisted:
            return 0.5
        if current_hp < max_hp:
            return effectiveness
        if effectiveness < 1:
            return effectiveness
        return 0.5

    # Teraform Zero: When Terapagos Terastallizes into its Stellar Form, it clears the weather and terrain. Returns the weather and terrain after.
    # terastallized = True if it just Terastallized.
    def teraform_zero_ability_attacker(self, terastallized=False):
        if "teraform-zero" not in self.attacker_abilities or not self.attacker.name.startswith("terapagos") or not terastallized:
            return self.weather, self.terrain
        self.weather = None
        self.weather_turns = 0
        self.terrain = None
        self.terrain_turns = 0
        return self.weather, self.terrain
    def teraform_zero_ability_defender(self, terastallized=False):
        if "teraform-zero" not in self.defender_abilities or not self.defender.name.startswith("terapagos") or not terastallized:
            return self.weather, self.terrain
        self.weather = None
        self.weather_turns = 0
        self.terrain = None
        self.terrain_turns = 0
        return self.weather, self.terrain

    # Poison Puppeteer: When Pecharunt poisons a target with a move, the target also becomes confused. Returns True if the target gets confused.
    # inflicted_status = the status Pecharunt's move just gave the target.
    def poison_puppeteer_ability_attacker(self, inflicted_status=None):
        if "poison-puppeteer" not in self.attacker_abilities or not self.attacker.name.startswith("pecharunt"):
            return False
        return inflicted_status in ("poison", "badly-poison")
    def poison_puppeteer_ability_defender(self, inflicted_status=None):
        if "poison-puppeteer" not in self.defender_abilities or not self.defender.name.startswith("pecharunt"):
            return False
        return inflicted_status in ("poison", "badly-poison")

    # Piercing Drill: The Pokémon's contact moves hit through Protect, but only do 1/4 of the damage. Returns the move's power.
    # protected = True if the target used Protect or a move like it.
    def piercing_drill_ability_attacker(self, protected=False):
        if not protected or not self.move_power:
            return self.move_power
        if "piercing-drill" in self.attacker_abilities and self.contact_move():
            return self.move_power * 0.25
        return 0
    def piercing_drill_ability_defender(self, protected=False):
        if not protected or not self.move_power:
            return self.move_power
        if "piercing-drill" in self.defender_abilities and self.contact_move():
            return self.move_power * 0.25
        return 0

    # Dragonize: The Pokémon's Normal-type moves become Dragon type and do 20% more damage. Returns the move's type and power.
    def dragonize_ability_attacker(self):
        if "dragonize" not in self.attacker_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "dragon", self.move_power
        return "dragon", self.move_power * 1.2
    def dragonize_ability_defender(self):
        if "dragonize" not in self.defender_abilities or self.move_type != "normal" or self.move_name in NORMALIZE_EXCEPTIONS:
            return self.move_type, self.move_power
        if not self.move_power:
            return "dragon", self.move_power
        return "dragon", self.move_power * 1.2

    # Mega Sol: The Pokémon's moves act like the weather is harsh sunlight. Returns the move's power after the weather.
    # Hydro Steam gets the sun boost like a Fire move instead of being weakened.
    def mega_sol_ability_attacker(self):
        if "mega-sol" not in self.attacker_abilities or not self.move_power:
            return self.weather_move_power()
        if self.move_type == "fire" or self.move_name == "hydro-steam":
            return self.move_power * WEATHER_EFFECTS["sun"]["boost_multiplier"]
        if self.move_type == "water":
            return self.move_power * WEATHER_EFFECTS["sun"]["weaken_multiplier"]
        return self.move_power
    def mega_sol_ability_defender(self):
        if "mega-sol" not in self.defender_abilities or not self.move_power:
            return self.weather_move_power()
        if self.move_type == "fire" or self.move_name == "hydro-steam":
            return self.move_power * WEATHER_EFFECTS["sun"]["boost_multiplier"]
        if self.move_type == "water":
            return self.move_power * WEATHER_EFFECTS["sun"]["weaken_multiplier"]
        return self.move_power
        # Will add sun-based moves like Solar Beam and Weather Ball later.

    # Spicy Spray: When the Pokémon is hit by a damaging move, the attacker gets burned. Returns the status that actually sticks.
    def spicy_spray_ability_attacker(self):
        if "spicy-spray" not in self.attacker_abilities or self.status_move() or self.type_effectiveness_attacker() == 0:
            return self.status_defender
        if self.status_effects_defender() or self.status_immune_defender("burn"):
            return self.status_defender
        return "burn"
    def spicy_spray_ability_defender(self):
        if "spicy-spray" not in self.defender_abilities or self.status_move() or self.type_effectiveness_defender() == 0:
            return self.status_attacker
        if self.status_effects_attacker() or self.status_immune_attacker("burn"):
            return self.status_attacker
        return "burn"

    # Eelevate: Same as Levitate. The Pokémon floats, so Ground-type moves don't affect it.
    # Eelevate also means the Pokémon isn't grounded (handled in grounded_attacker / grounded_defender).
    def eelevate_ability_attacker(self):
        if "eelevate" not in self.attacker_abilities or self.held_item_attacker() == "iron-ball":
            return self.move_power
        if self.move_type == "ground" and not self.status_move():
            return 0
        return self.move_power
    def eelevate_ability_defender(self):
        if "eelevate" not in self.defender_abilities or self.held_item_defender() == "iron-ball":
            return self.move_power
        if self.move_type == "ground" and not self.status_move():
            return 0
        return self.move_power

    # Eelevate: Same as Beast Boost. When the Pokémon knocks out another Pokémon with a move, its highest stat goes up 1 stage. Returns the stat that goes up.
    def eelevate_boost_attacker(self, knocked_out):
        if "eelevate" not in self.attacker_abilities or not knocked_out:
            return None
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        return max(stats, key=lambda stat: self.attacker_stats[stat])
    def eelevate_boost_defender(self, knocked_out):
        if "eelevate" not in self.defender_abilities or not knocked_out:
            return None
        stats = ["attack", "defense", "special-attack", "special-defense", "speed"]
        return max(stats, key=lambda stat: self.defender_stats[stat])

    # Fire Mane: Boosts the power of the Pokémon's Fire-type moves by 50%.
    def fire_mane_ability_attacker(self):
        if "fire-mane" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire":
            return self.move_power * 1.5
        return self.move_power
    def fire_mane_ability_defender(self):
        if "fire-mane" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.move_type == "fire":
            return self.move_power * 1.5
        return self.move_power

    # Aura Guard: Contact moves do half damage to the Pokémon. Moves from a Pokémon with Long Reach don't make contact, so they do full damage.
    def aura_guard_ability_attacker(self):
        if "aura-guard" not in self.attacker_abilities or not self.move_power:
            return self.move_power
        if self.contact_move() and "long-reach" not in self.defender_abilities:
            return self.move_power * 0.5
        return self.move_power
    def aura_guard_ability_defender(self):
        if "aura-guard" not in self.defender_abilities or not self.move_power:
            return self.move_power
        if self.contact_move() and "long-reach" not in self.attacker_abilities:
            return self.move_power * 0.5
        return self.move_power

    # -------- Items -------- 
    # Items can be held by a Pokémon to boost its stats, change its type, or give it immunity to certain moves. Some items are consumed after one use, while others last until the Pokémon switches out or faints.

    # The item each Pokémon is holding that still works. Klutz stops a Pokémon from using its item.
    def held_item_attacker(self):
        return self.klutz_ability_attacker(self.attacker_item)
    def held_item_defender(self):
        return self.klutz_ability_defender(self.defender_item)

    # The Berry each Pokémon can eat. Unnerve and As One on the other Pokémon stop it from eating Berries.
    def held_berry_attacker(self):
        berry = self.held_item_attacker()
        berry = self.unnerve_ability_defender(berry)
        berry = self.as_one_glastrier_unnerve_defender(berry)
        berry = self.as_one_spectrier_unnerve_defender(berry)
        return berry
    def held_berry_defender(self):
        berry = self.held_item_defender()
        berry = self.unnerve_ability_attacker(berry)
        berry = self.as_one_glastrier_unnerve_attacker(berry)
        berry = self.as_one_spectrier_unnerve_attacker(berry)
        return berry

    # Berry Juice: When the Pokémon's HP drops to 1/2 or less, it drinks the Berry Juice and heals 20 HP. Returns how much HP it heals.
    def berry_juice_item_attacker(self, current_hp, max_hp):
        if self.held_item_attacker() != "berry-juice" or current_hp > max_hp / 2 or current_hp <= 0:
            return 0
        return min(20, max_hp - current_hp)
    def berry_juice_item_defender(self, current_hp, max_hp):
        if self.held_item_defender() != "berry-juice" or current_hp > max_hp / 2 or current_hp <= 0:
            return 0
        return min(20, max_hp - current_hp)

    # Griseous Orb and Griseous Core: Boost the power of Giratina's Ghost and Dragon-type moves by 20%.
    def griseous_orb_item_attacker(self):
        if self.held_item_attacker() not in ("griseous-orb", "griseous-core") or self.attacker.pokedex_id != 487 or not self.move_power:
            return self.move_power
        if self.move_type in ("ghost", "dragon"):
            return self.move_power * 1.2
        return self.move_power
    def griseous_orb_item_defender(self):
        if self.held_item_defender() not in ("griseous-orb", "griseous-core") or self.defender.pokedex_id != 487 or not self.move_power:
            return self.move_power
        if self.move_type in ("ghost", "dragon"):
            return self.move_power * 1.2
        return self.move_power

    # Douse Drive: Genesect's Techno Blast becomes Water type. Returns the move's type.
    def douse_drive_item_attacker(self):
        if self.held_item_attacker() != "douse-drive" or self.attacker.pokedex_id != 649 or self.move_name != "techno-blast":
            return self.move_type
        return "water"
    def douse_drive_item_defender(self):
        if self.held_item_defender() != "douse-drive" or self.defender.pokedex_id != 649 or self.move_name != "techno-blast":
            return self.move_type
        return "water"

    # Shock Drive: Genesect's Techno Blast becomes Electric type. Returns the move's type.
    def shock_drive_item_attacker(self):
        if self.held_item_attacker() != "shock-drive" or self.attacker.pokedex_id != 649 or self.move_name != "techno-blast":
            return self.move_type
        return "electric"
    def shock_drive_item_defender(self):
        if self.held_item_defender() != "shock-drive" or self.defender.pokedex_id != 649 or self.move_name != "techno-blast":
            return self.move_type
        return "electric"

    # Burn Drive: Genesect's Techno Blast becomes Fire type. Returns the move's type.
    def burn_drive_item_attacker(self):
        if self.held_item_attacker() != "burn-drive" or self.attacker.pokedex_id != 649 or self.move_name != "techno-blast":
            return self.move_type
        return "fire"
    def burn_drive_item_defender(self):
        if self.held_item_defender() != "burn-drive" or self.defender.pokedex_id != 649 or self.move_name != "techno-blast":
            return self.move_type
        return "fire"

    # Chill Drive: Genesect's Techno Blast becomes Ice type. Returns the move's type.
    def chill_drive_item_attacker(self):
        if self.held_item_attacker() != "chill-drive" or self.attacker.pokedex_id != 649 or self.move_name != "techno-blast":
            return self.move_type
        return "ice"
    def chill_drive_item_defender(self):
        if self.held_item_defender() != "chill-drive" or self.defender.pokedex_id != 649 or self.move_name != "techno-blast":
            return self.move_type
        return "ice"

    # Adamant Orb and Adamant Crystal: Boost the power of Dialga's Steel and Dragon-type moves by 20%.
    def adamant_orb_item_attacker(self):
        if self.held_item_attacker() not in ("adamant-orb", "adamant-crystal") or self.attacker.pokedex_id != 483 or not self.move_power:
            return self.move_power
        if self.move_type in ("steel", "dragon"):
            return self.move_power * 1.2
        return self.move_power
    def adamant_orb_item_defender(self):
        if self.held_item_defender() not in ("adamant-orb", "adamant-crystal") or self.defender.pokedex_id != 483 or not self.move_power:
            return self.move_power
        if self.move_type in ("steel", "dragon"):
            return self.move_power * 1.2
        return self.move_power

    # Lustrous Orb and Lustrous Globe: Boost the power of Palkia's Water and Dragon-type moves by 20%.
    def lustrous_orb_item_attacker(self):
        if self.held_item_attacker() not in ("lustrous-orb", "lustrous-globe") or self.attacker.pokedex_id != 484 or not self.move_power:
            return self.move_power
        if self.move_type in ("water", "dragon"):
            return self.move_power * 1.2
        return self.move_power
    def lustrous_orb_item_defender(self):
        if self.held_item_defender() not in ("lustrous-orb", "lustrous-globe") or self.defender.pokedex_id != 484 or not self.move_power:
            return self.move_power
        if self.move_type in ("water", "dragon"):
            return self.move_power * 1.2
        return self.move_power

    # Cheri Berry: If the Pokémon is paralyzed, it eats the Berry and is cured. Returns the status after.
    def cheri_berry_item_attacker(self):
        if self.held_berry_attacker() != "cheri-berry" or self.status_attacker != "paralysis":
            return self.status_attacker
        return None
    def cheri_berry_item_defender(self):
        if self.held_berry_defender() != "cheri-berry" or self.status_defender != "paralysis":
            return self.status_defender
        return None

    # Chesto Berry: If the Pokémon falls asleep, it eats the Berry and wakes up. Returns the status after.
    def chesto_berry_item_attacker(self):
        if self.held_berry_attacker() != "chesto-berry" or self.status_attacker != "sleep":
            return self.status_attacker
        return None
    def chesto_berry_item_defender(self):
        if self.held_berry_defender() != "chesto-berry" or self.status_defender != "sleep":
            return self.status_defender
        return None

    # Pecha Berry: If the Pokémon is poisoned, it eats the Berry and is cured. Returns the status after.
    def pecha_berry_item_attacker(self):
        if self.held_berry_attacker() != "pecha-berry" or self.status_attacker not in ("poison", "badly-poison"):
            return self.status_attacker
        return None
    def pecha_berry_item_defender(self):
        if self.held_berry_defender() != "pecha-berry" or self.status_defender not in ("poison", "badly-poison"):
            return self.status_defender
        return None

    # Rawst Berry: If the Pokémon is burned, it eats the Berry and is cured. Returns the status after.
    def rawst_berry_item_attacker(self):
        if self.held_berry_attacker() != "rawst-berry" or self.status_attacker != "burn":
            return self.status_attacker
        return None
    def rawst_berry_item_defender(self):
        if self.held_berry_defender() != "rawst-berry" or self.status_defender != "burn":
            return self.status_defender
        return None

    # Aspear Berry: If the Pokémon is frozen, it eats the Berry and thaws out. Returns the status after.
    def aspear_berry_item_attacker(self):
        if self.held_berry_attacker() != "aspear-berry" or self.status_attacker != "freeze":
            return self.status_attacker
        return None
    def aspear_berry_item_defender(self):
        if self.held_berry_defender() != "aspear-berry" or self.status_defender != "freeze":
            return self.status_defender
        return None

    # Leppa Berry: When one of the Pokémon's moves runs out of PP, it eats the Berry and restores 10 PP to that move. Returns the move's PP after.
    # move_pp = the move's current PP.
    def leppa_berry_item_attacker(self, move_pp):
        if self.held_berry_attacker() != "leppa-berry" or move_pp > 0:
            return move_pp
        return min(move_pp + self.ripen_ability_attacker(10), self.move_data.pp)
    def leppa_berry_item_defender(self, move_pp):
        if self.held_berry_defender() != "leppa-berry" or move_pp > 0:
            return move_pp
        return min(move_pp + self.ripen_ability_defender(10), self.move_data.pp)

    # Oran Berry: When the Pokémon's HP drops to 1/2 or less, it eats the Berry and heals 10 HP. Returns how much HP it heals.
    def oran_berry_item_attacker(self, current_hp, max_hp):
        if self.held_berry_attacker() != "oran-berry" or current_hp > max_hp / 2 or current_hp <= 0:
            return 0
        return min(self.ripen_ability_attacker(10), max_hp - current_hp)
    def oran_berry_item_defender(self, current_hp, max_hp):
        if self.held_berry_defender() != "oran-berry" or current_hp > max_hp / 2 or current_hp <= 0:
            return 0
        return min(self.ripen_ability_defender(10), max_hp - current_hp)

    # Persim Berry: If the Pokémon is confused, it eats the Berry and snaps out of it. Returns True if it's still confused.
    # confused = True if the Pokémon is confused.
    def persim_berry_item_attacker(self, confused):
        if self.held_berry_attacker() != "persim-berry" or not confused:
            return confused
        return False
    def persim_berry_item_defender(self, confused):
        if self.held_berry_defender() != "persim-berry" or not confused:
            return confused
        return False

    # Lum Berry: If the Pokémon gets a status or becomes confused, it eats the Berry and is cured of both. Returns its status and whether it's still confused.
    def lum_berry_item_attacker(self, confused=False):
        if self.held_berry_attacker() != "lum-berry" or (not self.status_effects_attacker() and not confused):
            return self.status_attacker, confused
        return None, False
    def lum_berry_item_defender(self, confused=False):
        if self.held_berry_defender() != "lum-berry" or (not self.status_effects_defender() and not confused):
            return self.status_defender, confused
        return None, False

    # Sitrus Berry: When the Pokémon's HP drops to 1/2 or less, it eats the Berry and heals 1/4 of its max HP. Returns how much HP it heals.
    def sitrus_berry_item_attacker(self, current_hp, max_hp):
        if self.held_berry_attacker() != "sitrus-berry" or current_hp > max_hp / 2 or current_hp <= 0:
            return 0
        return min(self.ripen_ability_attacker(max_hp // 4), max_hp - current_hp)
    def sitrus_berry_item_defender(self, current_hp, max_hp):
        if self.held_berry_defender() != "sitrus-berry" or current_hp > max_hp / 2 or current_hp <= 0:
            return 0
        return min(self.ripen_ability_defender(max_hp // 4), max_hp - current_hp)

    # Figy, Wiki, Mago, Aguav and Iapapa Berry: When the Pokémon's HP drops to 1/4 or less, it eats the Berry and heals 1/3 of its max HP. If its nature lowers the Berry's stat, it also becomes confused. Returns how much HP it heals and whether it gets confused.
    # nature = the Pokémon's nature.
    def confusion_berry_item_attacker(self, current_hp, max_hp, nature=None):
        berry = self.held_berry_attacker()
        if berry not in CONFUSION_BERRIES or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_attacker(0.25):
            return 0, False
        heal = min(self.ripen_ability_attacker(max_hp // 3), max_hp - current_hp)
        return heal, NATURES.get(nature, (None, None))[1] == CONFUSION_BERRIES[berry]
    def confusion_berry_item_defender(self, current_hp, max_hp, nature=None):
        berry = self.held_berry_defender()
        if berry not in CONFUSION_BERRIES or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_defender(0.25):
            return 0, False
        heal = min(self.ripen_ability_defender(max_hp // 3), max_hp - current_hp)
        return heal, NATURES.get(nature, (None, None))[1] == CONFUSION_BERRIES[berry]

    # Resist Berries (Occa, Passho, Wacan, etc.): When the Pokémon is hit by a super-effective move of the Berry's type, it eats the Berry and takes half damage. Chilan Berry works on any Normal-type move. Returns the damage multiplier.
    def resist_berry_item_attacker(self):
        berry = self.held_berry_attacker()
        if berry not in RESIST_BERRIES or self.status_move() or self.move_type != RESIST_BERRIES[berry]:
            return 1
        if berry != "chilan-berry" and self.type_effectiveness_attacker() <= 1:
            return 1
        if "ripen" in self.attacker_abilities:
            return 0.25
        return 0.5
    def resist_berry_item_defender(self):
        berry = self.held_berry_defender()
        if berry not in RESIST_BERRIES or self.status_move() or self.move_type != RESIST_BERRIES[berry]:
            return 1
        if berry != "chilan-berry" and self.type_effectiveness_defender() <= 1:
            return 1
        if "ripen" in self.defender_abilities:
            return 0.25
        return 0.5

    # Liechi, Ganlon, Salac, Petaya and Apicot Berry: When the Pokémon's HP drops to 1/4 or less, it eats the Berry and one of its stats goes up 1 stage. Returns the stat that goes up and the stage change.
    def pinch_berry_item_attacker(self, current_hp, max_hp):
        berry = self.held_berry_attacker()
        if berry not in PINCH_BERRIES or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_attacker(0.25):
            return None, 0
        return PINCH_BERRIES[berry], self.ripen_ability_attacker(1)
    def pinch_berry_item_defender(self, current_hp, max_hp):
        berry = self.held_berry_defender()
        if berry not in PINCH_BERRIES or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_defender(0.25):
            return None, 0
        return PINCH_BERRIES[berry], self.ripen_ability_defender(1)

    # Lansat Berry: When the Pokémon's HP drops to 1/4 or less, it eats the Berry and its critical hit ratio goes up 2 stages. Returns how many crit stages it adds.
    def lansat_berry_item_attacker(self, current_hp, max_hp):
        if self.held_berry_attacker() != "lansat-berry" or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_attacker(0.25):
            return 0
        return 2
    def lansat_berry_item_defender(self, current_hp, max_hp):
        if self.held_berry_defender() != "lansat-berry" or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_defender(0.25):
            return 0
        return 2

    # Starf Berry: When the Pokémon's HP drops to 1/4 or less, it eats the Berry and a random stat goes up 2 stages. Returns the stat that goes up and the stage change.
    # stat_stages = the Pokémon's current stat stages. A stat already at +6 can't be picked.
    def starf_berry_item_attacker(self, current_hp, max_hp, stat_stages=None):
        if self.held_berry_attacker() != "starf-berry" or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_attacker(0.25):
            return None, 0
        stat_stages = stat_stages or {}
        stats = [stat for stat in ("attack", "defense", "special-attack", "special-defense", "speed") if stat_stages.get(stat, 0) < 6]
        if not stats:
            return None, 0
        return random.choice(stats), self.ripen_ability_attacker(2)
    def starf_berry_item_defender(self, current_hp, max_hp, stat_stages=None):
        if self.held_berry_defender() != "starf-berry" or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_defender(0.25):
            return None, 0
        stat_stages = stat_stages or {}
        stats = [stat for stat in ("attack", "defense", "special-attack", "special-defense", "speed") if stat_stages.get(stat, 0) < 6]
        if not stats:
            return None, 0
        return random.choice(stats), self.ripen_ability_defender(2)

    # Enigma Berry: When the Pokémon is hit by a super-effective move, it eats the Berry and heals 1/4 of its max HP. Returns how much HP it heals.
    # current_hp = its HP after the hit.
    def enigma_berry_item_attacker(self, current_hp, max_hp):
        if self.held_berry_attacker() != "enigma-berry" or self.status_move() or current_hp <= 0:
            return 0
        if self.type_effectiveness_attacker() <= 1:
            return 0
        return min(self.ripen_ability_attacker(max_hp // 4), max_hp - current_hp)
    def enigma_berry_item_defender(self, current_hp, max_hp):
        if self.held_berry_defender() != "enigma-berry" or self.status_move() or current_hp <= 0:
            return 0
        if self.type_effectiveness_defender() <= 1:
            return 0
        return min(self.ripen_ability_defender(max_hp // 4), max_hp - current_hp)

    # Micle Berry: When the Pokémon's HP drops to 1/4 or less, it eats the Berry and its next move is 20% more accurate. One-hit KO moves don't get the boost. Returns the move's accuracy. None means the move never misses.
    def micle_berry_item_attacker(self, current_hp, max_hp):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_berry_attacker() != "micle-berry" or self.ohko_move() or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_attacker(0.25):
            return accuracy
        return accuracy * 1.2
    def micle_berry_item_defender(self, current_hp, max_hp):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_berry_defender() != "micle-berry" or self.ohko_move() or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_defender(0.25):
            return accuracy
        return accuracy * 1.2

    # Custap Berry: When the Pokémon's HP is 1/4 or less, it eats the Berry and moves first among moves with the same priority. Returns the move's priority.
    def custap_berry_item_attacker(self, current_hp, max_hp):
        priority = self.move_data.priority
        if self.held_berry_attacker() != "custap-berry" or priority > 0 or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_attacker(0.25):
            return priority
        if self.status_move() and "mycelium-might" in self.attacker_abilities:
            return priority
        return priority + 0.1
    def custap_berry_item_defender(self, current_hp, max_hp):
        priority = self.move_data.priority
        if self.held_berry_defender() != "custap-berry" or priority > 0 or current_hp <= 0 or current_hp > max_hp * self.gluttony_ability_defender(0.25):
            return priority
        if self.status_move() and "mycelium-might" in self.defender_abilities:
            return priority
        return priority + 0.1

    # Jaboca Berry: When the Pokémon is hit by a physical move, it eats the Berry and the attacker loses 1/8 of its max HP. Returns the HP the attacker loses as a fraction of its max HP.
    def jaboca_berry_item_attacker(self):
        if self.held_berry_attacker() != "jaboca-berry" or self.move_data.damage_class != "physical" or self.type_effectiveness_attacker() == 0:
            return 0
        if "magic-guard" in self.defender_abilities:
            return 0
        if "ripen" in self.attacker_abilities:
            return 0.25
        return 0.125
    def jaboca_berry_item_defender(self):
        if self.held_berry_defender() != "jaboca-berry" or self.move_data.damage_class != "physical" or self.type_effectiveness_defender() == 0:
            return 0
        if "magic-guard" in self.attacker_abilities:
            return 0
        if "ripen" in self.defender_abilities:
            return 0.25
        return 0.125

    # Rowap Berry: When the Pokémon is hit by a special move, it eats the Berry and the attacker loses 1/8 of its max HP. Returns the HP the attacker loses as a fraction of its max HP.
    def rowap_berry_item_attacker(self):
        if self.held_berry_attacker() != "rowap-berry" or self.move_data.damage_class != "special" or self.type_effectiveness_attacker() == 0:
            return 0
        if "magic-guard" in self.defender_abilities:
            return 0
        if "ripen" in self.attacker_abilities:
            return 0.25
        return 0.125
    def rowap_berry_item_defender(self):
        if self.held_berry_defender() != "rowap-berry" or self.move_data.damage_class != "special" or self.type_effectiveness_defender() == 0:
            return 0
        if "magic-guard" in self.attacker_abilities:
            return 0
        if "ripen" in self.defender_abilities:
            return 0.25
        return 0.125

    # Bright Powder: Moves aimed at the Pokémon are 10% less accurate. Returns the move's accuracy. None means the move never misses.
    def bright_powder_item_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_item_attacker() != "bright-powder" or self.ohko_move():
            return accuracy
        return accuracy * 0.9
    def bright_powder_item_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_item_defender() != "bright-powder" or self.ohko_move():
            return accuracy
        return accuracy * 0.9

    # White Herb: If any of the Pokémon's stats are lowered, it uses the herb and they go back to normal. Returns its stat stages after.
    # stat_stages = the Pokémon's current stat stages.
    def white_herb_item_attacker(self, stat_stages):
        if self.held_item_attacker() != "white-herb" or not any(stage < 0 for stage in stat_stages.values()):
            return stat_stages
        return {stat: max(stage, 0) for stat, stage in stat_stages.items()}
    def white_herb_item_defender(self, stat_stages):
        if self.held_item_defender() != "white-herb" or not any(stage < 0 for stage in stat_stages.values()):
            return stat_stages
        return {stat: max(stage, 0) for stat, stage in stat_stages.items()}

    # Macho Brace: Halves the Pokémon's Speed. It still works with Klutz.
    def macho_brace_item_attacker(self):
        if self.held_item_attacker() != "macho-brace":
            return self.attacker_stats["speed"]
        return self.attacker_stats["speed"] * 0.5
    def macho_brace_item_defender(self):
        if self.held_item_defender() != "macho-brace":
            return self.defender_stats["speed"]
        return self.defender_stats["speed"] * 0.5

    # Quick Claw: The Pokémon has a 20% chance to move first among moves with the same priority. Returns the move's priority.
    def quick_claw_item_attacker(self):
        priority = self.move_data.priority
        if self.held_item_attacker() != "quick-claw" or priority > 0:
            return priority
        if self.status_move() and "mycelium-might" in self.attacker_abilities:
            return priority
        if random.random() < 0.2:
            return priority + 0.1
        return priority
    def quick_claw_item_defender(self):
        priority = self.move_data.priority
        if self.held_item_defender() != "quick-claw" or priority > 0:
            return priority
        if self.status_move() and "mycelium-might" in self.defender_abilities:
            return priority
        if random.random() < 0.2:
            return priority + 0.1
        return priority

    # Mental Herb: If the Pokémon gets infatuated, taunted, tormented, encored, disabled or heal blocked, it uses the herb and is cured. Returns True if the effect gets cured.
    # incoming_effect = the effect the Pokémon just got. Mental Herb cures the same effects Aroma Veil blocks.
    def mental_herb_item_attacker(self, incoming_effect):
        if self.held_item_attacker() != "mental-herb":
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["aroma-veil"]
    def mental_herb_item_defender(self, incoming_effect):
        if self.held_item_defender() != "mental-herb":
            return False
        return incoming_effect in VOLATILE_IMMUNITY_ABILITIES["aroma-veil"]

    # Choice Band: Boosts the Pokémon's Attack by 50%, but it can only use the first move it picks.
    def choice_band_item_attacker(self):
        if self.held_item_attacker() != "choice-band":
            return self.attacker_stats["attack"]
        return self.attacker_stats["attack"] * 1.5
    def choice_band_item_defender(self):
        if self.held_item_defender() != "choice-band":
            return self.defender_stats["attack"]
        return self.defender_stats["attack"] * 1.5

    # Choice items and Gorilla Tactics lock the Pokémon into the first move it uses until it switches out. Returns True if it can use this move.
    # locked_move = the move it's locked into, or None if it hasn't used a move yet.
    def choice_lock_item_attacker(self, locked_move=None):
        if self.held_item_attacker() not in CHOICE_ITEMS and "gorilla-tactics" not in self.attacker_abilities:
            return True
        return locked_move is None or locked_move == self.move_name or self.move_name == "struggle"
    def choice_lock_item_defender(self, locked_move=None):
        if self.held_item_defender() not in CHOICE_ITEMS and "gorilla-tactics" not in self.defender_abilities:
            return True
        return locked_move is None or locked_move == self.move_name or self.move_name == "struggle"

    # King's Rock and Razor Fang: The Pokémon's damaging moves get a 10% chance to make the target flinch. Moves that can already flinch keep their own chance. Returns the flinch chance as a decimal.
    def kings_rock_item_attacker(self):
        move_flinch_chance = 0
        if self.move_data.meta is not None:
            move_flinch_chance = (self.move_data.meta.get("flinch_chance") or 0) / 100
        if self.held_item_attacker() not in ("kings-rock", "razor-fang") or self.status_move() or move_flinch_chance > 0:
            return move_flinch_chance
        return 0.10
    def kings_rock_item_defender(self):
        move_flinch_chance = 0
        if self.move_data.meta is not None:
            move_flinch_chance = (self.move_data.meta.get("flinch_chance") or 0) / 100
        if self.held_item_defender() not in ("kings-rock", "razor-fang") or self.status_move() or move_flinch_chance > 0:
            return move_flinch_chance
        return 0.10

    # Type-boosting items (Charcoal, Mystic Water, Silk Scarf, etc.): Boost the power of the Pokémon's moves of the item's type by 20%.
    def type_boost_item_attacker(self):
        item = self.held_item_attacker()
        if item not in TYPE_BOOST_ITEMS or not self.move_power or self.move_type != TYPE_BOOST_ITEMS[item]:
            return self.move_power
        return self.move_power * 1.2
    def type_boost_item_defender(self):
        item = self.held_item_defender()
        if item not in TYPE_BOOST_ITEMS or not self.move_power or self.move_type != TYPE_BOOST_ITEMS[item]:
            return self.move_power
        return self.move_power * 1.2

    # Soul Dew: Boosts the power of Latias and Latios's Psychic and Dragon-type moves by 20%.
    def soul_dew_item_attacker(self):
        if self.held_item_attacker() != "soul-dew" or self.attacker.pokedex_id not in (380, 381) or not self.move_power:
            return self.move_power
        if self.move_type in ("psychic", "dragon"):
            return self.move_power * 1.2
        return self.move_power
    def soul_dew_item_defender(self):
        if self.held_item_defender() != "soul-dew" or self.defender.pokedex_id not in (380, 381) or not self.move_power:
            return self.move_power
        if self.move_type in ("psychic", "dragon"):
            return self.move_power * 1.2
        return self.move_power

    # Deep Sea Tooth: Doubles Clamperl's Sp. Atk.
    def deep_sea_tooth_item_attacker(self):
        if self.held_item_attacker() != "deep-sea-tooth" or self.attacker.pokedex_id != 366:
            return self.attacker_stats["special-attack"]
        return self.attacker_stats["special-attack"] * 2
    def deep_sea_tooth_item_defender(self):
        if self.held_item_defender() != "deep-sea-tooth" or self.defender.pokedex_id != 366:
            return self.defender_stats["special-attack"]
        return self.defender_stats["special-attack"] * 2

    # Deep Sea Scale: Doubles Clamperl's Sp. Def.
    def deep_sea_scale_item_attacker(self):
        if self.held_item_attacker() != "deep-sea-scale" or self.attacker.pokedex_id != 366:
            return self.attacker_stats["special-defense"]
        return self.attacker_stats["special-defense"] * 2
    def deep_sea_scale_item_defender(self):
        if self.held_item_defender() != "deep-sea-scale" or self.defender.pokedex_id != 366:
            return self.defender_stats["special-defense"]
        return self.defender_stats["special-defense"] * 2

    # Focus Band: The Pokémon has a 10% chance to survive a hit that would knock it out, with 1 HP left. Returns the damage it actually takes.
    # damage = the dmg from the hit. current_hp = its HP before the hit.
    def focus_band_item_attacker(self, damage, current_hp):
        if self.held_item_attacker() != "focus-band" or damage < current_hp:
            return damage
        if random.random() < 0.1:
            return current_hp - 1
        return damage
    def focus_band_item_defender(self, damage, current_hp):
        if self.held_item_defender() != "focus-band" or damage < current_hp:
            return damage
        if random.random() < 0.1:
            return current_hp - 1
        return damage

    # Scope Lens and Razor Claw: Raise the Pokémon's critical hit ratio by 1 stage. Returns how many crit stages it adds.
    def scope_lens_item_attacker(self):
        if self.held_item_attacker() not in ("scope-lens", "razor-claw"):
            return 0
        return 1
    def scope_lens_item_defender(self):
        if self.held_item_defender() not in ("scope-lens", "razor-claw"):
            return 0
        return 1

    # Leftovers: Heals 1/16 of the Pokémon's max HP at the end of each turn.
    def leftovers_item_attacker(self):
        if self.held_item_attacker() != "leftovers":
            return 0
        return 0.0625
    def leftovers_item_defender(self):
        if self.held_item_defender() != "leftovers":
            return 0
        return 0.0625

    # Light Ball: Doubles Pikachu's Attack and Sp. Atk. Returns its Attack and Sp. Atk.
    def light_ball_item_attacker(self):
        attack = self.attacker_stats["attack"]
        special_attack = self.attacker_stats["special-attack"]
        if self.held_item_attacker() != "light-ball" or self.attacker.pokedex_id != 25:
            return attack, special_attack
        return attack * 2, special_attack * 2
    def light_ball_item_defender(self):
        attack = self.defender_stats["attack"]
        special_attack = self.defender_stats["special-attack"]
        if self.held_item_defender() != "light-ball" or self.defender.pokedex_id != 25:
            return attack, special_attack
        return attack * 2, special_attack * 2

    # Shell Bell: The Pokémon heals 1/8 of the damage it deals. Sheer Force stops it from working. Returns how much HP it heals.
    # damage_dealt = the dmg the move did.
    def shell_bell_item_attacker(self, damage_dealt):
        if self.held_item_attacker() != "shell-bell" or damage_dealt <= 0 or self.sheer_force_effects_attacker():
            return 0
        return damage_dealt // 8
    def shell_bell_item_defender(self, damage_dealt):
        if self.held_item_defender() != "shell-bell" or damage_dealt <= 0 or self.sheer_force_effects_defender():
            return 0
        return damage_dealt // 8

    # Lax Incense: Moves aimed at the Pokémon are 10% less accurate. Returns the move's accuracy. None means the move never misses.
    def lax_incense_item_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_item_attacker() != "lax-incense" or self.ohko_move():
            return accuracy
        return accuracy * 0.9
    def lax_incense_item_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_item_defender() != "lax-incense" or self.ohko_move():
            return accuracy
        return accuracy * 0.9

    # Lucky Punch: Raises Chansey's critical hit ratio by 2 stages. Returns how many crit stages it adds.
    def lucky_punch_item_attacker(self):
        if self.held_item_attacker() != "lucky-punch" or self.attacker.pokedex_id != 113:
            return 0
        return 2
    def lucky_punch_item_defender(self):
        if self.held_item_defender() != "lucky-punch" or self.defender.pokedex_id != 113:
            return 0
        return 2

    # Metal Powder: Doubles Ditto's Defense as long as it hasn't transformed.
    def metal_powder_item_attacker(self, transformed=False):
        if self.held_item_attacker() != "metal-powder" or self.attacker.pokedex_id != 132 or transformed:
            return self.attacker_stats["defense"]
        return self.attacker_stats["defense"] * 2
    def metal_powder_item_defender(self, transformed=False):
        if self.held_item_defender() != "metal-powder" or self.defender.pokedex_id != 132 or transformed:
            return self.defender_stats["defense"]
        return self.defender_stats["defense"] * 2

    # Thick Club: Doubles Cubone and Marowak's Attack.
    def thick_club_item_attacker(self):
        if self.held_item_attacker() != "thick-club" or self.attacker.pokedex_id not in (104, 105):
            return self.attacker_stats["attack"]
        return self.attacker_stats["attack"] * 2
    def thick_club_item_defender(self):
        if self.held_item_defender() != "thick-club" or self.defender.pokedex_id not in (104, 105):
            return self.defender_stats["attack"]
        return self.defender_stats["attack"] * 2

    # Leek: Raises Farfetch'd and Sirfetch'd's critical hit ratio by 2 stages. Returns how many crit stages it adds.
    def leek_item_attacker(self):
        if self.held_item_attacker() != "leek" or self.attacker.pokedex_id not in (83, 865):
            return 0
        return 2
    def leek_item_defender(self):
        if self.held_item_defender() != "leek" or self.defender.pokedex_id not in (83, 865):
            return 0
        return 2

    # Wide Lens: The Pokémon's moves are 10% more accurate. Returns the move's accuracy. None means the move never misses.
    def wide_lens_item_attacker(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_item_attacker() != "wide-lens" or self.ohko_move():
            return accuracy
        return accuracy * 1.1
    def wide_lens_item_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_item_defender() != "wide-lens" or self.ohko_move():
            return accuracy
        return accuracy * 1.1

    # Muscle Band: Boosts the power of the Pokémon's physical moves by 10%.
    def muscle_band_item_attacker(self):
        if self.held_item_attacker() != "muscle-band" or not self.move_power or self.move_data.damage_class != "physical":
            return self.move_power
        return self.move_power * 1.1
    def muscle_band_item_defender(self):
        if self.held_item_defender() != "muscle-band" or not self.move_power or self.move_data.damage_class != "physical":
            return self.move_power
        return self.move_power * 1.1

    # Wise Glasses: Boosts the power of the Pokémon's special moves by 10%.
    def wise_glasses_item_attacker(self):
        if self.held_item_attacker() != "wise-glasses" or not self.move_power or self.move_data.damage_class != "special":
            return self.move_power
        return self.move_power * 1.1
    def wise_glasses_item_defender(self):
        if self.held_item_defender() != "wise-glasses" or not self.move_power or self.move_data.damage_class != "special":
            return self.move_power
        return self.move_power * 1.1

    # Expert Belt: Boosts the dmg of the Pokémon's super-effective moves by 20%. Returns the dmg multiplier.
    def expert_belt_item_attacker(self):
        if self.held_item_attacker() != "expert-belt" or self.status_move() or self.type_effectiveness_defender() <= 1:
            return 1
        return 1.2
    def expert_belt_item_defender(self):
        if self.held_item_defender() != "expert-belt" or self.status_move() or self.type_effectiveness_attacker() <= 1:
            return 1
        return 1.2

    # Life Orb: Boosts the dmg of the Pokémon's moves by 30%, but it loses 1/10 of its max HP each time it attacks. Returns the dmg multiplier and the HP it loses as a fraction of its max HP.
    # Magic Guard and Sheer Force stop the HP loss.
    def life_orb_item_attacker(self):
        if self.held_item_attacker() != "life-orb" or self.status_move():
            return 1, 0
        if "magic-guard" in self.attacker_abilities or self.sheer_force_effects_attacker():
            return 1.3, 0
        return 1.3, 0.1
    def life_orb_item_defender(self):
        if self.held_item_defender() != "life-orb" or self.status_move():
            return 1, 0
        if "magic-guard" in self.defender_abilities or self.sheer_force_effects_defender():
            return 1.3, 0
        return 1.3, 0.1

    # Power Herb: The Pokémon skips the charging turn of a two-turn move (Solar Beam, Fly, etc.) and uses up the herb. Returns True if it uses the herb.
    # Solar Beam and Solar Blade don't charge in sun, and Electro Shot doesn't charge in rain, so the herb isn't used.
    def power_herb_item_attacker(self):
        if self.held_item_attacker() != "power-herb" or self.move_name not in CHARGE_MOVES:
            return False
        if self.move_name in ("solar-beam", "solar-blade") and self.utility_umbrella_item_attacker() in ("sun", "extreme-sun"):
            return False
        if self.move_name == "electro-shot" and self.utility_umbrella_item_attacker() in ("rain", "heavy-rain"):
            return False
        return True
    def power_herb_item_defender(self):
        if self.held_item_defender() != "power-herb" or self.move_name not in CHARGE_MOVES:
            return False
        if self.move_name in ("solar-beam", "solar-blade") and self.utility_umbrella_item_defender() in ("sun", "extreme-sun"):
            return False
        if self.move_name == "electro-shot" and self.utility_umbrella_item_defender() in ("rain", "heavy-rain"):
            return False
        return True

    # Toxic Orb: At the end of the turn, the Pokémon gets badly poisoned. Returns its status.
    def toxic_orb_item_attacker(self):
        if self.held_item_attacker() != "toxic-orb" or self.status_attacker or self.status_immune_attacker("badly-poison"):
            return self.status_attacker
        return "badly-poison"
    def toxic_orb_item_defender(self):
        if self.held_item_defender() != "toxic-orb" or self.status_defender or self.status_immune_defender("badly-poison"):
            return self.status_defender
        return "badly-poison"

    # Flame Orb: At the end of the turn, the Pokémon gets burned. Returns its status.
    def flame_orb_item_attacker(self):
        if self.held_item_attacker() != "flame-orb" or self.status_attacker or self.status_immune_attacker("burn"):
            return self.status_attacker
        return "burn"
    def flame_orb_item_defender(self):
        if self.held_item_defender() != "flame-orb" or self.status_defender or self.status_immune_defender("burn"):
            return self.status_defender
        return "burn"

    # Quick Powder: Doubles Ditto's Speed as long as it hasn't transformed.
    def quick_powder_item_attacker(self, transformed=False):
        if self.held_item_attacker() != "quick-powder" or self.attacker.pokedex_id != 132 or transformed:
            return self.attacker_stats["speed"]
        return self.attacker_stats["speed"] * 2
    def quick_powder_item_defender(self, transformed=False):
        if self.held_item_defender() != "quick-powder" or self.defender.pokedex_id != 132 or transformed:
            return self.defender_stats["speed"]
        return self.defender_stats["speed"] * 2

    # Focus Sash: If the Pokémon is at full HP, it survives a hit that would knock it out with 1 HP left and the sash is used up. Returns the dmg it actually takes.
    # damage = the dmg from the hit. current_hp = its HP before the hit.
    def focus_sash_item_attacker(self, damage, current_hp, max_hp):
        if self.held_item_attacker() != "focus-sash" or current_hp != max_hp or damage < current_hp:
            return damage
        return current_hp - 1
    def focus_sash_item_defender(self, damage, current_hp, max_hp):
        if self.held_item_defender() != "focus-sash" or current_hp != max_hp or damage < current_hp:
            return damage
        return current_hp - 1

    # Zoom Lens: If the Pokémon moves after the target, its move is 20% more accurate. Returns the move's accuracy. None means the move never misses.
    def zoom_lens_item_attacker(self, moves_last):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_item_attacker() != "zoom-lens" or not moves_last or self.ohko_move():
            return accuracy
        return accuracy * 1.2
    def zoom_lens_item_defender(self, moves_last):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if self.held_item_defender() != "zoom-lens" or not moves_last or self.ohko_move():
            return accuracy
        return accuracy * 1.2

    # Metronome: Each time the Pokémon uses the same move in a row, it does 20% more dmg, up to double. Returns the dmg multiplier.
    # consecutive_uses = how many times in a row it already used this move.
    def metronome_item_attacker(self, consecutive_uses):
        if self.held_item_attacker() != "metronome" or self.status_move():
            return 1
        return (1, 1.2, 1.4, 1.6, 1.8, 2)[min(max(consecutive_uses, 0), 5)]
    def metronome_item_defender(self, consecutive_uses):
        if self.held_item_defender() != "metronome" or self.status_move():
            return 1
        return (1, 1.2, 1.4, 1.6, 1.8, 2)[min(max(consecutive_uses, 0), 5)]

    # Iron Ball: Halves the Pokémon's Speed and grounds it (handled in grounded_attacker / grounded_defender).
    def iron_ball_item_attacker(self):
        if self.held_item_attacker() != "iron-ball":
            return self.attacker_stats["speed"]
        return self.attacker_stats["speed"] * 0.5
    def iron_ball_item_defender(self):
        if self.held_item_defender() != "iron-ball":
            return self.defender_stats["speed"]
        return self.defender_stats["speed"] * 0.5

    # Iron Ball also lets Ground-type moves hit a Flying-type holder, and they always do neutral dmg to it. Returns the type effectiveness.
    def iron_ball_ground_item_attacker(self):
        if self.held_item_attacker() != "iron-ball" or self.move_type != "ground" or "flying" not in self.attacker.types:
            return self.type_effectiveness_attacker()
        return 1
    def iron_ball_ground_item_defender(self):
        if self.held_item_defender() != "iron-ball" or self.move_type != "ground" or "flying" not in self.defender.types:
            return self.type_effectiveness_defender()
        return 1

    # Lagging Tail and Full Incense: The Pokémon moves last among moves with the same priority. Returns the move's priority.
    def lagging_tail_item_attacker(self):
        priority = self.move_data.priority
        if self.held_item_attacker() not in ("lagging-tail", "full-incense"):
            return priority
        return priority - 0.1
    def lagging_tail_item_defender(self):
        priority = self.move_data.priority
        if self.held_item_defender() not in ("lagging-tail", "full-incense"):
            return priority
        return priority - 0.1

    # Destiny Knot: If the Pokémon gets infatuated, the Pokémon that infatuated it gets infatuated too. Returns True if it does.
    # incoming_effect = the effect the Pokémon just got.
    def destiny_knot_item_attacker(self, incoming_effect):
        if self.held_item_attacker() != "destiny-knot" or incoming_effect != "infatuation":
            return False
        for ability in self.defender_abilities:
            if "infatuation" in VOLATILE_IMMUNITY_ABILITIES.get(ability, ()):
                return False
        return True
    def destiny_knot_item_defender(self, incoming_effect):
        if self.held_item_defender() != "destiny-knot" or incoming_effect != "infatuation":
            return False
        for ability in self.attacker_abilities:
            if "infatuation" in VOLATILE_IMMUNITY_ABILITIES.get(ability, ()):
                return False
        return True

    # Black Sludge: At the end of each turn, Poison-type Pokémon heal 1/16 of their max HP. Other Pokémon lose 1/8 instead. Returns the HP change as a fraction of its max HP.
    def black_sludge_item_attacker(self):
        if self.held_item_attacker() != "black-sludge":
            return 0
        if "poison" in self.attacker.types:
            return 0.0625
        if "magic-guard" in self.attacker_abilities:
            return 0
        return -0.125
    def black_sludge_item_defender(self):
        if self.held_item_defender() != "black-sludge":
            return 0
        if "poison" in self.defender.types:
            return 0.0625
        if "magic-guard" in self.defender_abilities:
            return 0
        return -0.125

    # Choice Scarf: Boosts the Pokémon's Speed by 50%, but it can only use the first move it picks.
    def choice_scarf_item_attacker(self):
        if self.held_item_attacker() != "choice-scarf":
            return self.attacker_stats["speed"]
        return self.attacker_stats["speed"] * 1.5
    def choice_scarf_item_defender(self):
        if self.held_item_defender() != "choice-scarf":
            return self.defender_stats["speed"]
        return self.defender_stats["speed"] * 1.5

    # Sticky Barb: The Pokémon loses 1/8 of its max HP at the end of each turn. Returns the HP change as a fraction of its max HP.
    def sticky_barb_item_attacker(self):
        if self.held_item_attacker() != "sticky-barb" or "magic-guard" in self.attacker_abilities:
            return 0
        return -0.125
    def sticky_barb_item_defender(self):
        if self.held_item_defender() != "sticky-barb" or "magic-guard" in self.defender_abilities:
            return 0
        return -0.125

    # Sticky Barb also moves to the Pokémon that hits the holder with a contact move if that Pokémon isn't holding an item. Returns True if it moves.
    def sticky_barb_transfer_item_attacker(self):
        return self.held_item_attacker() == "sticky-barb" and self.contact_move() and self.defender_item is None
    def sticky_barb_transfer_item_defender(self):
        return self.held_item_defender() == "sticky-barb" and self.contact_move() and self.attacker_item is None

    # Power items (Power Bracer, Power Belt, etc.): Halve the Pokémon's Speed. They still work with Klutz.
    def power_item_attacker(self):
        if self.held_item_attacker() not in POWER_ITEMS:
            return self.attacker_stats["speed"]
        return self.attacker_stats["speed"] * 0.5
    def power_item_defender(self):
        if self.held_item_defender() not in POWER_ITEMS:
            return self.defender_stats["speed"]
        return self.defender_stats["speed"] * 0.5

    # Shed Shell: The Pokémon can always switch out, even if an ability like Shadow Tag is trapping it. Returns True if it's still trapped.
    # trapped = whether it would be trapped without Shed Shell.
    def shed_shell_item_attacker(self, trapped):
        if self.held_item_attacker() != "shed-shell":
            return trapped
        return False
    def shed_shell_item_defender(self, trapped):
        if self.held_item_defender() != "shed-shell":
            return trapped
        return False

    # Big Root: The Pokémon heals 30% more HP from draining moves. Returns the move's drain.
    def big_root_item_attacker(self):
        if self.move_data.meta is None:
            return 0
        drain = self.move_data.meta.get("drain", 0)
        if self.held_item_attacker() != "big-root" or drain <= 0:
            return drain
        return drain * 1.3
    def big_root_item_defender(self):
        if self.move_data.meta is None:
            return 0
        drain = self.move_data.meta.get("drain", 0)
        if self.held_item_defender() != "big-root" or drain <= 0:
            return drain
        return drain * 1.3

    # Choice Specs: Boosts the Pokémon's Sp. Atk by 50%, but it can only use the first move it picks.
    def choice_specs_item_attacker(self):
        if self.held_item_attacker() != "choice-specs":
            return self.attacker_stats["special-attack"]
        return self.attacker_stats["special-attack"] * 1.5
    def choice_specs_item_defender(self):
        if self.held_item_defender() != "choice-specs":
            return self.defender_stats["special-attack"]
        return self.defender_stats["special-attack"] * 1.5

    # Plates (Flame Plate, Splash Plate, etc.): Boost the power of the Pokémon's moves of the Plate's type by 20%.
    def plate_item_attacker(self):
        item = self.held_item_attacker()
        if item not in PLATE_TYPES or not self.move_power or self.move_type != PLATE_TYPES[item]:
            return self.move_power
        return self.move_power * 1.2
    def plate_item_defender(self):
        item = self.held_item_defender()
        if item not in PLATE_TYPES or not self.move_power or self.move_type != PLATE_TYPES[item]:
            return self.move_power
        return self.move_power * 1.2

    # Red Orb: When Groudon switches in holding it, Groudon turns into Primal Groudon and its ability becomes Desolate Land. Returns its form name, types, stats and ability.
    def red_orb_item_attacker(self):
        if self.held_item_attacker() != "red-orb" or self.attacker.pokedex_id != 383:
            return self.attacker.name, self.attacker.types, self.attacker.stats, self.attacker_abilities[0]
        form = BATTLE_FORMS["groudon-primal"]
        return "groudon-primal", form["types"], form["stats"], "desolate-land"
    def red_orb_item_defender(self):
        if self.held_item_defender() != "red-orb" or self.defender.pokedex_id != 383:
            return self.defender.name, self.defender.types, self.defender.stats, self.defender_abilities[0]
        form = BATTLE_FORMS["groudon-primal"]
        return "groudon-primal", form["types"], form["stats"], "desolate-land"

    # Blue Orb: When Kyogre switches in holding it, Kyogre turns into Primal Kyogre and its ability becomes Primordial Sea. Returns its form name, types, stats and ability.
    def blue_orb_item_attacker(self):
        if self.held_item_attacker() != "blue-orb" or self.attacker.pokedex_id != 382:
            return self.attacker.name, self.attacker.types, self.attacker.stats, self.attacker_abilities[0]
        form = BATTLE_FORMS["kyogre-primal"]
        return "kyogre-primal", form["types"], form["stats"], "primordial-sea"
    def blue_orb_item_defender(self):
        if self.held_item_defender() != "blue-orb" or self.defender.pokedex_id != 382:
            return self.defender.name, self.defender.types, self.defender.stats, self.defender_abilities[0]
        form = BATTLE_FORMS["kyogre-primal"]
        return "kyogre-primal", form["types"], form["stats"], "primordial-sea"

    # Eviolite: Boosts the Defense and Sp. Def of a Pokémon that can still evolve by 50%. Returns its Defense and Sp. Def.
    def eviolite_item_attacker(self):
        defense = self.attacker_stats["defense"]
        special_defense = self.attacker_stats["special-defense"]
        if self.held_item_attacker() != "eviolite" or self.attacker.name not in NOT_FULLY_EVOLVED:
            return defense, special_defense
        return defense * 1.5, special_defense * 1.5
    def eviolite_item_defender(self):
        defense = self.defender_stats["defense"]
        special_defense = self.defender_stats["special-defense"]
        if self.held_item_defender() != "eviolite" or self.defender.name not in NOT_FULLY_EVOLVED:
            return defense, special_defense
        return defense * 1.5, special_defense * 1.5

    # Float Stone: Halves the Pokémon's weight. Returns its weight.
    def float_stone_item_attacker(self):
        if self.held_item_attacker() != "float-stone":
            return self.attacker.weight
        return max(1, self.attacker.weight // 2)
    def float_stone_item_defender(self):
        if self.held_item_defender() != "float-stone":
            return self.defender.weight
        return max(1, self.defender.weight // 2)

    # Rocky Helmet: When the Pokémon is hit by a contact move, the attacker loses 1/6 of its max HP. Returns the HP the attacker loses as a fraction of its max HP.
    def rocky_helmet_item_attacker(self):
        if self.held_item_attacker() != "rocky-helmet" or not self.contact_move() or self.type_effectiveness_attacker() == 0:
            return 0
        if "magic-guard" in self.defender_abilities:
            return 0
        return 1 / 6
    def rocky_helmet_item_defender(self):
        if self.held_item_defender() != "rocky-helmet" or not self.contact_move() or self.type_effectiveness_defender() == 0:
            return 0
        if "magic-guard" in self.attacker_abilities:
            return 0
        return 1 / 6

    # Air Balloon: The Pokémon floats, so Ground-type moves don't affect it. The balloon pops when it's hit by any other move. Returns the move's power and True if the balloon pops.
    # Air Balloon also means the Pokémon isn't grounded (handled in grounded_attacker / grounded_defender).
    def air_balloon_item_attacker(self):
        if self.held_item_attacker() != "air-balloon" or self.status_move():
            return self.move_power, False
        if self.move_type == "ground":
            return 0, False
        return self.move_power, self.type_effectiveness_attacker() > 0
    def air_balloon_item_defender(self):
        if self.held_item_defender() != "air-balloon" or self.status_move():
            return self.move_power, False
        if self.move_type == "ground":
            return 0, False
        return self.move_power, self.type_effectiveness_defender() > 0

    # Red Card: When the Pokémon is hit by a move, the attacker is forced to switch out and the card is used up. Returns True if the attacker is forced out.
    # current_hp = the holder's HP after the hit. Suction Cups, Guard Dog and Sheer Force stop it.
    def red_card_item_attacker(self, current_hp):
        if self.held_item_attacker() != "red-card" or self.status_move() or current_hp <= 0 or self.type_effectiveness_attacker() == 0:
            return False
        if "suction-cups" in self.defender_abilities or "guard-dog" in self.defender_abilities:
            return False
        return not self.sheer_force_effects_defender()
    def red_card_item_defender(self, current_hp):
        if self.held_item_defender() != "red-card" or self.status_move() or current_hp <= 0 or self.type_effectiveness_defender() == 0:
            return False
        if "suction-cups" in self.attacker_abilities or "guard-dog" in self.attacker_abilities:
            return False
        return not self.sheer_force_effects_attacker()

    # Ring Target: The Pokémon loses its type immunities, so moves it would be immune to hit it for neutral dmg. Returns the type effectiveness.
    def ring_target_item_attacker(self):
        if self.held_item_attacker() != "ring-target":
            return self.type_effectiveness_attacker()
        removes_flying_weaknesses = self.weather_effects().get("removes_flying_weaknesses", False)
        multiplier = 1
        for type_name, type_data in zip(self.attacker.types, self.attacker_types_data):
            if self.move_type in type_data["double_damage_from"]:
                if not (removes_flying_weaknesses and type_name == "flying"):
                    multiplier *= 2
            elif self.move_type in type_data["half_damage_from"]:
                multiplier *= 0.5
        return multiplier
    def ring_target_item_defender(self):
        if self.held_item_defender() != "ring-target":
            return self.type_effectiveness_defender()
        removes_flying_weaknesses = self.weather_effects().get("removes_flying_weaknesses", False)
        multiplier = 1
        for type_name, type_data in zip(self.defender.types, self.defender_types_data):
            if self.move_type in type_data["double_damage_from"]:
                if not (removes_flying_weaknesses and type_name == "flying"):
                    multiplier *= 2
            elif self.move_type in type_data["half_damage_from"]:
                multiplier *= 0.5
        return multiplier

    # Absorb Bulb: When the Pokémon is hit by a Water-type move, its Sp. Atk goes up 1 stage and the bulb is used up. Returns the Sp. Atk stage change.
    def absorb_bulb_item_attacker(self):
        if self.held_item_attacker() != "absorb-bulb" or self.move_type != "water" or self.status_move():
            return 0
        if self.type_effectiveness_attacker() == 0:
            return 0
        return 1
    def absorb_bulb_item_defender(self):
        if self.held_item_defender() != "absorb-bulb" or self.move_type != "water" or self.status_move():
            return 0
        if self.type_effectiveness_defender() == 0:
            return 0
        return 1

    # Cell Battery: When the Pokémon is hit by an Electric-type move, its Attack goes up 1 stage and the battery is used up. Returns the Attack stage change.
    def cell_battery_item_attacker(self):
        if self.held_item_attacker() != "cell-battery" or self.move_type != "electric" or self.status_move():
            return 0
        if self.type_effectiveness_attacker() == 0:
            return 0
        return 1
    def cell_battery_item_defender(self):
        if self.held_item_defender() != "cell-battery" or self.move_type != "electric" or self.status_move():
            return 0
        if self.type_effectiveness_defender() == 0:
            return 0
        return 1

    # Eject Button: When the Pokémon is hit by a move, it switches out and the button is used up. Returns True if it switches out.
    # current_hp = the holder's HP after the hit. Sheer Force stops it.
    def eject_button_item_attacker(self, current_hp):
        if self.held_item_attacker() != "eject-button" or self.status_move() or current_hp <= 0 or self.type_effectiveness_attacker() == 0:
            return False
        return not self.sheer_force_effects_defender()
    def eject_button_item_defender(self, current_hp):
        if self.held_item_defender() != "eject-button" or self.status_move() or current_hp <= 0 or self.type_effectiveness_defender() == 0:
            return False
        return not self.sheer_force_effects_attacker()

    # Gems (Fire Gem, Water Gem, etc.): Boost the power of the Pokémon's first move of the Gem's type by 30%, then the Gem is used up.
    def gem_item_attacker(self):
        item = self.held_item_attacker()
        if item not in GEM_TYPES or not self.move_power or self.move_type != GEM_TYPES[item]:
            return self.move_power
        return self.move_power * 1.3
    def gem_item_defender(self):
        item = self.held_item_defender()
        if item not in GEM_TYPES or not self.move_power or self.move_type != GEM_TYPES[item]:
            return self.move_power
        return self.move_power * 1.3

    # Weakness Policy: When the Pokémon is hit by a super-effective move, its Attack and Sp. Atk go up 2 stages and it's used up. Returns the Attack and Sp. Atk stage changes.
    def weakness_policy_item_attacker(self):
        if self.held_item_attacker() != "weakness-policy" or self.status_move() or self.move_name in FIXED_DAMAGE_MOVES:
            return 0, 0
        if self.type_effectiveness_attacker() <= 1:
            return 0, 0
        return 2, 2
    def weakness_policy_item_defender(self):
        if self.held_item_defender() != "weakness-policy" or self.status_move() or self.move_name in FIXED_DAMAGE_MOVES:
            return 0, 0
        if self.type_effectiveness_defender() <= 1:
            return 0, 0
        return 2, 2

    # Assault Vest: Boosts the Pokémon's Sp. Def by 50%, but it can't use status moves.
    def assault_vest_item_attacker(self):
        if self.held_item_attacker() != "assault-vest":
            return self.attacker_stats["special-defense"]
        return self.attacker_stats["special-defense"] * 1.5
    def assault_vest_item_defender(self):
        if self.held_item_defender() != "assault-vest":
            return self.defender_stats["special-defense"]
        return self.defender_stats["special-defense"] * 1.5

    # Returns True if the Pokémon can use this move while holding Assault Vest. Me First still works.
    def assault_vest_move_item_attacker(self):
        if self.held_item_attacker() != "assault-vest":
            return True
        return not self.status_move() or self.move_name == "me-first"
    def assault_vest_move_item_defender(self):
        if self.held_item_defender() != "assault-vest":
            return True
        return not self.status_move() or self.move_name == "me-first"

    # Luminous Moss: When the Pokémon is hit by a Water-type move, its Sp. Def goes up 1 stage and the moss is used up. Returns the Sp. Def stage change.
    def luminous_moss_item_attacker(self):
        if self.held_item_attacker() != "luminous-moss" or self.move_type != "water" or self.status_move():
            return 0
        if self.type_effectiveness_attacker() == 0:
            return 0
        return 1
    def luminous_moss_item_defender(self):
        if self.held_item_defender() != "luminous-moss" or self.move_type != "water" or self.status_move():
            return 0
        if self.type_effectiveness_defender() == 0:
            return 0
        return 1

    # Snowball: When the Pokémon is hit by an Ice-type move, its Attack goes up 1 stage and the snowball is used up. Returns the Attack stage change.
    def snowball_item_attacker(self):
        if self.held_item_attacker() != "snowball" or self.move_type != "ice" or self.status_move():
            return 0
        if self.type_effectiveness_attacker() == 0:
            return 0
        return 1
    def snowball_item_defender(self):
        if self.held_item_defender() != "snowball" or self.move_type != "ice" or self.status_move():
            return 0
        if self.type_effectiveness_defender() == 0:
            return 0
        return 1

    # Safety Goggles: The Pokémon is immune to powder and spore moves. Returns True if the move is blocked.
    # Safety Goggles also block Effect Spore and sandstorm and hail dmg (handled in effect_spore_ability and weather_damage).
    def safety_goggles_item_attacker(self):
        if self.held_item_attacker() != "safety-goggles":
            return False
        return self.powder_and_spore_move() and self.move_name != "rage-powder"
    def safety_goggles_item_defender(self):
        if self.held_item_defender() != "safety-goggles":
            return False
        return self.powder_and_spore_move() and self.move_name != "rage-powder"

    # Kee Berry: When the Pokémon is hit by a physical move, it eats the Berry and its Defense goes up 1 stage. Returns the Defense stage change.
    def kee_berry_item_attacker(self):
        if self.held_berry_attacker() != "kee-berry" or self.move_data.damage_class != "physical" or self.type_effectiveness_attacker() == 0:
            return 0
        return self.ripen_ability_attacker(1)
    def kee_berry_item_defender(self):
        if self.held_berry_defender() != "kee-berry" or self.move_data.damage_class != "physical" or self.type_effectiveness_defender() == 0:
            return 0
        return self.ripen_ability_defender(1)

    # Maranga Berry: When the Pokémon is hit by a special move, it eats the Berry and its Sp. Def goes up 1 stage. Returns the Sp. Def stage change.
    def maranga_berry_item_attacker(self):
        if self.held_berry_attacker() != "maranga-berry" or self.move_data.damage_class != "special" or self.type_effectiveness_attacker() == 0:
            return 0
        return self.ripen_ability_attacker(1)
    def maranga_berry_item_defender(self):
        if self.held_berry_defender() != "maranga-berry" or self.move_data.damage_class != "special" or self.type_effectiveness_defender() == 0:
            return 0
        return self.ripen_ability_defender(1)

    # Adrenaline Orb: When the Pokémon is hit by Intimidate, its Speed goes up 1 stage and the orb is used up. Returns the Speed stage change.
    # incoming_effect = the effect the Pokémon just got. speed_stage = its current Speed stage.
    def adrenaline_orb_item_attacker(self, incoming_effect, speed_stage=0):
        if self.held_item_attacker() != "adrenaline-orb" or incoming_effect != "intimidate" or speed_stage >= 6:
            return 0
        return 1
    def adrenaline_orb_item_defender(self, incoming_effect, speed_stage=0):
        if self.held_item_defender() != "adrenaline-orb" or incoming_effect != "intimidate" or speed_stage >= 6:
            return 0
        return 1

    # Terrain Seeds (Electric Seed, Grassy Seed, etc.): When the matching terrain is up, the Pokémon's Defense or Sp. Def goes up 1 stage and the seed is used up. Returns the stat and the stage change.
    def terrain_seed_item_attacker(self):
        item = self.held_item_attacker()
        if item not in TERRAIN_SEEDS or self.terrain != TERRAIN_SEEDS[item][0]:
            return None, 0
        return TERRAIN_SEEDS[item][1], 1
    def terrain_seed_item_defender(self):
        item = self.held_item_defender()
        if item not in TERRAIN_SEEDS or self.terrain != TERRAIN_SEEDS[item][0]:
            return None, 0
        return TERRAIN_SEEDS[item][1], 1

    # Memories (Fire Memory, Water Memory, etc.): Silvally's Multi-Attack becomes the Memory's type. Silvally's own type change is in rks_system_ability. Returns the move's type.
    def memory_item_attacker(self):
        item = self.held_item_attacker()
        if item not in MEMORY_TYPES or self.move_name != "multi-attack":
            return self.move_type
        return MEMORY_TYPES[item]
    def memory_item_defender(self):
        item = self.held_item_defender()
        if item not in MEMORY_TYPES or self.move_name != "multi-attack":
            return self.move_type
        return MEMORY_TYPES[item]

    # Throat Spray: After the Pokémon uses a sound move, its Sp. Atk goes up 1 stage and the spray is used up. Returns the Sp. Atk stage change.
    def throat_spray_item_attacker(self):
        if self.held_item_attacker() != "throat-spray" or not self.sound_move() or self.sheer_force_effects_attacker():
            return 0
        if "soundproof" in self.defender_abilities:
            return 0
        return 1
    def throat_spray_item_defender(self):
        if self.held_item_defender() != "throat-spray" or not self.sound_move() or self.sheer_force_effects_defender():
            return 0
        if "soundproof" in self.attacker_abilities:
            return 0
        return 1

    # Eject Pack: When the Pokémon's stats are lowered, it switches out and the pack is used up. Parting Shot doesn't trigger it. Returns True if it switches out.
    # stat_changes = the stat changes the Pokémon just got.
    def eject_pack_item_attacker(self, stat_changes):
        if self.held_item_attacker() != "eject-pack" or self.move_name == "parting-shot":
            return False
        return any(change < 0 for change in stat_changes.values())
    def eject_pack_item_defender(self, stat_changes):
        if self.held_item_defender() != "eject-pack" or self.move_name == "parting-shot":
            return False
        return any(change < 0 for change in stat_changes.values())

    # Room Service: When Trick Room is set, the Pokémon's Speed goes down 1 stage and it's used up. Returns the Speed stage change.
    # trick_room = True if Trick Room is up.
    def room_service_item_attacker(self, trick_room):
        if self.held_item_attacker() != "room-service" or not trick_room:
            return 0
        return -1
    def room_service_item_defender(self, trick_room):
        if self.held_item_defender() != "room-service" or not trick_room:
            return 0
        return -1

    # Utility Umbrella: The Pokémon isn't affected by sun or rain. Returns the weather the Pokémon is affected by.
    def utility_umbrella_item_attacker(self):
        weather = self.current_weather()
        if self.held_item_attacker() == "utility-umbrella" and weather in ("sun", "extreme-sun", "rain", "heavy-rain"):
            return None
        return weather
    def utility_umbrella_item_defender(self):
        weather = self.current_weather()
        if self.held_item_defender() == "utility-umbrella" and weather in ("sun", "extreme-sun", "rain", "heavy-rain"):
            return None
        return weather

    # Adamant Crystal, Lustrous Globe and Griseous Core: Dialga, Palkia and Giratina change to their Origin Forme while holding them. Giratina's ability becomes Levitate. Returns its form name, types, stats and ability.
    # Their power boost is in adamant_orb_item, lustrous_orb_item and griseous_orb_item.
    def origin_forme_item_attacker(self):
        item = self.held_item_attacker()
        if item not in ORIGIN_FORME_ITEMS or self.attacker.pokedex_id != ORIGIN_FORME_ITEMS[item][0]:
            return self.attacker.name, self.attacker.types, self.attacker.stats, self.attacker_abilities[0]
        form_name = ORIGIN_FORME_ITEMS[item][1]
        form = BATTLE_FORMS[form_name]
        if form_name == "giratina-origin":
            return form_name, form["types"], form["stats"], "levitate"
        return form_name, form["types"], form["stats"], self.attacker_abilities[0]
    def origin_forme_item_defender(self):
        item = self.held_item_defender()
        if item not in ORIGIN_FORME_ITEMS or self.defender.pokedex_id != ORIGIN_FORME_ITEMS[item][0]:
            return self.defender.name, self.defender.types, self.defender.stats, self.defender_abilities[0]
        form_name = ORIGIN_FORME_ITEMS[item][1]
        form = BATTLE_FORMS[form_name]
        if form_name == "giratina-origin":
            return form_name, form["types"], form["stats"], "levitate"
        return form_name, form["types"], form["stats"], self.defender_abilities[0]

    # Booster Energy: Activates Protosynthesis without sun or Quark Drive without Electric Terrain, then it's used up. Returns True if it's used.
    # Pass this into protosynthesis_ability / quark_drive_ability as booster_energy.
    def booster_energy_item_attacker(self):
        if self.held_item_attacker() != "booster-energy":
            return False
        if "protosynthesis" in self.attacker_abilities and self.current_weather() != "sun":
            return True
        return "quark-drive" in self.attacker_abilities and self.terrain != "electric-terrain"
    def booster_energy_item_defender(self):
        if self.held_item_defender() != "booster-energy":
            return False
        if "protosynthesis" in self.defender_abilities and self.current_weather() != "sun":
            return True
        return "quark-drive" in self.defender_abilities and self.terrain != "electric-terrain"

    # Ability Shield: The Pokémon's ability can't be changed or ignored by other Pokémon (Mold Breaker, Neutralizing Gas, Mummy, etc.). It still works with Klutz. Returns True if the ability is protected.
    def ability_shield_item_attacker(self):
        return self.held_item_attacker() == "ability-shield"
    def ability_shield_item_defender(self):
        return self.held_item_defender() == "ability-shield"

    # Clear Amulet: Other Pokémon's moves and abilities can't lower this Pokémon's stats. It also blocks Intimidate.
    # stage_change = how many stages the stat is changing. Returns the stage change that actually happens.
    def clear_amulet_item_attacker(self, stage_change, from_opponent=True):
        if self.held_item_attacker() != "clear-amulet":
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change
    def clear_amulet_item_defender(self, stage_change, from_opponent=True):
        if self.held_item_defender() != "clear-amulet":
            return stage_change
        if stage_change < 0 and from_opponent:
            return 0
        return stage_change

    # Mirror Herb: When the other Pokémon's stats go up, the Pokémon copies the boosts and the herb is used up. Returns the stat changes it copies.
    # opponent_stat_changes = the stat changes the other Pokémon just got.
    def mirror_herb_item_attacker(self, opponent_stat_changes):
        if self.held_item_attacker() != "mirror-herb":
            return {}
        return {stat: change for stat, change in opponent_stat_changes.items() if change > 0}
    def mirror_herb_item_defender(self, opponent_stat_changes):
        if self.held_item_defender() != "mirror-herb":
            return {}
        return {stat: change for stat, change in opponent_stat_changes.items() if change > 0}

    # Punching Glove: Boosts the power of the Pokémon's punching moves by 10%, and they don't make contact. Returns the move's power and True if it makes contact.
    def punching_glove_item_attacker(self):
        if self.held_item_attacker() != "punching-glove" or self.move_name not in PUNCHING_MOVES:
            return self.move_power, self.contact_move()
        if not self.move_power:
            return self.move_power, False
        return self.move_power * 1.1, False
    def punching_glove_item_defender(self):
        if self.held_item_defender() != "punching-glove" or self.move_name not in PUNCHING_MOVES:
            return self.move_power, self.contact_move()
        if not self.move_power:
            return self.move_power, False
        return self.move_power * 1.1, False

    # Covert Cloak: The Pokémon isn't affected by the extra effects of moves (flinching, stat drops, status, etc.). It also blocks Poison Touch and Toxic Chain.
    # Returns (ailment_chance, flinch_chance) as decimals, so roll them with: random.random() < chance
    def covert_cloak_item_attacker(self):
        ailment_chance, flinch_chance, _ = self.serene_grace_ability_defender()
        if self.held_item_attacker() != "covert-cloak" or self.status_move():
            return ailment_chance, flinch_chance
        return 0, 0
    def covert_cloak_item_defender(self):
        ailment_chance, flinch_chance, _ = self.serene_grace_ability_attacker()
        if self.held_item_defender() != "covert-cloak" or self.status_move():
            return ailment_chance, flinch_chance
        return 0, 0

    # Loaded Dice: The Pokémon's multi-hit moves hit more times. 2-5 hit moves hit 4 or 5 times and Population Bomb hits 4-10 times. Returns how many times the move hits.
    def loaded_dice_item_attacker(self):
        if self.held_item_attacker() != "loaded-dice" or "skill-link" in self.attacker_abilities:
            return self.skill_link_ability_attacker()
        if self.move_name == "population-bomb":
            return random.randint(4, 10)
        if self.move_data.meta is not None and self.move_data.meta.get("min_hits") == 2 and self.move_data.meta.get("max_hits") == 5:
            return random.choice((4, 5))
        return self.skill_link_ability_attacker()
    def loaded_dice_item_defender(self):
        if self.held_item_defender() != "loaded-dice" or "skill-link" in self.defender_abilities:
            return self.skill_link_ability_defender()
        if self.move_name == "population-bomb":
            return random.randint(4, 10)
        if self.move_data.meta is not None and self.move_data.meta.get("min_hits") == 2 and self.move_data.meta.get("max_hits") == 5:
            return random.choice((4, 5))
        return self.skill_link_ability_defender()

    # Masks (Wellspring Mask, Hearthflame Mask, Cornerstone Mask): Boost the power of Ogerpon's moves by 20%.
    def ogerpon_mask_item_attacker(self):
        if self.held_item_attacker() not in OGERPON_MASKS or self.attacker.pokedex_id != 1017 or not self.move_power:
            return self.move_power
        return self.move_power * 1.2
    def ogerpon_mask_item_defender(self):
        if self.held_item_defender() not in OGERPON_MASKS or self.defender.pokedex_id != 1017 or not self.move_power:
            return self.move_power
        return self.move_power * 1.2

    # Masks also change Ogerpon's form, type and ability. Returns its form name, types, stats and ability.
    def ogerpon_mask_form_item_attacker(self):
        item = self.held_item_attacker()
        if item not in OGERPON_MASKS or self.attacker.pokedex_id != 1017:
            return self.attacker.name, self.attacker.types, self.attacker.stats, self.attacker_abilities[0]
        mask_type, ability = OGERPON_MASKS[item]
        return "ogerpon-" + item, ["grass", mask_type], self.attacker.stats, ability
    def ogerpon_mask_form_item_defender(self):
        item = self.held_item_defender()
        if item not in OGERPON_MASKS or self.defender.pokedex_id != 1017:
            return self.defender.name, self.defender.types, self.defender.stats, self.defender_abilities[0]
        mask_type, ability = OGERPON_MASKS[item]
        return "ogerpon-" + item, ["grass", mask_type], self.defender.stats, ability

    # Ivy Cudgel becomes the type of Ogerpon's mask. Returns the move's type.
    def ivy_cudgel_item_attacker(self):
        item = self.held_item_attacker()
        if item not in OGERPON_MASKS or self.move_name != "ivy-cudgel":
            return self.move_type
        return OGERPON_MASKS[item][0]
    def ivy_cudgel_item_defender(self):
        item = self.held_item_defender()
        if item not in OGERPON_MASKS or self.move_name != "ivy-cudgel":
            return self.move_type
        return OGERPON_MASKS[item][0]

    # -------- Damage Calculation --------
    # calculate() puts everything together and works out the dmg the attacker's move does to the defender, the same way the Gen 9 games (and Smogon's calc) do.
    # Order: battle forms -> abilities that get ignored -> move type -> immunities -> base power -> attack -> defense -> base dmg -> weather and crit -> 16 random rolls -> STAB -> type effectiveness -> burn -> final modifiers.
    # Only works attacker to defender -> Will add defenderr to attacker soon. 

    # The Pokémon's Speed after stat stages, abilities, items and paralysis. Used for turn order and moves like Gyro Ball.
    # boosts = its stat stages, like {"speed": 1}.
    def final_speed_attacker(self, boosts=None):
        boosts = boosts or {}
        base_speed = self.attacker_stats["speed"]
        speed = apply_stage(base_speed, boosts.get("speed", 0))
        modifiers = []
        for new_speed in (self.swift_swim_ability_attacker(), self.chlorophyll_ability_attacker(), self.sand_rush_ability_attacker(), self.slush_rush_ability_attacker(),
                          self.surge_surfer_ability_attacker(), self.quick_feet_ability_attacker(), self.choice_scarf_item_attacker(), self.iron_ball_item_attacker(),
                          self.macho_brace_item_attacker(), self.power_item_attacker(), self.quick_powder_item_attacker()):
            modifiers.append(modifier_from(new_speed, base_speed))
        if self.paradox_boosted_stat_attacker(boosts) == "speed":
            modifiers.append(6144)
        speed = poke_round(speed * chain_modifiers(modifiers, 410, 131172) / 4096)
        if self.status_attacker == "paralysis" and "quick-feet" not in self.attacker_abilities:
            speed = speed // 2
        return speed
    def final_speed_defender(self, boosts=None):
        boosts = boosts or {}
        base_speed = self.defender_stats["speed"]
        speed = apply_stage(base_speed, boosts.get("speed", 0))
        modifiers = []
        for new_speed in (self.swift_swim_ability_defender(), self.chlorophyll_ability_defender(), self.sand_rush_ability_defender(), self.slush_rush_ability_defender(),
                          self.surge_surfer_ability_defender(), self.quick_feet_ability_defender(), self.choice_scarf_item_defender(), self.iron_ball_item_defender(),
                          self.macho_brace_item_defender(), self.power_item_defender(), self.quick_powder_item_defender()):
            modifiers.append(modifier_from(new_speed, base_speed))
        if self.paradox_boosted_stat_defender(boosts) == "speed":
            modifiers.append(6144)
        speed = poke_round(speed * chain_modifiers(modifiers, 410, 131172) / 4096)
        if self.status_defender == "paralysis" and "quick-feet" not in self.defender_abilities:
            speed = speed // 2
        return speed

    # Protosynthesis and Quark Drive boost the Pokémon's highest stat, counting stat stages. Returns that stat, or None if neither is active.
    # boosts = its stat stages.
    def paradox_boosted_stat_attacker(self, boosts=None):
        boosts = boosts or {}
        booster_energy = self.booster_energy_item_attacker()
        if self.protosynthesis_ability_attacker(booster_energy)[0] is None and self.quark_drive_ability_attacker(booster_energy)[0] is None:
            return None
        return max(("attack", "defense", "special-attack", "special-defense", "speed"), key=lambda stat: apply_stage(self.attacker_stats[stat], boosts.get(stat, 0)))
    def paradox_boosted_stat_defender(self, boosts=None):
        boosts = boosts or {}
        booster_energy = self.booster_energy_item_defender()
        if self.protosynthesis_ability_defender(booster_energy)[0] is None and self.quark_drive_ability_defender(booster_energy)[0] is None:
            return None
        return max(("attack", "defense", "special-attack", "special-defense", "speed"), key=lambda stat: apply_stage(self.defender_stats[stat], boosts.get(stat, 0)))

    # The Pokémon's weight in hectograms (same as the database) after Heavy Metal, Light Metal and Float Stone.
    def final_weight_attacker(self):
        weight = self.heavy_metal_ability_attacker()
        if weight == self.attacker.weight:
            weight = self.light_metal_ability_attacker()
        if self.held_item_attacker() == "float-stone":
            weight = max(1, weight // 2)
        return weight
    def final_weight_defender(self):
        weight = self.heavy_metal_ability_defender()
        if weight == self.defender.weight:
            weight = self.light_metal_ability_defender()
        if self.held_item_defender() == "float-stone":
            weight = max(1, weight // 2)
        return weight

    # Swaps in a new form for the attacker or defender for the rest of the calc. The form's base stats go through calculate_stats with the same build.
    # side = "attacker" or "defender".
    def change_form(self, side, name, types, base_stats, ability):
        form = copy.copy(getattr(self, side))
        form.name = name
        form.types = list(types)
        form.stats = dict(base_stats)
        setattr(self, side, form)
        setattr(self, f"{side}_types_data", [Type.objects.get(name=t).type_data for t in form.types])
        setattr(self, f"{side}_stats", calculate_stats(form.stats, getattr(self, f"{side}_build"), form.pokedex_id))
        setattr(self, f"{side}_abilities", [ability])

    # Changes each Pokémon into the form its held item forces (Primal Groudon and Kyogre, the Origin Formes, Ogerpon's masks, Arceus's Plates, Silvally's Memories),
    # Castform into its weather form, and Aegislash into Blade Forme when it attacks.
    def use_battle_forms(self):
        for form_function in (self.red_orb_item_attacker, self.blue_orb_item_attacker, self.origin_forme_item_attacker, self.ogerpon_mask_form_item_attacker):
            name, types, base_stats, ability = form_function()
            if name != self.attacker.name:
                self.change_form("attacker", name, types, base_stats, ability)
                break
        for form_function in (self.red_orb_item_defender, self.blue_orb_item_defender, self.origin_forme_item_defender, self.ogerpon_mask_form_item_defender):
            name, types, base_stats, ability = form_function()
            if name != self.defender.name:
                self.change_form("defender", name, types, base_stats, ability)
                break
        if "multitype" in self.attacker_abilities and self.attacker.pokedex_id == 493 and self.multitype_ability_attacker(self.attacker_item) != self.attacker.types:
            types = self.multitype_ability_attacker(self.attacker_item)
            self.change_form("attacker", "arceus-" + types[0], types, self.attacker.stats, "multitype")
        if "multitype" in self.defender_abilities and self.defender.pokedex_id == 493 and self.multitype_ability_defender(self.defender_item) != self.defender.types:
            types = self.multitype_ability_defender(self.defender_item)
            self.change_form("defender", "arceus-" + types[0], types, self.defender.stats, "multitype")
        if "rks-system" in self.attacker_abilities and self.attacker.pokedex_id == 773 and self.rks_system_ability_attacker(self.attacker_item) != self.attacker.types:
            types = self.rks_system_ability_attacker(self.attacker_item)
            self.change_form("attacker", "silvally-" + types[0], types, self.attacker.stats, "rks-system")
        if "rks-system" in self.defender_abilities and self.defender.pokedex_id == 773 and self.rks_system_ability_defender(self.defender_item) != self.defender.types:
            types = self.rks_system_ability_defender(self.defender_item)
            self.change_form("defender", "silvally-" + types[0], types, self.defender.stats, "rks-system")
        castform_forms = {"fire": "castform-sunny", "water": "castform-rainy", "ice": "castform-snowy"}
        if self.attacker.pokedex_id == 351 and self.forecast_ability_attacker() != self.attacker.types:
            types = self.forecast_ability_attacker()
            self.change_form("attacker", castform_forms[types[0]], types, self.attacker.stats, "forecast")
        if self.defender.pokedex_id == 351 and self.forecast_ability_defender() != self.defender.types:
            types = self.forecast_ability_defender()
            self.change_form("defender", castform_forms[types[0]], types, self.defender.stats, "forecast")
        name, types, base_stats = self.stance_change_ability_attacker()
        if name != self.attacker.name:
            self.change_form("attacker", name, types, base_stats, self.attacker_abilities[0])

    # Neutralizing Gas, Mold Breaker (and the moves that act like it) stop the other Pokémon's abilities from working for this calc.
    def ignore_abilities(self):
        attacker_abilities = self.neutralizing_gas_ability_defender()
        defender_abilities = self.neutralizing_gas_ability_attacker()
        self.attacker_abilities = attacker_abilities or [""]
        self.defender_abilities = defender_abilities or [""]
        for ability_breaker in (self.mold_breaker_ability_attacker, self.teravolt_ability_attacker, self.turboblaze_ability_attacker):
            self.defender_abilities = ability_breaker() or [""]
        if self.move_name in ABILITY_IGNORING_MOVES and not self.ability_shield_item_defender():
            self.defender_abilities = [ability for ability in self.defender_abilities if ability not in BREAKABLE_ABILITIES] or [""]

         # Works out the move's type after items, abilities and the field change it. Returns the type and True if an -ate ability or Normalize changed it (those also boost its power by 20%).
    def final_move_type(self):
        name = self.move_name
        if name == "weather-ball":
            weather = self.utility_umbrella_item_attacker()
            if "mega-sol" in self.attacker_abilities and self.held_item_attacker() != "utility-umbrella":
                weather = "sun"
            weather_types = {"sun": "fire", "extreme-sun": "fire", "rain": "water", "heavy-rain": "water", "sandstorm": "rock", "snow": "ice", "hail": "ice"}
            return weather_types.get(weather, "normal"), False
        if name == "judgment" and self.held_item_attacker() in PLATE_TYPES:
            return PLATE_TYPES[self.held_item_attacker()], False
        if name == "techno-blast":
            for drive in (self.douse_drive_item_attacker, self.shock_drive_item_attacker, self.burn_drive_item_attacker, self.chill_drive_item_attacker):
                if drive() != self.move_type:
                    return drive(), False
            return self.move_type, False
        if name == "multi-attack":
            return self.memory_item_attacker(), False
        if name == "ivy-cudgel":
            return self.ivy_cudgel_item_attacker(), False
        if name == "terrain-pulse":
            terrain_types = {"electric-terrain": "electric", "grassy-terrain": "grass", "misty-terrain": "fairy", "psychic-terrain": "psychic"}
            if self.grounded_attacker():
                return terrain_types.get(self.terrain, "normal"), False
            return "normal", False
        if name == "revelation-dance":
            return self.attacker.types[0], False
        if name == "hidden-power":
            ivs = self.attacker_build["ivs"]
            bits = sum((ivs[stat] % 2) << place for place, stat in enumerate(("hp", "attack", "defense", "speed", "special-attack", "special-defense")))
            return HIDDEN_POWER_TYPES[bits * 15 // 63], False
        if name == "struggle":
            return "typeless", False
        move_type, new_power = self.normalize_ability_attacker()
        if new_power != self.move_power:
            return move_type, True
        for ate_ability in (self.aerilate_ability_attacker, self.galvanize_ability_attacker, self.pixilate_ability_attacker, self.refrigerate_ability_attacker, self.dragonize_ability_attacker):
            move_type, _ = ate_ability()
            if move_type != self.move_type:
                return move_type, True
        return self.liquid_voice_ability_attacker(), False
    
    def final_type_effectiveness(self, defender_hp):
        if self.move_name == "struggle":
            return 1
        if "scrappy" in self.attacker_abilities:
            effectiveness = self.scrappy_ability_attacker()
        elif "minds-eye" in self.attacker_abilities:
            effectiveness = self.minds_eye_ability_attacker()
        else:
            effectiveness = self.type_effectiveness_defender()
        if self.move_name == "freeze-dry" and "water" in self.defender.types:
            effectiveness *= 4
        if self.move_name == "flying-press":
            for type_data in self.defender_types_data:
                if "flying" in type_data["double_damage_from"]:
                    effectiveness *= 2
                elif "flying" in type_data["half_damage_from"]:
                    effectiveness *= 0.5
                elif "flying" in type_data["no_damage_from"]:
                    effectiveness *= 0
        if effectiveness == 0:
            effectiveness = self.ring_target_item_defender()
        if effectiveness == 0 and self.move_type == "ground":
            effectiveness = self.iron_ball_ground_item_defender()
        if effectiveness == 0 and self.move_name == "thousand-arrows":
            effectiveness = 1
        if effectiveness > 0 and "tera-shell" in self.defender_abilities and self.tera_shell_ability_defender(defender_hp, self.defender_stats["hp"]) == 0.5:
            effectiveness = 0.5
        return effectiveness
    
      # Checks the defender's abilities, its item, primal weather and Psychic Terrain for anything that stops the move completely. Returns True if the move does no dmg.
    def move_blocked(self):
        name = self.move_name
        # Moves that fail on their own in some situations.
        if ((name == "poltergeist" and self.defender_item is None)
                or (name == "dream-eater" and self.status_defender != "sleep" and "comatose" not in self.defender_abilities)
                or (name == "steel-roller" and not self.terrain)
                or (name == "synchronoise" and not set(self.attacker.types) & set(self.defender.types))
                or (name == "burn-up" and "fire" not in self.attacker.types)
                or (name == "double-shock" and "electric" not in self.attacker.types)
                or (name == "sky-drop" and ("flying" in self.defender.types or self.final_weight_defender() >= 2000))):
            return True
        if self.weather_move_power() == 0 or self.wonder_guard_ability_defender() == 0:
            return True
        if self.move_name != "thousand-arrows" and (self.levitate_ability_defender() == 0 or self.eelevate_ability_defender() == 0 or self.air_balloon_item_defender()[0] == 0):
            return True
        for absorb_ability in (self.flash_fire_ability_defender, self.well_baked_body_ability_defender, self.water_absorb_ability_defender, self.storm_drain_ability_defender,
                               self.dry_skin_ability_defender, self.volt_absorb_ability_defender, self.lightning_rod_ability_defender, self.motor_drive_ability_defender,
                               self.sap_sipper_ability_defender, self.earth_eater_ability_defender, self.wind_rider_ability_defender):
            if absorb_ability()[0] == 0:
                return True
        if self.soundproof_ability_defender() == 0 or self.bulletproof_ability_defender() == 0:
            return True
        if self.queenly_majesty_ability_defender() or self.dazzling_ability_defender() or self.armor_tail_ability_defender():
            return True
        return self.terrain_blocks_priority_defender()
    
      # Moves that do a set amount of dmg (Seismic Toss, Super Fang, one-hit KO moves, etc.). Returns the dmg, or None if the move isn't one of them.
    def fixed_damage(self, attacker_hp, defender_hp):
        name = self.move_name
        if name in ("seismic-toss", "night-shade"):
            return self.attacker_level
        if name == "dragon-rage":
            return 40
        if name == "sonic-boom":
            return 20
        if name in ("super-fang", "ruination", "natures-madness"):
            return max(1, defender_hp // 2)
        if name == "final-gambit":
            return attacker_hp
        if name == "endeavor":
            return max(0, defender_hp - attacker_hp)
        if self.ohko_move():
            if "sturdy" in self.defender_abilities or self.attacker_level < self.defender_level:
                return 0
            if name == "sheer-cold" and "ice" in self.defender.types:
                return 0
            return defender_hp
        return None
    
     # Knock Off does 50% more dmg if the target is holding an item it can knock off. Returns True if it gets the boost.
    def knock_off_boost(self):
        item = self.defender_item
        if item is None or UNREMOVABLE_ITEMS.get(item) == self.defender.pokedex_id:
            return False
        if (item in PLATE_TYPES and self.defender.pokedex_id == 493) or (item in MEMORY_TYPES and self.defender.pokedex_id == 773):
            return False
        if item in ("douse-drive", "shock-drive", "burn-drive", "chill-drive") and self.defender.pokedex_id == 649:
            return False
        if item == "booster-energy" and ("protosynthesis" in self.defender_abilities or "quark-drive" in self.defender_abilities):
            return False
        return True

    # Works out the power of moves whose power depends on weight, Speed, HP, stat stages, status, items, terrain or weather. Returns the power before modifiers, or None for moves that do set dmg. (This one was quite difficult to figure out :o) 
    def variable_move_power(self, attacker_hp, defender_hp, attacker_boosts, defender_boosts, attacker_speed, defender_speed):
        name = self.move_name
        power = self.move_power
        attacker_max_hp = self.attacker_stats["hp"]
        defender_max_hp = self.defender_stats["hp"]
        if name in ("low-kick", "grass-knot"):
            weight = self.final_weight_defender() / 10
            return 120 if weight >= 200 else 100 if weight >= 100 else 80 if weight >= 50 else 60 if weight >= 25 else 40 if weight >= 10 else 20
        if name in ("heavy-slam", "heat-crash"):
            ratio = self.final_weight_attacker() / self.final_weight_defender()
            return 120 if ratio >= 5 else 100 if ratio >= 4 else 80 if ratio >= 3 else 60 if ratio >= 2 else 40
        if name == "gyro-ball":
            return min(150, 25 * defender_speed // attacker_speed + 1) if attacker_speed else 1
        if name == "electro-ball":
            if not defender_speed:
                return 40
            ratio = attacker_speed // defender_speed
            return 150 if ratio >= 4 else 120 if ratio >= 3 else 80 if ratio >= 2 else 60 if ratio >= 1 else 40
        if name in ("eruption", "water-spout", "dragon-energy"):
            return max(1, 150 * attacker_hp // attacker_max_hp)
        if name in ("flail", "reversal"):
            portion = 48 * attacker_hp // attacker_max_hp
            return 200 if portion <= 1 else 150 if portion <= 4 else 100 if portion <= 9 else 80 if portion <= 16 else 40 if portion <= 32 else 20
        if name in ("crush-grip", "wring-out", "hard-press"):
            max_power = 100 if name == "hard-press" else 120
            portion = 100 * (defender_hp * 4096 // defender_max_hp)
            return (max_power * portion + 2047) // 4096 // 100 or 1
        if name in ("stored-power", "power-trip"):
            return 20 + 20 * sum(stage for stage in attacker_boosts.values() if stage > 0)
        if name == "punishment":
            return min(200, 60 + 20 * sum(stage for stage in defender_boosts.values() if stage > 0))
        if name in FRIENDSHIP_MOVES:
            return 102
        if name == "weather-ball":
            return 100 if self.utility_umbrella_item_attacker() not in (None, "strong-winds") else 50
        if name == "terrain-pulse":
            return 100 if self.terrain and self.grounded_attacker() else 50
        if name == "rising-voltage":
            return 140 if self.terrain == "electric-terrain" and self.grounded_defender() else 70
        if name == "psyblade":
            return 120 if self.terrain == "electric-terrain" else 80
        if power is None:
            return None
        doubled = ((name in ("hex", "infernal-parade") and (self.status_defender or "comatose" in self.defender_abilities))
                   or (name == "barb-barrage" and self.status_defender in ("poison", "badly-poison"))
                   or (name == "wake-up-slap" and (self.status_defender == "sleep" or "comatose" in self.defender_abilities))
                   or (name == "smelling-salts" and self.status_defender == "paralysis")
                   or (name == "acrobatics" and self.attacker_item in (None, "flying-gem"))
                   or (name == "payback" and attacker_speed <= defender_speed)
                   or (name in ("bolt-beak", "fishious-rend") and attacker_speed > defender_speed))
        return power * 2 if doubled else power

    # How many times the move hits. 2-5 hit moves count as 3 hits (4 with Loaded Dice, 5 with Skill Link), same as Smogon's calc. This is done for simplicity sake. 
    def damage_calc_hits(self):
        meta = self.move_data.meta or {}
        min_hits = meta.get("min_hits") or MISSING_HIT_COUNTS.get(self.move_name, 1)
        max_hits = meta.get("max_hits") or MISSING_HIT_COUNTS.get(self.move_name, 1)
        if min_hits == max_hits or "skill-link" in self.attacker_abilities:
            return max_hits
        if self.held_item_attacker() == "loaded-dice":
            return 4
        return 3

    # The move's power after every ability, item, terrain and move effect that changes it. Same order as the games.
    def final_base_power(self, physical, effectiveness, ate_changed, moves_last, makes_contact, attacker_boosts, defender_hp):
        name = self.move_name
        power = self.move_power
        modifiers = []
        # Moves that get stronger in certain situations.
        if ((name == "facade" and self.status_attacker in ("burn", "paralysis", "poison", "badly-poison"))
                or (name == "brine" and defender_hp <= self.defender_stats["hp"] / 2)
                or (name == "venoshock" and self.status_defender in ("poison", "badly-poison"))):
            modifiers.append(8192)
        elif name == "expanding-force" and self.grounded_attacker() and self.terrain == "psychic-terrain":
            modifiers.append(6144)
        elif (name == "knock-off" and self.knock_off_boost()) or (name == "misty-explosion" and self.grounded_attacker() and self.terrain == "misty-terrain"):
            modifiers.append(6144)
        elif name in ("solar-beam", "solar-blade") and self.utility_umbrella_item_attacker() in ("rain", "heavy-rain", "sandstorm", "snow", "hail"):
            modifiers.append(2048)
        elif name in ("collision-course", "electro-drift") and effectiveness > 1:
            modifiers.append(5461)
        # Terrain boosts or weakens the move.
        modifiers.append(modifier_from(self.terrain_move_power(), power))
        # Abilities that boost certain kinds of moves by 50%.
        for new_power in (self.technician_ability_attacker(), self.mega_launcher_ability_attacker(), self.strong_jaw_ability_attacker(), self.steely_spirit_ability_attacker(), self.sharpness_ability_attacker()):
            modifiers.append(modifier_from(new_power, power))
        if physical:
            modifiers.append(modifier_from(self.toxic_boost_ability_attacker(), self.attacker_stats["attack"]))
        else:
            modifiers.append(modifier_from(self.flare_boost_ability_attacker(), self.attacker_stats["special-attack"]))
        modifiers.append(modifier_from(self.dark_aura_ability(), power))
        modifiers.append(modifier_from(self.fairy_aura_ability(), power))
        # Abilities that boost certain kinds of moves by 30%.
        for new_power in (self.sheer_force_ability_attacker(), self.sand_force_ability_attacker(), self.analytic_ability_attacker(moves_last), self.punk_rock_power_attacker()):
            modifiers.append(modifier_from(new_power, power))
        # Tough Claws goes by whether the move ends up making contact (Punching Glove, Long Reach and Shell Side Arm can change it).
        if makes_contact and "tough-claws" in self.attacker_abilities:
            modifiers.append(5325)
        if ate_changed:
            modifiers.append(4915)
        for new_power in (self.reckless_ability_attacker(), self.iron_fist_ability_attacker()):
            modifiers.append(modifier_from(new_power, power))
        modifiers.append(modifier_from(self.dry_skin_ability_defender()[0], power))
        # Items that boost the move's power.
        for new_power in (self.gem_item_attacker(), self.adamant_orb_item_attacker(), self.lustrous_orb_item_attacker(), self.griseous_orb_item_attacker(), self.soul_dew_item_attacker(),
                          self.type_boost_item_attacker(), self.plate_item_attacker(), self.ogerpon_mask_item_attacker(), self.punching_glove_item_attacker()[0]):
            modifiers.append(modifier_from(new_power, power))
        # Muscle Band and Wise Glasses go by the category the move ends up using (Photon Geyser and Shell Side Arm can switch).
        if (physical and self.held_item_attacker() == "muscle-band") or (not physical and self.held_item_attacker() == "wise-glasses"):
            modifiers.append(4505)
        return max(1, poke_round(power * chain_modifiers(modifiers, 41, 2097152) / 4096))

    # The attacking stat after stat stages and modifiers. Foul Play uses the target's Attack and Body Press uses Defense.
    def final_attack(self, physical, critical_hit, attacker_boosts, defender_boosts, attacker_hp):
        if self.move_name == "foul-play":
            attack, stage = self.defender_stats["attack"], defender_boosts.get("attack", 0)
        elif self.move_name == "body-press":
            attack, stage = self.attacker_stats["defense"], attacker_boosts.get("defense", 0)
        else:
            stat = "attack" if physical else "special-attack"
            attack, stage = self.attacker_stats[stat], attacker_boosts.get(stat, 0)
        # Crits ignore the attacker's stat drops, and Unaware ignores all of its stat changes.
        if stage != 0 and not (critical_hit and stage < 0) and "unaware" not in self.defender_abilities:
            attack = apply_stage(attack, stage)
        if physical and self.hustle_ability_attacker() != self.attacker_stats["attack"]:
            attack = poke_round(attack * 3 / 2)
        power = self.move_power
        stat = "attack" if physical else "special-attack"
        base_stat = self.attacker_stats[stat]
        modifiers = []
        # The attacker's abilities.
        modifiers.append(modifier_from(self.defeatist_ability_attacker(attacker_hp, self.attacker_stats["hp"])[0], self.attacker_stats["attack"]))
        if physical:
            for new_stat in (self.flower_gift_ability_attacker()[0], self.gorilla_tactics_ability_attacker(), self.guts_ability_attacker(), self.huge_power_ability_attacker(), self.pure_power_ability_attacker(), self.orichalcum_pulse_attack_attacker()):
                modifiers.append(modifier_from(new_stat, base_stat))
        else:
            for new_stat in (self.solar_power_ability_attacker(), self.hadron_engine_special_attack_attacker()):
                modifiers.append(modifier_from(new_stat, base_stat))
        for pinch_ability in (self.overgrow_ability_attacker, self.blaze_ability_attacker, self.torrent_ability_attacker, self.swarm_ability_attacker):
            modifiers.append(modifier_from(pinch_ability(attacker_hp, self.attacker_stats["hp"]), power))
        for new_power in (self.steelworker_ability_attacker(), self.dragons_maw_ability_attacker(), self.rocky_payload_ability_attacker(), self.fire_mane_ability_attacker(), self.transistor_ability_attacker(), self.water_bubble_power_attacker()):
            modifiers.append(modifier_from(new_power, power))
        # The defender's abilities that weaken the attacker's attacking stat.
        for new_power in (self.thick_fat_ability_defender(), self.water_bubble_ability_defender(), self.purifying_salt_ability_defender(), self.heatproof_ability_defender()):
            modifiers.append(modifier_from(new_power, power))
        if physical:
            modifiers.append(modifier_from(self.tablets_of_ruin_ability_defender(), base_stat))
        else:
            modifiers.append(modifier_from(self.vessel_of_ruin_ability_defender(), base_stat))
        # Protosynthesis and Quark Drive boost the attacker's highest stat by 30%.
        if self.paradox_boosted_stat_attacker(attacker_boosts) == stat:
            modifiers.append(5325)
        # The attacker's items.
        light_ball = self.light_ball_item_attacker()
        if physical:
            for new_stat in (self.thick_club_item_attacker(), light_ball[0], self.choice_band_item_attacker()):
                modifiers.append(modifier_from(new_stat, base_stat))
        else:
            for new_stat in (self.deep_sea_tooth_item_attacker(), light_ball[1], self.choice_specs_item_attacker()):
                modifiers.append(modifier_from(new_stat, base_stat))
        return max(1, poke_round(attack * chain_modifiers(modifiers, 410, 131072) / 4096))