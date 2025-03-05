import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Correlation Explorer", layout="wide")

# Title and introduction
st.title("📊 Interactive Correlation Explorer")
st.markdown("""
    Discover why correlation isn't always the best way to understand relationships in data! 
    This interactive tool will show you three important cases where looking at correlation alone might mislead you.
""")

# Helper functions
def generate_correlated_data(correlation, n_points=150):
    """Generate correlated data using Box-Muller transform"""
    x = np.random.normal(0, 1, n_points)
    eps = np.random.normal(0, 1, n_points)
    y = correlation * x + np.sqrt(1 - correlation**2) * eps
    return pd.DataFrame({'x': x, 'y': y})

def generate_curved_data(curvature=1.0, n_points=150):
    """Generate U-shaped data"""
    x = np.random.uniform(-2, 2, n_points)
    noise = np.random.normal(0, 0.1, n_points)
    y = curvature * x**2 + noise - 2
    return pd.DataFrame({'x': x, 'y': y})

def generate_simpsons_data(slope_diff=-1, n_points=150):
    """Generate Simpson's paradox data"""
    # Group A
    n_a = n_points // 2
    x_a = np.random.uniform(0, 5, n_a)
    y_a = x_a + np.random.normal(0, 0.5, n_a)
    df_a = pd.DataFrame({'x': x_a, 'y': y_a, 'group': 'Group A'})
    
    # Group B
    n_b = n_points - n_a
    x_b = np.random.uniform(4, 9, n_b)
    y_b = slope_diff * (x_b - 4) + 5 + np.random.normal(0, 0.5, n_b)
    df_b = pd.DataFrame({'x': x_b, 'y': y_b, 'group': 'Group B'})
    
    return pd.concat([df_a, df_b])

# Tabs for different scenarios
tab1, tab2, tab3 = st.tabs(["Linear Correlation", "Non-linear Patterns", "Simpson's Paradox"])

# Tab 1: Linear Correlation
with tab1:
    st.header("1️⃣ Linear Correlation")
    st.markdown("""
        Move the slider to see how different correlation values affect the scatter plot.
        Notice that even with the same correlation target, each random sample looks slightly different!
    """)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        correlation = st.slider("Target Correlation", -1.0, 1.0, 0.0, 0.1)
        if st.button("🎲 Generate New Sample"):
            st.session_state.linear_data = generate_correlated_data(correlation)
    
    # Initialize or update data
    if 'linear_data' not in st.session_state:
        st.session_state.linear_data = generate_correlated_data(correlation)
    
    # Plot
    fig = px.scatter(st.session_state.linear_data, x='x', y='y', 
                     title=f"Sample Correlation: {st.session_state.linear_data['x'].corr(st.session_state.linear_data['y']):.2f}")
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Non-linear Patterns
with tab2:
    st.header("2️⃣ Non-linear Patterns (The U-Shape)")
    st.markdown("""
        Here's where correlation can trick us! This data shows a clear U-shaped pattern,
        but the correlation might be close to zero. Adjust the curvature to see how the pattern changes.
    """)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        curvature = st.slider("Curvature", 0.1, 2.0, 1.0, 0.1)
        if st.button("🎲 Generate New U-Shape"):
            st.session_state.curved_data = generate_curved_data(curvature)
    
    # Initialize or update data
    if 'curved_data' not in st.session_state:
        st.session_state.curved_data = generate_curved_data(curvature)
    
    # Plot
    fig = px.scatter(st.session_state.curved_data, x='x', y='y',
                     title=f"Correlation: {st.session_state.curved_data['x'].corr(st.session_state.curved_data['y']):.2f}")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("📌 Even though there's a clear pattern, the correlation is near zero! This shows why we should always visualize our data.")

# Tab 3: Simpson's Paradox
with tab3:
    st.header("3️⃣ Simpson's Paradox")
    st.markdown("""
        ### Understanding Simpson's Paradox
        
        Simpson's Paradox is a fascinating statistical phenomenon where a trend that appears in several groups disappears or reverses when the groups are combined. Here's a real-world example:

        🏥 **The Medical School Example:**
        - A medical school's admission data showed they accepted a higher percentage of men than women overall
        - But when looking at each department separately, they actually accepted a higher percentage of women in EVERY department!
        - How? Women applied more to competitive departments with lower acceptance rates
        - Men applied more to less competitive departments with higher acceptance rates
        
        In our interactive plot below:
        - Group A (orange) and Group B (blue) each show positive trends
        - But when you look at all the data together, you might see a negative trend!
        - This happens because Group B is shifted up and right from Group A
        
        Try adjusting the slope to see how the overall pattern can differ from the individual group patterns.
    """)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        slope_diff = st.slider("Group B Slope", -2.0, 2.0, -1.0, 0.1)
        if st.button("🎲 Generate New Groups"):
            st.session_state.simpson_data = generate_simpsons_data(slope_diff)
    
    # Initialize or update data
    if 'simpson_data' not in st.session_state:
        st.session_state.simpson_data = generate_simpsons_data(slope_diff)
    
    # Calculate correlations
    overall_corr = st.session_state.simpson_data['x'].corr(st.session_state.simpson_data['y'])
    group_a = st.session_state.simpson_data[st.session_state.simpson_data['group'] == 'Group A']
    group_b = st.session_state.simpson_data[st.session_state.simpson_data['group'] == 'Group B']
    corr_a = group_a['x'].corr(group_a['y'])
    corr_b = group_b['x'].corr(group_b['y'])
    
    # Plot
    fig = px.scatter(st.session_state.simpson_data, x='x', y='y', color='group',
                     title=f"Overall Correlation: {overall_corr:.2f}")
    st.plotly_chart(fig, use_container_width=True)
    
    # Show correlations
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Correlation", f"{overall_corr:.2f}")
    col2.metric("Group A Correlation", f"{corr_a:.2f}")
    col3.metric("Group B Correlation", f"{corr_b:.2f}")
    
    st.info("""
        📌 **What to Notice:**
        1. Look at the correlations above. Each group (A and B) might show positive correlations
        2. But the overall correlation can be very different or even negative!
        3. This is why it's crucial to check if your data contains distinct groups before drawing conclusions
    """)

# Key Takeaways
st.divider()
st.header("🎯 Key Takeaways")
st.markdown("""
* 📊 Correlation only measures **linear** relationships
* 🔄 A perfect U-shape can have zero correlation despite a clear pattern
* 🎯 Different groups in your data might show opposite patterns
* 👀 Always visualize your data - don't trust summary statistics alone!
* 🤔 Correlation doesn't imply causation
""")

# Add a fun footer
# Footer
st.divider()
st.caption("© 2025 Correlation Teaching Tool | Developed for educational purposes")
st.caption("Prof. José Américo – Coppead")
