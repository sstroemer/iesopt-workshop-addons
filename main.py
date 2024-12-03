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
    energy_bought = sum(model.results.components["energy_supplier"].exp.value) / 1e3
    print(f"{opt}")
    print(f"      ╰──>  {model.objective_value:.1f} EUR      {discharging:.1f} kWh  |  (buy: {energy_bought:.1f} MWh)\n")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BEFORE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# {'battery_power': 5, 'battery_hours': 2}
#       ╰──>  2746.0 EUR  |  1322.2 kWh  |  (buy: 17.30 MWh)

# {'battery_power': 10, 'battery_hours': 1}
#       ╰──>  2746.0 EUR  |  1322.2 kWh  |  (buy: 17.30 MWh)

# {'battery_power': 1, 'battery_hours': 10}
#       ╰──>  2751.1 EUR  |  1106.1 kWh  |  (buy: 17.49 MWh)

# {'battery_power': 2, 'battery_hours': 5}
#       ╰──>  2746.1 EUR  |  1317.7 kWh  |  (buy: 17.30 MWh)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# NOW
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# {'battery_power': 5, 'battery_hours': 2}
#       ╰──>  2745.9 EUR      1319.3 kWh  |  (buy: 17.3 MWh)

# {'battery_power': 10, 'battery_hours': 1}
#       ╰──>  2745.9 EUR      1319.3 kWh  |  (buy: 17.3 MWh)

# {'battery_power': 1, 'battery_hours': 10}
#       ╰──>  2751.0 EUR      1105.7 kWh  |  (buy: 17.5 MWh)

# {'battery_power': 2, 'battery_hours': 5}
#       ╰──>  2746.0 EUR      1314.9 kWh  |  (buy: 17.3 MWh)
