import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import requests
import io
import zipfile
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="GDELT Data - Simple Version",
    page_icon="📊",
    layout="centered"
)

# Title and description
st.title("GDELT Data Explorer - Minimal Version")
st.markdown("This is a simplified version of the GDELT data explorer that you can run locally.")

# Function to fetch GDELT data
def fetch_gdelt_data():
    try:
        # Calculate the timestamps for the last 15 minutes
        now = datetime.datetime.utcnow()
        fifteen_min_ago = now - datetime.timedelta(minutes=15)
        
        # Format dates for GDELT API
        date_format = "%Y%m%d"
        time_format = "%H%M%S"
        
        # Construct the GDELT URL for the last 15 minutes
        gdelt_url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
        
        # Get the latest update file references
        response = requests.get(gdelt_url)
        response.raise_for_status()
        
        # Parse the response to get the CSV file URLs
        update_info = response.text.strip().split('\n')
        csv_urls = []
        
        for line in update_info:
            parts = line.split()
            if len(parts) >= 3:
                file_url = parts[2]
                # Check if it's an events CSV file
                if file_url.endswith('.export.CSV.zip'):
                    csv_urls.append(file_url)
        
        # Initialize empty DataFrame to hold all data
        all_data = pd.DataFrame()
        
        # Process each CSV file
        for url in csv_urls:
            try:
                # Download the CSV
                file_response = requests.get(url)
                file_response.raise_for_status()
                
                # Define GDELT column names
                gdelt_columns = [
                    'GlobalEventID', 'Day', 'MonthYear', 'Year', 'FractionDate', 
                    'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode', 
                    'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code', 
                    'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', 
                    'Actor2Code', 'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode', 
                    'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code', 
                    'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code', 
                    'IsRootEvent', 'EventCode', 'EventBaseCode', 'EventRootCode', 
                    'QuadClass', 'GoldsteinScale', 'NumMentions', 'NumSources', 
                    'NumArticles', 'AvgTone', 'Actor1Geo_Type', 'Actor1Geo_FullName', 
                    'Actor1Geo_CountryCode', 'Actor1Geo_ADM1Code', 'Actor1Geo_ADM2Code', 
                    'Actor1Geo_Lat', 'Actor1Geo_Long', 'Actor1Geo_FeatureID', 
                    'Actor2Geo_Type', 'Actor2Geo_FullName', 'Actor2Geo_CountryCode', 
                    'Actor2Geo_ADM1Code', 'Actor2Geo_ADM2Code', 'Actor2Geo_Lat', 
                    'Actor2Geo_Long', 'Actor2Geo_FeatureID', 'ActionGeo_Type', 
                    'ActionGeo_FullName', 'ActionGeo_CountryCode', 'ActionGeo_ADM1Code', 
                    'ActionGeo_ADM2Code', 'ActionGeo_Lat', 'ActionGeo_Long', 
                    'ActionGeo_FeatureID', 'DATEADDED', 'SOURCEURL'
                ]
                
                # Read the CSV data
                z = zipfile.ZipFile(BytesIO(file_response.content))
                csv_filename = z.namelist()[0]  # Get the CSV filename inside the zip
                
                with z.open(csv_filename) as f:
                    df = pd.read_csv(f, sep='\t', header=None, names=gdelt_columns)
                
                # Filter out events older than 15 minutes
                # DATEADDED format in GDELT is YYYYMMDDHHMMSS
                df['datetime'] = pd.to_datetime(df['DATEADDED'], format='%Y%m%d%H%M%S')
                df = df[df['datetime'] >= fifteen_min_ago]
                
                # Append to our collection
                all_data = pd.concat([all_data, df])
            
            except Exception as e:
                st.error(f"Error processing file {url}: {e}")
                continue
        
        # Define GDELT columns outside the condition for scope clarity
        gdelt_columns = [
            'GlobalEventID', 'Day', 'MonthYear', 'Year', 'FractionDate', 
            'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode', 
            'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code', 
            'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', 
            'Actor2Code', 'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode', 
            'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code', 
            'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code', 
            'IsRootEvent', 'EventCode', 'EventBaseCode', 'EventRootCode', 
            'QuadClass', 'GoldsteinScale', 'NumMentions', 'NumSources', 
            'NumArticles', 'AvgTone', 'Actor1Geo_Type', 'Actor1Geo_FullName', 
            'Actor1Geo_CountryCode', 'Actor1Geo_ADM1Code', 'Actor1Geo_ADM2Code', 
            'Actor1Geo_Lat', 'Actor1Geo_Long', 'Actor1Geo_FeatureID', 
            'Actor2Geo_Type', 'Actor2Geo_FullName', 'Actor2Geo_CountryCode', 
            'Actor2Geo_ADM1Code', 'Actor2Geo_ADM2Code', 'Actor2Geo_Lat', 
            'Actor2Geo_Long', 'Actor2Geo_FeatureID', 'ActionGeo_Type', 
            'ActionGeo_FullName', 'ActionGeo_CountryCode', 'ActionGeo_ADM1Code', 
            'ActionGeo_ADM2Code', 'ActionGeo_Lat', 'ActionGeo_Long', 
            'ActionGeo_FeatureID', 'DATEADDED', 'SOURCEURL'
        ]
        
        # If we found any data
        if not all_data.empty:
            # Remove duplicates based on GlobalEventID
            all_data = all_data.drop_duplicates(subset=['GlobalEventID'])
            
            # Sort by datetime
            all_data = all_data.sort_values('datetime', ascending=False)
            
            return all_data
        else:
            # Create a sample empty dataframe with the right columns if no data
            return pd.DataFrame(columns=gdelt_columns)
    
    except Exception as e:
        st.error(f"Error fetching GDELT data: {e}")
        return None

