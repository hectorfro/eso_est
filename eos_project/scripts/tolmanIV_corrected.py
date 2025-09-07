# tolmanIV_corrected.py
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

class TolmanIV:
    def __init__(self, A, R):
        """
        Solución Tolman IV
        Para que sea física, debe cumplirse R > A
        """
        self.A = A
        self.R = R
        
        # Verificar condición de validez
        if R <= A:
            print(f"Advertencia: R debe ser > A para solución física")
            
    def pressure(self, r):
        """
        Presión según Tolman IV
        La presión central debe ser positiva
        """
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        # Términos de la ecuación (6.3) de Tolman
        numerator1 = 1 - A2/R2 - 3*r2/R2
        denominator1 = A2 * (1 + 2*r2/A2)
        
        numerator2 = 2 * (1 - r2/R2)
        denominator2 = A2 * (1 + 2*r2/A2)**2
        
        # 8πp = term1 - term2
        eight_pi_p = numerator1/denominator1
        
        return eight_pi_p / (8 * np.pi)
    
    def density(self, r):
        """Densidad según Tolman IV"""
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        numerator = 1 + 3*A2/R2 + 3*r2/R2
        denominator = A2 * (1 + 2*r2/A2)
        numerator2 = 2 * (1 - r2/R2)
        denominator2 = A2 * (1 + 2*r2/A2)**2
       
        eight_pi_rho = numerator / denominator + numerator2 / denominator2 
        return eight_pi_rho / (8 * np.pi)
    
    def find_valid_parameters(self):
        """
        Encuentra condiciones para que p(0) > 0
        """
        # En r=0:
        # 8πp(0) = (1/A²)(1 + 3A²/R²) - 2/A²
        # 8πp(0) = (1/A²)[(1 + 3A²/R²) - 2]
        # 8πp(0) = (1/A²)[3A²/R² - 1]
        
        # Para p(0) > 0 necesitamos: 3A²/R² > 1
        # Es decir: R < √3 * A
        
        p_central = self.pressure(0)
        rho_central = self.density(0)
        
        print(f"Análisis de parámetros:")
        print(f"A = {self.A}, R = {self.R}")
        print(f"R/A = {self.R/self.A:.3f}")
        print(f"√3 = {np.sqrt(3):.3f}")
        print(f"Condición para p(0)>0: R < √3*A = {np.sqrt(3)*self.A:.3f}")
        print(f"¿Se cumple? {self.R < np.sqrt(3)*self.A}")
        print(f"p(0) = {p_central:.3e}")
        print(f"ρ(0) = {rho_central:.3e}")
        
        return p_central > 0
    
    def generate_eos_data(self, n_points=50):
        """Genera datos solo si los parámetros son válidos"""
        
        # Verificar validez
        is_valid = self.find_valid_parameters()
        
        if not is_valid:
            print("⚠️  Parámetros no producen solución física")
            # Sugerir parámetros corregidos
            R_suggested = np.sqrt(3) * self.A * 0.9  # 90% del límite
            print(f"Sugerencia: usar R < {np.sqrt(3)*self.A:.3f}, por ejemplo R = {R_suggested:.3f}")
            return pd.DataFrame()
        
        # Generar datos
        r_max = self.R * 0.99
        r_values = np.linspace(0, r_max, n_points)
        
        data = []
        for r in r_values:
            p = self.pressure(r)
            rho = self.density(r)
            
            if p >= 0 and rho > 0:  # Solo valores físicos
                data.append({
                    'r': r,
                    'rho': rho,
                    'p': p,
                    'p_over_rho': p/rho,
                    'cs2': np.gradient([self.pressure(r*0.99), p, self.pressure(r*1.01)])[1] / 
                           np.gradient([self.density(r*0.99), rho, self.density(r*1.01)])[1]
                           if r > 0 else 0
                })
        
        return pd.DataFrame(data)

# Probar con parámetros físicamente válidos
if __name__ == "__main__":
    print("SOLUCIÓN TOLMAN IV - BÚSQUEDA DE PARÁMETROS VÁLIDOS")
    print("="*60)
    
    # Casos de prueba
    test_cases = [
        (1.0, 1.5),   # R < √3*A ✓
        (1.0, 1.7),   # R ≈ √3*A
        (1.0, 2.0),   # R > √3*A ✗
        (10.0, 15.0), # R < √3*A ✓
    ]
    
    for A, R in test_cases:
        print(f"\n{'='*60}")
        print(f"Caso: A={A}, R={R}")
        print('='*60)
        
        tolman = TolmanIV(A, R)
        df = tolman.generate_eos_data(30)
        
        if len(df) > 0:
            # Guardar
            script_dir = Path(__file__).parent
            project_dir = script_dir.parent
            output_file = project_dir / 'data' / 'tolman' / f'tolmanIV_A{A}_R{R}_valid.csv'
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_csv(output_file, index=False)
            print(f"✓ Guardado: {output_file}")
            print(f"  Puntos generados: {len(df)}")
            print(f"  p/ρ en centro: {df.iloc[0]['p_over_rho']:.3f}")

