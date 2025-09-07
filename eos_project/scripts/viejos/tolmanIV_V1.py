# ======================================================
# Script: tolman_iv.py
# Genera tabla rho(r), P(r) para la Solución IV de Tolman
# Héctor - Proyecto EoS en Relatividad General
# ======================================================

import numpy as np
import pandas as pd

# ----------------------------
# Parámetros del modelo
# ----------------------------
A = 5.0   # parámetro de escala (km, por ejemplo)
R = 10.0  # radio estelar máximo (condición P(R)=0)
Npoints = 100

# ----------------------------
# Definición de las funciones
# ----------------------------
def rho_tolmanIV(r, A):
    """Densidad Tolman IV (en unidades geométricas, 8πρ)."""
    return (3*A**2 + r**2) / (A**2 + r**2)**2

def P_tolmanIV(r, A):
    """Presión Tolman IV (en unidades geométricas, 8πP)."""
    return (A**2 - r**2) / (A**2 + r**2)**2

# ----------------------------
# Generar tabla
# ----------------------------
r_vals = np.linspace(0, R, Npoints)
rho_vals = rho_tolmanIV(r_vals, A)
P_vals = P_tolmanIV(r_vals, A)

# Etiquetado simple (ejemplo: P y rho no negativos)
labels = []
for i in range(len(r_vals)):
    if rho_vals[i] >= 0 and P_vals[i] >= 0:
        labels.append(1)
    else:
        labels.append(0)

# ----------------------------
# Guardar en CSV
# ----------------------------
df = pd.DataFrame({
    "r": r_vals,
    "rho": rho_vals,
    "P": P_vals,
    "label": labels
})

df.to_csv("tolmanIV.csv", index=False)
print("Tabla generada: tolmanIV.csv")

