#!/usr/bin/env python3
"""
tolman_iv_simple.py
Versión simplificada para generar datos de Tolman IV
"""

import numpy as np
import pandas as pd
from pathlib import Path

class TolmanIV:
    def __init__(self, A, R):
        self.A = A
        self.R = R
        if R <= A:
            raise ValueError(f"R debe ser > A. Dados: R={R}, A={A}")
    
    # ===== ECUACIONES FUNDAMENTALES (NO MODIFICAR) =====
    
    def pressure(self, r):
        """Ecuación (6.3) del paper"""
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        eight_pi_p = (1/A2) * (1 - A2/R2 - 3*r2/R2)/(1 + 2*r2/A2)
        return eight_pi_p / (8 * np.pi)
    
    def density(self, r):
        """Ecuación (6.2) del paper"""
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        term1 = (1/A2) * (1 + 3*A2/R2 + 3*r2/R2)/(1 + 2*r2/A2)
        term2 = (2/A2) * (1 - r2/R2) / (1 + 2*r2/A2)**2
        eight_pi_rho = term1 + term2
        return eight_pi_rho / (8 * np.pi)
    
    def boundary_radius(self):
        """Ecuación (6.6) del paper"""
        A2 = self.A**2
        R2 = self.R**2
        if A2/R2 >= 1:
            return 0
        rb = (self.R / np.sqrt(3)) * np.sqrt(1 - A2/R2)
        return rb
    
    # ===== FIN DE ECUACIONES FUNDAMENTALES =====
    
    def generate_data(self, n_points=100):
        """Genera datos de la solución"""
        rb = self.boundary_radius()
        if rb <= 0:
            return None
        
        r_values = np.linspace(0, rb * 0.999, n_points)
        
        data = []
        for r in r_values:
            p = self.pressure(r)
            rho = self.density(r)
            
            if p >= 0 and rho > 0:
                data.append({
                    'r': r,
                    'rho': rho,
                    'p': p,
                    'p_over_rho': p/rho
                })
        
        return pd.DataFrame(data)
    
    def save_data(self, df, output_dir='../data/tolman'):
        """Guarda los datos en CSV"""
        if df is None or df.empty:
            return None
            
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filename = f'tolmanIV_A{self.A}_R{self.R}.csv'
        full_path = output_path / filename
        df.to_csv(full_path, index=False)
        
        return full_path


def main():
    """Función principal"""
    
    # Casos a procesar
    cases = [
        (1.0, 1.5),
        (1.0, 1.7), 
        (5.0, 8.0),
        (5.0, 10.0),
        (10.0, 15.0),
        (10.0, 17.0),
    ]
    
    print("="*50)
    print("GENERANDO DATOS TOLMAN IV")
    print("="*50)
    
    for A, R in cases:
        print(f"\nProcesando A={A}, R={R}...")
        
        try:
            # Crear solución
            tolman = TolmanIV(A, R)
            
            # Generar datos
            df = tolman.generate_data(100)
            
            if df is not None and not df.empty:
                # Guardar
                path = tolman.save_data(df)
                print(f"  ✓ Guardado: {path}")
                print(f"  Puntos: {len(df)}")
                
                # Info básica
                pc = tolman.pressure(0)
                rhoc = tolman.density(0)
                rb = tolman.boundary_radius()
                print(f"  pc(0) = {pc:.4e}, ρc(0) = {rhoc:.4e}")
                print(f"  rb = {rb:.4f}")
            else:
                print(f"  ✗ No se pudieron generar datos")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*50)
    print("COMPLETADO")
    print("="*50)


if __name__ == "__main__":
    main()
