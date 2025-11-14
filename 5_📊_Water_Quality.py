import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Water Quality", layout="wide")

st.title("📊 Water Quality & SAN 241 Compliance")
st.markdown("**South African National Standard 241:2015 Drinking Water Compliance**")

# SAN 241:2015 Drinking Water Standards
SANS241_STANDARDS = {
    "turbidity": {"max": 1, "unit": "NTU", "risk": "Microbiological indicator"},
    "ecoli": {"max": 0, "unit": "count/100ml", "risk": "Faecal contamination"},
    "thermotolerant_coliforms": {"max": 0, "unit": "count/100ml", "risk": "Faecal contamination"},
    "ph": {"min": 6, "max": 9, "unit": "pH units", "risk": "Corrosivity/Scaling"},
    "chlorine_residual": {"min": 0.2, "max": 5, "unit": "mg/L", "risk": "Disinfection efficacy"},
    "total_dissolved_solids": {"max": 1200, "unit": "mg/L", "risk": "Taste/Acceptability"},
    "electrical_conductivity": {"max": 170, "unit": "mS/m", "risk": "Mineral content"},
    "fluoride": {"max": 1.5, "unit": "mg/L", "risk": "Dental/Skeletal fluorosis"},
    "nitrate": {"max": 11, "unit": "mg/L N", "risk": "Methaemoglobinaemia"},
    "nitrite": {"max": 0.9, "unit": "mg/L N", "risk": "Methaemoglobinaemia"},
    "aluminium": {"max": 0.3, "unit": "mg/L", "risk": "Discolouration"},
    "iron": {"max": 0.3, "unit": "mg/L", "risk": "Discolouration/Taste"},
    "manganese": {"max": 0.1, "unit": "mg/L", "risk": "Discolouration/Taste"},
    "sulphate": {"max": 400, "unit": "mg/L", "risk": "Gastrointestinal effects"},
    "zinc": {"max": 5, "unit": "mg/L", "risk": "Taste"}
}

class SANS241Checker:
    def __init__(self):
        self.standards = SANS241_STANDARDS
    
    def check_compliance(self, sample_data, source_type):
        """Check water sample against SAN 241 standards"""
        results = []
        compliant = True
        critical_failures = 0
        
        for parameter, measured_value in sample_data.items():
            if parameter in self.standards:
                standard = self.standards[parameter]
                status = "✅ PASS"
                deviation = 0
                
                # Check maximum limits
                if 'max' in standard and measured_value > standard['max']:
                    status = "❌ FAIL"
                    # FIXED: Handle division by zero when max is 0
                    if standard['max'] == 0:
                        deviation = float('inf')  # Infinite deviation for zero-tolerance parameters
                    else:
                        deviation = ((measured_value - standard['max']) / standard['max']) * 100
                    compliant = False
                    if parameter in ['ecoli', 'thermotolerant_coliforms']:
                        critical_failures += 1
                
                # Check minimum limits
                elif 'min' in standard and measured_value < standard['min']:
                    status = "❌ FAIL" 
                    deviation = ((standard['min'] - measured_value) / standard['min']) * 100
                    compliant = False
            
                results.append({
                    'Parameter': parameter,
                    'Measured Value': f"{measured_value} {standard['unit']}",
                    'Standard': f"≤ {standard.get('max', 'N/A')} {standard['unit']}",
                    'Status': status,
                    'Deviation %': "Zero tolerance violated" if deviation == float('inf') else f"{deviation:+.1f}%" if deviation != 0 else "Within limits",
                    'Risk': standard['risk']
                })
        
        return pd.DataFrame(results), compliant, critical_failures
    
    def generate_treatment_recommendations(self, failed_parameters, source_type):
        """Generate treatment recommendations based on failures"""
        recommendations = []
        
        if 'ecoli' in failed_parameters or 'thermotolerant_coliforms' in failed_parameters:
            recommendations.append({
                "priority": "🚨 CRITICAL",
                "treatment": "Disinfection System",
                "description": "Urgent: Faecal contamination detected! Install chlorination or UV disinfection immediately.",
                "equipment": ["Chlorine dosing system", "UV sterilizer", "Ozone generator"],
                "cost_estimate": "ZAR 45,000 - 120,000"
            })
        
        if 'turbidity' in failed_parameters:
            recommendations.append({
                "priority": "🔴 HIGH", 
                "treatment": "Filtration System",
                "description": "High turbidity requires coagulation, flocculation and multi-stage filtration.",
                "equipment": ["Sand filters", "Activated carbon", "Membrane filtration"],
                "cost_estimate": "ZAR 75,000 - 200,000"
            })
        
        if any(param in failed_parameters for param in ['iron', 'manganese', 'aluminium']):
            recommendations.append({
                "priority": "🟡 MEDIUM",
                "treatment": "Oxidation & Filtration", 
                "description": "Metal content requires oxidation followed by filtration removal.",
                "equipment": ["Aeration system", "Oxidant dosing", "Multi-media filters"],
                "cost_estimate": "ZAR 60,000 - 150,000"
            })
        
        if source_type == "river":
            recommendations.append({
                "priority": "💡 STANDARD",
                "treatment": "Multi-Barrier Protection",
                "description": "River sources always need comprehensive treatment: Coagulation + Filtration + Disinfection",
                "equipment": ["Complete water treatment plant", "Chemical dosing", "Filter media"],
                "cost_estimate": "ZAR 150,000 - 500,000"
            })
        elif source_type == "borehole":
            recommendations.append({
                "priority": "💡 STANDARD", 
                "treatment": "Disinfection & pH Adjustment",
                "description": "Borehole water typically needs disinfection and sometimes pH correction.",
                "equipment": ["Chlorination system", "pH adjustment", "Storage tanks"],
                "cost_estimate": "ZAR 35,000 - 90,000"
            })
        
        return recommendations

