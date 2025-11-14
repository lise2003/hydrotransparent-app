import streamlit as st

st.set_page_config(
    page_title="HydroTransparent - Where Every Drop Tells a Story",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Hero Section
    st.markdown("<h1 style='text-align: center; color: #00b4db; font-size: 4rem;'>💧 HydroTransparent</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Every Rand Has a Journey. Let's Make It Count.</h2>", unsafe_allow_html=True)
    
    # Split Screen Story - Simple Version
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 The Crisis")
        st.markdown("""
        - **Corruption drains hope**
        - Families walk kilometers for water  
        - Every missing rand = fewer jobs, fewer projects
        - Communities lose trust in leadership
        """)
    
    with col2:
        st.markdown("### 🟢 The Solution") 
        st.markdown("""
        - **We track every rand**
        - Bring water directly to communities
        - Create 450+ sustainable jobs per project
        - Build trust through transparency
        """)
    
    # Impact Metrics
    st.markdown("---")
    st.markdown("## 📊 The Impact: From Crisis to Hope")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Water Access", "42% → 85%", "+43%")
    
    with col2:
        st.metric("Cost Reduction", "30%", "Anti-corruption")
    
    with col3:
        st.metric("Jobs Created", "450+", "Per project")
    
    with col4:
        st.metric("Economic Stimulus", "ZAR 85M", "Annual")
    
    # Call to Action
    st.markdown("---")
    st.markdown("## 🚀 Ready to Build a Water-Secure Future?")
    
    st.info("""
    **💡 How to navigate:** Use the **sidebar on the left** to explore all features:
    
    - **🏠 Province Map** - Start here! Explore water data by region
    - **💧 Water Solutions** - Browse engineering options  
    - **🔧 3D Equipment** - View sensor visualizations
    - **💰 Cost Calculator** - Get project cost estimates
    - **📊 Water Quality** - Check SAN 241 compliance
    - **📋 Financial Transparency** - Track every rand
    """)
    
    # Quick navigation buttons
    st.markdown("### 🎯 Quick Start")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌍 Start with Province Map", use_container_width=True, type="primary"):
            st.success("Click '🏠 Province Map' in the sidebar to begin!")
    
    with col2:
        if st.button("💧 Browse All Solutions", use_container_width=True):
            st.success("Explore all features using the sidebar navigation!")
    
    # Final message
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #e0f7fa; font-style: italic;'>
        <p>"When every rand is traceable, corruption cannot hide. When every transaction is public, trust is rebuilt.</p>
        <p>When communities can see where money flows, hope returns. This is the HydroTransparent promise."</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
