import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import math
import numpy as np
from sklearn.preprocessing import StandardScaler

df = pd.read_csv(r"../Data/muzyczka_z_gatunkami.csv")
df = df.dropna()
X = df.drop(columns=['Artist','Track','Album','Album_type','Duration_ms','Views',
                     'Likes','Stream'])

print(X)

X = X[X['Genre'].isin(['Hip-Hop','country','latin','Reggaeton','rock','rap','electronic','pop','rnb','indie'])].reset_index(drop=True)
# X = X[X['Genre'].isin(['Classical','electronic','rap'])].reset_index(drop=True)
print(X)

y_true = X['Genre']
X = X.drop(columns='Genre')

print(y_true)
print(y_true.unique())
print(X)

# Zamiana string na int
label_mapping = {label: idx for idx, label in enumerate(np.unique(y_true))}
print(label_mapping)
numeric_y_true = np.array([label_mapping[label] for label in y_true])
print(numeric_y_true)

# Skalowanie
scaler = StandardScaler()
col2scale = ['Tempo','Loudness','Key']
X[col2scale] = scaler.fit_transform(X[col2scale])
# print(X)

# Redukcja wymiarów
from sklearn.decomposition import PCA

pca = PCA(n_components= 2)
X_red = pca.fit_transform(X)
# print(X_red)

# Klasteryzacja K-means dla zredukowanych wymiarów
n = 5 # co n-ta próbka

y_true_n =y_true[::n] # co któraś próbka
X_red_n = X_red[::n] # co któraś próbka

# Wykres

plt.figure(figsize=(8, 6))

# Pętla po unikalnych wartościach w kolumnie 'gatunek'
for gatunek in np.unique(y_true_n):
    # Wybieranie danych dla danego gatunku
    data = X_red_n[y_true_n == gatunek]
    # Wyświetlanie danych na wykresie scatter
    plt.scatter(data[:, 0], data[:, 1], label=gatunek)  # Zakładając, że X_red_n ma dwie kolumny



plt.legend()
plt.xlabel('Główna składowa PCA X')
plt.ylabel('Główna składowa PCA Y')
# plt.title('Przykładowe próbki po redukcji wymiarów po gatunku')
plt.show()

from sklearn.cluster import KMeans
from matplotlib.colors import ListedColormap
kmeans = KMeans(n_clusters = len(y_true_n.unique()), n_init= 'auto')
kmeans.fit(X_red_n)
labels_kmeans = kmeans.labels_
print(labels_kmeans)
plt.scatter(X_red_n[:, 0], X_red_n[:, 1], c=labels_kmeans, cmap='viridis', marker='o')
plt.title('Klasteryzacja za pomocą K-means')
plt.xlabel('Pierwsza składowa główna (PCA)')
plt.ylabel('Druga składowa główna (PCA)')
plt.colorbar(label='Klaster')
plt.show()
# Ocena
from sklearn.metrics import adjusted_rand_score, silhouette_score
ari = adjusted_rand_score(y_true_n,labels_kmeans)
print(f"Adjusted Rand Index KMEANS (z redukcją): {ari}")

# from sklearn.metrics import confusion_matrix

# # Macierz dopasowania
# conf_matrix = confusion_matrix(y_true_n, labels)
# print(conf_matrix)
# # Obliczenie procentowego dopasowania próbek do ich klastrów
# percent_accuracy = np.sum(np.max(conf_matrix, axis=1)) / len(y_true_n) * 100
# print(f"Procentowe dopasowanie próbek do ich klastrów: {percent_accuracy:.2f}%")


# # Klasteryzacja K-means dla pełnych wymiarów
X_n = X.iloc[::n] # co któraś próbka
kmeans = KMeans(n_clusters = len(y_true_n.unique()), n_init= 'auto')
kmeans.fit(X_n)
labels_kmeans_bez = kmeans.labels_
ari = adjusted_rand_score(y_true_n,labels_kmeans_bez)
print(f"Adjusted Rand Index KMEANS (bez redukcji): {ari}")

# # Kohonen

# from minisom import MiniSom
# X_nKoh = np.array(X_red_n)
# som_grid_rows = 20 # Wiersze x Kolumny = 5 x sqr(LiczbaPróbek)
# som_grid_columns = 20
# input_len = X_nKoh.shape[1]
# sigma = 1.0
# lr = 0.5

# som = MiniSom(som_grid_rows,som_grid_columns,input_len,sigma,lr)
# som.random_weights_init(X_nKoh)

# epochs = 1000
# som.train_batch(X_nKoh,epochs, verbose=True)

# winner_coordinates = np.array([som.winner(x) for x in X_nKoh]).T

# mapped_clusters = winner_coordinates[0] * 3 // som_grid_rows + winner_coordinates[1]

# print(mapped_clusters)# cluster_index = np.ravel_multi_index(winner_coordinates, (1,3))

# # Plotowanie klastrów
# for c in range(3):
#     plt.scatter(X_nKoh[mapped_clusters == c, 0],
#                 X_nKoh[mapped_clusters == c, 1], label='cluster='+str(c), alpha=.7)

