import pandas as pd
import datetime
import requests
import io
import os
import time

def fetch_gdelt_data():
    """
    Fetches GDELT data from the last 15 minutes.
    
    Returns:
        pandas.DataFrame: Processed GDELT data
    """
    try:
        # Calculate the timestamps for the last 15 minutes
        now = datetime.datetime.utcnow()
        fifteen_min_ago = now - datetime.timedelta(minutes=15)
        
        # Format dates for GDELT API
        date_format = "%Y%m%d"
        time_format = "%H%M%S"
        
        now_date = now.strftime(date_format)
        now_time = now.strftime(time_format)
        fifteen_min_ago_date = fifteen_min_ago.strftime(date_format)
        fifteen_min_ago_time = fifteen_min_ago.strftime(time_format)
        
        # Construct the GDELT URL for the last 15 minutes
        # Using the GDELT 2.0 Events Export API
        gdelt_url = f"http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
        
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
                import zipfile
                from io import BytesIO
                
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
                print(f"Error processing file {url}: {e}")
                continue
        
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
        print(f"Error fetching GDELT data: {e}")
        return None

def get_event_details(event_code):
    """
    Maps GDELT event codes to human-readable event types.
    
    Args:
        event_code (str): GDELT event code
    
    Returns:
        str: Human-readable event type
    """
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
