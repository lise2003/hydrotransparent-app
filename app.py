import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="HydroTransparent",
    page_icon="💧",
    layout="wide"
)

# Initialize session state
if 'selected_province' not in st.session_state:
    st.session_state.selected_province = None

st.title("💧 HydroTransparent")
st.markdown("**Powered by IBM Z & LinuxONE**")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌍 South Africa's Water Crisis")
    st.write("""
    - **Rural areas**: Families walk kilometers for clean water
    - **Urban suburbs**: Frequent water cuts despite large budgets  
    - **Corruption drains hope** from communities
    - **Every missing rand** = fewer jobs, fewer projects, fewer drops of water
    """)
    
    st.subheader("💡 Our Solution")
    st.write("""
    **HydroTransparent** creates a tamper-proof system that:
    - Tracks every rand and every drop
    - Eliminates corruption through transparency
    - Provides real water solutions for rural areas
    - Creates sustainable local employment
    """)

with col2:
    st.success("""
    ### 🎯 Key Impacts
    **Water Access**: 42% → 85%
    
    **Cost Reduction**: 30% savings
    
    **Employment**: 450+ jobs per project
    
    **Economic Effect**: ZAR 85M annual stimulus
    """)
    
    st.info("""
    ### 🚀 Get Started
    1. Go to **Province Map**
    2. Select a province
    3. Explore water solutions
    4. See costs and impacts
    """)

st.markdown("---")
st.caption("HydroTransparent - A CPUT & IBM Z Initiative | 'When every rand is traceable, every drop becomes possible.'")
