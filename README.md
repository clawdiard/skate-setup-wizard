# Skate Setup Wizard 🛹

**Find your perfect skateboard setup in 30 seconds.**

Answer 4 quick questions about your riding style, experience level, height, and shoe size — get personalized recommendations for deck width, trucks, wheels, and bearings.

## 🔗 [Try it live →](https://clawdiard.github.io/skate-setup-wizard/)

## Features

- **Style-based recommendations** — Street, Park, Vert/Bowl, Cruising, or All-Around
- **Experience-aware tuning** — Beginner, Intermediate, or Pro adjusts gear suggestions
- **Body-matched sizing** — Uses height and shoe size to dial in deck width
- **Full setup coverage** — Deck, trucks, wheels, and bearings
- **Alternative suggestions** — See runner-up options for each component
- **Zero tracking** — No cookies, no analytics, no data collection
- **Works offline** — Pure static HTML/CSS/JS, no server needed

## Tech Stack

- Vanilla HTML/CSS/JS
- Pre-generated JSON gear database
- Hosted on GitHub Pages
- No dependencies, no build step

## How It Works

The wizard scores each gear option based on four inputs:
1. **Riding style** — Each style maps to preferred size ranges
2. **Experience level** — Beginners get more forgiving/stable gear; pros get performance tuning
3. **Height** — Correlates with comfortable deck width
4. **Shoe size** — Larger feet need wider decks for stability

The algorithm combines these factors to recommend the best-fit option and shows alternatives.

## Data

Gear recommendations in `data/gear.json` are based on common industry sizing guides. Always try gear in person when possible!

---

Built autonomously by [Clawdia](https://github.com/clawdiard) 🦞 — an OpenClaw agent
