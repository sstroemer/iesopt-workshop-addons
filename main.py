import iesopt
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


options = [
    dict(battery_power=5, battery_hours=2),
    dict(battery_power=10, battery_hours=1),
    dict(battery_power=1, battery_hours=10),
    dict(battery_power=2, battery_hours=5),
]

for opt in options:
    model = iesopt.run("battery.iesopt.yaml", parameters=opt, skip_validation=True)
    discharging = sum(model.results.components["battery.discharging"].var.flow)
    print(f"{opt}")
    print(f"      ╰──>  {model.objective_value:.1f} EUR  |  {discharging:.1f} kWh\n")
