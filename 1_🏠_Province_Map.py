import streamlit as st
import pandas as pd
import os

# Data loading functions
@st.cache_data
def load_water_service_data():
    """Load your main water service levels CSV"""
    try:
        file_path = "data/Water Service Levels - Households_ 2025_10_08.csv"
        df = pd.read_csv(file_path, encoding='latin-1')
        return df
    except Exception as e:
        st.error(f"❌ Could not load water service data: {e}")
        return None

@st.cache_data
def load_wash_data():
    """Load your WASH data CSV"""
    try:
        file_path = "data/washdata.csv"
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"❌ Could not load WASH data: {e}")
        return None

def clean_number(value):
    """Clean numbers with special spaces and convert to integer"""
    if pd.isna(value):
        return 0
    # Remove ALL types of spaces (regular spaces, non-breaking spaces, etc.)
    cleaned = str(value).replace(' ', '').replace('\xa0', '').replace(',', '')
    try:
        return int(cleaned)
    except:
        return 0

# Main app
st.title("🌍 Select Province & Rural Area")
st.markdown("**Using Real South African Water Data**")

# Load data
water_data = load_water_service_data()
wash_data = load_wash_data()

# Province selection
provinces = ["Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", 
             "Limpopo", "Mpumalanga", "North West", "Northern Cape", "Western Cape"]

selected_province = st.selectbox("Choose a province:", provinces)

if selected_province and water_data is not None:
    st.session_state.selected_province = selected_province
    
    # Get data for selected province
    province_data = water_data[water_data['Region'] == selected_province]
    
    if not province_data.empty:
        # Extract the row
        row = province_data.iloc[0]
        
        # Clean and convert all numbers (handles special spaces)
        total_households = clean_number(row['Total Households'])
        piped_inside = clean_number(row['Piped water inside dwelling Households'])
        piped_yard = clean_number(row['Piped water inside yard Households'])
        borehole = clean_number(row['Borehole Households'])
        river_stream = clean_number(row['River/stream Households'])
        water_vendor = clean_number(row['Water vendor Households'])
        spring = clean_number(row['Spring Households'])
        rainwater = clean_number(row['Rain-water tank Households'])
        
        # Calculate percentages
        piped_inside_pct = (piped_inside / total_households) * 100 if total_households > 0 else 0
        piped_yard_pct = (piped_yard / total_households) * 100 if total_households > 0 else 0
        borehole_pct = (borehole / total_households) * 100 if total_households > 0 else 0
        river_stream_pct = (river_stream / total_households) * 100 if total_households > 0 else 0
        water_vendor_pct = (water_vendor / total_households) * 100 if total_households > 0 else 0
        
        # Total piped water access
        total_piped_pct = piped_inside_pct + piped_yard_pct
        
        st.success(f"✅ Selected: {selected_province}")
        
        # Key Metrics Dashboard
        st.subheader("📊 Water Access Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Households", 
                f"{total_households:,}",
                "Families needing water"
            )
        
        with col2:
            st.metric(
                "Piped Water Access", 
                f"{total_piped_pct:.1f}%",
                f"{piped_inside + piped_yard:,} households"
            )
        
        with col3:
            st.metric(
                "Using Boreholes", 
                f"{borehole_pct:.1f}%",
                f"{borehole:,} households"
            )
        
        with col4:
            st.metric(
                "Using Rivers/Streams", 
                f"{river_stream_pct:.1f}%",
                "Urgent intervention needed"
            )
        
        # Water Source Breakdown
        st.subheader("💧 Water Source Distribution")
        
        sources_data = {
            'Water Source': ['Piped Inside Home', 'Piped in Yard', 'Boreholes', 'Rivers/Streams', 'Water Vendors', 'Springs', 'Rainwater Tanks', 'Other Sources'],
            'Households': [piped_inside, piped_yard, borehole, river_stream, water_vendor, spring, rainwater, total_households - (piped_inside + piped_yard + borehole + river_stream + water_vendor + spring + rainwater)],
            'Percentage': [piped_inside_pct, piped_yard_pct, borehole_pct, river_stream_pct, water_vendor_pct, (spring/total_households)*100, (rainwater/total_households)*100, 100 - total_piped_pct - borehole_pct - river_stream_pct - water_vendor_pct - (spring/total_households)*100 - (rainwater/total_households)*100]
        }
        
        sources_df = pd.DataFrame(sources_data)
        st.dataframe(sources_df, use_container_width=True)
        
        # Urgency Indicators
        st.subheader("🚨 Priority Interventions Needed")
        
        if river_stream_pct > 5:
            st.error(f"**URGENT**: {river_stream:,} households ({river_stream_pct:.1f}%) using rivers/streams - high health risk!")
        
        if total_piped_pct < 70:
            st.warning(f"**PIPED WATER GAP**: Only {total_piped_pct:.1f}% have piped water - {total_households - (piped_inside + piped_yard):,} households need piped access")
        
        if borehole_pct > 10:
            st.info(f"**GROUNDWATER POTENTIAL**: {borehole_pct:.1f}% using boreholes - good candidate for solar borehole upgrades")
        
        # Water Solutions Recommendation
        st.subheader("💡 Recommended Solutions")
        
        if river_stream_pct > 5:
            st.write("🎯 **Priority Solution**: Community Water Treatment Pods")
            st.write("   - Install solar-powered water purification systems")
            st.write("   - Treat river water to SAN 241 standards")
            st.write("   - Serve communities currently using unsafe sources")
        
        if total_piped_pct < 70:
            st.write("🎯 **Infrastructure Solution**: Micro-Distribution Networks")
            st.write("   - Lay HDPE pipelines to unserved households")
            st.write("   - Connect to existing water sources")
            st.write("   - Create permanent water access")
        
        if borehole_pct > 10:
            st.write("🎯 **Upgrade Solution**: Solar Borehole Systems")
            st.write("   - Replace manual/diesel pumps with solar")
            st.write("   - Add smart meters for sustainable use")
            st.write("   - Install elevated storage tanks")
        
        # Show raw data for debugging
        with st.expander("🔍 View Raw Data (Debug)"):
            st.write("**Raw values from CSV:**")
            debug_data = {
                'Field': ['Total Households', 'Piped Inside', 'Piped Yard', 'Boreholes', 'Rivers'],
                'Raw Value': [str(row['Total Households']), str(row['Piped water inside dwelling Households']), str(row['Piped water inside yard Households']), str(row['Borehole Households']), str(row['River/stream Households'])],
                'Cleaned': [total_households, piped_inside, piped_yard, borehole, river_stream]
            }
            st.dataframe(pd.DataFrame(debug_data))
            
    else:
        st.error(f"No data found for {selected_province}")

else:
    st.info("👆 Please select a province to see water access data")

# Data overview section
st.markdown("---")
st.subheader("📁 Data Overview")

if water_data is not None:
    with st.expander("🔍 View All Provincial Water Data"):
        st.write(f"**Dataset**: Water Service Levels - {water_data.shape[0]} provinces, {water_data.shape[1]} indicators")
        st.dataframe(water_data, use_container_width=True)

if wash_data is not None:
    with st.expander("🔍 View WASH National Data"):
        st.write(f"**Dataset**: WASH Coverage - {wash_data.shape[0]} records, {wash_data.shape[1]} indicators")
        st.dataframe(wash_data, use_container_width=True)

st.info("💡 **Next**: Go to 'Water Solutions' to see detailed engineering plans and cost estimates!")
