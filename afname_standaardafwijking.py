import numpy as np
import matplotlib.pyplot as plt

x = np.array([34.99, 39.99, 50.02, 54.99, 60.02, 70.01])
y = np.array([2.257e+04, 2.080e+04, 2.028e+04, 1.680e+04, 1.580e+04, 1.543e+04])

# lineare fit
a, b = np.polyfit(x, y, 1)

plt.plot(x, y, 'o')
plt.plot(x, a * x + b, 'r-')
plt.xlabel('Stroomsterkte (mA)')
plt.ylabel('Standaardafwijking (AU)')
plt.ylim(14000, 23000)
plt.xlim(30, 75)
plt.grid(True)
plt.show()
