import neuron_efficient as neuron
import matplotlib.pyplot as plt
import numpy as np
import random

RUNTIME_MS = 4000
TOTAL_NEURON_COUNT = 6000
PERCENT_CONNECTED_NEURONS_PER = 10
EXCITATORY_PROBABILITY = 0.8

# Array of all our neurons in the model
neurons = []
# All the activity calls to show the activity graph
activity_data = []
# All our stored data. We use this to not have to keep running the simulation every call and instead rely on this data
# to help with the model.
stored_timestamps = []
# Timestamps2 is specifically important for how we track when a spike has occurred.
stored_timestamps2 = []


def get_stored_data():
    """ Gets all the stored data we need at the beginning of the model simulation """
    global stored_timestamps
    global stored_timestamps2
    test_neuron = neuron.Neuron(-1)
    dat, _, stored_timestamps2 = test_neuron.get_data_behind()
    # The data from our neuron calculations are 10x the usual scale in order to improve accuracy so need to downscale
    stored_timestamps = [x/10 for x in dat[0][0]]


def run_model():
    """ This code makes every neuron, assigns all connections, and starts signal propagation. """
    global activity_data

    # Appends the neuron array with all the connections it needs
    populate_neurons()

    # Gives each neuron the connections given the constants provided
    for i in range(TOTAL_NEURON_COUNT):
        n = neurons[i]
        populate_neuron_connections(n)

    # Starts the propagation
    activity_data_add = neurons[0].send_data_forward(stored_data=[stored_timestamps, stored_timestamps2])
    activity_data += activity_data_add


def populate_neurons():
    """ Appends the neuron array with all the connections it needs """
    for i in range(TOTAL_NEURON_COUNT):
        neurons.append(neuron.Neuron(TOTAL_NEURON_COUNT - i))


def populate_neuron_connections(n):
    """
    Gives each neuron the connections given the constants provided
    :param n: the neuron to add the connections to
    """
    forward_connections = {}
    # We don't want to connect to ourselves
    neurons_wo = list(neurons)
    neurons_wo.remove(n)

    # We want to choose a random selection of k neurons, where k is eg 10% of all neurons
    for connection in random.choices(neurons_wo, k=round(len(neurons) * PERCENT_CONNECTED_NEURONS_PER / 100)):
        # There is an 80% chance that each connection is excitatory, 20% inhibitory
        if random.random() < EXCITATORY_PROBABILITY:
            connection_type = neuron.NeuronType.EXCITATORY
        else:
            connection_type = neuron.NeuronType.INHIBITORY
        # Setting the connection type for each connection
        forward_connections[connection] = connection_type
    # Setting the forward connections of each neuron
    n.forward_connections = forward_connections


if __name__ == '__main__':
    get_stored_data()

    # Running our model for RUNTIME_MS ms
    run_model()

    # Counting the number of times spikes occur for a unit of time
    activity_set = list(set(activity_data))
    activity_y = [0]*len(activity_set)
    for i, d in enumerate(activity_data):
        activity_y[activity_set.index(d)] += 1

    # We need to sort the data by timestamp for a line plot to look correct
    activity_set, activity_y = zip(*sorted(zip(activity_set, activity_y)))

    # Writing the data for permanent storage
    with open('activity.txt', 'a') as f:
        f.write(f"{activity_set}\n{activity_y}\nRUNTIME_MS {RUNTIME_MS} TOTAL_NEURON_COUNT {TOTAL_NEURON_COUNT} EXCITE_PROB {EXCITATORY_PROBABILITY}\n\n")

    # Plotting the data
    plt.plot([x*10 for x in activity_set], activity_y, label=f"RUNTIME_MS {RUNTIME_MS} TOTAL_NEURON_COUNT {TOTAL_NEURON_COUNT} EXCITE_PROB {EXCITATORY_PROBABILITY}")
    plt.xlabel("Time [ms]")
    plt.ylabel("Count per unit time")
    plt.legend()
    plt.show()
