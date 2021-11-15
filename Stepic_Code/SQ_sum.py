# Питонистам важно понимать как каждый из рассматриваемых методов реализуется на Питоне

from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# Запишем координаты точек в виде массива numpy
X = np.array([[-3, 3], [1, 4], [2, 6], [3, 8], [5, 2], [6, 11], [7, 1]])
# Обучим модель KMeans на нашем массиве с одним кластером
kmeans = KMeans(n_clusters=1).fit(X)
# Выведем координаты центроида данного кластера
print(kmeans.cluster_centers_)
# Выведем сумму квадратов расстояний точек от центроида = аттрибут модели kmeans
print(kmeans.inertia_)
plt.figure()
plt.plot(X)
plt.show()