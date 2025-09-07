#!/usr/bin/env python3
"""
main_tolman.py
Script principal para generar y analizar soluciones Tolman IV
"""

import numpy as np
import pandas as pd
from pathlib import Path
import sys
import json
from datetime import datetime

# Importar los módulos de Tolman IV
from tolmanIV_modular import TolmanIVCore, TolmanIVAnalysis, TolmanIVData

def process_single_case(A, R, n_points=100, output_dir='data/tolman'):
    """
    Procesa un caso individual de Tolman IV
    
    Retorna:
        dict: Resultados del análisis o None si falla
    """
    print(f"\n{'='*60}")
    print(f"Procesando: A={A}, R={R}")
    print('='*60)
    
    try:
        # 1. Crear instancia del núcleo
        core = TolmanIVCore(A, R)
        
        # 2. Análisis
        analysis = TolmanIVAnalysis(core)
        analysis_results = analysis.analyze_solution()
        
        # Si no es válido, continuar con el siguiente
        if not analysis_results['valid']:
            print("⚠️  Solución no cumple condiciones de validez")
            return None
        
        # 3. Generar datos
        data_gen = TolmanIVData(core)
        df = data_gen.generate_eos_data(n_points)
        
        if len(df) == 0:
            print("⚠️  No se pudieron generar datos")
            return None
        
        # 4. Verificaciones físicas
        physical_checks = analysis.check_physical_conditions(df)
        print("\nVerificación de condiciones físicas:")
        for check, value in physical_checks.items():
            if isinstance(value, (bool, np.bool_)):
                symbol = '✓' if value else '✗'
                print(f"  {symbol} {check}: {value}")
            else:
                print(f"    {check}: {value:.4f}")
        
        # 5. Verificar ecuación de estado
        eos_verification = analysis.verify_equation_of_state(20)
        if eos_verification:
            print(f"\nVerificación Ecuación (6.5):")
            print(f"  Error promedio: {eos_verification['mean_error']:.2e}%")
            print(f"  Error máximo: {eos_verification['max_error']:.2e}%")
        
        # 6. Guardar datos
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filename = f'tolmanIV_A{A}_R{R}.csv'
        full_path = output_path / filename
        df.to_csv(full_path, index=False)
        print(f"\n✓ Datos guardados: {full_path}")
        print(f"  Total de puntos: {len(df)}")
        
        # 7. Retornar resumen
        return {
            'A': A,
            'R': R,
            'valid': True,
            'data_points': len(df),
            'file': str(full_path),
            'central_pressure': analysis_results['p_c'],
            'central_density': analysis_results['rho_c'],
            'boundary_radius': analysis_results['rb'],
            'physical_checks': physical_checks,
            'eos_error': eos_verification['mean_error'] if eos_verification else None
        }
        
    except Exception as e:
        print(f"✗ Error procesando caso: {e}")
        return None


def run_parameter_study(parameter_sets, n_points=100):
    """
    Ejecuta un estudio paramétrico completo
    
    Parámetros:
        parameter_sets: Lista de tuplas (A, R)
        n_points: Puntos por solución
    """
    print("="*70)
    print("ESTUDIO PARAMÉTRICO - SOLUCIÓN TOLMAN IV")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Casos a procesar: {len(parameter_sets)}")
    print(f"Puntos por solución: {n_points}")
    
    results = []
    successful = 0
    failed = 0
    
    for A, R in parameter_sets:
        result = process_single_case(A, R, n_points)
        if result:
            results.append(result)
            successful += 1
        else:
            failed += 1
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DEL PROCESAMIENTO")
    print("="*70)
    print(f"Casos exitosos: {successful}")
    print(f"Casos fallidos: {failed}")
    
    if results:
        # Guardar resumen en JSON
        summary_file = Path('data/tolman/summary.json')
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_cases': len(parameter_sets),
                'successful': successful,
                'failed': failed,
                'results': results
            }, f, indent=2)
        
        print(f"\n✓ Resumen guardado en: {summary_file}")
        
        # Tabla resumen
        print("\nTabla de resultados exitosos:")
        print("-"*70)
        print(f"{'A':>8} {'R':>8} {'rb':>10} {'ρc':>12} {'pc':>12} {'pc/ρc':>8}")
        print("-"*70)
        
        for r in results:
            ratio = r['central_pressure']/r['central_density'] if r['central_density'] > 0 else 0
            print(f"{r['A']:8.2f} {r['R']:8.2f} {r['boundary_radius']:10.4f} "
                  f"{r['central_density']:12.4e} {r['central_pressure']:12.4e} "
                  f"{ratio:8.4f}")
    
    return results


def main():
    """
    Función principal del script
    """
    # Definir casos a estudiar
    parameter_sets = [
        # Casos con presión central positiva (R < √3*A)
        (1.0, 1.5),    # R/A = 1.5 < √3 ≈ 1.732
        (1.0, 1.7),    # R/A = 1.7 ≈ √3
        (5.0, 8.0),    # R/A = 1.6 < √3
        (5.0, 10.0),   # R/A = 2.0 > √3 (presión central negativa)
        (10.0, 15.0),  # R/A = 1.5 < √3
        (10.0, 17.0),  # R/A = 1.7 ≈ √3
        
        # Casos adicionales para exploración
        (2.0, 3.0),    # R/A = 1.5
        (3.0, 5.0),    # R/A = 1.67
        (7.0, 11.0),   # R/A = 1.57
    ]
    
    # Configuración
    n_points = 100  # Número de puntos por solución
    
    # Ejecutar estudio
    results = run_parameter_study(parameter_sets, n_points)
    
    # Mensaje final
    print("\n" + "="*70)
    print("PROCESAMIENTO COMPLETADO")
    print("="*70)
    print("\nPróximos pasos:")
    print("1. Revisar los archivos CSV generados en data/tolman/")
    print("2. Ejecutar notebooks/explora_tolmanIV.py para visualización")
    print("3. Revisar data/tolman/summary.json para el resumen completo")
    
    return results


if __name__ == "__main__":
    # Ejecutar el programa principal
    results = main()
    
    # Retornar código de salida apropiado
    sys.exit(0 if results else 1)
    