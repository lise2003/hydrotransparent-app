import pandas as pd
import streamlit as st
import os

@st.cache_data
def list_data_files():
    """List all data files in the data folder"""
    data_files = []
    data_folder = "data"
    
    if os.path.exists(data_folder):
        for file in os.listdir(data_folder):
            data_files.append(file)
    
    return data_files

@st.cache_data
def load_water_service_data():
    """Load your main water service levels CSV"""
    try:
        file_path = "data/Water Service Levels - Households_2025_10_08.csv"
        df = pd.read_csv(file_path)
        st.success(f"✅ Loaded Water Service Data: {len(df)} rows")
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
        st.success(f"✅ Loaded WASH Data: {len(df)} rows")
        return df
    except Exception as e:
        st.error(f"❌ Could not load WASH data: {e}")
        return None

@st.cache_data
def load_esk_data():
    """Load your ESK2033 CSV data"""
    try:
        file_path = "data/ESK2033.csv"
        df = pd.read_csv(file_path)
        st.success(f"✅ Loaded ESK Data: {len(df)} rows")
        return df
    except Exception as e:
        st.error(f"❌ Could not load ESK data: {e}")
        return None

@st.cache_data
def load_dams_data():
    """Load global dams database"""
    try:
        file_path = "data/globaldamsdatabase_global_coverage_november_2020.csv"
        df = pd.read_csv(file_path)
        st.success(f"✅ Loaded Dams Data: {len(df)} rows")
        return df
    except Exception as e:
        st.error(f"❌ Could not load dams data: {e}")
        return None