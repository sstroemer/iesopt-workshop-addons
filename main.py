import iesopt
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


model = iesopt.run("heat.iesopt.yaml", skip_validation=True)

# => infeasible because not enough HP power ( ~1.81 kW would be necessary )

model = iesopt.run(
    "heat.iesopt.yaml", parameters=dict(hp_pnom=1.85), skip_validation=True
)
model.objective_value

# => OR .... more flexibility in the house temperature

model = iesopt.run(
    "heat.iesopt.yaml", parameters=dict(house_tlo=20), skip_validation=True
)
model.objective_value

# Plot: temperature profile
model.results.components["house"].var.state
temperature_profile = model.results.components["house"].var.state[0:168]

go.Figure().add_hline(
    y=20, line_dash="dash", annotation_text="20°C", annotation_position="bottom right"
).add_hline(
    y=23, line_dash="dash", annotation_text="23°C", annotation_position="bottom right"
).add_trace(
    go.Scatter(
        x=np.arange(len(temperature_profile)),
        y=temperature_profile,
        mode="lines",
        name="House Temperature",
        line=dict(width=2),  # Set line thickness to 2
    )
).update_layout(
    title="Temperature Profile",
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
    yaxis=dict(range=[18, 25]),  # Set y-axis range from 18 to 25 degrees
).show()
