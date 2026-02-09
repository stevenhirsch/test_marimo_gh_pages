import marimo

__generated_with = "0.19.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    return go, make_subplots, mo, pd


@app.cell
def _(pd):
    # Read fitness data from CSV file
    fitness_df = pd.read_csv('fitness_data.csv')

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
def _(fitness_df, go, make_subplots, person_dropdown):
    # Get selected person's data
    selected_person = person_dropdown.value
    person_data = fitness_df[fitness_df['name'] == selected_person].iloc[0]

    # Prepare data for radial plot (percentiles)
    categories = ['Strength', 'Power', 'Endurance', 'Movement Quality', 'Mobility']
    percentiles = [
        person_data['strength_percentile'],
        person_data['power_percentile'],
        person_data['endurance_percentile'],
        person_data['movement_quality_percentile'],
        person_data['mobility_percentile']
    ]

    # Prepare data for bar chart (raw values)
    raw_values = [
        person_data['strength'],
        person_data['power'],
        person_data['endurance'],
        person_data['movement_quality'],
        person_data['mobility']
    ]

    # Create subplots: 1 row, 2 columns
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f'{selected_person} - Percentile Rankings',
                       f'{selected_person} - Raw Values'),
        specs=[[{'type': 'polar'}, {'type': 'bar'}]],
        horizontal_spacing=0.15
    )

    # Radial plot (radar chart) for percentiles
    fig.add_trace(
        go.Scatterpolar(
            r=percentiles + [percentiles[0]],  # Close the polygon
            theta=categories + [categories[0]],
            fill='toself',
            name='Percentile',
            line=dict(color='rgb(0, 123, 255)', width=2),
            fillcolor='rgba(0, 123, 255, 0.3)'
        ),
        row=1, col=1
    )

    # Bar chart for raw values
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    fig.add_trace(
        go.Bar(
            x=categories,
            y=raw_values,
            name='Raw Value',
            marker=dict(color=colors),
            text=[f'{v:.1f}' for v in raw_values],
            textposition='outside'
        ),
        row=1, col=2
    )

    # Update radial plot layout
    fig.update_polars(
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickfont=dict(size=10)
        ),
        angularaxis=dict(
            tickfont=dict(size=11)
        )
    )

    # Update bar chart layout
    fig.update_xaxes(tickangle=45, row=1, col=2)
    fig.update_yaxes(title_text="Value", row=1, col=2)

    # Update overall layout
    fig.update_layout(
        height=500,
        showlegend=False,
        title_text=f"Performance Metrics for {selected_person}",
        title_x=0.5,
        title_font=dict(size=20)
    )

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
