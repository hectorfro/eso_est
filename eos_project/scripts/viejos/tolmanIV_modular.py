# tolmanIV_modular.py
"""
Solución Tolman IV - Versión Modular
Estructura:
  - TolmanIVCore: Ecuaciones fundamentales (NO MODIFICAR)
  - TolmanIVAnalysis: Análisis y verificaciones
  - TolmanIVData: Generación de datos
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ==============================================================================
# MÓDULO 1: ECUACIONES FUNDAMENTALES (NO MODIFICAR)
# ==============================================================================

class TolmanIVCore:
    """
    Ecuaciones fundamentales de Tolman IV.
    IMPORTANTE: No modificar estas ecuaciones, están verificadas con el paper.
    """
    
    def __init__(self, A, R):
        """
        Parámetros de la solución Tolman IV
        
        Parámetros:
        -----------
        A : float
            Parámetro A de la solución
        R : float
            Parámetro R de la solución (debe ser > A)
        """
        self.A = A
        self.R = R
        
        # Verificación básica
        if R <= A:
            raise ValueError(f"R debe ser > A para solución física. Dados: R={R}, A={A}")
    
    def pressure(self, r):
        """
        Presión según Tolman IV - Ecuación (6.3) del paper
        NO MODIFICAR
        """
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        eight_pi_p = (1/A2) * (1 - A2/R2 - 3*r2/R2)/(1 + 2*r2/A2)
        
        return eight_pi_p / (8 * np.pi)
    
    def density(self, r):
        """
        Densidad según Tolman IV - Ecuación (6.2) del paper
        NO MODIFICAR
        """
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        term1 = (1/A2) * (1 + 3*A2/R2 + 3*r2/R2)/(1 + 2*r2/A2)
        term2 = (2/A2) * (1 - r2/R2) / (1 + 2*r2/A2)**2
        
        eight_pi_rho = term1 + term2
        return eight_pi_rho / (8 * np.pi)
    
    def central_values(self):
        """
        Valores centrales según ecuación (6.4) del paper
        NO MODIFICAR
        """
        A2 = self.A**2
        R2 = self.R**2
        
        # Densidad central
        eight_pi_rho_c = 3/A2 + 3/R2
        rho_c = eight_pi_rho_c / (8 * np.pi)
        
        # Presión central
        eight_pi_p_c = 1/A2 - 1/R2
        p_c = eight_pi_p_c / (8 * np.pi)
        
        return rho_c, p_c
    
    def boundary_radius(self):
        """
        Radio del borde según ecuación (6.6) del paper
        NO MODIFICAR
        """
        A2 = self.A**2
        R2 = self.R**2
        
        if A2/R2 >= 1:
            return 0  # No hay solución física
        
        rb = (self.R / np.sqrt(3)) * np.sqrt(1 - A2/R2)
        return rb
    
    def equation_of_state(self, p):
        """
        Ecuación de estado según ecuación (6.5) del paper
        ρ = ρc - 5(pc - p) + 8(pc - p)²/(ρc + pc)
        NO MODIFICAR
        """
        rho_c, p_c = self.central_values()
        
        # Verificar que p no exceda p_c
        if np.any(p > p_c):
            print("Advertencia: La presión no puede exceder la presión central")
            
        # Aplicar ecuación (6.5)
        rho = rho_c - 5*(p_c - p) + 8*(p_c - p)**2/(rho_c + p_c)
        
        return rho


# ==============================================================================
# MÓDULO 2: ANÁLISIS Y VERIFICACIONES
# ==============================================================================

class TolmanIVAnalysis:
    """
    Análisis y verificaciones de la solución Tolman IV
    """
    
    def __init__(self, tolman_core):
        """
        Inicializa con una instancia de TolmanIVCore
        """
        self.core = tolman_core
    
    def check_validity_conditions(self):
        """
        Verifica las condiciones de validez física
        """
        A = self.core.A
        R = self.core.R
        
        conditions = {
            'R > A': R > A,
            'pc > 0': R < np.sqrt(3) * A,
            'R/A ratio': R/A,
            'sqrt(3)*A': np.sqrt(3) * A
        }
        
        return conditions
    
    def analyze_solution(self):
        """
        Análisis completo de la solución
        """
        print("="*60)
        print("ANÁLISIS DE LA SOLUCIÓN TOLMAN IV")
        print("="*60)
        print(f"Parámetros: A = {self.core.A}, R = {self.core.R}")
        print(f"Razón R/A = {self.core.R/self.core.A:.3f}")
        print()
        
        # Condiciones de validez
        conditions = self.check_validity_conditions()
        print("Condiciones de validez:")
        print(f"  • R > A: {'✓' if conditions['R > A'] else '✗'}")
        print(f"  • R < √3*A para pc>0: {'✓' if conditions['pc > 0'] else '✗'}")
        print()
        
        # Valores centrales
        rho_c, p_c = self.core.central_values()
        print("Valores centrales (r=0):")
        print(f"  • ρ(0) = {rho_c:.4e}")
        print(f"  • p(0) = {p_c:.4e}")
        if rho_c > 0:
            print(f"  • p(0)/ρ(0) = {p_c/rho_c:.4f}")
        print()
        
        # Radio del borde
        rb = self.core.boundary_radius()
        if rb > 0:
            rho_b = self.core.density(rb)
            p_b = self.core.pressure(rb)
            print(f"Radio del borde (donde p=0):")
            print(f"  • rb = {rb:.4f}")
            print(f"  • ρ(rb) = {rho_b:.4e}")
            print(f"  • p(rb) = {p_b:.4e} (debe ser ≈0)")
        else:
            print("No existe radio de borde físico")
        
        return {
            'valid': conditions['R > A'] and conditions['pc > 0'],
            'rho_c': rho_c,
            'p_c': p_c,
            'rb': rb
        }
    
    def verify_equation_of_state(self, n_points=20):
        """
        Verifica la consistencia de la ecuación (6.5)
        """
        rb = self.core.boundary_radius()
        if rb <= 0:
            return None
        
        r_values = np.linspace(0, rb * 0.99, n_points)
        errors = []
        
        for r in r_values:
            p_direct = self.core.pressure(r)
            rho_direct = self.core.density(r)
            rho_eos = self.core.equation_of_state(p_direct)
            
            if rho_direct > 0:
                error = abs(rho_eos - rho_direct) / rho_direct * 100
                errors.append(error)
        
        return {
            'mean_error': np.mean(errors) if errors else None,
            'max_error': np.max(errors) if errors else None
        }
    
    def check_physical_conditions(self, data_df):
        """
        Verifica condiciones físicas en los datos
        """
        checks = {}
        
        # Condición de energía
        checks['energy_condition'] = (data_df['rho'] >= data_df['p']).all()
        
        # Presión no negativa
        checks['positive_pressure'] = (data_df['p'] >= 0).all()
        
        # Densidad positiva
        checks['positive_density'] = (data_df['rho'] > 0).all()
        
        # Causalidad
        if 'p_over_rho' in data_df.columns:
            checks['causality'] = (data_df['p_over_rho'] <= 1).all()
            checks['max_p_over_rho'] = data_df['p_over_rho'].max()
        
        # Monotonicidad
        checks['pressure_monotonic'] = (data_df['p'].diff().dropna() <= 0).all()
        checks['density_monotonic'] = (data_df['rho'].diff().dropna() <= 0).all()
        
        return checks


# ==============================================================================
# MÓDULO 3: GENERACIÓN DE DATOS
# ==============================================================================

class TolmanIVData:
    """
    Generación y manejo de datos para Tolman IV
    """
    
    def __init__(self, tolman_core):
        """
        Inicializa con una instancia de TolmanIVCore
        """
        self.core = tolman_core
    
    def generate_eos_data(self, n_points=100):
        """
        Genera datos de la ecuación de estado
        """
        rb = self.core.boundary_radius()
        
        if rb <= 0:
            print("⚠️  No hay solución física con borde definido")
            return pd.DataFrame()
        
        r_values = np.linspace(0, rb * 0.999, n_points)
        
        data = []
        for i, r in enumerate(r_values):
            p = self.core.pressure(r)
            rho = self.core.density(r)
            
            if p >= 0 and rho > 0:
                # Velocidad del sonido (diferencias finitas)
                if i > 0 and len(data) > 0:
                    dp = p - data[-1]['p']
                    drho = rho - data[-1]['rho']
                    cs2 = dp/drho if abs(drho) > 1e-10 else 0
                else:
                    cs2 = 0
                
                data.append({
                    'r': r,
                    'rho': rho,
                    'p': p,
                    'p_over_rho': p/rho if rho > 0 else 0,
                    'cs2': cs2
                })
        
        return pd.DataFrame(data)
    
    def save_data(self, df, output_dir='../data/tolman/', filename=None):
        """
        Guarda los datos en un archivo CSV
        """
        if filename is None:
            filename = f'tolmanIV_A{self.core.A}_R{self.core.R}.csv'
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        full_path = output_path / filename
        df.to_csv(full_path, index=False)
        
        print(f"✓ Datos guardados en: {full_path}")
        print(f"  Puntos generados: {len(df)}")
        
        return full_path


# ==============================================================================
# FUNCIÓN PRINCIPAL DE USO
# ==============================================================================

def analyze_tolman_iv(A, R, n_points=100, save_data=True):
    """
    Función conveniente para analizar una solución Tolman IV
    """
    try:
        # Crear instancias
        core = TolmanIVCore(A, R)
        analysis = TolmanIVAnalysis(core)
        data_gen = TolmanIVData(core)
        
        # Análisis
        results = analysis.analyze_solution()
        
        # Generar datos
        df = data_gen.generate_eos_data(n_points)
        
        if len(df) > 0:
            # Verificar condiciones físicas
            physical_checks = analysis.check_physical_conditions(df)
            
            # Verificar ecuación de estado
            eos_verification = analysis.verify_equation_of_state(20)
            
            # Guardar datos si se solicita
            if save_data:
                data_gen.save_data(df)
            
            return {
                'data': df,
                'analysis': results,
                'physical_checks': physical_checks,
                'eos_verification': eos_verification
            }
        else:
            return None
            
    except ValueError as e:
        print(f"✗ Error: {e}")
        return None


# ==============================================================================
# EJEMPLO DE USO
# ==============================================================================

if __name__ == "__main__":
    print("SOLUCIÓN TOLMAN IV - VERSIÓN MODULAR")
    print("="*60)
    
    # Casos de prueba
    test_cases = [
        (5.0, 10.0),  # Caso válido
        (10.0, 15.0), # Otro caso válido
    ]
    
    for A, R in test_cases:
        print(f"\n{'='*60}")
        print(f"Caso: A={A}, R={R}")
        
        result = analyze_tolman_iv(A, R, n_points=50)
        
        if result and result['eos_verification']:
            print(f"\nVerificación Ec. (6.5):")
            print(f"  Error promedio: {result['eos_verification']['mean_error']:.2e}%")
            print(f"  Error máximo: {result['eos_verification']['max_error']:.2e}%")
