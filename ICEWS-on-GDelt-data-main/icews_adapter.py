import pandas as pd
import numpy as np
from gdelt_processor import get_event_details

def adapt_gdelt_to_icews(gdelt_df):
    """
    Transforms GDELT data to match ICEWS format for compatibility with ICEWS Explorer.
    
    Args:
        gdelt_df (pandas.DataFrame): DataFrame containing GDELT data
    
    Returns:
        pandas.DataFrame: Transformed data in ICEWS format
    """
    if gdelt_df is None or gdelt_df.empty:
        return pd.DataFrame()
    
    # Create a new DataFrame for ICEWS format
    icews_data = pd.DataFrame()
    
    # Map GDELT fields to ICEWS format
    # Core fields
    icews_data['event_id'] = gdelt_df['GlobalEventID']
    icews_data['date'] = pd.to_datetime(gdelt_df['DATEADDED'], format='%Y%m%d%H%M%S')
    
    # Event type info
    icews_data['cameo_code'] = gdelt_df['EventCode']
    icews_data['event_type'] = gdelt_df['EventCode'].apply(get_event_details)
    
    # Source and target actors
    icews_data['source_name'] = gdelt_df['Actor1Name']
    icews_data['source_country'] = gdelt_df['Actor1CountryCode']
    icews_data['target_name'] = gdelt_df['Actor2Name']
    icews_data['target_country'] = gdelt_df['Actor2CountryCode']
    
    # Location information
    icews_data['country'] = gdelt_df['ActionGeo_CountryCode']
    icews_data['latitude'] = gdelt_df['ActionGeo_Lat']
    icews_data['longitude'] = gdelt_df['ActionGeo_Long']
    icews_data['location'] = gdelt_df['ActionGeo_FullName']
    
    # Event details
    icews_data['intensity'] = gdelt_df['GoldsteinScale']
    icews_data['tone'] = gdelt_df['AvgTone']
    icews_data['quad_class'] = gdelt_df['QuadClass']
    
    # Source URL
    icews_data['source_url'] = gdelt_df['SOURCEURL']
    
    # Fill missing values with appropriate placeholders
    icews_data['source_name'] = icews_data['source_name'].fillna('Unknown')
    icews_data['target_name'] = icews_data['target_name'].fillna('Unknown')
    icews_data['source_country'] = icews_data['source_country'].fillna('Unknown')
    icews_data['target_country'] = icews_data['target_country'].fillna('Unknown')
    icews_data['country'] = icews_data['country'].fillna('Unknown')
    icews_data['location'] = icews_data['location'].fillna('Unknown')
    
    # Convert numeric columns
    icews_data['intensity'] = pd.to_numeric(icews_data['intensity'], errors='coerce')
    icews_data['tone'] = pd.to_numeric(icews_data['tone'], errors='coerce')
    
    # Add additional ICEWS-specific fields
    icews_data['source_sectors'] = 'Unknown'
    icews_data['target_sectors'] = 'Unknown'
    
    # Remove records with invalid values
    icews_data = icews_data.dropna(subset=['event_id', 'date', 'event_type'])
    
    return icews_data
