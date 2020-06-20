"""
This file can be used to directly call any model you want with specific parameters.
To make this work, need to convert the map model into an OOP so that we can view multiple models at the same time
on the same graph to compare them.
"""
import map_connections_model_numerical as map_model_numerical
import matplotlib.pyplot as plt
import numpy as np

models = []

# Ideally would make a class called Layer that would handle all this stuff for me right?

# Source Neuronal Dynamics Wolfram

# Eg: '2': 0.1 = there are 0.1 * len(all neurons in layer) connections from 2 -> 2
# Eg: '2->5a': 0.15 = there are 0.15 * len(all neurons in layer) connections from 2 -> 5a
layer_fixed_conn_probs = {'1->1': 0.05,
                       '2->2': 0.10, '2->3': 0.05, '2->5a': 0.15, '2->5b': 0.10,
                       '3->3': 0.2, '3->2': 0.2, '3->5a': 0.05, '3->5b': 0.15,
                       '4->4': 0.25, '4->2': 0.15, '4->3': 0.15, '4->5a': 0.15, '4->5b': 0.10, '4->6': 0.05,
                       '5a->5a': 0.2, '5a->2': 0.05, '5a->5b': 0.10, '5a->6': 0.05,
                       '5b->5b': 0.10, '5b->6': 0.10,
                       '6->6': 0.025}  # 1, 6 are actually < 0.05

# Multiply each layer count by some random number between eg 0.9 and 1.1
layer_neuron_count = {'1': 26, '2': 653, '3': 1268, '4': 1796, '5a': 544, '5b': 772, '6': 1450}

# Probs from this layer?
layer_excitatory_probs = {'1': 0, '2': 0.80, '3': 0.89, '4': 0.92, '5a': 0.80, '5b': 0.80, '6': 0.90}
# Excitatory probability is prob that any neuron connection may be excitatory in nature
map1 = map_model_numerical.MapModel(runtime_ms=200, layer_neuron_count=layer_neuron_count,
                                    layer_fixed_conn_probs=layer_fixed_conn_probs,
                                    layer_excitatory_probs=layer_excitatory_probs,
                                    layers=list(layer_neuron_count.keys()))
# map2 = map_model.MapModel(runtime_ms=5000, total_neuron_count=10000, fixed_connectivity_probability=0.1,
#                           excitatory_probability=0.8)
models.append(map1)
# models.append(map2)

for m in models:
    x, y = m.run_model()
    print(len(x))
    plt.plot([a * 1 for a in x], [b / 60 for b in y],
             label=f"RUNTIME_MS {m.runtime_ms}",
             linewidth=0.5, color='k')
    plt.xlabel("Time [ms]")
    plt.ylabel("Activity [Hz]")
    plt.legend()
    plt.show()
#plt.show()


# with open('activity.txt', 'r') as f:
#     f = f.readlines()
#     x = [float(a) for a in f[-3][1:-2].split(",")]
#     y = [float(a) for a in f[-2][1:-2].split(",")]
#     plt.plot([a * 1 for a in x], [b / 60 for b in y], linewidth=0.5, color='k')
#     plt.xlim(0, 400)
#     plt.xlabel("Time [ms]")
#     plt.ylabel(""A [Hz]"")
#
#     plt.show()
