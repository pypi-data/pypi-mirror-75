
import numpy as np
import matplotlib.pyplot as plt


def show_weight(pre_ids, post_ids, weights, geometry, neu_id):
    height, width = geometry
    ids = np.where(pre_ids == neu_id)[0]
    post_ids = post_ids[ids]
    weights = weights[ids]

    X, Y = np.arange(height), np.arange(width)
    X, Y = np.meshgrid(X, Y)
    Z = np.zeros(geometry)
    for id_, weight in zip(post_ids, weights):
        h, w = id_ // width, id_ % width
        Z[h, w] = weight

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.coolwarm, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


import npbrain as nn
# pre_ids, post_ids, anchors, weights = nn.connect.gaussian_weight(
#         (30, 30), (30, 30), sigma=0.1, w_max=1., w_min=0.,
#         normalize=True, include_self=True)
# show_weight(pre_ids, post_ids, weights, (30, 30), 465)

h = 40
pre_ids, post_ids, anchors, weights = nn.connect.dog(
        (h, h), (h, h), sigmas=[0.08, 0.15], ws_max=[1.0, 0.7], w_min=0.01,
        normalize=True, include_self=True)
show_weight(pre_ids, post_ids, weights, (h, h), h * h // 2 + h // 2)
