import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Tolman IV Explorer",
    page_icon="🌟",
    layout="wide"
)

def load_csv_files():
    """Encuentra todos los archivos CSV de Tolman"""
    data_path = Path("../data/tolman")
    csv_files = list(data_path.glob("*.csv"))
    return {file.name: file for file in csv_files}

def load_data(file_path):
    """Carga un archivo CSV"""
    return pd.read_csv(file_path)

def create_plots(data, filename):
    """Crea las 3 gráficas principales"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Densidad vs radio
    axes[0].plot(data['r'], data['rho'], 'b-', linewidth=2)
    axes[0].set_xlabel('r')
    axes[0].set_ylabel('ρ (densidad)')
    axes[0].set_title('Densidad vs Radio')
    axes[0].grid(True, alpha=0.3)
    
    # Presión vs radio
    axes[1].plot(data['r'], data['p'], 'r-', linewidth=2)
    axes[1].set_xlabel('r')
    axes[1].set_ylabel('p (presión)')
    axes[1].set_title('Presión vs Radio')
    axes[1].grid(True, alpha=0.3)
    
    # Ecuación de estado
    axes[2].plot(data['rho'], data['p'], 'g-', linewidth=2)
    axes[2].set_xlabel('ρ (densidad)')
    axes[2].set_ylabel('p (presión)')
    axes[2].set_title('Ecuación de Estado')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# INTERFAZ PRINCIPAL
def main():
    st.title("🌟 Tolman IV Explorer")
    st.markdown("Explorador interactivo de soluciones Tolman IV")
    
    # Cargar archivos disponibles
    csv_files = load_csv_files()
    
    if not csv_files:
        st.error("❌ No se encontraron archivos CSV en ../data/tolman/")
        return
    
    # Sidebar para selección
    st.sidebar.header("📁 Seleccionar Archivo")
    selected_file = st.sidebar.selectbox(
        "Archivo CSV:",
        options=list(csv_files.keys()),
        index=0
    )
    
    # Cargar y mostrar datos
    if selected_file:
        try:
            data = load_data(csv_files[selected_file])
            
            # Información del archivo
            st.header(f"📊 {selected_file}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Puntos de datos", len(data))
            with col2:
                st.metric("ρ central", f"{data['rho'].iloc[0]:.4f}")
            with col3:
                st.metric("p central", f"{data['p'].iloc[0]:.4f}")
            
            # Gráficas
            st.subheader("📈 Gráficas")
            fig = create_plots(data, selected_file)
            st.pyplot(fig)
            
            # Verificación física básica
            st.subheader("🔍 Verificación Física")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rho_ok = (data['rho'] > 0).all()
                st.metric("Densidad positiva", "✅" if rho_ok else "❌")
            
            with col2:
                p_ok = (data['p'] >= 0).all()
                st.metric("Presión no negativa", "✅" if p_ok else "❌")
            
            with col3:
                energy_ok = (data['rho'] >= data['p']).all()
                st.metric("Condición energía", "✅" if energy_ok else "❌")
            
        except Exception as e:
            st.error(f"❌ Error cargando archivo: {e}")

if __name__ == "__main__":
    main()

