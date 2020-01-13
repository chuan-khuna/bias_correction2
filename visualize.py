import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
color_palette = sns.color_palette("muted")
sns.set_palette(color_palette)
sns.set_style("whitegrid")
sns.set_context("paper",
                font_scale=1.10,
                rc={
                    "lines.linewidth": 1.5,
                    'markers.linewidth': 0.25,
                    'figure.figsize': (8, 4.5),
                    'figure.dpi': 150
                })


def qqplot(observed, model, num_points=50):
    qth = np.linspace(0, 100, num_points+1)
    obs_quartile = np.percentile(observed, qth)
    mod_quartile = np.percentile(model, qth)
    sns.scatterplot(obs_quartile, mod_quartile)
