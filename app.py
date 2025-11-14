import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="HydroTransparent",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/lise2003/hydrotransparent-app',
        'Report a bug': "https://github.com/lise2003/hydrotransparent-app/issues",
        'About': "# HydroTransparent - Water Management Solution"
    }
)

def main():
    st.title("💧 HydroTransparent")
    st.markdown("""
    Welcome to HydroTransparent - Your comprehensive water management solution.
    
    **Navigate through the pages using the sidebar** to explore:
    - 🏠 Province-level water service maps
    - 💧 Water solutions and technologies  
    - 🔧 3D equipment visualization
    - 💰 Cost estimation tools
    - 📊 Water quality analysis
    - 📋 Financial transparency reports
    """)
    
    # Fixed button
    if st.button("🚀 See How It Works", type="primary", use_container_width=True):
        st.success("Use the sidebar on the left to navigate between pages!")

if __name__ == "__main__":
    main()
