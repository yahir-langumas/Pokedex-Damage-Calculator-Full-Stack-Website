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

# Moves Normalize doesn't change to Normal type. Refrigerate, Pixilate and Aerilate skip these too.
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
BATTLE_FORMS = {
    "darmanitan-zen": {"types": ["fire", "psychic"], "stats": {"hp": 105, "attack": 30, "defense": 105, "special-attack": 140, "special-defense": 105, "speed": 55}},
    "aegislash-blade": {"types": ["steel", "ghost"], "stats": {"hp": 60, "attack": 140, "defense": 50, "special-attack": 140, "special-defense": 50, "speed": 60}},
    "minior-core": {"types": ["rock", "flying"], "stats": {"hp": 60, "attack": 100, "defense": 60, "special-attack": 100, "special-defense": 60, "speed": 120}},
}

# Moves Parental Bond doesn't make hit twice (charge moves, future moves and moves that only work once).
PARENTAL_BOND_EXCEPTIONS = {
    "bounce", "dig", "dive", "doom-desire", "dragon-darts", "dynamax-cannon", "electro-shot",
    "endeavor", "explosion", "final-gambit", "fling", "fly", "freeze-shock", "future-sight",
    "ice-ball", "ice-burn", "meteor-beam", "phantom-force", "razor-wind", "rollout",
    "self-destruct", "shadow-force", "skull-bash", "sky-attack", "sky-drop", "solar-beam",
    "solar-blade",
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
        attack = self.attacker.stats["attack"]
        special_defense = self.attacker.stats["special-defense"]
        if "flower-gift" not in self.attacker_abilities or not self.attacker.name.startswith("cherrim"):
            return attack, special_defense
        if self.current_weather() in ("sun", "extreme-sun"):
            return attack * 1.5, special_defense * 1.5
        return attack, special_defense
    def flower_gift_ability_defender(self):
        attack = self.defender.stats["attack"]
        special_defense = self.defender.stats["special-defense"]
        if "flower-gift" not in self.defender_abilities or not self.defender.name.startswith("cherrim"):
            return attack, special_defense
        if self.current_weather() in ("sun", "extreme-sun"):
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
        attack = self.attacker.stats["attack"]
        special_attack = self.attacker.stats["special-attack"]
        if "defeatist" not in self.attacker_abilities or current_hp > max_hp / 2:
            return attack, special_attack
        return attack * 0.5, special_attack * 0.5
    def defeatist_ability_defender(self, current_hp, max_hp):
        attack = self.defender.stats["attack"]
        special_attack = self.defender.stats["special-attack"]
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
        if "shield-dust" in self.defender_abilities:
            return self.status_defender
        if self.status_effects_defender() or self.status_immune_defender("poison"):
            return self.status_defender
        if random.random() < 0.30:
            return "poison"
        return self.status_defender
    def poison_touch_ability_defender(self):
        if "poison-touch" not in self.defender_abilities or not self.contact_move():
            return self.status_attacker
        if "shield-dust" in self.attacker_abilities:
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
            return self.attacker.stats["speed"]
        if self.current_weather() == "sandstorm":
            return self.attacker.stats["speed"] * 2
        return self.attacker.stats["speed"]
    def sand_rush_ability_defender(self):
        if "sand-rush" not in self.defender_abilities:
            return self.defender.stats["speed"]
        if self.current_weather() == "sandstorm":
            return self.defender.stats["speed"] * 2
        return self.defender.stats["speed"]

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
    def imposter_ability_attacker(self):
        if "imposter" not in self.attacker_abilities:
            return self.attacker.types, self.attacker.stats, self.attacker_abilities
        stats = dict(self.defender.stats)
        stats["hp"] = self.attacker.stats["hp"]
        return self.defender.types, stats, self.defender_abilities
    def imposter_ability_defender(self):
        if "imposter" not in self.defender_abilities:
            return self.defender.types, self.defender.stats, self.defender_abilities
        stats = dict(self.attacker.stats)
        stats["hp"] = self.defender.stats["hp"]
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
        if "mummy" not in self.attacker_abilities or not self.contact_move():
            return self.defender_abilities
        for ability in self.defender_abilities:
            if ability in CANT_SUPPRESS_ABILITIES or ability == "mummy":
                return self.defender_abilities
        return ["mummy"]
    def mummy_ability_defender(self):
        if "mummy" not in self.defender_abilities or not self.contact_move():
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
        if "victory-star" not in self.attacker_abilities:
            return accuracy
        return accuracy * 1.1
    def victory_star_ability_defender(self):
        accuracy = self.move_data.accuracy
        if accuracy is None:
            return None
        if "victory-star" not in self.defender_abilities:
            return accuracy
        return accuracy * 1.1

    # Turboblaze: Same as Mold Breaker. The Pokémon's moves ignore abilities that would block or weaken them. Returns the target's abilities that still work.
    def turboblaze_ability_attacker(self):
        if "turboblaze" not in self.attacker_abilities:
            return self.defender_abilities
        return [ability for ability in self.defender_abilities if ability not in BREAKABLE_ABILITIES]
    def turboblaze_ability_defender(self):
        if "turboblaze" not in self.defender_abilities:
            return self.attacker_abilities
        return [ability for ability in self.attacker_abilities if ability not in BREAKABLE_ABILITIES]

    # Teravolt: Same as Mold Breaker. The Pokémon's moves ignore abilities that would block or weaken them. Returns the target's abilities that still work.
    def teravolt_ability_attacker(self):
        if "teravolt" not in self.attacker_abilities:
            return self.defender_abilities
        return [ability for ability in self.defender_abilities if ability not in BREAKABLE_ABILITIES]
    def teravolt_ability_defender(self):
        if "teravolt" not in self.defender_abilities:
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
            return self.attacker.stats["defense"]
        return self.attacker.stats["defense"] * 2
    def fur_coat_ability_defender(self):
        if "fur-coat" not in self.defender_abilities:
            return self.defender.stats["defense"]
        return self.defender.stats["defense"] * 2

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
            return self.attacker.stats["defense"]
        return self.attacker.stats["defense"] * 1.5
    def grass_pelt_ability_defender(self):
        if "grass-pelt" not in self.defender_abilities or self.terrain != "grassy-terrain":
            return self.defender.stats["defense"]
        return self.defender.stats["defense"] * 1.5

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
        attack = self.attacker.stats["attack"]
        special_attack = self.attacker.stats["special-attack"]
        if "stakeout" not in self.attacker_abilities or not target_switched_in:
            return attack, special_attack
        return attack * 2, special_attack * 2
    def stakeout_ability_defender(self, target_switched_in=False):
        attack = self.defender.stats["attack"]
        special_attack = self.defender.stats["special-attack"]
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

    # -------- Items -------- 
    # Items can be held by a Pokémon to boost its stats, change its type, or give it immunity to certain moves. Some items are consumed after one use, while others last until the Pokémon switches out or faints.
    # Will add after finishing abilities 
    def life_orb_item(self):
        pass
    def choice_band_item(self):
        pass