
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


time = np.arange(0,7,0.001)
valor = pd.read_csv('Output/female/1_glucose.csv')

plt.plot(time, valor)
plt.savefig("glucose7dias.png")