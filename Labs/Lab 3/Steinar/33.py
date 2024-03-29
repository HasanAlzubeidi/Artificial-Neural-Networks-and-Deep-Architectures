import numpy as np
from Hopfield_Network import Hopfield_Network
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

with open('../pict.dat') as f:
    line = str.split(f.readline(), ',')
    dataset = np.array(line, dtype=float)
    dataset = dataset.reshape((int(dataset.shape[0] / 1024), 1024))


first_three = dataset[0:3]

model = Hopfield_Network(1024, True)
model.fit_data(first_three)
print('energy', model.energy(dataset[10]))

converged, converged_data = model.recall(dataset[10], 200, True)
intermediate_results = model.get_intermediate_results()
energy_results = model.get_energy_results()

plt.plot(energy_results)
plt.xlabel('Iteration')
plt.ylabel('Energy')
plt.title('Energy of the network as a function of recall iteration')
plt.show()