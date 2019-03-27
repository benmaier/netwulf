import matplotlib.pyplot as pl
import json
from netwulf import draw_netwulf

with open('BA_network_properties.json', 'r') as f:
    props = json.load(f)

fig, ax = draw_netwulf(props)
pl.show()
