import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def visual():
    # Adatok beolvasása lebegőpontosként
    adatok = []
    with open('data.txt', 'r') as file:
        for sor in file:
            if sor.strip():
                n, k, eff1, eff2 = map(float, sor.strip().split())
                adatok.append((n, k, eff1, eff2))

    adatok = np.array(adatok)
    n_values = adatok[:, 0]
    k_values = adatok[:, 1]
    eff1_values = adatok[:, 2]
    eff2_values = adatok[:, 3]

    # Egyedi n és k értékek
    n_unique = np.unique(n_values)
    k_unique = np.unique(k_values)
    N, K = np.meshgrid(n_unique, k_unique)

    # Felületek létrehozása
    eff1_grid = np.zeros_like(N, dtype=float)
    eff2_grid = np.zeros_like(K, dtype=float)

    for i in range(len(n_values)):
        ni = np.where(n_unique == n_values[i])[0][0]
        ki = np.where(k_unique == k_values[i])[0][0]
        eff1_grid[ki, ni] = eff1_values[i]
        eff2_grid[ki, ni] = eff2_values[i]

    # Ábrázolás
    fig = plt.figure(figsize=(14, 6))

    # 1. ábra logaritmikus tengelyekkel
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(N, K, eff1_grid, cmap='viridis')
    ax1.set_title('Eredeti')
    ax1.set_xlabel('n')
    ax1.set_ylabel('k')
    ax1.set_zlabel('Kiértékelt LP feladatok')

    # 2. ábra logaritmikus tengelyekkel
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(N, K, eff2_grid, cmap='plasma')
    ax2.set_title('Új')
    ax2.set_xlabel('n')
    ax2.set_ylabel('k')
    ax2.set_zlabel('Kiértékelt LP feladatok')

    plt.tight_layout()
    plt.show()