# # # Plotowanie centroidów
# # for centroid in som.get_weights():
# #     plt.scatter(centroid[:, 0], centroid[:, 1], marker='x',
# #                 s=80, linewidths=35, color='k', label='centroid')
# plt.legend()
# plt.show()






# clusters = np.array([som.winner(x) for x in X_nKoh])

# # print(clusters)

# plt.figure(figsize=(8, 8))
# plt.pcolor(som.distance_map().T, cmap='bone_r')  # mapa odległości
# target = numeric_y_true[::n]
# markers = ['o', 's', 'D']
# colors = ['C0', 'C1', 'C2']
# for cnt, xx in enumerate(X_nKoh):
#     w = som.winner(xx)  # getting the winner
#     # palce a marker on the winning position for the sample xx
#     plt.plot(w[0]+.5, w[1]+.5, markers[target[cnt]-1], markerfacecolor='None',
#              markeredgecolor=colors[target[cnt]-1], markersize=12, markeredgewidth=2)
# plt.show()

# inverted_mapping = {value: key for key, value in label_mapping.items()}

# print(inverted_mapping)

# w_x, w_y = zip(*[som.winner(d) for d in X_nKoh])
# w_x = np.array(w_x)
# w_y = np.array(w_y)

# plt.figure(figsize=(10, 9))
# plt.pcolor(som.distance_map().T, cmap='bone_r', alpha=.2)
# plt.colorbar()

# for c in np.unique(target):
#     idx_target = target==c
#     plt.scatter(w_x[idx_target],
#                 w_y[idx_target], 
#                 s=50, c=colors[c-1], label=inverted_mapping[c])
# plt.legend(loc='upper right')
# plt.grid()
# plt.show()

# # clusters = som.labels_map(X_nKoh, y_true_n)
# # print(clusters)
# # silhouette_avg = silhouette_score(X_red_n, clusters)
# # print(f"Silhouette Score: {silhouette_avg}")

# predicted_clusters = np.array([som.winner(x) for x in X_nKoh])
# # Konwertowanie współrzędnych neuronów na unikalne etykiety klastrów
# _, labels = np.unique(predicted_clusters, axis=0, return_inverse=True)
# print(labels)
# silhouette_avg = silhouette_score(X_nKoh, labels)
# print(f"Silhouette Score: {silhouette_avg}")

# DBSCAN

from sklearn.cluster import DBSCAN

# Tworzenie obiektu DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)  # eps - promień sąsiedztwa, min_samples - minimalna liczba punktów w sąsiedztwie
dbscan.fit(X_red_n)
clusters_dbscan = dbscan.labels_

plt.scatter(X_red_n[:, 0], X_red_n[:, 1], c=clusters_dbscan, cmap='viridis', marker='o', s=30, edgecolors='k')
plt.title('DBSCAN Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.colorbar(label='Cluster')
plt.show()

ari = adjusted_rand_score(y_true_n,clusters_dbscan)
print(f"Adjusted Rand Index DBSCAN (z redukcją): {ari}")

dbscan = DBSCAN(eps=0.5, min_samples=5)  # eps - promień sąsiedztwa, min_samples - minimalna liczba punktów w sąsiedztwie
dbscan.fit(X_n)
clusters_dbscan_bez = dbscan.labels_
ari = adjusted_rand_score(y_true_n,clusters_dbscan_bez)
print(f"Adjusted Rand Index DBSCAN (bez redukcji): {ari}")

# BIRCH
from sklearn.cluster import Birch

brc = Birch(n_clusters=3)
brc.fit(X_red_n)
brc.predict(X_red_n)
clusters_birch = brc.labels_
plt.scatter(X_red_n[:, 0], X_red_n[:, 1], c=clusters_birch, cmap='viridis', marker='o', s=30, edgecolors='k')
plt.title('BIRCH Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.colorbar(label='Cluster')
plt.show()
ari = adjusted_rand_score(y_true_n,clusters_birch)
print(f"Adjusted Rand Index BIRCH (z redukcją): {ari}")

brc = Birch(n_clusters=3)
brc.fit(X_red_n)
brc.predict(X_red_n)
clusters_birch_bez = brc.labels_

ari = adjusted_rand_score(y_true_n,clusters_birch_bez)
print(f"Adjusted Rand Index BIRCH (bez redukcji): {ari}")


fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey = True)  # 1 wiersz, 3 kolumny

scatter1 = axs[0].scatter(X_red_n[:, 0], X_red_n[:, 1], c=labels_kmeans, cmap='viridis', marker='o')
axs[0].set_title('KMEANS')

axs[0].set_ylabel('Druga składowa główna (PCA)')


scatter2 = axs[1].scatter(X_red_n[:, 0], X_red_n[:, 1], c=clusters_dbscan, cmap='viridis', marker='o')
axs[1].set_title('DBSCAN')
axs[1].set_xlabel('Pierwsza składowa główna (PCA)')


scatter3 = axs[2].scatter(X_red_n[:, 0], X_red_n[:, 1], c=clusters_birch, cmap='viridis', marker='o')
axs[2].set_title('BIRCH')



fig.colorbar(scatter3, ax=axs.ravel().tolist(), label='Klaster')

# plt.xlabel('Pierwsza składowa główna (PCA)')
# plt.ylabel('Druga składowa główna (PCA)')


# plt.tight_layout()
plt.show()