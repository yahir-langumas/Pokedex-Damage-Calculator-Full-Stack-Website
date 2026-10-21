# Pokédex Damage Calculator

A full-stack Django web app for browsing Pokémon and calculating battle damage between them — built on top of live [PokeAPI](https://pokeapi.co/) data.

## About

This project pulls Pokémon species, moves, learnsets, and type-effectiveness data directly from PokeAPI into a local database, then uses that data to power a browsable Pokédex and an in-progress damage calculator modeling real battle mechanics — move categories, abilities, held items, and status conditions.

## Features

- **Pokédex table** — search and browse every Pokémon by name, with base stats, typing, and abilities pulled straight from the database.
- **Expandable reference panels** — click any Pokémon card to reveal direct links to its Bulbapedia, Smogon (SV), and Limitless VGC pages.
- **Home page** with an overview and entry points into the Pokédex and team builder.
- **Moves page** — every move with its type, category, power, accuracy, and PP.
- **Damage calculator engine** (in progress) — move-category checks (sound, slicing, biting, punching, pulse, wind, ball-and-bomb, powder/spore moves, and more), weather, terrain, status conditions, all 314 abilities, and held items (being added now), all modeling real in-game mechanics rather than approximations.

The team builder page is scaffolded but not functional yet. The damage calculator doesn't have a page yet; the final damage formula is the next step.

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Data source:** [PokeAPI](https://pokeapi.co/) via the `requests` library
- **Frontend:** Server-rendered HTML/CSS/vanilla JS — no frontend framework

## Project Structure

```
pokedata/
├── models.py                     # Species, Moves, Learnset, Type
├── views.py / urls.py            # Page routing
├── damage_calculator.py          # DamageCalculator class + move, ability, and item reference data
├── tests.py                      # Tests for the damage calculator
├── fixtures/pokedata.json        # Saved copy of all the PokeAPI data (loads in seconds)
├── templates/                    # base.html, home.html, pokemon_table.html, moves.html, team_builder.html
└── management/commands/
    ├── import_species.py         # Species, stats, types, abilities
    ├── import_moves.py           # Move data + metadata (power, drain, ailments, etc.)
    ├── import_learnset.py        # Links each species to its learnable moves
    └── import_types.py           # Type effectiveness chart
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

## Data & Attribution

All Pokémon data is sourced from [PokeAPI](https://pokeapi.co/). This is a personal project built for learning purposes and is not affiliated with or endorsed by Nintendo, Game Freak, or The Pokémon Company.

## Status

Actively in progress. The data pipeline, Pokédex, and moves page are functional. All abilities are in the damage calculator; held items are being added now, followed by the stat and damage formulas and a calculator page.