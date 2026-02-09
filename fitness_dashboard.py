import marimo

__generated_with = "0.19.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from math import pi

    return mo, pd, pi, plt


@app.cell
def _(pd):
    # Define fitness data directly (for WASM compatibility)
    fitness_data = {
        'name': ['Alex Johnson', 'Sam Williams', 'Jordan Lee', 'Casey Martinez',
                 'Taylor Brown', 'Morgan Davis', 'Riley Garcia', 'Avery Wilson',
                 'Quinn Anderson', 'Skylar Thomas'],
        'strength': [245.3, 312.7, 178.9, 289.4, 198.2, 267.8, 223.5, 301.6, 186.4, 254.1],
        'power': [1823.5, 2134.8, 1456.2, 1987.3, 1678.9, 2245.6, 1534.7, 2089.4, 1712.3, 1891.2],
        'endurance': [67.2, 45.8, 78.5, 52.4, 82.1, 38.9, 71.3, 48.7, 75.6, 63.8],
        'movement_quality': [88.4, 72.1, 94.7, 81.9, 69.3, 91.2, 77.6, 85.8, 93.5, 79.8],
        'mobility': [79.3, 91.2, 68.5, 85.7, 73.8, 88.4, 82.1, 76.9, 67.2, 94.6]
    }

    fitness_df = pd.DataFrame(fitness_data)

    # Calculate percentiles for each metric
    metrics = ['strength', 'power', 'endurance', 'movement_quality', 'mobility']
    for metric in metrics:
        fitness_df[f'{metric}_percentile'] = fitness_df[metric].rank(pct=True) * 100
    return (fitness_df,)


@app.cell
def _(fitness_df, mo):
    # Create dropdown for person selection
    person_dropdown = mo.ui.dropdown(
        options={name: name for name in fitness_df['name'].tolist()},
        value=fitness_df['name'].iloc[0],
        label="Select Person"
    )
    return (person_dropdown,)


@app.cell
def _(mo, person_dropdown):
    mo.md(f"""
    # Fitness Dashboard\n\nSelect a person to view their performance metrics:\n\n{person_dropdown}
    """)
    return


@app.cell
def _(fitness_df, mo, person_dropdown, pi, plt):
    # Get selected person's data
    selected_person = person_dropdown.value
    person_data = fitness_df[fitness_df['name'] == selected_person].iloc[0]

    # Prepare data
    categories = ['Strength', 'Power', 'Endurance', 'Movement\nQuality', 'Mobility']
    percentiles = [
        person_data['strength_percentile'],
        person_data['power_percentile'],
        person_data['endurance_percentile'],
        person_data['movement_quality_percentile'],
        person_data['mobility_percentile']
    ]
    raw_values = [
        person_data['strength'],
        person_data['power'],
        person_data['endurance'],
        person_data['movement_quality'],
        person_data['mobility']
    ]

    # Create figure with two subplots
    fig = plt.figure(figsize=(14, 6))
    fig.patch.set_facecolor('white')

    # Radar chart (left) - Percentile Rankings
    ax1 = plt.subplot(121, projection='polar')
    ax1.set_facecolor('white')

    # Number of variables
    num_vars = len(categories)

    # Compute angle for each axis
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    percentiles_plot = percentiles + [percentiles[0]]  # Close the plot
    angles += angles[:1]

    # Plot radar chart
    ax1.plot(angles, percentiles_plot, 'o-', linewidth=3, color='steelblue', markersize=10)
    ax1.fill(angles, percentiles_plot, alpha=0.3, color='steelblue')
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(categories, size=13, fontweight='500', color='black')
    ax1.set_ylim(0, 100)
    ax1.set_yticks([25, 50, 75, 100])
    ax1.set_yticklabels(['25', '50', '75', '100'], size=11, color='black')
    ax1.grid(True, linewidth=0.8, alpha=0.4, color='gray')
    ax1.set_title(f'{selected_person}\nPercentile Rankings',
                  size=15, pad=25, fontweight='bold', color='black')
    ax1.tick_params(colors='black')
    ax1.spines['polar'].set_color('black')

    # Bar chart (right) - Raw Values
    ax2 = plt.subplot(122)
    ax2.set_facecolor('white')
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    bars = ax2.bar(range(len(categories)), raw_values, color=colors, alpha=0.85, width=0.7)
    ax2.set_xticks(range(len(categories)))
    ax2.set_xticklabels(categories, rotation=45, ha='right', size=13, fontweight='500', color='black')
    ax2.set_ylabel('Value', fontsize=14, fontweight='bold', color='black')
    ax2.tick_params(axis='y', labelsize=11, colors='black')
    ax2.tick_params(axis='x', colors='black')
    ax2.set_title(f'{selected_person}\nRaw Values',
                  size=15, pad=15, fontweight='bold', color='black')
    ax2.grid(True, axis='y', alpha=0.3, linewidth=0.8, color='gray')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_color('black')
    ax2.spines['left'].set_color('black')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='black')

    plt.tight_layout()

    # Display
    mo.md(f"## Performance Metrics for {selected_person}")
    fig
    return (person_data,)


@app.cell
def _(mo, person_data):
    # Display detailed stats
    mo.md(f"""
    ## Detailed Statistics

    | Metric | Raw Value | Percentile Ranking |
    |--------|-----------|-------------------|
    | Strength | {person_data['strength']:.1f} kg | {person_data['strength_percentile']:.0f}th percentile |
    | Power | {person_data['power']:.1f} watts | {person_data['power_percentile']:.0f}th percentile |
    | Endurance | {person_data['endurance']:.1f} min | {person_data['endurance_percentile']:.0f}th percentile |
    | Movement Quality | {person_data['movement_quality']:.1f} | {person_data['movement_quality_percentile']:.0f}th percentile |
    | Mobility | {person_data['mobility']:.1f} | {person_data['mobility_percentile']:.0f}th percentile |
    """)
    return


if __name__ == "__main__":
    app.run()
