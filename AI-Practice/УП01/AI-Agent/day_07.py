import numpy as np

data = np.array([
    [70, 80, 90, 60],
    [55, 75, 85, 95],
    [40, 65, 50, 70]
])

group_means = np.mean(data, axis=1)
print("Средние по группам:", group_means)
best_mean = np.max(group_means)
print("Максимальное среднее:", best_mean)