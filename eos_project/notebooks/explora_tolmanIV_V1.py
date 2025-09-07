# ===========================================
# Notebook: explore_tolmanIV.ipynb
# Explora y grafica los datos de Tolman IV
# ===========================================

import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# 1. Cargar datos
# ----------------------------
df = pd.read_csv("../data/tolman/tolmanIV.csv")
print(df.head())

# ----------------------------
# 2. Graficar perfiles
# ----------------------------
plt.figure(figsize=(8,5))
plt.plot(df["r"], df["rho"], label=r"$\rho(r)$")
plt.plot(df["r"], df["P"], label=r"$P(r)$")
plt.xlabel("r")
plt.ylabel("Magnitud (unidades arbitrarias)")
plt.title("Solución Tolman IV")
plt.legend()
plt.grid(True)
plt.show()

# ----------------------------
# 3. Verificar etiquetas
# ----------------------------
print("¿Todas las condiciones cumplidas?:", df["label"].all())