# Function to map event codes to descriptions
def get_event_description(event_code):
    # CAMEO event codes mapping (simplified)
    cameo_codes = {
        '01': 'Make public statement',
        '02': 'Appeal',
        '03': 'Express intent to cooperate',
        '04': 'Consult',
        '05': 'Engage in diplomatic cooperation',
        '06': 'Engage in material cooperation',
        '07': 'Provide aid',
        '08': 'Yield',
        '09': 'Investigate',
        '10': 'Demand',
        '11': 'Disapprove',
        '12': 'Reject',
        '13': 'Threaten',
        '14': 'Protest',
        '15': 'Exhibit military posture',
        '16': 'Reduce relations',
        '17': 'Coerce',
        '18': 'Assault',
        '19': 'Fight',
        '20': 'Use unconventional mass violence'
    }
    
    # Extract the root code (first two digits)
    root_code = str(event_code)[:2]
    
    return cameo_codes.get(root_code, 'Other')

# Create a button to fetch data
if st.button("🔄 Fetch GDELT Data (Last 15 Minutes)"):
    with st.spinner("Fetching latest GDELT data..."):
        data = fetch_gdelt_data()
        
        if data is not None and not data.empty:
            st.session_state.data = data
            st.session_state.last_update = datetime.datetime.now()
            st.success(f"Successfully loaded {len(data)} events from GDELT!")
        else:
            st.error("No GDELT data available for the last 15 minutes. Please try again later.")

# Display last update time if available
if 'last_update' in st.session_state and st.session_state.last_update:
    st.info(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Display data if available
if 'data' in st.session_state and st.session_state.data is not None and not st.session_state.data.empty:
    # Show basic statistics
    st.header("Data Overview")
    
    # Create two columns for statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Events", len(st.session_state.data))
        
        # Count unique countries
        countries = st.session_state.data['ActionGeo_CountryCode'].dropna().unique()
        st.metric("Countries Involved", len(countries))
    
    with col2:
        # Calculate average tone
        avg_tone = st.session_state.data['AvgTone'].mean()
        st.metric("Average Tone", f"{avg_tone:.2f}")
        
        # Calculate average Goldstein scale
        avg_goldstein = st.session_state.data['GoldsteinScale'].mean()
        st.metric("Average Intensity", f"{avg_goldstein:.2f}")
    
    # Add event type analysis
    st.header("Event Types")
    
    # Map event codes to descriptions
    st.session_state.data['EventType'] = st.session_state.data['EventCode'].apply(get_event_description)
    
    # Count event types
    event_counts = st.session_state.data['EventType'].value_counts().reset_index()
    event_counts.columns = ['Event Type', 'Count']
    
    # Create a bar chart for event types
    st.bar_chart(event_counts.set_index('Event Type'))
    
    # Display the raw data
    st.header("Raw Data")
    
    # Select columns to display
    display_cols = ['GlobalEventID', 'Actor1Name', 'Actor2Name', 'EventCode', 'EventType', 
                   'GoldsteinScale', 'AvgTone', 'ActionGeo_FullName', 'ActionGeo_CountryCode', 
                   'ActionGeo_Lat', 'ActionGeo_Long', 'DATEADDED', 'SOURCEURL']
    
    # Display the data
    st.dataframe(st.session_state.data[display_cols].head(50))
    
    # Option to download the data
    csv = st.session_state.data.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"gdelt_events_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )
else:
    st.info("Click the '🔄 Fetch GDELT Data' button above to load the latest GDELT events.")

# Add some information about GDELT
st.markdown("---")
st.header("About GDELT")
st.markdown("""
The [GDELT Project](https://www.gdeltproject.org/) monitors world news media in over 100 languages and processes this information to identify events, entities, and themes.

This simple application fetches the most recent events (last 15 minutes) from GDELT and displays them in a basic format.
""")

# Footer
st.markdown("---")
st.markdown("GDELT Data Explorer - Simple Version | Created for local development")