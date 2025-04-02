# Local Installation Guide for GDELT Data Visualization with ICEWS Explorer

This guide provides detailed step-by-step instructions for setting up and running the GDELT Data Visualization with ICEWS Explorer application on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed on your computer:

- Python 3.7 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Step 1: Get the Code

### Option A: Clone the Repository Using Git

If you have Git installed, open a terminal or command prompt and run:

```bash
git clone https://github.com/your-username/gdelt-icews-explorer.git
cd gdelt-icews-explorer
```

### Option B: Download as ZIP

1. On the repository page, click the "Code" button and select "Download ZIP"
2. Extract the ZIP file to a folder on your computer
3. Open a terminal or command prompt and navigate to the extracted folder:
   ```bash
   cd path/to/extracted/folder
   ```

## Step 2: Install Required Packages

Install all the necessary Python packages using pip:

```bash
pip install streamlit pandas numpy plotly requests
```

If you're using a virtual environment (recommended), activate it first:

### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install streamlit pandas numpy plotly requests
```

### For macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
pip install streamlit pandas numpy plotly requests
```

## Step 3: Launch the Application

### Option A: Using the Local Launcher (Recommended)

Run the local launcher script which will set up the proper configuration and start the application:

```bash
python local_launcher.py
```

The application should automatically open in your default web browser.

### Option B: Using Streamlit Directly

Alternatively, you can run the Streamlit app directly:

```bash
streamlit run app.py
```

## Step 4: Using the Application

1. Once the application is running, you'll see the GDELT Data Visualization with ICEWS Explorer interface in your web browser
2. Click the "🔄 Refresh Data" button in the sidebar to fetch the latest GDELT events from the last 15 minutes
3. Explore the data using the different tabs:
   - Event Analysis: View distributions of event types and timeline
   - Geographic View: Explore events on a world map
   - Data Explorer: Filter and search through the raw event data

## Troubleshooting

### Installation Issues

- **Package installation fails**: Try upgrading pip first: `pip install --upgrade pip`
- **Python version conflicts**: Use a virtual environment with Python 3.7+
- **Permission errors**: 
  - Windows: Try running the command prompt as Administrator
  - macOS/Linux: Use `sudo pip install` or create a virtual environment

### Runtime Issues

- **Import errors**: Ensure you're running the command from the directory containing all the project files
- **Port already in use**: If port 8501 is already in use, Streamlit will try to use another port. Check the terminal output for the URL.
- **Browser doesn't open**: Manually navigate to `http://localhost:8501` in your web browser
- **No data displayed**: 
  - Check your internet connection
  - GDELT's API might be temporarily unavailable, try again later
  - Click the "Refresh Data" button again

### GDELT API Issues

- The application relies on GDELT's public API which may have rate limits or occasional downtime
- If you see errors when fetching data, wait a few minutes and try again
- Check the GDELT Project website (https://www.gdeltproject.org/) for any announcements about API availability

## Advanced Configuration

If you need to modify advanced settings:

1. Edit the `.streamlit/config.toml` file for Streamlit configuration
2. To change the port, modify the `port = 8501` line in the config file
3. To enable additional Streamlit features, refer to the [Streamlit configuration documentation](https://docs.streamlit.io/library/advanced-features/configuration)

## Running on Different Platforms

### Windows

- Make sure to use the correct path separators (`\`) in file paths
- If Python is not in your PATH, use the full path to the Python executable

### macOS

- You may need to install developer tools: `xcode-select --install`
- For package installation issues, try using `pip3` instead of `pip`

### Linux

- Ensure you have the required development libraries: `sudo apt-get install python3-dev`
- For visualization issues, you might need to install additional dependencies: `sudo apt-get install python3-tk`

## Getting Help

If you encounter issues not covered in this guide, check:

1. The README.md file for general information
2. The Troubleshooting section in the README
3. The Streamlit documentation at https://docs.streamlit.io/