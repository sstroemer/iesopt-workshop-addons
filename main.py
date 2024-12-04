import iesopt
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


model = iesopt.run(
    "heat.iesopt.yaml",
    parameters=dict(hp_pnom=4.0, upgrade_cost=1000.0),
    skip_validation=True,
)

# => see "heat_temp.html"

# Heatmap: Opt. TEMP based on PNOM and COST.

# results = []
# pnoms = np.concatenate(
#     [
#         np.arange(2.15, 2.65, 0.0625),
#         np.arange(2.65, 3.15, 0.125),
#         np.arange(3.15, 4.65, 0.25),
#         np.arange(4.65, 7.16, 0.5),
#     ]
# )
# for pnom in pnoms:
#     for cost in np.concatenate([np.arange(0, 1500, 125), np.arange(1500, 5001, 500)]):
#         model = iesopt.run(
#             "heat.iesopt.yaml",
#             parameters=dict(hp_pnom=pnom, upgrade_cost=cost),
#             skip_validation=True,
#         )
#         temp = iesopt.jump_value(model.get_component("heating").temperature.var.value)
#         results.append((pnom, cost, temp))
#         print(".", end="", flush=True)
# print()

# go.Figure(
#     data=go.Heatmap(
#         z=[float(it[2]) for it in results],
#         x=[float(it[0]) for it in results],
#         y=[float(it[1]) for it in results],
#         colorscale="Viridis",
#     )
# ).update_layout(
#     title="Optimal Temperature",
#     xaxis_title="Heatpump Power",
#     yaxis_title="Upgrade Cost",
# ).write_html("heat_temp.html")
