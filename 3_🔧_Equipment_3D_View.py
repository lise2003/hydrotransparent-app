import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="3D Equipment", layout="wide")

st.title("🔧 3D Sensor Equipment Gallery")
st.markdown("**Advanced Water Monitoring Technology for Rural South Africa**")

# Your sensor equipment database
sensor_equipment = {
    "acoustic_leak": {
        "name": "Acoustic Leak Detection Sensors",
        "type": "Permanent/Long-life",
        "lifespan": "20+ years",
        "power": "Solar + Battery",
        "description": "Detect leaks in water pipes using sound signatures. Installed inside pipes or on valves.",
        "cost": 8500,
        "placement": "Along pipeline every 2km",
        "specs": {
            "Detection Range": "500m radius",
            "Accuracy": "95% leak detection",
            "Data Interval": "15 minutes",
            "Communication": "LoRaWAN"
        }
    },
    "pressure_sensor": {
        "name": "Smart Pressure Sensors", 
        "type": "Pressure Monitoring",
        "lifespan": "15+ years",
        "power": "Solar + Battery",
        "description": "Monitor water pressure to detect leaks, bursts, and system anomalies.",
        "cost": 5200,
        "placement": "At high/low points in system",
        "specs": {
            "Range": "0-10 bar",
            "Accuracy": "±0.5%",
            "Data Interval": "5 minutes", 
            "Communication": "NB-IoT"
        }
    },
    "flow_meter": {
        "name": "Electromagnetic Flowmeters",
        "type": "Flow Monitoring",
        "lifespan": "25+ years", 
        "power": "Solar + Battery",
        "description": "Measure water flow with no moving parts. Highly accurate for leak detection.",
        "cost": 12500,
        "placement": "Main distribution lines",
        "specs": {
            "Flow Range": "0.5-5000 m³/h",
            "Accuracy": "±0.2%",
            "Data Interval": "1 minute",
            "Communication": "LoRaWAN + Cellular"
        }
    },
    "water_quality": {
        "name": "Multi-Parameter Water Quality Sensor",
        "type": "Quality Monitoring", 
        "lifespan": "10+ years",
        "power": "Solar + Battery",
        "description": "Monitor turbidity, pH, chlorine, conductivity for SAN 241 compliance.",
        "cost": 9800,
        "placement": "Treatment output & key points",
        "specs": {
            "Parameters": "Turbidity, pH, Cl, Conductivity",
            "Accuracy": "±1% FS",
            "Data Interval": "30 minutes",
            "Communication": "NB-IoT"
        }
    }
}

# Sensor selection
st.sidebar.subheader("🎯 Select Sensor Type")
selected_sensor = st.sidebar.selectbox(
    "Choose sensor to view:",
    list(sensor_equipment.keys()),
    format_func=lambda x: sensor_equipment[x]["name"]
)

