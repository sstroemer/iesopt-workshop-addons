import iesopt
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


model = iesopt.Model("battery.iesopt.yaml", skip_validation=True)
model.generate()

model.get_component("battery").var.useable_capacity
