# Pokédex Damage Calculator

A full-stack Django web app for browsing Pokémon and calculating battle damage between them — built on top of live [PokeAPI](https://pokeapi.co/) data.

## About

This project pulls Pokémon species, moves, learnsets, and type-effectiveness data directly from PokeAPI into a local database, then uses that data to power a browsable Pokédex and an in-progress damage calculator modeling real battle mechanics — move categories, abilities, held items, status conditions, and real stats from EVs, IVs, natures, and levels.

## Features

- **Pokédex table** — search and browse every Pokémon by name, with base stats, typing, and abilities pulled straight from the database.
- **Expandable reference panels** — click any Pokémon card to reveal direct links to its Bulbapedia, Smogon (SV), and Limitless VGC pages.
- **Home page** with an overview and entry points into the Pokédex and team builder.
- **Moves page** — every move with its type, category, power, accuracy, and PP.
- **Stat calculator** — turns base stats into real stats using level (1–50, default 50 like most competitive formats), EVs, IVs, and natures, with checks that every build is legal.
- **Damage calculator engine** (in progress) — move-category checks (sound, slicing, biting, punching, pulse, wind, ball-and-bomb, powder/spore moves, and more), weather, terrain, status conditions, all 314 abilities, and all 218 battle-relevant held items, all modeling real in-game mechanics rather than approximations. The damage formula is being built step by step: move type changes, Speed, weight, battle forms (Primal Groudon and Kyogre, Origin Formes, Ogerpon's masks, Arceus, Silvally, Castform, and Aegislash), and ignored abilities (Mold Breaker, Neutralizing Gas) are done.

The team builder page is scaffolded but not functional yet. The damage calculator doesn't have a page yet; the rest of the damage formula comes first.

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Data source:** [PokeAPI](https://pokeapi.co/) via the `requests` library
- **Frontend:** Server-rendered HTML/CSS/vanilla JS — no frontend framework

## Getting Started

```bash
# Clone and enter the project
git clone https://github.com/yahir-langumas/Pokedex-Damage-Calculator-Full-Stack-Website.git
cd Pokedex-Damage-Calculator-Full-Stack-Website

# Set up a virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up the database and load the saved Pokémon data
python manage.py migrate
python manage.py loaddata pokedata

# Run the dev server
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/`.

To refresh the data straight from PokeAPI instead of using the saved copy, run the import commands (this takes a while — it's a lot of API calls):

```bash
python manage.py import_types
python manage.py import_moves
python manage.py import_species
python manage.py import_learnset
```

## Running Tests

```bash
python manage.py test
```

59 tests cover type effectiveness, weather, abilities, held items, the stat calculator, and the damage formula steps built so far (Speed, weight, battle forms, ignored abilities, and move types).

## Data & Attribution

All Pokémon data is sourced from [PokeAPI](https://pokeapi.co/). This is a personal project built for learning purposes and is not affiliated with or endorsed by Nintendo, Game Freak, or The Pokémon Company.

## Status

Actively in progress. The data pipeline, Pokédex, and moves page are functional. All 314 abilities and all 218 held items are in the damage calculator, and the stat formula (EVs, IVs, natures, and levels) is done. The damage formula is being added now: move types, Speed, weight, battle forms, and ignored abilities are in. Next up: type effectiveness and immunities, base power, attack and defense, the final modifiers, and then a calculator page.