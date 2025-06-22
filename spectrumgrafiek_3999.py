import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.ticker as ticker

x_all = []
y_all = []

with open("current3999.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        try:
            x_val = float(row[0])
            y_val = float(row[1])
            x_all.append(x_val)
            y_all.append(y_val)
        except:
            continue

sorted_indices = np.argsort(y_all)
second_min_index = sorted_indices[1]
x_minimum = x_all[second_min_index]

delta = 0.1e6
x_fit = []
y_fit = []

for x_val, y_val in zip(x_all, y_all):
    if x_minimum - delta <= x_val <= x_minimum + delta:
        x_fit.append(x_val)
        y_fit.append(y_val)

x_fit = np.array(x_fit)
y_fit = np.array(y_fit)

y_fit_norm = (y_fit - np.min(y_fit)) / (np.max(y_fit) - np.min(y_fit))
intensity_rel = 1 - y_fit_norm

def gaussian(x, a, mu, sigma, c):
    return a * np.exp(-(x - mu)**2 / (2 * sigma**2)) + c

a_guess = max(intensity_rel) - min(intensity_rel)
mu_guess = x_minimum
sigma_guess = 0.05e6
c_guess = min(intensity_rel)
p0 = [a_guess, mu_guess, sigma_guess, c_guess]

params, _ = curve_fit(gaussian, x_fit, intensity_rel, p0=p0)
a_fit, mu_fit, sigma_fit, c_fit = params

plt.plot(x_fit, intensity_rel, label="Relatieve intensiteit (genormaliseerd)")
plt.plot(x_fit, gaussian(x_fit, *params), color='red', linewidth=2, label="Gaussische fit")

plt.xlabel("plaats op de CCD (AU)")
plt.ylabel("Relatieve intensiteit (AU)")
plt.ylim(0.0, 1.0)
plt.title("Laserspectrum bij 39.99 mA")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


params, cov = curve_fit(gaussian, x_fit, intensity_rel, p0=p0)
a_fit, mu_fit, sigma_fit, c_fit = params

sigma_error = np.sqrt(cov[2, 2])
print(f"Standaardafwijking = {sigma_fit:.3e} ± {sigma_error:.3e} AU")