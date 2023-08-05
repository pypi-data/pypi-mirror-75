# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.1
#   kernelspec:
#     display_name: py37
#     language: python
#     name: py37
# ---

# # Usage if `input_factory` module

# +

import sys

sys.path.append('../../')

import npbrain as nn
import matplotlib.pyplot as plt
# -

nn.utils

# ## `constant_current()`

# +
fig, gs = nn.visualize.get_figure(2, 1)

current, duration = nn.input_factory.spike_current([(0, 100), (1, 300), (0, 100)], 0.1)
ts = np.arange(0, duration, 0.1)
fig.add_subplot(gs[0, 0])
plt.plot(ts, current)
plt.title('[(0, 100), (1, 300), (0, 100)]')

current, duration = nn.input_factory.spike_current([(-1, 10), (1, 3), (3, 30), (-0.5, 10)], 0.1)
ts = np.arange(0, duration, 0.1)
fig.add_subplot(gs[1, 0])
plt.plot(ts, current)
plt.title('[(-1, 10), (1, 3), (3, 30), (-0.5, 10)]')

plt.show()
# -


