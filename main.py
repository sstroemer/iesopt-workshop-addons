import iesopt
import plotly.graph_objects as go
import numpy as np


# Run the model
model = iesopt.run("bess_01.iesopt.yaml", skip_validation=True)

# Extract generation and curtailment data
generation = model.results.components["pv"].exp.value
curtailment = model.get_component("pv").ub.value - generation

# Group and sum data into 12 monthly values
mg = np.array([sum(generation[i * 730 : (i + 1) * 730]) for i in range(12)])
mc = np.array([sum(curtailment[i * 730 : (i + 1) * 730]) for i in range(12)])

# Create the stacked bar plot
fig = go.Figure(
    data=[
        go.Bar(name="Generation", x=list(range(1, 13)), y=mg, marker_color="green"),
        go.Bar(name="Curtailment", x=list(range(1, 13)), y=mc, marker_color="red"),
    ]
)

# Update the layout to stack the bars
fig.update_layout(
    barmode="stack",
    title="Monthly Gen. / Curt.",
    xaxis_title="Month",
    yaxis_title="kWh",
)

# Show the plot
fig.show()
