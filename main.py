import iesopt
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


model = iesopt.run("battery.iesopt.yaml")

generation = model.results.components["pv"].exp.value
curtailment = model.get_component("pv").ub.value - generation

mg = np.array([sum(generation[i * 730 : (i + 1) * 730]) for i in range(12)])
mc = np.array([sum(curtailment[i * 730 : (i + 1) * 730]) for i in range(12)])
state_of_charge = model.results.components["grid"].var.state
state_of_charge_week = state_of_charge[:168]

make_subplots(
    rows=1, cols=2, subplot_titles=("Monthly Gen. / Curt.", "Energy stored")
).add_trace(
    go.Bar(name="Generation", x=list(range(1, 13)), y=mg, marker_color="green"),
    row=1,
    col=1,
).add_trace(
    go.Bar(name="Curtailment", x=list(range(1, 13)), y=mc, marker_color="red"),
    row=1,
    col=1,
).add_trace(
    go.Scatter(
        x=list(range(168)),
        y=state_of_charge_week,
        name="Battery",
        mode="lines",
        line_shape="hv",
        line_color="black",
    ),
    row=1,
    col=2,
).update_layout(
    barmode="stack",
    title="Monthly Generation and Curt. / Battery content",
    xaxis_title="Month",
    yaxis_title="kWh",
).update_xaxes(title_text="Time", row=1, col=2).update_yaxes(
    title_text="kWh", row=1, col=2
).show()
