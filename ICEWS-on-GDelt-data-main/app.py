import streamlit as st

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="GDELT Data Visualization with ICEWS Explorer",
    page_icon="📊",
    layout="centered",  # Changed to centered for better compatibility
    # Add this to allow HTML rendering for clickable links
    initial_sidebar_state="expanded"
)

# Import basic packages first
import pandas as pd
import numpy as np
import datetime
import time

# Then import visualization packages
import plotly.express as px
import plotly.graph_objects as go

# Finally import the local modules
from gdelt_processor import fetch_gdelt_data
from icews_adapter import adapt_gdelt_to_icews

# Initialize session state variables if they don't exist
if 'data' not in st.session_state:
    st.session_state.data = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'selected_event' not in st.session_state:
    st.session_state.selected_event = None

# Title and description
st.title("GDELT Data Visualization with ICEWS Explorer")
st.markdown("""
This application demonstrates the use of ICEWS Explorer with GDELT data.
- Data is fetched from GDELT for the last 15 minutes
- The data is processed to match ICEWS format
- Visualizations are generated using ICEWS Explorer-inspired components
""")

# Sidebar with controls
with st.sidebar:
    st.header("Controls")

    # Refresh button to get the latest data
    if st.button("🔄 Refresh Data (Last 15 Minutes)"):
        with st.spinner("Fetching latest GDELT data..."):
            gdelt_data = fetch_gdelt_data()
            if gdelt_data is not None and not gdelt_data.empty:
                # Adapt GDELT to ICEWS format
                st.session_state.data = adapt_gdelt_to_icews(gdelt_data)
                st.session_state.last_update = datetime.datetime.now()
                st.success("Data successfully loaded!")
            else:
                st.error("No GDELT data available for the last 15 minutes. Please try again later.")

    # Display last update time if available
    if st.session_state.last_update:
        st.info(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add information about ICEWS Explorer
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This app is inspired by the [ICEWS Explorer](https://github.com/brendancooley/icews-explorer) 
    but implemented in Streamlit using GDELT data.
    """)

# Main content area
if st.session_state.data is not None and not st.session_state.data.empty:
    st.success(f"Loaded {len(st.session_state.data)} events from GDELT")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Event Analysis", "Geographic View", "Data Explorer"])
    
    with tab1:
        st.subheader("Event Analysis")
        
        # Event types distribution
        event_counts = st.session_state.data['event_type'].value_counts().reset_index()
        event_counts.columns = ['Event Type', 'Count']
        
        fig = px.bar(
            event_counts, 
            x='Event Type', 
            y='Count',
            title="Distribution of Event Types",
            color='Count',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Event timeline
        st.subheader("Event Timeline")
        timeline_data = st.session_state.data.copy()
        timeline_data['hour'] = timeline_data['date'].dt.hour
        timeline_data['minute'] = timeline_data['date'].dt.minute
        
        timeline_counts = timeline_data.groupby(['hour', 'minute']).size().reset_index(name='count')
        timeline_counts['time_label'] = timeline_counts.apply(lambda x: f"{int(x['hour']):02d}:{int(x['minute']):02d}", axis=1)
        
        fig = px.line(
            timeline_counts, 
            x='time_label', 
            y='count',
            title="Events Over Time",
            markers=True
        )
        fig.update_layout(xaxis_title="Time (UTC)", yaxis_title="Number of Events")
        st.plotly_chart(fig, use_container_width=True)
        
        # Event intensity analysis
        st.subheader("Event Intensity Analysis")
        if 'intensity' in st.session_state.data.columns:
            intensity_data = st.session_state.data.dropna(subset=['intensity']).copy()
            
            # Bin intensity into categories
            intensity_data['intensity_category'] = pd.cut(
                intensity_data['intensity'],
                bins=[-10, -5, 0, 5, 10],
                labels=['Very Negative', 'Negative', 'Positive', 'Very Positive']
            )
            
            intensity_counts = intensity_data['intensity_category'].value_counts().reset_index()
            intensity_counts.columns = ['Intensity', 'Count']
            
            fig = px.pie(
                intensity_counts,
                values='Count',
                names='Intensity',
                title="Distribution of Event Intensities",
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Geographic Distribution")
        
        # Map of events
        map_data = st.session_state.data.dropna(subset=['latitude', 'longitude']).copy()
        
        if not map_data.empty:
            # Add a slider to filter by event intensity if available
            if 'intensity' in map_data.columns:
                intensity_min, intensity_max = st.slider(
                    "Filter by Event Intensity", 
                    float(map_data['intensity'].min()), 
                    float(map_data['intensity'].max()),
                    (float(map_data['intensity'].min()), float(map_data['intensity'].max()))
                )
                map_data = map_data[(map_data['intensity'] >= intensity_min) & (map_data['intensity'] <= intensity_max)]
            
            # Create a new column for displaying "Source Link" instead of the full URL
            map_data['source_link'] = "Source Link"
            
            # Create the scatter_geo plot 
            fig = px.scatter_geo(
                map_data,
                lat='latitude',
                lon='longitude',
                color='event_type',
                hover_name='event_type',
                hover_data={
                    'source_name': True,
                    'target_name': True, 
                    'intensity': True, 
                    'location': True,
                    'source_link': True,  # Display "Source Link" text
                    'source_url': False,  # Hide the actual URL
                    'latitude': False,    # Hide latitude
                    'longitude': False    # Hide longitude
                },
                custom_data=['event_id', 'source_url'],  # Keep source_url in custom_data for reference
                projection='natural earth',
                title="Geographic Distribution of Events"
            )
            
            # Place legend horizontally below the map
            fig.update_layout(
                height=600,
                legend=dict(
                    orientation="h",  # horizontal orientation
                    yanchor="top",
                    y=-0.1,  # Position below the map
                    xanchor="center",
                    x=0.5,  # Center horizontally
                    title=dict(text="Event Types", side="top"),
                    font=dict(size=12),
                    traceorder="normal"
                ),
                margin=dict(l=0, r=0, t=40, b=100),  # Add bottom margin for legend
                geo=dict(
                    showland=True,
                    landcolor="rgb(212, 212, 212)",
                    subunitcolor="rgb(255, 255, 255)",
                    countrycolor="rgb(255, 255, 255)",
                    showlakes=True,
                    lakecolor="rgb(255, 255, 255)",
                    showsubunits=True,
                    showcountries=True,
                    showframe=False,
                    showcoastlines=True,
                    coastlinecolor="rgb(255, 255, 255)",
                    projection_type="equirectangular",                    
                    lonaxis=dict(range=[-180, 180]),
                    lataxis=dict(range=[-90, 90])
                )
            )
            
            # Adjust marker size for better visibility
            fig.update_traces(
                marker=dict(size=10, opacity=0.7, line=dict(width=1, color='white'))
            )
            
            # Display the map
            st.plotly_chart(fig, use_container_width=True)
            
            # Simplified approach: Use a selection widget to choose coordinates
            st.subheader("Select a Location to View Source URL")
            
            # Create location options with more descriptive labels
            location_options = []
            for i, row in map_data.reset_index().iterrows():
                # Create a descriptive label
                label = f"{row.event_type}: {row.source_name} → {row.target_name} in {row.location}"
                if len(label) > 80:  # Truncate if too long
                    label = label[:77] + "..."
                location_options.append({"label": label, "value": i})
            
            # Create selectbox with descriptive format function
            selected_location_index = st.selectbox(
                "Choose an event location:",
                options=range(len(location_options)),
                format_func=lambda x: location_options[x]["label"] if x < len(location_options) else "Select a location"
            )
            
            # Display the selected location's URL in a highlighted box
            if selected_location_index is not None and selected_location_index < len(map_data):
                selected_location = map_data.iloc[selected_location_index]
                
                # Display event details first
                st.markdown("### Selected Event Details")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Event Type:** {selected_location['event_type']}")
                    st.markdown(f"**Location:** {selected_location['location']}")
                    st.markdown(f"**Country:** {selected_location['country']}")
                
                with col2:
                    st.markdown(f"**Source:** {selected_location['source_name']}")
                    st.markdown(f"**Target:** {selected_location['target_name']}")
                    st.markdown(f"**Date:** {selected_location['date'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Display source URL in a highlighted box
                st.markdown("### Source URL")
                if pd.notna(selected_location['source_url']) and selected_location['source_url']:
                    url = selected_location['source_url']
                    st.markdown(
                        f"""
                        <div style="padding: 15px; background-color: #f0f2f6; border-radius: 5px; margin: 10px 0; border: 1px solid #e0e0e0;">
                            <a href="{url}" target="_blank" style="word-break: break-all; color: #1E88E5; text-decoration: underline; font-size: 16px;">
                                {url}
                            </a>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    # Add an explicit button for opening the URL in a new tab
                    st.markdown(
                        f"""
                        <div style="text-align: center; margin: 10px 0;">
                            <a href="{url}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #1E88E5; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">
                                Open Source Link in New Tab
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div style="padding: 15px; background-color: #f0f2f6; border-radius: 5px; margin: 10px 0; border: 1px solid #e0e0e0;">
                            <span style="color: #757575; font-style: italic;">No source URL available for this event</span>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
            
            # Country distribution
            st.subheader("Top Countries")
            country_counts = map_data['country'].value_counts().head(10).reset_index()
            country_counts.columns = ['Country', 'Count']
            
            fig = px.bar(
                country_counts,
                x='Country',
                y='Count',
                color='Count',
                color_continuous_scale='Viridis',
                title="Top 10 Countries by Event Count"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Geographic data not available for mapping")
    
    with tab3:
        st.subheader("Data Explorer")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            selected_event_types = st.multiselect(
                "Filter by Event Type",
                options=sorted(st.session_state.data['event_type'].unique()),
                default=[]
            )
        
        with col2:
            selected_countries = st.multiselect(
                "Filter by Country",
                options=sorted(st.session_state.data['country'].unique()),
                default=[]
            )
        
        # Apply filters
        filtered_data = st.session_state.data.copy()
        if selected_event_types:
            filtered_data = filtered_data[filtered_data['event_type'].isin(selected_event_types)]
        if selected_countries:
            filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
        
        # Show filtered data
        st.write(f"Showing {len(filtered_data)} events after filtering")
        
        # Add search functionality
        search_term = st.text_input("Search in data (source, target, location):", "")
        if search_term:
            search_mask = (
                filtered_data['source_name'].astype(str).str.contains(search_term, case=False) |
                filtered_data['target_name'].astype(str).str.contains(search_term, case=False) |
                filtered_data['location'].astype(str).str.contains(search_term, case=False)
            )
            filtered_data = filtered_data[search_mask]
            st.write(f"Found {len(filtered_data)} events matching '{search_term}'")
        
        # Display the data with pagination and clickable source URLs
        if not filtered_data.empty:
            # Select which columns to display
            display_data = filtered_data[['date', 'event_type', 'source_name', 'target_name', 
                                        'country', 'location', 'intensity', 'tone', 'source_url']].copy()
            
            # Format the date column for better readability
            display_data['date'] = display_data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Make the source_url clickable
            # We need to create a new column with formatted HTML
            display_data['source_url_link'] = display_data['source_url'].apply(
                lambda x: f'<a href="{x}" target="_blank">Source Link</a>' if pd.notna(x) and x else 'No URL'
            )
            
            # Display the data, excluding the raw URL column (we'll show the HTML links instead)
            final_display_data = display_data.drop(columns=['source_url'])
            
            # Create a column with clickable links using HTML
            st.write("### Event Data")
            
            
            # Convert source_url_link to HTML-rendered columns
            html_table = "<table style='width:100%'><tr>"
            
            # Header row
            for col in final_display_data.columns:
                if col != 'source_url_link':
                    display_name = col.replace('_', ' ').title()
                    html_table += f"<th style='text-align:left;padding:8px;border-bottom:1px solid #ddd;'>{display_name}</th>"
                else:
                    html_table += f"<th style='text-align:left;padding:8px;border-bottom:1px solid #ddd;'>Source URL</th>"
            
            html_table += "</tr>"
            
            # Data rows
            for _, row in final_display_data.iterrows():
                html_table += "<tr>"
                for col in final_display_data.columns:
                    if col != 'source_url_link':
                        cell_value = str(row[col]) if pd.notna(row[col]) else ""
                        html_table += f"<td style='text-align:left;padding:8px;border-bottom:1px solid #ddd;'>{cell_value}</td>"
                    else:
                        html_table += f"<td style='text-align:left;padding:8px;border-bottom:1px solid #ddd;'>{row[col]}</td>"
                html_table += "</tr>"
            
            html_table += "</table>"
            st.markdown(html_table, unsafe_allow_html=True)
            
            # Also show the regular dataframe for sorting/filtering (without the HTML column)
            st.write("### Data Table (Sortable)")
            regular_display = display_data.drop(columns=['source_url_link'])
            st.dataframe(regular_display, use_container_width=True)
            
            # Option to download the filtered data
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f"gdelt_events_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
        else:
            st.info("No data found with the current filters")
    
else:
    st.info("Click '🔄 Refresh Data' in the sidebar to load the latest GDELT events from the last 15 minutes")
    
    # Sample visualization explanation
    st.header("How it works")
    st.markdown("""
    1. **Data Collection**: When you click 'Refresh Data', we fetch the latest events from GDELT (last 15 minutes)
    2. **Data Processing**: The GDELT data is transformed to match the ICEWS data format
    3. **Visualization**: The processed data is displayed using ICEWS Explorer-inspired visualization components
    4. **Interaction**: You can filter and explore the data using the interactive controls
    
    The GDELT Project monitors world news media in over 100 languages and processes this information to identify events, entities, and themes.
    This application demonstrates how the ICEWS Explorer methodology can be used with GDELT data due to their compatible ontologies.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("About GDELT")
        st.markdown("""
        The [GDELT Project](https://www.gdeltproject.org/) is an open platform for monitoring and research on global news media.
        It captures events, entities, tones, themes, and locations from news reports worldwide.
        
        GDELT uses the CAMEO event coding system to categorize events, making it compatible with ICEWS data.
        """)
    
    with col2:
        st.subheader("About ICEWS Explorer")
        st.markdown("""
        The [ICEWS Explorer](https://github.com/brendancooley/icews-explorer) is a tool created to visualize and explore
        the Integrated Crisis Early Warning System (ICEWS) dataset.
        
        This Streamlit app adapts the visualization concepts from ICEWS Explorer to work with real-time GDELT data.
        """)

# Footer
st.markdown("---")
st.markdown("GDELT Data Visualization with ICEWS Explorer | Streamlit App")
