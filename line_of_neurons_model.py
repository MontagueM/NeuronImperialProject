import neuron
import matplotlib.pyplot as plt

neurons = []
data = []
number_of_neurons = 3

# This populates the neuron array with all the connections it needs
for i in range(number_of_neurons):
    if len(neurons) != 0:
        neurons.append(neuron.Neuron([neurons[-1]]))
        continue
    neurons.append(neuron.Neuron([]))  # if its the first one then we want it to have no link
neurons = neurons[::-1]  # Reversing the array as we want to end with no connections

# Looping through all the neurons to begin the propagation signal
for n in neurons:
    # (temp) we need this to get the first one to run
    if neurons.index(n) == 0:
        # Basic action potential logic
        run1, timestamps1 = n.run(50, 0)
        run2, timestamps2 = n.run(3, 1)
        run3, timestamps3 = n.run(50, 0)
        data.append([[timestamps1 + timestamps2 + timestamps3, run1 + run2 + run3]])

    # Propagating to connecting neuron
    data.append(n.send_data_forward())

# Graph plotting
for d in data:
    if not d:  # We've reached the end
        break
    d = d[0]
    # Removing duplicates
    time_points, volt_array = neuron.remove_duplicates(d[0], d[1])
    plt.plot(time_points, volt_array)
plt.xlabel('Time (ms)')
plt.ylabel('Action potential (mV)')
plt.show()