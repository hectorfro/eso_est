# tolmanIV_complete.py
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

class TolmanIV:
    def __init__(self, A, R):
        """
        Solución Tolman IV completa
        Para que sea física, debe cumplirse R > A
        
        Parámetros:
        -----------
        A : float
            Parámetro A de la solución
        R : float
            Parámetro R de la solución (debe ser > A)
        """
        self.A = A
        self.R = R
        
        # Verificar condición de validez física
        if R <= A:
            raise ValueError(f"R debe ser > A para solución física. Dados: R={R}, A={A}")
        
        # Verificar condición para presión central positiva
        if R >= np.sqrt(3) * A:
            print(f"⚠️  Advertencia: Para pc(0)>0 se necesita R < √3*A = {np.sqrt(3)*A:.3f}")
            print(f"   Valor actual: R = {R}")
            
    def pressure(self, r):
        """
        Presión según Tolman IV - Ecuación (6.3) del paper
        8πp = (1/A²)(1 - A²/R² - 3r²/R²)
        """
        r2 = r**2
        A2 = self.A**2
        R2 = self.R**2
        
        eight_pi_p = (1/A2) * (1 - A2/R2 - 3*r2/R2)/(1 + 2*r2/A2)
        
        return eight_pi_p / (8 * np.pi)
    
    def density(self, r):
        """
        Densidad según Tolman IV - Ecuación (6.2) del paper
        8πρ = (1/A²)(1 + 3A²/R² + 3r²/R²) + (2/A²) * (1-r²/R²)/(1+2r²/A²)
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
        8πρc = 3/A² + 3/R²
        8πpc = 1/A² - 1/R²
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
        rb = (R/3^(1/2)) * (1 - A²/R²)^(1/2)
        """
        A2 = self.A**2
        R2 = self.R**2
        
        if A2/R2 >= 1:
            return 0  # No hay solución física
        
        rb = (self.R / np.sqrt(3)) * np.sqrt(1 - A2/R2)
        return rb
    
    def boundary_density(self):
        """
        Densidad en el borde (donde p=0)
        """
        rb = self.boundary_radius()
        if rb > 0:
            return self.density(rb)
        return None
    
    def analyze_solution(self):
        """
        Análisis completo de la solución
        """
        print("="*60)
        print("ANÁLISIS DE LA SOLUCIÓN TOLMAN IV")
        print("="*60)
        print(f"Parámetros: A = {self.A}, R = {self.R}")
        print(f"Razón R/A = {self.R/self.A:.3f}")
        print()
        
        # Condiciones de validez
        print("Condiciones de validez:")
        print(f"  • R > A: {'✓' if self.R > self.A else '✗'}")
        print(f"  • R < √3*A para pc>0: {'✓' if self.R < np.sqrt(3)*self.A else '✗'}")
        print()
        
        # Valores centrales
        rho_c, p_c = self.central_values()
        print("Valores centrales (r=0):")
        print(f"  • ρ(0) = {rho_c:.4e}")
        print(f"  • p(0) = {p_c:.4e}")
        print(f"  • p(0)/ρ(0) = {p_c/rho_c:.4f}" if rho_c > 0 else "  • p(0)/ρ(0) = indefinido")
        print()
        
        # Valores por método directo (verificación)
        rho_0_direct = self.density(0)
        p_0_direct = self.pressure(0)
        print("Verificación (evaluación directa en r=0):")
        print(f"  • ρ(0) = {rho_0_direct:.4e}")
        print(f"  • p(0) = {p_0_direct:.4e}")
        print()
        
        # Radio del borde
        rb = self.boundary_radius()
        if rb > 0:
            rho_b = self.boundary_density()
            print(f"Radio del borde (donde p=0):")
            print(f"  • rb = {rb:.4f}")
            print(f"  • ρ(rb) = {rho_b:.4e}")
            print(f"  • p(rb) = {self.pressure(rb):.4e} (debe ser ≈0)")
        else:
            print("No existe radio de borde físico")
        
        return {
            'rho_c': rho_c,
            'p_c': p_c,
            'rb': rb,
            'rho_b': self.boundary_density() if rb > 0 else None
        }
    
    def generate_eos_data(self, n_points=100):
        """
        Genera datos de la ecuación de estado
        """
        rb = self.boundary_radius()
        
        if rb <= 0:
            print("⚠️  No hay solución física con borde definido")
            return pd.DataFrame()
        
        # Generar puntos desde el centro hasta el borde
        r_values = np.linspace(0, rb * 0.999, n_points)
        
        data = []
        for r in r_values:
            p = self.pressure(r)
            rho = self.density(r)
            
            # Solo incluir valores físicos
            if p >= 0 and rho > 0:
                # Calcular velocidad del sonido
                if len(data) > 0:
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
    
    def plot_solution(self, save_path=None):
        """
        Grafica la solución
        """
        df = self.generate_eos_data(200)
        
        if len(df) == 0:
            print("No hay datos para graficar")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Presión vs radio
        ax = axes[0, 0]
        ax.plot(df['r'], df['p'], 'b-', linewidth=2)
        ax.set_xlabel('r')
        ax.set_ylabel('p')
        ax.set_title('Presión vs Radio')
        ax.grid(True, alpha=0.3)
        
        # Densidad vs radio
        ax = axes[0, 1]
        ax.plot(df['r'], df['rho'], 'r-', linewidth=2)
        ax.set_xlabel('r')
        ax.set_ylabel('ρ')
        ax.set_title('Densidad vs Radio')
        ax.grid(True, alpha=0.3)
        
        # Ecuación de estado
        ax = axes[1, 0]
        ax.plot(df['rho'], df['p'], 'g-', linewidth=2)
        ax.set_xlabel('ρ')
        ax.set_ylabel('p')
        ax.set_title('Ecuación de Estado')
        ax.grid(True, alpha=0.3)
        
        # p/ρ vs radio
        ax = axes[1, 1]
        ax.plot(df['r'], df['p_over_rho'], 'm-', linewidth=2)
        ax.axhline(y=1/3, color='k', linestyle='--', alpha=0.5, label='p/ρ = 1/3')
        ax.set_xlabel('r')
        ax.set_ylabel('p/ρ')
        ax.set_title('Razón Presión/Densidad vs Radio')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.suptitle(f'Solución Tolman IV: A={self.A}, R={self.R}')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Gráfica guardada en: {save_path}")
        
        plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    print("SOLUCIÓN TOLMAN IV - ANÁLISIS COMPLETO")
    print("="*60)
    
    # Casos de prueba con diferentes valores de A y R
    test_cases = [
        (1.0, 1.5),   # R < √3*A ✓ (presión central positiva)
        (1.0, 1.7),   # R ≈ √3*A (presión central casi cero)
        (1.0, 2.0),   # R > √3*A (presión central negativa)
        (5.0, 10.0),  # Caso sugerido en documentos
        (10.0, 15.0), # R < √3*A ✓ (escala mayor)
    ]
    
    for A, R in test_cases:
        print(f"\n{'='*60}")
        print(f"Caso: A={A}, R={R}")
        
        try:
            tolman = TolmanIV(A, R)
            
            # Análisis completo
            results = tolman.analyze_solution()
            
            # Generar datos
            df = tolman.generate_eos_data(50)
            
            if len(df) > 0:
                # Guardar datos
                script_dir = Path(__file__).parent
                project_dir = script_dir.parent
                output_file = project_dir / 'data' / 'tolman' / f'tolmanIV_A{A}_R{R}_complete.csv'
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                df.to_csv(output_file, index=False)
                print(f"\n✓ Datos guardados en: {output_file}")
                print(f"  Puntos generados: {len(df)}")
                
                # Graficar
                plot_file = project_dir / 'plots' / f'tolmanIV_A{A}_R{R}.png'
                plot_file.parent.mkdir(parents=True, exist_ok=True)
                tolman.plot_solution(save_path=plot_file)
                
        except ValueError as e:
            print(f"✗ Error: {e}")
