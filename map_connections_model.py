import neuron
import matplotlib.pyplot as plt
import numpy as np
import random
import multiprocessing
import time


RUNTIME_MS = 200
TOTAL_NEURON_COUNT = 100
NUMBER_CONNECTED_NEURONS_PER = 10
EXCITATORY_PROBABILITY = 0.8

neurons = []
data = []


def calculate_activity():
    global data
    print(len(data))
    return len(data) / (TOTAL_NEURON_COUNT * RUNTIME_MS)


def run_model():
    global data
    # This populates the neuron array with all the connections it needs
    for i in range(TOTAL_NEURON_COUNT):
        neurons.append(neuron.Neuron(TOTAL_NEURON_COUNT - i))

    for i in range(TOTAL_NEURON_COUNT):
        n = neurons[i]
        forward_connections = {}
        # We don't want to connect to ourselves
        neurons_wo = list(neurons)
        neurons_wo.remove(n)
        for choice in random.choices(neurons_wo, k=NUMBER_CONNECTED_NEURONS_PER):
            if random.random() < EXCITATORY_PROBABILITY:
                connection_type = neuron.NeuronType.EXCITATORY
            else:
                connection_type = neuron.NeuronType.INHIBITORY
            forward_connections[choice] = connection_type
        n.forward_connections = forward_connections

    data += neurons[0].send_data_forward()


if __name__ == '__main__':
    run_model()
    print(f"Activity count: {calculate_activity()}")
