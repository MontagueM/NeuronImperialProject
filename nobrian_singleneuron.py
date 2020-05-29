import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.special import exprel


#####################################################################

# Definitions of the required variables with respect to voltage. Numbers taken from paper below.
# https://neuronaldynamics.epfl.ch/online/Ch2.S2.html


def f_alphan(v):
    return 0.01 * (v + 55) / (1 - (np.exp(-(v + 55) / 10)))


def f_betan(v):
    return 0.125 * np.exp(-(v + 65) / 80)


def f_alpham(v):
    return 0.1 * (v + 40) / (1 - (np.exp(-(v + 40) / 10)))


def f_betam(v):
    return 4 * np.exp(-(v + 65) / 18)


def f_alphah(v):
    return 0.07 * np.exp(-(v + 65) / 20)


def f_betah(v):
    return 1 / (1 + np.exp(-(v + 35) / 10))

#####################################################################

# Dealing with plotting the neuron


def remove_duplicates(time_points, array):
    """
    Since the algorithm produces duplicate results for some of the data, this removes duplicates for speed of computation
    (in case a higher complexity calculation must be done) and visual appeal on a graph.

    :return: the arrays with zero duplicates
    """
    print("Removing duplicates")

    # removed duplicates
    rd_time_points = []
    rd_array = []

    num = 0
    for i in range(len(time_points)):
        if time_points[i] not in rd_time_points:
            rd_time_points.append(time_points[i])
            rd_array.append(array[i])
        else:
            num += 1

    print(f"Removed {num} duplicates")
    return rd_time_points, rd_array


def plot_graph(time_points, array):
    """
    Plots the graph of the given data for an single neuron.

    :param time_points: the time points to plot along x-axis
    :param array: voltage array to plot along y-axis
    """
    # Removes any duplicates we have generated in the sample to provide a clearer-looking graph
    time_points, array = remove_duplicates(time_points, array)

    # Fix overlaps in graph? could just delete overlapping ones (using set)
    plt.plot(time_points, array, 'b', linewidth=1)
    plt.xlabel('Time (ms)')
    plt.ylabel('Action potential (mV)')
    #plt.yticks(np.arange(-80, 35, 5))
    plt.show()

#####################################################################


class Neuron:
    """
    A class to represent a single neuron.

    ...

    Attributes
    ----------

    Methods
    -------
    f(init, t):
        Stores the equations necessary for solving the differential equations, as well as recording the data
        for graphs.

    run(time_length, current_start):
        Runs the differential equation solver over a specified time period in ms with a specified constant current.
    """
    # Our constants for the diff. equations
    EL = -54.4
    ENa = 50
    EK = -70
    gL = 0.3
    gNa = 120
    gK = 36

    # Initial conditions
    v = -65
    h = 0
    m = 0
    n = 0.5
    C = 1e-6
    #R = 35.4
    voltages = []
    timestamps = [0]
    I = 0

    def __init__(self):
        """
        The neuron specifics will be put here. For example:
         - different threshold limits
         - excitatory vs inhibitory
         - numerical identifications
         - groups
         - etc
        """

    def f(self, init, t):
        """
        The main function we are integrating over with odeint. odeint solvs the four DEs below, solving them
        and then those results being used for the next solutions (n, m, h, v)

        :param init: an array of the four initial conditions for n, m, h, and v
        :param t: the time instant this solution is being made for
        :return: the four functions odeint will solve
        """
        self.n = init[0]
        self.m = init[1]
        self.h = init[2]
        self.v = init[3]

        # The differential equations that will be solved
        dndt = f_alphan(self.v) * (1 - self.n) - f_betan(self.v) * self.n
        dmdt = f_alpham(self.v) * (1 - self.m) - f_betam(self.v) * self.m
        dhdt = f_alphah(self.v) * (1 - self.h) - f_betah(self.v) * self.h
        dvdt = (1/self.C) * (self.I + self.gK * self.n**4 * (self.EK-self.v) +
                             self.gNa * self.m**3 * self.h * (self.ENa-self.v) + self.gL * (self.EL-self.v))

        # Recording the data the sim has calculated (could do directly but seems to be messy)
        self.voltages.append(self.v)
        self.timestamps.append(t)

        return [dndt, dmdt, dhdt, dvdt]

    def run(self, time_length, current_start):
        """
        Runs the differential equation solver over a specified time period in ms with a specified constant current.

        :param time_length: the length of time to run the simulation for
        :param current_start: the current the simulation will run with over the time period
        :return: two arrays of voltages and timestamps as calculated by the simulation
        """
        # We want each successive run() to start from the last simulation timestamp so it looks continuous.
        new_start_time = np.floor(self.timestamps[-1])

        # Temporary fix for misalignment
        if new_start_time == 50:
            new_start_time += 1

        time_region = np.linspace(new_start_time, new_start_time + time_length, 1000).tolist()

        # Initialising the recording system
        self.voltages = [self.v]
        self.timestamps = [time_region[0]]  # Defining where we want to start with our timestamps

        self.I = current_start

        # The actual differential equation solving
        odeint(self.f, [self.n, self.m, self.h, self.v], time_region)

        return self.voltages, self.timestamps


neuron = Neuron()

run1, timestamps1 = neuron.run(50, 0)
run2, timestamps2 = neuron.run(3, 1)
run3, timestamps3 = neuron.run(50, 0)

plot_graph(timestamps1 + timestamps2 + timestamps3, run1 + run2 + run3)
