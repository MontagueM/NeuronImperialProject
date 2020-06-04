import neuron
import matplotlib.pyplot as plt
import numpy as np
import random

neurons = []
data = []
number_of_neurons = 3

# This populates the neuron array with all the connections it needs
for i in range(number_of_neurons):
    if len(neurons) != 0:
        neurons.append(neuron.Neuron([neurons[-1]], number_of_neurons-i, neuron.NeuronType.INHIBITORY))
        continue
    neurons.append(neuron.Neuron([], number_of_neurons-i, neuron.NeuronType.EXCITATORY))  # if its the first one then we want it to have no link
neurons = neurons[::-1]  # Reversing the array as we want to end with no connections

# Looping through all the neurons to begin the propagation signal
data += neurons[0].get_data_behind()
# Propagating to connecting neuron
rand = random.random()
if rand < neurons[0].neuron_type.value:
    data += neurons[0].send_data_forward()
# Graph plotting
for d in data:
    if not d:  # We've reached the end of the neuron chain as no more chain data
        break
    # Removing duplicates
    time_points = d[0]
    volt_array = d[1]
    number_identifier = d[2]
    #time_points, volt_array = neuron.remove_duplicates(time_points, volt_array)

    plt.plot([x/10 for x in time_points], volt_array, label=f"Neuron {number_identifier}") # x/10 to make the timings more realistic
plt.legend()
plt.xlabel('Time (ms)')
plt.ylabel('Action potential (mV)')
plt.show()
