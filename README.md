# Pokédex Damage Calculator

A full-stack Django web app for browsing Pokémon and calculating battle damage between them — built on top of live [PokeAPI](https://pokeapi.co/) data.

## About

This project pulls Pokémon species, moves, learnsets, and type-effectiveness data directly from PokeAPI into a local database, then uses that data to power a browsable Pokédex and an in-progress damage calculator modeling real battle mechanics — move categories, abilities, held items, and status conditions.

## Features

- **Pokédex table** — search and browse every Pokémon by name, with base stats, typing, and abilities pulled straight from the database.
- **Expandable reference panels** — click any Pokémon card to reveal direct links to its Bulbapedia, Smogon (SV), and Limitless VGC pages.
- **Home page** with an overview and entry points into the Pokédex and team builder.
- **Damage calculator engine** (in progress) — move-category checks (sound, slicing, biting, punching, pulse, wind, ball-and-bomb, powder/spore moves, and more) plus ability implementations (Rock Head, Levitate, Wonder Guard, Huge Power so far), all modeling real in-game mechanics rather than approximations.

The team builder and a dedicated moves page are scaffolded (routes exist) but not fully functional yet.

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Data source:** [PokeAPI](https://pokeapi.co/) via the `requests` library
- **Frontend:** Server-rendered HTML/CSS/vanilla JS — no frontend framework

## Project Structure

```
pokedata/
├── models.py                     # Species, Moves, Learnset, Type, Status_Effect
├── views.py / urls.py            # Page routing
├── templates/                    # home.html, pokemon_table.html, base.html
└── management/commands/
    ├── import_species.py         # Species, stats, types, abilities
    ├── import_moves.py           # Move data + metadata (power, drain, ailments, etc.)
    ├── import_learnset.py        # Links each species to its learnable moves
    ├── import_types.py           # Type effectiveness chart
    ├── import_status_effects.py  # Status condition data (in progress)
    └── damage_calculator.py      # DamageCalculator class + move-category reference data
```

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

# Set up the database
python manage.py migrate

# Populate it from PokeAPI (takes a while — this is a lot of API calls)
python manage.py import_species
python manage.py import_moves
python manage.py import_learnset
python manage.py import_types

# Run the dev server
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/`.

## Data & Attribution

All Pokémon data is sourced live from [PokeAPI](https://pokeapi.co/). This is a personal project built for learning purposes and is not affiliated with or endorsed by Nintendo, Game Freak, or The Pokémon Company.

## Status

Actively in progress. The data pipeline and core Pokédex browsing are functional; the damage calculator is the current focus, being built out one move category, ability, item, and status effect at a time.
