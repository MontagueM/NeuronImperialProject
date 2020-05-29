import neuron
import matplotlib.pyplot as plt

neurons = []
data = []
number_of_neurons = 3

for i in range(number_of_neurons):
    if len(neurons) != 0:
        neurons.append(neuron.Neuron([neurons[-1]]))
        continue
    neurons.append(neuron.Neuron([]))  # if its the first one then we want it to have no link

neurons = neurons[::-1]

for n in neurons:
    run1, timestamps1 = n.run(50, 0)
    run2, timestamps2 = n.run(3, 1)
    run3, timestamps3 = n.run(50, 0)
    data.append([[timestamps1 + timestamps2 + timestamps3, run1 + run2 + run3]])
    data.append(n.send_voltage_forward())

#print(data)

for d in data:
    print(d)
    if not d:  # We've reached the end
        break
    d = d[0]
    time_points, volt_array = neuron.remove_duplicates(d[0], d[1])
    plt.plot(time_points, volt_array)
plt.show()