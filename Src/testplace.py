import matplotlib.pyplot as plt
import numpy as np

# Dane do wykresu słupkowego
values = [5, 10, 8, 6, 7]
colors = ['blue', 'blue', 'blue', 'blue', 'blue']  # Wybierz kolor dla każdego słupka

# Tworzenie wykresu słupkowego z różnymi odcieniami koloru
plt.figure(figsize=(8, 6))

for i, value in enumerate(values):
    plt.bar(i, value, color=colors[i], alpha=0.7)  # Ustawienie koloru dla każdego słupka

plt.xlabel('Kategorie')
plt.ylabel('Wartości')
plt.title('Wykres słupkowy z różnymi odcieniami kolorów')
plt.xticks(np.arange(len(values)), ['A', 'B', 'C', 'D', 'E'])  # Etykiety na osi X
plt.show()
