# Pokédex Damage Calculator

[![Tests](https://github.com/yahir-langumas/Pokedex-Damage-Calculator-Full-Stack-Website/actions/workflows/tests.yml/badge.svg)](https://github.com/yahir-langumas/Pokedex-Damage-Calculator-Full-Stack-Website/actions/workflows/tests.yml)

A full-stack Django web app for calculating Pokémon battle damage and browsing the Pokédex, built on [PokeAPI](https://pokeapi.co/) data. Pick an attacker, a defender and a move to see all 16 damage rolls, how much HP it takes and the chance to KO, using real Gen 9 battle mechanics.

**Live site:** coming soon — see the [roadmap](#roadmap).

![The damage calculator updating live as Life Orb, a critical hit and a new defender are picked](docs/images/damage-calculator.gif)

## About

This project pulls Pokémon species, moves, learnsets, and type matchups from PokeAPI into a local database, then uses that data to power a damage calculator and a browsable Pokédex. The damage engine models real battle mechanics — abilities, held items, weather, terrain, status conditions, stat stages, screens, and real stats from EVs, IVs, natures, and levels.

Every full damage result in the tests was checked roll for roll against [Smogon's damage calculator](https://calc.pokemonshowdown.com/).

## Features

- **Damage calculator page** — set each side's Pokémon, move, ability, item, level, nature, EVs, IVs, stat stages, status, and current HP, plus weather, terrain, critical hits, and Reflect / Light Screen / Aurora Veil. Results update live as you change things, and every calc has its own link you can share.
- **Full results** — all 16 damage rolls, the damage as a % of HP, the KO chance, an HP bar, and a Smogon-style summary line, like `252 Atk Life Orb Garchomp Earthquake vs. 252 HP / 0 Def Kingambit: 195-229 (94.2 - 110.6%) -- 56.2% chance to OHKO`.
- **Damage engine** — the full Gen 9 damage formula with the games' exact rounding, all 314 abilities, all 218 battle-relevant held items, multi-hit moves, moves whose power changes (Low Kick, Eruption, Gyro Ball, Knock Off, and more), set-damage moves, immunities, and battle forms (Primal Groudon and Kyogre, Origin Formes, Ogerpon's masks, Arceus, Silvally, Castform, and Aegislash).
- **Stat calculator** — turns base stats into real stats using level (1–50, default 50 like most competitive formats), EVs, IVs, and natures, with checks that every build is legal.
- **Pokédex** — search all 1,025 Pokémon by name to see their types and base stat totals. Click any Pokémon for quick links to its Bulbapedia page, its Smogon sets, and its Limitless VGC tournament results.
- **Moves page** (`/moves/`) — every move with its type, category, power, accuracy, and PP.

The team builder is next — see the [roadmap](#roadmap).

![The damage calculator showing Life Orb Garchomp's Earthquake against Kingambit](docs/images/damage-calculator.png)

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Data source:** [PokeAPI](https://pokeapi.co/) via the `requests` library
- **Frontend:** Server-rendered HTML/CSS/vanilla JS — no frontend framework
- **Testing & CI:** Django's test framework, with GitHub Actions running the tests, Ruff linting, and a coverage report on every push and pull request

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

296 tests cover:

- **The damage engine** — type effectiveness, weather, terrain, abilities, held items, stats, and every step of the damage formula. The full damage results in the tests were checked against Smogon's calculator.
- **The calculator page** — results, form validation, and the endpoint that fills in each Pokémon's abilities and moves.
- **The home page and nav bar.**
- **The PokeAPI import commands** — with the API faked, so the tests never make real requests.

GitHub Actions runs every test on each push and pull request.

## Credits & Attribution

- **[PokeAPI](https://pokeapi.co/)** — all of the Pokémon data and sprite images.
- **[Smogon's damage calculator](https://calc.pokemonshowdown.com/)** ([source on GitHub](https://github.com/smogon/damage-calc)) — the damage formula here is based on Smogon's open-source calculator, and its results were used to check this calculator's numbers. Smogon's damage calculator is MIT licensed, Copyright (c) 2013-2025 Honko and other contributors ([license](https://github.com/smogon/damage-calc/blob/master/LICENSE)).
- **[Bulbapedia](https://bulbapedia.bulbagarden.net/)** — reference for how abilities and held items work in battle.

This is a personal project and is not affiliated with or endorsed by Nintendo, Game Freak, The Pokémon Company, or Smogon.

## Roadmap

Actively in progress.

- [x] Damage engine — the full Gen 9 damage formula, all 314 abilities, and all 218 held items
- [x] Damage calculator page with live results and shareable links
- [x] Pokédex and moves page
- [x] 296 tests running on every push with GitHub Actions
- [ ] **Going live** — deploy with Docker on AWS, with the link at the top of this page
- [ ] **Team builder** — build a team of six and check its matchups with the damage calculator
- [ ] **Multi-hit moves** — pick how many times 2–5 hit moves hit (they count as 3 hits for now)
- [ ] **Accounts and saved teams** — sign up and log in to save your teams and come back to them