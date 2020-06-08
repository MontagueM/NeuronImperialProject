import neuron_efficient as neuron
import neuron as neuron_original
import matplotlib.pyplot as plt
import random


class MapModel:
    # Array of all our neurons in the model
    neurons = []
    # All the activity calls to show the activity graph
    activity_data = []
    # All stored data. We use this to not have to keep running the simulation every call and instead rely on this data
    # to help with the model.
    stored_timestamps = []

    def __init__(self, runtime_ms, total_neuron_count, fixed_connectivity_probability, excitatory_probability):
        self.runtime_ms = runtime_ms
        self.total_neuron_count = total_neuron_count
        self.fixed_connectivity_probability = fixed_connectivity_probability
        self.excitatory_probability = excitatory_probability

    def get_stored_data(self):
        """ Gets all the stored data we need at the beginning of the model simulation """
        test_neuron = neuron_original.Neuron(-1)
        data = test_neuron.get_data_behind()
        # The data from our neuron calculations are 10x the usual scale in order to improve accuracy, need to downscale
        self.stored_timestamps = [x / 10 for x in data]

    def populate_neurons(self):
        """ Appends the neuron array with all the connections it needs """
        for i in range(self.total_neuron_count):
            self.neurons.append(neuron.Neuron(self.total_neuron_count - i))

    def populate_neuron_connections(self, n):
        """
        Gives each neuron the connections given the constants provided
        :param n: the neuron to add the connections to
        """
        forward_connections = {}
        # We don't want to connect to ourselves
        neurons_wo = list(self.neurons)
        neurons_wo.remove(n)

        # We want to choose a random selection of k neurons, where k is eg 10% of all neurons
        for connection in random.choices(neurons_wo, k=round(len(self.neurons) * self.fixed_connectivity_probability)):
            # There is an 80% chance that each connection is excitatory, 20% inhibitory
            if random.random() < self.excitatory_probability:
                connection_type = neuron.NeuronType.EXCITATORY
            else:
                connection_type = neuron.NeuronType.INHIBITORY
            # Setting the connection type for each connection
            forward_connections[connection] = connection_type
        # Setting the forward connections of each neuron
        n.forward_connections = forward_connections

    def propagate(self):
        """ This code makes every neuron, assigns all connections, and starts signal propagation. """
        # Appends the neuron array with all the connections it needs
        self.populate_neurons()

        # Gives each neuron the connections given the constants provided
        for i in range(self.total_neuron_count):
            n = self.neurons[i]
            self.populate_neuron_connections(n)

        # Starts the propagation
        activity_data_add = self.neurons[0].send_data_forward(runtime_ms=self.runtime_ms,
                                                              stored_data=self.stored_timestamps)
        self.activity_data += activity_data_add

    def run_model(self):
        self.get_stored_data()

        # Running our model for RUNTIME_MS ms
        self.propagate()

        activity_set, activity_y = self.get_activity_axes()

        return activity_set, activity_y
        #self.write_data(activity_set, activity_y)
        #self.plot_activity_graph(activity_set, activity_y)

    def get_activity_axes(self):
        # Counting the number of times spikes occur for a unit of time
        activity_set = list(set(self.activity_data))
        activity_y = [0] * len(activity_set)
        for i, d in enumerate(self.activity_data):
            activity_y[activity_set.index(d)] += 1

        # We need to sort the data by timestamp for a line plot to look correct
        return zip(*sorted(zip(activity_set, activity_y)))

    def write_data(self, activity_set, activity_y):
        # Writing the data for permanent storage
        with open('activity.txt', 'a') as f:
            f.write(
                f"\n\n{activity_set}\n{activity_y}\nRUNTIME_MS {self.runtime_ms} TOTAL_NEURON_COUNT {self.total_neuron_count} EXCITE_PROB {self.excitatory_probability}")

    def plot_activity_graph(self, x, y):
        # Plotting the data
        plt.plot([x * 1 for x in x], y,
                 label=f"RUNTIME_MS {self.runtime_ms} TOTAL_NEURON_COUNT {self.total_neuron_count} EXCITE_PROB {self.excitatory_probability}")
        plt.xlabel("Time [ms]")
        plt.ylabel("Count per unit time")
        plt.legend()