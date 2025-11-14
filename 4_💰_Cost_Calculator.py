import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Cost Calculator", layout="wide")

st.title("💰 Project Cost Calculator")
st.markdown("**Engineering Cost Correlations & Detailed Budget Analysis**")

class WaterProjectCostCalculator:
    def __init__(self):
        # Chemical engineering cost correlations
        self.equipment_factors = {
            "pumps": {"a": 5000, "b": 120, "c": 0.6},
            "tanks": {"k": 800, "exp": 0.7},
            "filters": {"k": 1500, "exp": 0.8},
            "membranes": {"k1": 200, "k2": 5000, "k3": 8000},
            "piping": {"cost_per_m": 150, "fitting_factor": 1.4},
            "solar_panels": {"cost_per_watt": 12},
            "sensors": {"base_cost": 5000, "per_unit": 2500}
        }
        
        # Material cost factors
        self.material_factors = {
            "HDPE": 1.0,
            "SS304": 2.5,
            "SS316": 3.2,
            "PVC": 0.8,
            "FRP": 1.8
        }
    
    def calculate_pump_cost(self, flow_rate_m3h, material="SS304"):
        """Pump cost correlation: C = a + b(Q)^c"""
        factors = self.equipment_factors["pumps"]
        base_cost = factors["a"] + factors["b"] * (flow_rate_m3h ** factors["c"])
        material_factor = self.material_factors.get(material, 1.0)
        return base_cost * material_factor
    
    def calculate_tank_cost(self, volume_m3, material="HDPE"):
        """Tank cost correlation: C = k * V^exp"""
        factors = self.equipment_factors["tanks"]
        base_cost = factors["k"] * (volume_m3 ** factors["exp"])
        material_factor = self.material_factors.get(material, 1.0)
        return base_cost * material_factor
    
    def calculate_membrane_system_cost(self, membrane_area_m2, flow_rate_m3h):
        """Membrane system: C = k1*A + k2*controls + k3*pumps"""
        factors = self.equipment_factors["membranes"]
        return (factors["k1"] * membrane_area_m2 + 
                factors["k2"] +  # controls
                self.calculate_pump_cost(flow_rate_m3h))
    
    def calculate_piping_cost(self, length_m, diameter_mm, material="HDPE"):
        """Piping cost with fittings"""
        factors = self.equipment_factors["piping"]
        base_cost = length_m * factors["cost_per_m"] * (diameter_mm / 50)  # Scale with diameter
        material_factor = self.material_factors.get(material, 1.0)
        return base_cost * material_factor * factors["fitting_factor"]
    
    def calculate_solar_system_cost(self, power_watts):
        """Solar system cost"""
        factors = self.equipment_factors["solar_panels"]
        return power_watts * factors["cost_per_watt"]
    
    def calculate_sensor_network_cost(self, num_sensors):
        """Sensor network cost"""
        factors = self.equipment_factors["sensors"]
        return factors["base_cost"] + (num_sensors * factors["per_unit"])
    
    def calculate_installation_cost(self, equipment_cost, complexity="medium"):
        """Installation factors based on complexity"""
        installation_factors = {
            "simple": 1.3,
            "medium": 1.8,
            "complex": 2.5
        }
        return equipment_cost * (installation_factors.get(complexity, 1.8) - 1)
    
    def calculate_operating_costs(self, equipment_cost, flow_rate_m3d, electricity_cost=2.5):
        """Annual operating costs"""
        # Electricity for pumps (assuming 8 hours operation)
        pump_power_kw = (flow_rate_m3d * 20) / (3.6 * 0.7 * 0.9)  # Simplified pump power calculation
        annual_electricity = pump_power_kw * 8 * 365 * electricity_cost / 1000
        
        # Chemicals (simplified)
        chemical_cost = flow_rate_m3d * 0.5 * 365
        
        # Maintenance (3-5% of equipment cost)
        maintenance_cost = equipment_cost * 0.04
        
        # Labor (2 operators)
        labor_cost = 120000 * 2  # Annual salary for 2 operators
        
        return {
            "electricity": annual_electricity,
            "chemicals": chemical_cost,
            "maintenance": maintenance_cost,
            "labor": labor_cost,
            "total_annual": annual_electricity + chemical_cost + maintenance_cost + labor_cost
        }

# Initialize calculator
calculator = WaterProjectCostCalculator()

st.header("🔧 Project Configuration")

