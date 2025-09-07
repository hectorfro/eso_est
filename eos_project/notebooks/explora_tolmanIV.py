# ===========================================
# Notebook: explore_tolmanIV.ipynb
# Explora y grafica los datos de Tolman IV
# ===========================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import glob

# ----------------------------
# 1. Cargar datos disponibles
# ----------------------------
# Buscar todos los archivos CSV de Tolman IV
data_path = Path("../data/tolman/")
csv_files = list(data_path.glob("tolmanIV*.csv"))

if not csv_files:
    print("No se encontraron archivos CSV de Tolman IV")
else:
    print(f"Archivos encontrados: {len(csv_files)}")
    for file in csv_files:
        print(f"  - {file.name}")

# Cargar el primer archivo o uno específico
if csv_files:
    # Puedes cambiar esto para cargar un archivo específico
    df = pd.read_csv(csv_files[0])
    print(f"\nCargando: {csv_files[0].name}")
    print(f"Forma del dataset: {df.shape}")
    print("\nPrimeras filas:")
    print(df.head())
    print("\nColumnas disponibles:", df.columns.tolist())
    print("\nEstadísticas básicas:")
    print(df.describe())

# ----------------------------
# 2. Graficar perfiles radiales
# ----------------------------
if 'df' in locals():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Densidad vs radio
    ax1 = axes[0, 0]
    ax1.plot(df["r"], df["rho"], 'b-', linewidth=2)
    ax1.set_xlabel("r (unidades geométricas)")
    ax1.set_ylabel(r"$\rho(r)$")
    ax1.set_title("Perfil de Densidad")
    ax1.grid(True, alpha=0.3)
    
    # Presión vs radio
    ax2 = axes[0, 1]
    ax2.plot(df["r"], df["p"], 'r-', linewidth=2)
    ax2.set_xlabel("r (unidades geométricas)")
    ax2.set_ylabel(r"$p(r)$")
    ax2.set_title("Perfil de Presión")
    ax2.grid(True, alpha=0.3)
    
    # Ambos perfiles normalizados
    ax3 = axes[1, 0]
    ax3.plot(df["r"], df["rho"]/df["rho"].max(), 'b-', label=r"$\rho/\rho_c$", linewidth=2)
    ax3.plot(df["r"], df["p"]/df["p"].max(), 'r--', label=r"$p/p_c$", linewidth=2)
    ax3.set_xlabel("r (unidades geométricas)")
    ax3.set_ylabel("Valor normalizado")
    ax3.set_title("Perfiles Normalizados")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Relación p/ρ vs radio
    ax4 = axes[1, 1]
    if 'p_over_rho' in df.columns:
        ax4.plot(df["r"], df["p_over_rho"], 'g-', linewidth=2)
        ax4.set_xlabel("r (unidades geométricas)")
        ax4.set_ylabel(r"$p/\rho$")
        ax4.set_title("Razón Presión/Densidad")
        ax4.axhline(y=1/3, color='k', linestyle=':', label='Límite causal (1/3)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
    
    plt.suptitle(f"Solución Tolman IV - {csv_files[0].stem}", fontsize=14)
    plt.tight_layout()
    plt.show()

# ----------------------------
# 3. Ecuación de Estado p(ρ)
# ----------------------------
if 'df' in locals():
    plt.figure(figsize=(10, 6))
    
    # Plot principal: p vs ρ
    plt.subplot(1, 2, 1)
    plt.plot(df["rho"], df["p"], 'b-', linewidth=2)
    plt.xlabel(r"$\rho$ (densidad)")
    plt.ylabel(r"$p$ (presión)")
    plt.title("Ecuación de Estado p(ρ)")
    plt.grid(True, alpha=0.3)
    
    # Plot log-log para ver comportamiento en escalas
    plt.subplot(1, 2, 2)
    # Filtrar valores positivos para log
    mask = (df["rho"] > 0) & (df["p"] > 0)
    if mask.any():
        plt.loglog(df.loc[mask, "rho"], df.loc[mask, "p"], 'b-', linewidth=2)
        
        # Agregar líneas de referencia para diferentes EoS
        rho_range = df.loc[mask, "rho"]
        plt.loglog(rho_range, rho_range, 'k:', alpha=0.5, label=r'$p=\rho$ (stiff)')
        plt.loglog(rho_range, rho_range/3, 'r:', alpha=0.5, label=r'$p=\rho/3$ (radiation)')
        plt.loglog(rho_range, rho_range**2/rho_range.max(), 'g:', alpha=0.5, label=r'$p \propto \rho^2$')
        
        plt.xlabel(r"$\rho$ (densidad)")
        plt.ylabel(r"$p$ (presión)")
        plt.title("Ecuación de Estado (escala log-log)")
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# ----------------------------
# 4. Verificar condiciones físicas
# ----------------------------
if 'df' in locals():
    print("\n" + "="*50)
    print("VERIFICACIÓN DE CONDICIONES FÍSICAS")
    print("="*50)
    
    # Condición de energía
    energy_condition = (df["rho"] >= df["p"]).all()
    print(f"✓ Condición de energía (ρ ≥ p): {energy_condition}")
    
    # Presión no negativa
    positive_pressure = (df["p"] >= 0).all()
    print(f"✓ Presión no negativa: {positive_pressure}")
    
    # Densidad positiva
    positive_density = (df["rho"] > 0).all()
    print(f"✓ Densidad positiva: {positive_density}")
    
    # Causalidad (p/ρ ≤ 1)
    if 'p_over_rho' in df.columns:
        causality = (df["p_over_rho"] <= 1).all()
        max_p_over_rho = df["p_over_rho"].max()
        print(f"✓ Causalidad (p/ρ ≤ 1): {causality}")
        print(f"  Máximo p/ρ = {max_p_over_rho:.4f}")
    
    # Velocidad del sonido
    if 'cs2' in df.columns:
        sound_speed_ok = (df["cs2"] <= 1).all() & (df["cs2"] >= 0).all()
        print(f"✓ Velocidad del sonido (0 ≤ cs² ≤ 1): {sound_speed_ok}")
        if not sound_speed_ok:
            print(f"  Rango de cs²: [{df['cs2'].min():.4f}, {df['cs2'].max():.4f}]")
    
    # Monotonicidad
    pressure_monotonic = (df["p"].diff().dropna() <= 0).all()  # p debe decrecer con r
    density_monotonic = (df["rho"].diff().dropna() <= 0).all()  # ρ debe decrecer con r
    print(f"✓ Presión monótona decreciente: {pressure_monotonic}")
    print(f"✓ Densidad monótona decreciente: {density_monotonic}")
    
    print("\n" + "="*50)
    if all([energy_condition, positive_pressure, positive_density]):
        print("✅ SOLUCIÓN FÍSICAMENTE ACEPTABLE")
    else:
        print("⚠️  SOLUCIÓN NO CUMPLE TODAS LAS CONDICIONES")
    print("="*50)

# ----------------------------
# 5. Comparar múltiples soluciones
# ----------------------------
if len(csv_files) > 1:
    print("\n" + "="*50)
    print("COMPARACIÓN DE MÚLTIPLES SOLUCIONES")
    print("="*50)
    
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    for file in csv_files[:5]:  # Máximo 5 archivos para claridad
        df_temp = pd.read_csv(file)
        label = file.stem.replace("tolmanIV_", "")
        plt.plot(df_temp["rho"], df_temp["p"], label=label, linewidth=2)
    
    plt.xlabel(r"$\rho$")
    plt.ylabel(r"$p$")
    plt.title("Comparación de EoS")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    for file in csv_files[:5]:
        df_temp = pd.read_csv(file)
        label = file.stem.replace("tolmanIV_", "")
        if 'p_over_rho' in df_temp.columns:
            plt.plot(df_temp["r"], df_temp["p_over_rho"], label=label, linewidth=2)
    
    plt.xlabel("r")
    plt.ylabel(r"$p/\rho$")
    plt.title("Comparación de p/ρ")
    plt.axhline(y=1/3, color='k', linestyle=':', alpha=0.5)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

