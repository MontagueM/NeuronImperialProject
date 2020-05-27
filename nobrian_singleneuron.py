import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.special import exprel


def f_betah(v):
    return 1 / (np.exp((-v + 30) / 10) + 1)


def f_alphan(v):
    return 0.01 * 10 / exprel((-v + 10) / 10)


def f_alpham(v):
    return 0.1 * 10 / exprel((-v + 25) / 10)


def f_alphah(v):
    return 0.07 * np.exp(-v / 20)


def f_betan(v):
    return 0.125 * np.exp(-v / 80)


def f_betam(v):
    return 4 * np.exp(-v / 18)


def plot_graph(time_points, array):
    plt.plot(time_points, array, 'b', linewidth=1.5)
    plt.xlabel('Time (ms)')
    plt.ylabel('Action potential (mV)')
    plt.show()


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
    EL = 10.613
    ENa = 115
    EK = -12
    gL = 0.3
    gNa = 120
    gK = 36

    # Initial conditions
    v = 0
    h = 1
    m = 0
    n = .5
    C = 1e-6
    R = 35.4
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
        The main function we are integrating over with odeint. odeint solvs the four FODEs below, solving them
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
        dvdt = (1/self.C) * (self.I + self.gK * self.n**4 * (self.EK-self.v) + self.gNa * self.m**3 * self.h * (self.ENa-self.v) + self.gL * (self.EL-self.v))

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
        new_start_time = int(np.floor(self.timestamps[-1]))
        time_region = np.linspace(new_start_time, new_start_time + time_length, 1000).tolist()

        # Initialising the recording system
        self.voltages = [self.v]
        self.timestamps = [time_region[0]] # Defining where we want to start with our timestamps

        self.I = current_start

        # The actual differential equation solving
        odeint(self.f, [self.n, self.m, self.h, self.v], time_region)

        return self.voltages, self.timestamps


neuron = Neuron()

run1, timestamps1 = neuron.run(50, 0)
run2, timestamps2 = neuron.run(3, 1)
run3, timestamps3 = neuron.run(50, 0)

plot_graph(timestamps1 + timestamps2 + timestamps3, [x - 70 for x in run1 + run2 + run3])
