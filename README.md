# Fitness Dashboard

An interactive fitness dashboard built with [marimo](https://marimo.io/) and deployed to GitHub Pages.

## Features

- View performance metrics for 10 athletes
- Interactive dropdown to select different people
- Radial plot showing percentile rankings across 5 fitness dimensions
- Bar chart displaying raw performance values
- Detailed statistics table

## Metrics

- **Strength** (kg)
- **Power** (watts)
- **Endurance** (minutes)
- **Movement Quality** (score)
- **Mobility** (score)

## Local Development

### Prerequisites

- [pixi](https://pixi.sh/)

### Installation

```bash
pixi install
```

### Running the App

Edit mode:
```bash
pixi run marimo edit fitness_dashboard.py
```

Run mode:
```bash
pixi run marimo run fitness_dashboard.py
```

## Deployment

This app automatically deploys to GitHub Pages on every push to the main branch using GitHub Actions.

### Setup GitHub Pages

1. Go to your repository settings
2. Navigate to Pages
3. Under "Build and deployment", select "GitHub Actions" as the source

The workflow will:
1. Install dependencies
2. Export the marimo notebook to HTML-WASM
3. Deploy to GitHub Pages

## License

MIT
