import tensorflow_hub as hub
import tensorflow.compat.v1 as tf
import matplotlib.pyplot as plt
import numpy as np
import os

tf.disable_v2_behavior()


def heatmap(x_labels, y_labels, values):
    fig, ax = plt.subplots()
    im = ax.imshow(values)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(
        ax.get_xticklabels(),
        rotation=45,
        ha="right",
        fontsize=10,
        rotation_mode="anchor",
    )

    # Loop over data dimensions and create text annotations.
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            text = ax.text(
                j,
                i,
                "%.2f" % values[i, j],
                ha="center",
                va="center",
                color="w",
                fontsize=6,
            )

    fig.tight_layout()
    plt.show()





getSimilarityScore(
    ["he's energy conscious", "he's energy-conscious",]
)

