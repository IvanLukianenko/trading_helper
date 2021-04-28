import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.facecolor'] = '#F0F0F0'
x = np.arange(0, 10, 0.1)
y = [2.71 ** x_ for x_ in x]
print(y)
plt.plot(x, y)
plt.title("Happiness")
plt.xlabel("Time")
plt.ylabel("Happiness")
plt.savefig("plots/Happiness_plot.png", dpi=80)