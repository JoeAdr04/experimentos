import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

k_observed = np.array([0, 1, 3, 6, 10])
frequencies_observed = np.array([12, 68, 110, 143, 28])
probabilities_observed = frequencies_observed / np.sum(frequencies_observed)
mu_calculated = 4.2933

k_theoretical = np.arange(0, 15) 

probabilities_theoretical = poisson.pmf(k_theoretical, mu_calculated)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1) 
plt.bar(k_observed, probabilities_observed, color='lightcoral', width=0.8)
plt.xlabel('Frecuencia de Uso de IA por Semana (k)')
plt.ylabel('Proporción Observada')
plt.title('Distribución de Frecuencia Observada de Uso de IA')
plt.xticks(k_observed)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.subplot(1, 2, 2) 
plt.bar(k_theoretical, probabilities_theoretical, color='skyblue', width=0.8)
plt.xlabel('Número de Eventos (k)')
plt.ylabel('Probabilidad P(X=k)')
plt.title(f'Distribución Poisson Teórica ($\lambda$ = {mu_calculated:.2f})')
plt.xticks(k_theoretical)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout() 
plt.show()
