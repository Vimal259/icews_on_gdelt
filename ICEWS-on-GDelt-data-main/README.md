# GDELT Data Visualization with ICEWS Explorer

This Streamlit application demonstrates the use of ICEWS Explorer with GDELT data. It fetches recent GDELT events (from the last 15 minutes), processes them to match the ICEWS data format, and visualizes them using components inspired by the ICEWS Explorer tool.

## Features

- **Real-time GDELT Data**: Fetches events from the last 15 minutes only
- **ICEWS Format Adaptation**: Converts GDELT data to match ICEWS format
- **Interactive Visualizations**: Explore events with filters and interactive charts
- **Geospatial Analysis**: Map-based visualization of global events
- **Event Intensity Analysis**: Analyze the tone and intensity of global events
- **Refresh Button**: Get the latest data with a single click
- **Data Export**: Download filtered data as CSV

## How It Works

1. Click the "🔄 Refresh Data" button in the sidebar to fetch the latest GDELT data
2. The GDELT data is transformed to match the ICEWS format
3. Explore the data through three different tabs:
   - Event Analysis: Charts showing event types and temporal distribution
   - Geographic View: Map-based visualization of event locations
   - Data Explorer: Detailed data table with filtering options

## Technical Details

This application demonstrates how the ICEWS Explorer methodology can be used with GDELT data due to their compatible ontologies. Both GDELT and ICEWS use CAMEO (Conflict and Mediation Event Observations) codes for event classification, which allows for seamless integration.

The main components of the application are:

- `app.py`: The main Streamlit application
- `gdelt_processor.py`: Functions for fetching and processing GDELT data
- `icews_adapter.py`: Functions for adapting GDELT data to ICEWS format

## Running the Application

This application can be run locally on your machine or deployed to any Python-compatible hosting platform.

### Running Locally

To run the full application locally with all ICEWS Explorer features:

1. Clone or download this entire repository to your local machine:
   ```
   git clone https://github.com/your-username/gdelt-icews-explorer.git
   ```
   
   Or download all files as a ZIP and extract them to a folder.

2. Install all required packages:
   ```
   pip install streamlit pandas numpy plotly requests
   ```

3. Launch the application using our local launcher script:
   ```
   python local_launcher.py
   ```
   
   This will automatically:
   - Create the necessary `.streamlit` configuration for local use
   - Start the Streamlit server
   - Open the app in your default browser

4. Alternatively, you can run the Streamlit app directly:
   ```
   streamlit run app.py
   ```

The application provides all ICEWS Explorer features and visualizations when run locally.

**For a detailed, step-by-step installation guide with troubleshooting tips and platform-specific instructions, see [LOCAL_INSTALLATION.md](LOCAL_INSTALLATION.md).**

## About the Data

The [GDELT Project](https://www.gdeltproject.org/) monitors world news media in over 100 languages and processes this information to identify events, entities, and themes. It captures a wide range of information about global events, including actors, event types, locations, and sentiment.

The [ICEWS Explorer](https://github.com/brendancooley/icews-explorer) is a tool created to visualize and explore the Integrated Crisis Early Warning System (ICEWS) dataset. This Streamlit application adapts the visualization concepts from ICEWS Explorer to work with real-time GDELT data.

## Troubleshooting

### Common Issues When Running Locally

1. **Package Installation Problems**:
   - Make sure you have Python 3.7+ installed
   - Install all required packages: `pip install streamlit pandas numpy plotly requests`
   - If you're using a virtual environment, make sure it's activated

2. **Port Already in Use**:
   - If you see an error about port 8501 being in use, you might have another Streamlit app running
   - Stop the other app or modify the port in `.streamlit/config.toml`

3. **Import Errors**:
   - Ensure all project files are in the same directory
   - Check that you have all the required files: `app.py`, `gdelt_processor.py`, `icews_adapter.py`

4. **GDELT Data Access Issues**:
   - The app fetches data from GDELT's public API which might occasionally be slow or unavailable
   - Try clicking the refresh button again after a brief wait
   - Check your internet connection

5. **Browser Issues**:
   - If the app doesn't open automatically, manually navigate to `http://localhost:8501`
   - Clear your browser cache
   - Try a different browser

### Deployment Issues

1. **Server Configuration**:
   - When deploying to a server, ensure port settings are configured correctly
   - For production deployment, consider using a proper WSGI server
   
2. **Environment Variables**:
   - Configure any necessary environment variables for your hosting platform
   - Ensure the server has proper permissions to access required resources