# Main display
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📐 3D Equipment Visualization")
    
    # Create 3D visualization based on sensor type
    if selected_sensor == "acoustic_leak":
        # Acoustic sensor - cylindrical shape
        fig = go.Figure()
        
        # Main sensor body (cylinder)
        fig.add_trace(go.Mesh3d(
            x=[0, 1, 1, 0, 0, 1, 1, 0],
            y=[0, 0, 1, 1, 0, 0, 1, 1],
            z=[0, 0, 0, 0, 1, 1, 1, 1],
            color='lightblue',
            opacity=0.8
        ))
        
        # Sensor elements
        fig.add_trace(go.Scatter3d(
            x=[0.5, 0.5], y=[0.5, 0.5], z=[1.2, 1.5],
            mode='lines',
            line=dict(color='red', width=5)
        ))
        
    elif selected_sensor == "pressure_sensor":
        # Pressure sensor - spherical with ports
        fig = go.Figure()
        
        # Main sphere
        fig.add_trace(go.Mesh3d(
            x=[0, 1, 0.5], y=[0, 0.5, 1], z=[0, 1, 0.5],
            color='lightgreen',
            opacity=0.8
        ))
        
    elif selected_sensor == "flow_meter":
        # Flow meter - tubular shape
        fig = go.Figure()
        
        # Pipe section
        fig.add_trace(go.Mesh3d(
            x=[0, 2, 2, 0, 0, 2, 2, 0],
            y=[0.3, 0.3, 0.7, 0.7, 0.3, 0.3, 0.7, 0.7],
            z=[0.3, 0.3, 0.3, 0.3, 0.7, 0.7, 0.7, 0.7],
            color='orange',
            opacity=0.7
        ))
        
    else:  # water_quality
        # Multi-parameter sensor - rectangular with multiple elements
        fig = go.Figure()
        
        # Main unit
        fig.add_trace(go.Mesh3d(
            x=[0, 1.5, 1.5, 0, 0, 1.5, 1.5, 0],
            y=[0, 0, 1, 1, 0, 0, 1, 1],
            z=[0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5],
            color='purple',
            opacity=0.8
        ))
    
    # Configure 3D scene
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False), 
            zaxis=dict(visible=False),
            bgcolor='white'
        ),
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        title=f"3D Model: {sensor_equipment[selected_sensor]['name']}"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Interactive controls
    st.subheader("🔄 Sensor Network Simulation")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        show_network = st.checkbox("Show Sensor Network", True)
    with col_b:
        show_data_flow = st.checkbox("Show Data Flow", True)
    with col_c:
        show_maintenance = st.checkbox("Show Maintenance Status", True)

with col2:
    st.subheader("📋 Sensor Specifications")
    
    sensor = sensor_equipment[selected_sensor]
    
    st.metric("Sensor Type", sensor["type"])
    st.metric("Lifespan", sensor["lifespan"])
    st.metric("Unit Cost", f"ZAR {sensor['cost']:,}")
    st.metric("Power Source", sensor["power"])
    
    st.subheader("📝 Technical Specifications")
    for spec, value in sensor["specs"].items():
        st.write(f"**{spec}**: {value}")
    
    st.subheader("📍 Placement Guide")
    st.info(sensor["placement"])

# Maintenance and Alerts Section
st.markdown("---")
st.subheader("🔧 Maintenance & Monitoring")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Sensor Health Status")
    
    # Mock sensor status data
    sensor_status = {
        "Battery Level": "🔋 85%",
        "Signal Strength": "📶 Excellent",
        "Last Maintenance": "🛠️ 45 days ago",
        "Next Service": "📅 30 days",
        "Data Uptime": "✅ 99.8%"
    }
    
    for status, value in sensor_status.items():
        st.write(f"**{status}**: {value}")

with col2:
    st.subheader("🚨 Alert System")
    
    # Mock alerts
    alerts = [
        {"type": "⚠️", "message": "Low battery in sector B sensors", "priority": "Medium"},
        {"type": "✅", "message": "All acoustic sensors operational", "priority": "Info"},
        {"type": "🔧", "message": "Scheduled maintenance in 2 weeks", "priority": "Low"}
    ]
    
    for alert in alerts:
        st.write(f"{alert['type']} **{alert['priority']}**: {alert['message']}")

# Installation Guide
with st.expander("📖 Installation & Deployment Guide"):
    st.write("""
    ### 🛠️ Installation Steps:
    1. **Site Survey**: Identify optimal sensor locations every 2km
    2. **Solar Setup**: Install solar panels with battery backup
    3. **Sensor Mounting**: Secure sensors to pipes or install inline
    4. **Network Setup**: Configure LoRaWAN/NB-IoT communication
    5. **Calibration**: Calibrate sensors for accurate readings
    6. **Testing**: Verify data transmission and alerts
    
    ### 👥 Local Employment Opportunities:
    - **2 Technicians** for installation
    - **1 Network Specialist** for setup
    - **1 Maintenance Worker** per 50 sensors
    - **1 Data Analyst** for monitoring
    """)

st.info("💡 **Pro Tip**: Start with acoustic leak detectors in high-risk areas, then expand to full sensor network")