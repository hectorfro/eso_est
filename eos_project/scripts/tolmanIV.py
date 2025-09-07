# tolmanIV.py - versión mejorada
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

class TolmanIV:
    """
    Solución de Tolman IV para fluidos esféricos estáticos
    Ref: Tolman, R.C. (1939) Phys. Rev. 55, 364
    """
    
    def __init__(self, A, R):
        """
        Parámetros:
        A: parámetro de escala radial
        R: parámetro relacionado con la densidad
        """
        self.A = A
        self.R = R
        self.c = 2.998e10  # cm/s
        self.G = 6.674e-8  # cgs
        
    def calculate_metric(self, r):
        """
        Calcula los componentes de la métrica
        e^λ = (1+2r²/A²) / ((1-r²/R²)(1+r²/A²))
        e^ν = B²(1+r²/A²)
        """
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        e_lambda = (1 + 2*r2/A2) / ((1 - r2/R2) * (1 + r2/A2))
        # B² se determina por condiciones de frontera
        
        return e_lambda
    
    def pressure(self, r):
        """
        Presión según Eq. (6.3) del paper de Tolman
        8πp = (1/A²) * (1+3A²/R²+3r²/R²)/(1+2r²/A²) 
              - (2/A²) * (1-r²/R²)/((1+2r²/A²)²)
        """
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        term1 = (1/A2) * (1 + 3*A2/R2 + 3*r2/R2) / (1 + 2*r2/A2)
        term2 = (2/A2) * (1 - r2/R2) / ((1 + 2*r2/A2)**2)
        
        p_8pi = term1 - term2
        return p_8pi / (8 * np.pi)
    
    def density(self, r):
        """
        Densidad según Eq. (6.2) del paper de Tolman
        8πρ = (1/A²) * (1+3A²/R²+3r²/R²)/(1+2r²/A²)
        """
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        rho_8pi = (1/A2) * (1 + 3*A2/R2 + 3*r2/R2) / (1 + 2*r2/A2)
        return rho_8pi / (8 * np.pi)
    
    def generate_eos_data(self, n_points=50):
        """
        Genera datos de la ecuación de estado p(ρ)
        """
        # Radio desde el centro hasta donde p=0
        r_max = self.find_boundary()
        r_values = np.linspace(0, r_max, n_points)
        
        data = []
        for r in r_values:
            rho = self.density(r)
            p = self.pressure(r)
            
            if p >= 0:  # Solo valores físicos
                data.append({
                    'r': r,
                    'rho': rho,
                    'p': p,
                    'p_over_rho': p/rho if rho > 0 else 0
                })
        
        return pd.DataFrame(data)
    
    def find_boundary(self):
        """
        Encuentra el radio donde la presión se vuelve cero
        """
        # Para Tolman IV, esto ocurre cuando el numerador de p se anula
        # Necesita solución numérica en general
        from scipy.optimize import brentq
        
        try:
            r_b = brentq(self.pressure, 0, self.R*0.99)
            return r_b
        except:
            return self.R * 0.9  # Aproximación si no converge

# Uso
if __name__ == "__main__":
    # Parámetros de ejemplo
    A = 1.0  # en unidades geométricas
    R = 2.0
    
    tolman = TolmanIV(A, R)
    df = tolman.generate_eos_data()

    
    # Configurar rutas correctamente
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    output_file = project_dir / 'data' / 'tolman' / 'tolmanIV.csv'
    
    # Crear directorio si no existe
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Guardar
    df.to_csv(output_file, index=False)
    print(f"Archivo guardado en: {output_file}")
    print(f"Generados {len(df)} puntos para Tolman IV")
    

