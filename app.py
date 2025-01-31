import streamlit as st  # Para la interfaz web
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.cluster import KMeans
import plotly.express as px

# Configuración inicial
st.set_page_config(page_title="FinVisionPy", layout="wide")

# --- Funciones clave ---
def load_data():
    """Carga datos de presupuestos y transacciones"""
    try:
        budget = pd.read_csv("data/budget.csv")
        transactions = pd.read_csv("data/transactions.csv")
        return budget, transactions
    except FileNotFoundError:
        return pd.DataFrame(), pd.DataFrame()

def save_data(budget, transactions):
    """Guarda los datos actualizados"""
    budget.to_csv("data/budget.csv", index=False)
    transactions.to_csv("data/transactions.csv", index=False)

# --- Interfaz de Usuario ---
st.title("📊 FinVisionPy: Gestión Financiera Inteligente")

# 1. Gestión de Presupuestos
with st.expander("📋 Registrar Presupuesto"):
    category = st.selectbox("Categoría", ["Marketing", "RRHH", "TI", "Operaciones"])
    amount = st.number_input("Monto Presupuestado ($)", min_value=0)
    if st.button("Guardar Presupuesto"):
        budget, _ = load_data()
        new_entry = pd.DataFrame([[category, amount]], columns=["Categoría", "Presupuesto"])
        budget = pd.concat([budget, new_entry], ignore_index=True)
        save_data(budget, _)
        st.success("✅ Presupuesto registrado!")

# 2. Proyecciones Financieras
with st.expander("🔮 Generar Proyecciones"):
    df = load_data()[1]
    if not df.empty:
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df_prophet = df.rename(columns={'Fecha': 'ds', 'Monto': 'y'})
        model = Prophet(seasonality_mode='multiplicative')
        model.fit(df_prophet)
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)
        fig = px.line(forecast, x='ds', y='yhat', title="Proyección de Ingresos/Gastos")
        st.plotly_chart(fig)

# 3. Optimización de Gastos (K-Means)
with st.expander("⚡ Optimizar Gastos (K-Means)"):
    transactions = load_data()[1]
    
    if not transactions.empty:
        transactions['Monto'] = pd.to_numeric(transactions['Monto'], errors='coerce')
        transactions.dropna(subset=['Monto'], inplace=True)
        
        if not transactions.empty:
            # A. Calcular clusters dinámicamente según los datos disponibles
            n_clusters = min(3, len(transactions))  # Máximo 3 clusters o el número de muestras
            if n_clusters < 3:
                st.warning(f"⚠️ Insufficient data. Usando {n_clusters} clústeres.")
            
            kmeans = KMeans(n_clusters=n_clusters)  # Clusters dinámicos
            try:
                transactions['cluster'] = kmeans.fit_predict(transactions[['Monto']])
                fig = px.scatter(transactions, x='Fecha', y='Monto', color='cluster', 
                                title="Segmentación de Gastos")
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"❌ Error al optimizar gastos: {str(e)}")
        else:
            st.warning("⚠️ No hay datos válidos para optimizar.")
    else:
        st.warning("⚠️ Sube un archivo de transacciones en CSV.")

# 4. Seguimiento de Ingresos vs. Gastos
with st.expander("📈 Dashboard Financiero"):
    budget, transactions = load_data()
    if not transactions.empty:
        fig = px.bar(transactions, x='Categoría', y='Monto', color='Tipo',
                     title="Ingresos vs. Gastos por Categoría")
        st.plotly_chart(fig, use_container_width=True)

# --- Ejecutar con ---
# streamlit run app.py