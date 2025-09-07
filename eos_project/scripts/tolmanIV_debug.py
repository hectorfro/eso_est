# tolmanIV_debug.py
import numpy as np
import pandas as pd
from pathlib import Path

class TolmanIV:
    def __init__(self, A, R):
        self.A = A
        self.R = R
        
    def pressure(self, r):
        """Presión según Tolman IV"""
        if r >= self.R:  # Fuera del rango válido
            return -1
            
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        # Evitar división por cero
        if abs(1 - r2/R2) < 1e-10:
            return 0
        
        term1 = (1/A2) * (1 + 3*A2/R2 + 3*r2/R2) / (1 + 2*r2/A2)
        term2 = (2/A2) * (1 - r2/R2) / ((1 + 2*r2/A2)**2)
        
        p_8pi = term1 - term2
        return p_8pi / (8 * np.pi)
    
    def density(self, r):
        """Densidad según Tolman IV"""
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        rho_8pi = (1/A2) * (1 + 3*A2/R2 + 3*r2/R2) / (1 + 2*r2/A2)
        return rho_8pi / (8 * np.pi)
    
    def generate_eos_data(self, n_points=50):
        """Genera datos con mejor debugging"""
        data = []
        
        # Usar un rango más conservador
        r_max = self.R * 0.8  # 80% del radio R
        r_values = np.linspace(0, r_max, n_points)
        
        print(f"Generando datos desde r=0 hasta r={r_max:.3f}")
        print(f"Parámetros: A={self.A}, R={self.R}")
        
        for i, r in enumerate(r_values):
            rho = self.density(r)
            p = self.pressure(r)
            
            # Debug: mostrar primeros valores
            if i < 5:
                print(f"r={r:.3f}: ρ={rho:.3e}, p={p:.3e}")
            
            # Guardar todos los valores para análisis
            data.append({
                'r': r,
                'rho': rho,
                'p': p,
                'p_over_rho': p/rho if rho > 0 else 0,
                'is_physical': 1 if p >= 0 else 0
            })
        
        df = pd.DataFrame(data)
        
        # Información de debug
        print(f"\nResumen:")
        print(f"Puntos totales: {len(df)}")
        print(f"Puntos con p≥0: {df['is_physical'].sum()}")
        print(f"Presión central p(0) = {df.iloc[0]['p']:.3e}")
        print(f"Densidad central ρ(0) = {df.iloc[0]['rho']:.3e}")
        
        return df

if __name__ == "__main__":
    # Probar diferentes parámetros
    test_params = [
        (1.0, 2.0),
        (1.0, 10.0),
        (10.0, 20.0),
    ]
    
    for A, R in test_params:
        print(f"\n{'='*50}")
        print(f"Probando A={A}, R={R}")
        print('='*50)
        
        tolman = TolmanIV(A, R)
        df = tolman.generate_eos_data(n_points=20)
        
        # Guardar solo si hay datos físicos
        if df['is_physical'].sum() > 0:
            script_dir = Path(__file__).parent
            project_dir = script_dir.parent
            output_file = project_dir / 'data' / 'tolman' / f'tolmanIV_A{A}_R{R}.csv'
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar solo puntos físicos
            df_physical = df[df['is_physical'] == 1].copy()
            df_physical.to_csv(output_file, index=False)
            print(f"Guardado: {output_file}")