# Main Application
checker = SANS241Checker()

st.header("🔍 Water Quality Analysis")

# Water source selection
col1, col2 = st.columns(2)

with col1:
    water_source = st.selectbox(
        "Select Water Source Type:",
        ["River/Stream", "Borehole/Groundwater", "Dam/Reservoir", "Spring", "Rainwater", "Municipal Supply"]
    )

with col2:
    st.info(f"💧 **Source**: {water_source}")
    st.write("Different sources have different treatment requirements")

# Water quality input form
st.subheader("📝 Enter Water Quality Parameters")

st.write("**Enter measured values from your water tests:**")

col1, col2, col3 = st.columns(3)

# Initialize session state for form values
if 'turbidity' not in st.session_state:
    st.session_state.turbidity = 2.5
if 'ecoli' not in st.session_state:
    st.session_state.ecoli = 2
if 'ph' not in st.session_state:
    st.session_state.ph = 7.2

sample_data = {}

with col1:
    sample_data['turbidity'] = st.number_input("Turbidity (NTU)", min_value=0.0, max_value=100.0, value=st.session_state.turbidity, step=0.1, key="turbidity_input")
    sample_data['ph'] = st.number_input("pH", min_value=0.0, max_value=14.0, value=st.session_state.ph, step=0.1, key="ph_input")
    sample_data['chlorine_residual'] = st.number_input("Chlorine Residual (mg/L)", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
    sample_data['electrical_conductivity'] = st.number_input("Conductivity (mS/m)", min_value=0.0, max_value=1000.0, value=85.0, step=1.0)

with col2:
    sample_data['ecoli'] = st.number_input("E. coli (count/100ml)", min_value=0, max_value=1000, value=st.session_state.ecoli, step=1, key="ecoli_input")
    sample_data['total_dissolved_solids'] = st.number_input("TDS (mg/L)", min_value=0, max_value=5000, value=650, step=10)
    sample_data['fluoride'] = st.number_input("Fluoride (mg/L)", min_value=0.0, max_value=10.0, value=0.8, step=0.1)
    sample_data['nitrate'] = st.number_input("Nitrate (mg/L N)", min_value=0.0, max_value=50.0, value=8.5, step=0.1)

with col3:
    sample_data['iron'] = st.number_input("Iron (mg/L)", min_value=0.0, max_value=10.0, value=0.4, step=0.1)
    sample_data['manganese'] = st.number_input("Manganese (mg/L)", min_value=0.0, max_value=5.0, value=0.08, step=0.01)
    sample_data['aluminium'] = st.number_input("Aluminium (mg/L)", min_value=0.0, max_value=5.0, value=0.1, step=0.01)
    sample_data['sulphate'] = st.number_input("Sulphate (mg/L)", min_value=0, max_value=2000, value=250, step=10)

# Analyze button
if st.button("🔬 Analyze Water Quality", type="primary"):
    with st.spinner("Checking compliance with SAN 241:2015..."):
        # Check compliance
        results_df, is_compliant, critical_failures = checker.check_compliance(sample_data, water_source.lower())
        
        # Display results
        st.header("📊 Compliance Results")
        
        # Overall status
        if is_compliant and critical_failures == 0:
            st.success("🎉 **EXCELLENT**: Water meets all SAN 241:2015 drinking water standards!")
        elif critical_failures > 0:
            st.error(f"🚨 **CRITICAL FAILURE**: {critical_failures} parameters pose immediate health risks!")
        else:
            st.warning("⚠️ **NON-COMPLIANT**: Water fails some SAN 241 standards")
        
        # Results table
        st.dataframe(results_df, use_container_width=True)
        
        # Treatment recommendations
        failed_params = results_df[results_df['Status'] == '❌ FAIL']['Parameter'].tolist()
        if failed_params:
            st.header("🛠️ Treatment Recommendations")
            recommendations = checker.generate_treatment_recommendations(failed_params, water_source.lower())
            
            for rec in recommendations:
                with st.expander(f"{rec['priority']} {rec['treatment']}"):
                    st.write(rec['description'])
                    st.write("**Required Equipment:**")
                    for equipment in rec['equipment']:
                        st.write(f"- {equipment}")
                    st.write(f"**Cost Estimate:** {rec['cost_estimate']}")
        
        # Visualization
        st.header("📈 Quality Parameters Visualization")
        
        # Create compliance chart (only for parameters with numeric max limits)
        compliance_data = []
        for param, value in sample_data.items():
            if param in SANS241_STANDARDS:
                std = SANS241_STANDARDS[param]
                max_limit = std.get('max', None)
                if max_limit is not None and max_limit > 0:  # Only include parameters with positive max limits
                    compliance_data.append({
                        'Parameter': param,
                        'Measured Value': value,
                        'Standard Limit': max_limit,
                        'Status': 'Within Limits' if value <= max_limit else 'Exceeds Limits'
                    })
        
        if compliance_data:
            df_viz = pd.DataFrame(compliance_data)
            fig = px.bar(df_viz, x='Parameter', y='Measured Value', color='Status',
                        title='Water Quality Parameters vs SAN 241 Limits',
                        hover_data=['Standard Limit'])
            fig.add_scatter(x=df_viz['Parameter'], y=df_viz['Standard Limit'], 
                          mode='markers', name='SAN 241 Limit', marker=dict(size=10, color='red'))
            st.plotly_chart(fig, use_container_width=True)

# SAN 241 Standards Reference
with st.expander("📚 SAN 241:2015 Standards Reference"):
    st.write("**Complete South African National Standard 241:2015 Drinking Water Specifications**")
    standards_df = pd.DataFrame([
        {
            'Parameter': param,
            'Maximum Limit': std.get('max', 'N/A'),
            'Minimum Limit': std.get('min', 'N/A'), 
            'Unit': std['unit'],
            'Health Risk': std['risk']
        }
        for param, std in SANS241_STANDARDS.items()
    ])
    st.dataframe(standards_df, use_container_width=True)

# Quick Test Templates
with st.expander("💧 Quick Test Templates"):
    st.write("**Common water source typical values (modify as needed):**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Load River Water Template"):
            st.session_state.turbidity = 8.5
            st.session_state.ecoli = 12
            st.session_state.ph = 6.8
            st.rerun()
    
    with col2:
        if st.button("Load Borehole Template"):
            st.session_state.turbidity = 1.2
            st.session_state.ecoli = 0
            st.session_state.ph = 7.8
            st.rerun()

st.info("💡 **Remember**: Regular water quality testing is essential for community health. Test monthly for critical parameters.")