# Project type selection
project_type = st.selectbox(
    "Select Project Type:",
    ["Solar Borehole System", "Water Treatment Pod", "Distribution Network", "Sensor Monitoring System", "Custom Project"]
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏗️ System Specifications")
    
    # Common parameters
    daily_demand = st.number_input("Daily Water Demand (m³/day)", min_value=10, max_value=10000, value=500, step=50)
    flow_rate = daily_demand / 24  # m³/hour
    
    if project_type == "Solar Borehole System":
        borehole_depth = st.number_input("Borehole Depth (m)", min_value=20, max_value=500, value=150, step=10)
        tank_volume = st.number_input("Storage Tank Volume (m³)", min_value=10, max_value=500, value=50, step=10)
        solar_power = st.number_input("Solar Power Required (W)", min_value=1000, max_value=20000, value=5000, step=500)
        
    elif project_type == "Water Treatment Pod":
        treatment_capacity = st.number_input("Treatment Capacity (m³/hour)", min_value=1, max_value=100, value=20, step=1)
        membrane_area = st.number_input("Membrane Area (m²)", min_value=10, max_value=1000, value=200, step=10)
        
    elif project_type == "Distribution Network":
        pipe_length = st.number_input("Pipeline Length (m)", min_value=100, max_value=50000, value=5000, step=100)
        pipe_diameter = st.selectbox("Pipe Diameter (mm)", [50, 75, 100, 150, 200], index=2)
        
    elif project_type == "Sensor Monitoring System":
        num_sensors = st.number_input("Number of Sensors", min_value=5, max_value=200, value=20, step=5)
        monitoring_points = st.number_input("Monitoring Points", min_value=1, max_value=50, value=10, step=1)

with col2:
    st.subheader("⚙️ Engineering Parameters")
    
    material_type = st.selectbox("Primary Material", ["HDPE", "SS304", "SS316", "PVC", "FRP"])
    installation_complexity = st.selectbox("Installation Complexity", ["simple", "medium", "complex"])
    
    # Economic parameters
    electricity_tariff = st.number_input("Electricity Cost (ZAR/kWh)", min_value=1.0, max_value=5.0, value=2.5, step=0.1)
    project_lifespan = st.number_input("Project Lifespan (years)", min_value=5, max_value=30, value=20, step=1)
    annual_inflation = st.number_input("Annual Inflation Rate (%)", min_value=0.0, max_value=10.0, value=6.5, step=0.1) / 100

# Calculate costs
if st.button("🧮 Calculate Detailed Costs", type="primary"):
    with st.spinner("Running engineering cost calculations..."):
        
        # Initialize cost breakdown
        equipment_costs = {}
        total_equipment_cost = 0
        
        # Calculate based on project type
        if project_type == "Solar Borehole System":
            equipment_costs["Solar Pump"] = calculator.calculate_pump_cost(flow_rate, material_type)
            equipment_costs["Storage Tank"] = calculator.calculate_tank_cost(tank_volume, "HDPE")
            equipment_costs["Solar Power System"] = calculator.calculate_solar_system_cost(solar_power)
            equipment_costs["Borehole Drilling"] = borehole_depth * 800  # ZAR per meter
            
        elif project_type == "Water Treatment Pod":
            equipment_costs["Membrane System"] = calculator.calculate_membrane_system_cost(membrane_area, treatment_capacity)
            equipment_costs["Chemical Dosing"] = treatment_capacity * 5000
            equipment_costs["Control System"] = 75000
            equipment_costs["Piping & Valves"] = calculator.calculate_piping_cost(50, 100, material_type)
            
        elif project_type == "Distribution Network":
            equipment_costs["Pipeline Network"] = calculator.calculate_piping_cost(pipe_length, pipe_diameter, material_type)
            equipment_costs["Distribution Pumps"] = calculator.calculate_pump_cost(flow_rate, material_type)
            equipment_costs["Storage Tanks"] = calculator.calculate_tank_cost(daily_demand/2, "HDPE")  # Half daily demand
            
        elif project_type == "Sensor Monitoring System":
            equipment_costs["Sensor Network"] = calculator.calculate_sensor_network_cost(num_sensors)
            equipment_costs["Data System"] = 45000
            equipment_costs["Installation"] = num_sensors * 1500
            
        # Add common equipment
        equipment_costs["Instrumentation"] = total_equipment_cost * 0.15
        equipment_costs["Electrical Systems"] = total_equipment_cost * 0.12
        equipment_costs["Civil Works"] = total_equipment_cost * 0.25
        
        # Calculate totals
        total_equipment_cost = sum(equipment_costs.values())
        installation_cost = calculator.calculate_installation_cost(total_equipment_cost, installation_complexity)
        total_installed_cost = total_equipment_cost + installation_cost
        
        # Operating costs
        operating_costs = calculator.calculate_operating_costs(total_installed_cost, daily_demand, electricity_tariff)
        
        # Display Results
        st.header("📊 Cost Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Equipment Cost", f"ZAR {total_equipment_cost:,.0f}")
            st.metric("Installation Cost", f"ZAR {installation_cost:,.0f}")
            
        with col2:
            st.metric("Total Installed Cost", f"ZAR {total_installed_cost:,.0f}")
            st.metric("Cost per m³ Water", f"ZAR {total_installed_cost/daily_demand:,.2f}")
            
        with col3:
            st.metric("Annual Operating Cost", f"ZAR {operating_costs['total_annual']:,.0f}")
            st.metric("Cost per m³ (O&M)", f"ZAR {operating_costs['total_annual']/(daily_demand*365):,.2f}")
        
        # Equipment Cost Breakdown Chart
        st.subheader("📈 Equipment Cost Distribution")
        
        equipment_df = pd.DataFrame({
            'Category': list(equipment_costs.keys()),
            'Cost (ZAR)': list(equipment_costs.values())
        })
        
        fig_pie = px.pie(equipment_df, values='Cost (ZAR)', names='Category', 
                        title='Equipment Cost Breakdown')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Detailed Cost Table
        st.subheader("📋 Detailed Cost Analysis")
        
        detailed_costs = []
        for category, cost in equipment_costs.items():
            detailed_costs.append({
                'Category': category,
                'Bare Equipment Cost': cost,
                'Installation Factor': calculator.equipment_factors["piping"]["fitting_factor"],
                'Installed Cost': cost * calculator.equipment_factors["piping"]["fitting_factor"],
                'Percentage': (cost / total_equipment_cost) * 100
            })
        
        detailed_df = pd.DataFrame(detailed_costs)
        st.dataframe(detailed_df, use_container_width=True)
        
        # Operating Cost Breakdown
        st.subheader("🔧 Operating & Maintenance Costs")
        
        op_ex_df = pd.DataFrame({
            'Category': list(operating_costs.keys())[:-1],  # Exclude total
            'Annual Cost (ZAR)': list(operating_costs.values())[:-1]
        })
        
        fig_bar = px.bar(op_ex_df, x='Category', y='Annual Cost (ZAR)', 
                        title='Annual Operating Cost Breakdown', color='Category')
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Employment Impact
        st.subheader("👥 Employment & Economic Impact")
        
        employment_data = {
            'Phase': ['Construction', 'Operations', 'Maintenance', 'Administration'],
            'Direct Jobs': [8, 3, 2, 1],
            'Indirect Jobs': [12, 6, 3, 0],
            'Duration (months)': [6, project_lifespan*12, project_lifespan*12, project_lifespan*12]
        }
        
        jobs_df = pd.DataFrame(employment_data)
        st.dataframe(jobs_df, use_container_width=True)
        
        # Cost Over Time Analysis
        st.subheader("📅 Lifecycle Cost Analysis")
        
        years = list(range(project_lifespan + 1))
        capital_costs = [total_installed_cost if i == 0 else 0 for i in years]
        operating_costs_series = [0] + [operating_costs['total_annual'] * ((1 + annual_inflation) ** i) for i in range(project_lifespan)]
        cumulative_costs = np.cumsum([cap + op for cap, op in zip(capital_costs, operating_costs_series)])
        
        lifecycle_df = pd.DataFrame({
            'Year': years,
            'Capital Cost': capital_costs,
            'Operating Cost': operating_costs_series,
            'Cumulative Cost': cumulative_costs
        })
        
        fig_lifecycle = go.Figure()
        fig_lifecycle.add_trace(go.Scatter(x=lifecycle_df['Year'], y=lifecycle_df['Cumulative Cost'], 
                                         name='Cumulative Cost', line=dict(color='red', width=3)))
        fig_lifecycle.add_trace(go.Bar(x=lifecycle_df['Year'], y=lifecycle_df['Operating Cost'], 
                                     name='Annual Operating Cost'))
        fig_lifecycle.update_layout(title='Project Lifecycle Cost Analysis', xaxis_title='Year', yaxis_title='Cost (ZAR)')
        st.plotly_chart(fig_lifecycle, use_container_width=True)

# Engineering Reference
with st.expander("📚 Engineering Cost Correlations Reference"):
    st.write("""
    ### Chemical Engineering Cost Estimation Methods
    
    **1. Lang Factor Method**
    - Total Installed Cost = Bare Equipment Cost × Lang Factor
    - Factors: 3.1 (solids), 4.7 (fluids), 3.6 (mixed)
    
    **2. Equipment Cost Correlations**
    - Pumps: C = a + b(Q)^c where Q = flow rate (m³/h)
    - Tanks: C = k × V^exp where V = volume (m³)
    - Heat Exchangers: C = k × A^0.6 where A = area (m²)
    
    **3. Material Factors**
    - HDPE = 1.0 (baseline)
    - SS304 = 2.5×
    - SS316 = 3.2×
    - FRP = 1.8×
    
    **4. Installation Factors**
    - Simple: 1.3× equipment cost
    - Medium: 1.8× equipment cost  
    - Complex: 2.5× equipment cost
    """)

# Quick Cost Estimates
with st.expander("💡 Quick Cost Estimates"):
    st.write("**Typical Project Cost Ranges:**")
    
    quick_estimates = {
        "Small Community System (500 people)": "ZAR 1.5M - 3M",
        "Medium Village System (2,000 people)": "ZAR 4M - 8M", 
        "Large Rural System (10,000 people)": "ZAR 15M - 30M",
        "Sensor Monitoring Network": "ZAR 200K - 800K",
        "Water Treatment Upgrade": "ZAR 2M - 5M"
    }
    
    for project, cost_range in quick_estimates.items():
        st.write(f"- **{project}**: {cost_range}")

st.info("💡 **Pro Tip**: Use the engineering correlations for accurate budgeting. Consider both capital and operating costs for total lifecycle analysis.")