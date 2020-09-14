import matplotlib.pyplot as plt
import numpy as np

filename = './lossFile/multiLan.txt'
f = open(filename, 'r')

losses = []
for line in f:
    losses.append(float(line.strip()))

x = np.arange(1, len(losses)+1)

plt.plot(x, losses, 'b--')
plt.xlabel('epoch')
plt.ylabel('loss')

plt.show()