import streamlit as st
import pandas as pd

st.set_page_config(page_title="Water Solutions", layout="wide")

st.title("💧 Water Supply Solutions")
st.markdown("**Permanent, Innovative Solutions for Rural South Africa**")

# Check if province is selected
if 'selected_province' not in st.session_state:
    st.warning("👈 Please select a province first on the Province Map page")
    st.stop()

selected_province = st.session_state.selected_province
st.success(f"🎯 Showing solutions for: **{selected_province}**")

# Your 12 Water Solutions Database
water_solutions = {
    "low_tech": [
        {
            "id": "solar_borehole",
            "name": "Community Solar Boreholes with Smart Meters",
            "description": "Drill boreholes + install solar-powered pumps with prepaid smart meters to manage usage and prevent over-extraction.",
            "cost_per_beneficiary": 2500,
            "implementation_time": "3-6 months",
            "lifespan": "20+ years",
            "maintenance": "Low",
            "jobs_created": 15,
            "suitable_for": "Areas with groundwater potential"
        },
        {
            "id": "managed_aquifer",
            "name": "Managed Aquifer Recharge (MAR)",
            "description": "Store water underground during rainy seasons using recharge basins and extract during dry periods.",
            "cost_per_beneficiary": 1800,
            "implementation_time": "6-12 months", 
            "lifespan": "30+ years",
            "maintenance": "Medium",
            "jobs_created": 12,
            "suitable_for": "Areas with seasonal rainfall"
        }
    ],
    "high_tech": [
        {
            "id": "water_treatment_pods",
            "name": "Decentralised Community Water Treatment Pods",
            "description": "Modular 'treatment-in-a-box' units that run on solar power and treat river/dam water to drinking standards.",
            "cost_per_beneficiary": 3200,
            "implementation_time": "2-4 months",
            "lifespan": "15+ years", 
            "maintenance": "Medium",
            "jobs_created": 8,
            "suitable_for": "Areas using river/stream water"
        },
        {
            "id": "atmospheric_water",
            "name": "Atmospheric Water Generators (Community-Scale)",
            "description": "Machines that pull water from air using solar power, producing 500-3,000 L/day where humidity > 40%.",
            "cost_per_beneficiary": 4500,
            "implementation_time": "1-3 months",
            "lifespan": "10+ years",
            "maintenance": "High", 
            "jobs_created": 6,
            "suitable_for": "Coastal and high-humidity areas"
        }
    ]
}

# Solution Selection
st.subheader("🔧 Choose Your Water Solution Type")

solution_type = st.radio(
    "Select solution category:",
    ["🚜 Low-Tech Permanent", "⚡ High-Tech Advanced", "🌱 Nature-Based", "🚰 Large Infrastructure"],
    horizontal=True
)

# Show solutions based on selection
if "Low-Tech" in solution_type:
    solutions = water_solutions["low_tech"]
    st.info("💡 **Low-Tech Solutions**: Quick to deploy, low maintenance, community-managed")
else:
    solutions = water_solutions["high_tech"] 
    st.info("💡 **High-Tech Solutions**: Advanced features, higher capacity, tech-supported")

# Display solutions
for solution in solutions:
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"🔧 {solution['name']}")
        st.write(solution['description'])
        st.write(f"**Suitable for**: {solution['suitable_for']}")
        
    with col2:
        st.metric("Cost per Person", f"ZAR {solution['cost_per_beneficiary']:,}")
        st.metric("Jobs Created", solution['jobs_created'])
        st.metric("Lifespan", solution['lifespan'])
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"📊 View Details", key=f"detail_{solution['id']}"):
            st.session_state.selected_solution = solution
    with col2:
        if st.button(f"💰 Cost Calculator", key=f"cost_{solution['id']}"):
            st.session_state.selected_solution = solution
    with col3:
        if st.button(f"🛠️ Select Solution", key=f"select_{solution['id']}"):
            st.session_state.selected_solution = solution
            st.success(f"✅ {solution['name']} selected!")

# Next steps
st.markdown("---")
st.subheader("🚀 Next Steps")

st.write("""
1. **Select a solution** that fits your community's needs
2. **View detailed specifications** and requirements  
3. **Calculate exact costs** for your specific situation
4. **See employment opportunities** for local community
5. **Check water quality compliance** with SAN 241 standards
""")

st.info("💡 **Pro Tip**: Start with low-tech solutions for quick impact, then add high-tech features for long-term sustainability")