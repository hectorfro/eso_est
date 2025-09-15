#!/usr/bin/env python3
"""
Script súper simple para Tolman IV
Solo carga archivos CSV y los grafica - NADA MÁS
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def cargar_y_graficar(archivo):
    """Carga un CSV y lo grafica - súper simple"""
    try:
        # Cargar datos
        datos = pd.read_csv(archivo, comment='#')
        print(f"✅ Cargado: {archivo}")
        print(f"   Filas: {len(datos)}, Columnas: {list(datos.columns)}")
        
        # Graficar
        plt.figure(figsize=(12, 4))
        
        # Densidad
        plt.subplot(1, 3, 1)
        plt.plot(datos["r"], datos["rho"], 'b-', linewidth=2)
        plt.title("Densidad")
        plt.xlabel("r")
        plt.ylabel("ρ")
        plt.grid(True)
        
        # Presión
        plt.subplot(1, 3, 2)
        plt.plot(datos["r"], datos["p"], 'r-', linewidth=2)
        plt.title("Presión")
        plt.xlabel("r")
        plt.ylabel("p")
        plt.grid(True)
        
        # Ecuación de estado
        plt.subplot(1, 3, 3)
        plt.plot(datos["rho"], datos["p"], 'g-', linewidth=2)
        plt.title("p vs ρ")
        plt.xlabel("ρ")
        plt.ylabel("p")
        plt.grid(True)
        
        plt.suptitle(f"Datos de {Path(archivo).name}")
        plt.tight_layout()
        plt.show()
        
        return datos
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def buscar_archivos():
    """Busca archivos CSV de Tolman"""
    # Buscar en varias ubicaciones
    ubicaciones = [
        ".",
        "../data/tolman/",
        "data/tolman/",
        "../",
    ]
    
    archivos = []
    for ubicacion in ubicaciones:
        path = Path(ubicacion)
        if path.exists():
            archivos.extend(list(path.glob("*.csv")))
            archivos.extend(list(path.glob("tolman*.csv")))
    
    # Quitar duplicados
    archivos = list(set(archivos))
    
    if archivos:
        print(f"📁 Encontrados {len(archivos)} archivos:")
        for i, archivo in enumerate(archivos):
            print(f"  {i}: {archivo.name}")
        return archivos
    else:
        print("❌ No se encontraron archivos CSV")
        return []

def comparar_archivos(archivos):
    """Compara varios archivos en una gráfica"""
    plt.figure(figsize=(15, 4))
    
    datos_list = []
    
    # Cargar todos los archivos
    for archivo in archivos:
        try:
            datos = pd.read_csv(archivo, comment='#')
            datos_list.append((archivo.name, datos))
        except:
            continue
    
    if not datos_list:
        print("❌ No se pudieron cargar archivos")
        return
    
    # Densidades
    plt.subplot(1, 3, 1)
    for nombre, datos in datos_list:
        plt.plot(datos["r"], datos["rho"], linewidth=2, label=nombre)
    plt.title("Densidades")
    plt.xlabel("r")
    plt.ylabel("ρ")
    plt.legend()
    plt.grid(True)
    
    # Presiones
    plt.subplot(1, 3, 2)
    for nombre, datos in datos_list:
        plt.plot(datos["r"], datos["p"], linewidth=2, label=nombre)
    plt.title("Presiones")
    plt.xlabel("r")
    plt.ylabel("p")
    plt.legend()
    plt.grid(True)
    
    # Ecuaciones de estado
    plt.subplot(1, 3, 3)
    for nombre, datos in datos_list:
        plt.plot(datos["rho"], datos["p"], linewidth=2, label=nombre)
    plt.title("p vs ρ")
    plt.xlabel("ρ")
    plt.ylabel("p")
    plt.legend()
    plt.grid(True)
    
    plt.suptitle("Comparación de archivos")
    plt.tight_layout()
    plt.show()

def verificar_fisica(datos):
    """Verifica si los datos son físicamente válidos"""
    if datos is None:
        return
    
    print("\n🔍 Verificación:")
    
    # Verificaciones básicas
    rho_ok = (datos["rho"] > 0).all()
    p_ok = (datos["p"] >= 0).all()
    energia_ok = (datos["rho"] >= datos["p"]).all()
    
    print(f"  {'✅' if rho_ok else '❌'} Densidad positiva")
    print(f"  {'✅' if p_ok else '❌'} Presión no negativa")
    print(f"  {'✅' if energia_ok else '❌'} Condición energía (ρ≥p)")
    
    if rho_ok and p_ok and energia_ok:
        print("🎉 Datos físicamente válidos")
    else:
        print("⚠️  Problemas físicos detectados")

def menu():
    """Menú súper simple"""
    while True:
        print("\n" + "="*40)
        print("📊 TOLMAN IV - EXPLORADOR SIMPLE")
        print("="*40)
        print("1. Ver archivos disponibles")
        print("2. Cargar y graficar UN archivo")
        print("3. Comparar TODOS los archivos")
        print("0. Salir")
        print("="*40)
        
        opcion = input("¿Qué hacer? ").strip()
        
        if opcion == "0":
            print("👋 ¡Adiós!")
            break
            
        elif opcion == "1":
            buscar_archivos()
            
        elif opcion == "2":
            archivos = buscar_archivos()
            if archivos:
                try:
                    idx = int(input("¿Cuál archivo? (número): "))
                    if 0 <= idx < len(archivos):
                        datos = cargar_y_graficar(archivos[idx])
                        if datos is not None:
                            verificar_fisica(datos)
                    else:
                        print("❌ Número no válido")
                except:
                    print("❌ Ingresa un número")
                    
        elif opcion == "3":
            archivos = buscar_archivos()
            if archivos:
                comparar_archivos(archivos)
            
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    print("📊 Explorador súper simple de archivos Tolman IV")
    print("Solo necesitas archivos CSV - no depende de nada más")
    print()
    
    # Ver si hay archivos
    archivos = buscar_archivos()
    
    if archivos:
        print("\n¿Qué quieres hacer?")
        print("1. Usar menú interactivo")
        print("2. Cargar el primer archivo encontrado")
        
        opcion = input("Opción (1/2) o Enter para menú: ").strip() or "1"
        
        if opcion == "2" and archivos:
            datos = cargar_y_graficar(archivos[0])
            if datos is not None:
                verificar_fisica(datos)
        else:
            menu()
    else:
        print("❌ No se encontraron archivos CSV")
        print("💡 Asegúrate de tener archivos .csv en la carpeta actual o data/tolman/")