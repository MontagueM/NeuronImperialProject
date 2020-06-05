import neuron_efficient as neuron
import matplotlib.pyplot as plt
import numpy as np
import random
import sys

# remember the scale is 10x so need to run for 10x this amount and shrink values
RUNTIME_MS = 4000
TOTAL_NEURON_COUNT = 6000
PERCENT_CONNECTED_NEURONS_PER = 10
EXCITATORY_PROBABILITY = 0.8
# CHECK IF THIS PROB IS ACTUALLY BEING USED
# FIGURE OUT HOW TO CORRECT THE DATA BEING WRONG

neurons = []
data = []
activity_data = []
stored_voltages = []
stored_timestamps = []
stored_timestamps2 = []


def get_stored_data():
    global stored_timestamps
    global stored_voltages
    global stored_timestamps2
    test_neuron = neuron.Neuron(-1)
    dat, _, stored_timestamps2 = test_neuron.get_data_behind()
    stored_timestamps = dat[0][0]
    stored_voltages = dat[0][1]


def calculate_activity():
    global data
    return len(data) / (TOTAL_NEURON_COUNT * RUNTIME_MS)


def run_model():
    global data
    global activity_data
    # This populates the neuron array with all the connections it needs
    for i in range(TOTAL_NEURON_COUNT):
        neurons.append(neuron.Neuron(TOTAL_NEURON_COUNT - i))

    for i in range(TOTAL_NEURON_COUNT):
        n = neurons[i]
        forward_connections = {}
        # We don't want to connect to ourselves
        neurons_wo = list(neurons)
        neurons_wo.remove(n)
        for choice in random.choices(neurons_wo, k=round(len(neurons_wo) * PERCENT_CONNECTED_NEURONS_PER/100)):
            if random.random() < EXCITATORY_PROBABILITY:
                connection_type = neuron.NeuronType.EXCITATORY
            else:
                connection_type = neuron.NeuronType.INHIBITORY
            forward_connections[choice] = connection_type
        n.forward_connections = forward_connections

    data_add, activity_data_add = neurons[0].send_data_forward(stored_data=[stored_timestamps, stored_voltages,
                                                                            stored_timestamps2])
    data += data_add
    activity_data += activity_data_add


if __name__ == '__main__':
    sys.setrecursionlimit(1000000)
    get_stored_data()
    run_model()
    print(f"Activity count: {calculate_activity()}")
    # fix the x here to add up
    activity_set = list(set(activity_data))
    activity_y = [0]*len(activity_set)
    for i, d in enumerate(activity_data):
        activity_y[activity_set.index(d)] += 1
    activity_set, activity_y = zip(*sorted(zip(activity_set, activity_y)))
    print(activity_set, activity_y)
    with open('activity.txt', 'a') as f:
        f.write(f"{activity_set}\n{activity_y}\nRUNTIME_MS {RUNTIME_MS} TOTCOUNT {TOTAL_NEURON_COUNT} EXCITE_PROB {EXCITATORY_PROBABILITY} ACTIVITY {calculate_activity()}\n\n")
    plt.plot([x/10 for x in activity_set], activity_y)
    plt.xlabel("Time [ms]")
    plt.ylabel("Count per unit time")
    plt.show()
