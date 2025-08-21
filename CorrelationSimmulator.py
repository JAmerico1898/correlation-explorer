import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Explorador de Correlação", layout="wide")

# Título e introdução
st.title("📊 Explorador Interativo de Correlação")
st.markdown("""
    Descubra por que a correlação nem sempre é a melhor maneira de entender relações nos dados! 
    Esta ferramenta interativa mostra três casos importantes onde olhar apenas a correlação pode nos enganar.
""")

# Funções auxiliares
def generate_correlated_data(correlation, n_points=150):
    """Gera dados correlacionados usando transformação Box-Muller"""
    x = np.random.normal(0, 1, n_points)
    eps = np.random.normal(0, 1, n_points)
    y = correlation * x + np.sqrt(1 - correlation**2) * eps
    return pd.DataFrame({'x': x, 'y': y})

def generate_curved_data(curvature=1.0, n_points=150):
    """Gera dados em formato de U"""
    x = np.random.uniform(-2, 2, n_points)
    noise = np.random.normal(0, 0.1, n_points)
    y = (curvature**2) * x**2 + noise - 2
    return pd.DataFrame({'x': x, 'y': y})

def generate_simpsons_data(slope_diff=-1, n_points=150):
    """Gera dados do paradoxo de Simpson"""
    # Grupo A
    n_a = n_points // 2
    x_a = np.random.uniform(0, 5, n_a)
    y_a = x_a + np.random.normal(0, 0.5, n_a)
    df_a = pd.DataFrame({'x': x_a, 'y': y_a, 'group': 'Grupo A'})
    
    # Grupo B
    n_b = n_points - n_a
    x_b = np.random.uniform(4, 9, n_b)
    y_b = slope_diff * (x_b - 4) + 5 + np.random.normal(0, 0.5, n_b)
    df_b = pd.DataFrame({'x': x_b, 'y': y_b, 'group': 'Grupo B'})
    
    return pd.concat([df_a, df_b])

# Abas para diferentes cenários
tab1, tab2 = st.tabs(["Correlação Linear", "Padrões Não-lineares"])

# Aba 1: Correlação Linear
with tab1:
    st.header("1️⃣ Correlação Linear")
    st.markdown("""
        Mova o controle deslizante para ver como diferentes valores de correlação afetam o gráfico de dispersão.
        Note que mesmo com o mesmo alvo de correlação, cada amostra aleatória parece ligeiramente diferente!
    """)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        correlation = st.slider("Correlação Alvo", -1.0, 1.0, 0.0, 0.1)
        if st.button("🎲 Gerar Nova Amostra"):
            st.session_state.linear_data = generate_correlated_data(correlation)
    
    # Inicializar ou atualizar dados
    if 'linear_data' not in st.session_state:
        st.session_state.linear_data = generate_correlated_data(correlation)
    
    # Gráfico
    fig = px.scatter(st.session_state.linear_data, x='x', y='y', 
                     title=f"Correlação da Amostra: {st.session_state.linear_data['x'].corr(st.session_state.linear_data['y']):.2f}")
    st.plotly_chart(fig, use_container_width=True)

# Aba 2: Padrões Não-lineares
with tab2:
    st.header("2️⃣ Padrões Não-lineares (A Forma de U)")
    st.markdown("""
        Aqui é onde a correlação pode nos enganar! Estes dados mostram um padrão claro em forma de U,
        mas a correlação pode estar próxima de zero. Ajuste a curvatura para ver como o padrão muda.
    """)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        curvature = st.slider("Curvatura", 0.1, 2.0, 1.0, 0.1)
        if st.button("🎲 Gerar Nova Forma de U"):
            st.session_state.curved_data = generate_curved_data(curvature)
    
    # Inicializar ou atualizar dados
    if 'curved_data' not in st.session_state:
        st.session_state.curved_data = generate_curved_data(curvature)
    
    # Gráfico
    fig = px.scatter(st.session_state.curved_data, x='x', y='y',
                     title=f"Correlação: {st.session_state.curved_data['x'].corr(st.session_state.curved_data['y']):.2f}")
    fig.update_layout(
        yaxis=dict(range=[-3, 8]),
        xaxis=dict(range=[-2.5, 2.5])
    )    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("📌 Mesmo havendo um padrão claro, a correlação está próxima de zero! Isso mostra por que devemos sempre visualizar nossos dados.")


# Principais Conclusões
st.divider()
st.header("🎯 Principais Conclusões")
st.markdown("""
* 📊 A correlação mede apenas relações **lineares**
* 🔄 Uma forma de U perfeita pode ter correlação zero apesar de um padrão claro
* 🎯 Diferentes grupos nos seus dados podem mostrar padrões opostos
* 👀 Sempre visualize seus dados - não confie apenas em estatísticas resumidas!
* 🤔 Correlação não implica causalidade
""")

# Adicionar um rodapé divertido
# Rodapé
st.divider()
st.caption("2025 Ferramenta de Ensino de Correlação | Desenvolvida para fins educacionais")
st.caption("Prof. José Américo — Coppead/UCAM")