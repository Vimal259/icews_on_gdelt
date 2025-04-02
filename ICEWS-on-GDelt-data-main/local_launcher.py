#!/usr/bin/env python3
"""
Local launcher for the full GDELT Data Visualization with ICEWS Explorer application.
"""
import subprocess
import sys
import time
import os

def main():
    """Launch the full Streamlit app with ICEWS Explorer features."""
    print("Starting GDELT Data Visualization with ICEWS Explorer...")
    
    # Check if the .streamlit directory exists, if not create it
    streamlit_dir = ".streamlit"
    if not os.path.exists(streamlit_dir):
        os.makedirs(streamlit_dir)
    
    # Create the Streamlit config file if it doesn't exist
    config_file = os.path.join(streamlit_dir, "config.toml")
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write("""[server]
headless = false
address = "localhost"
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
""")
        print(f"Created Streamlit configuration file at {config_file}")
    
    # Check for required packages
    try:
        subprocess.run(["streamlit", "--version"], 
                      check=True, 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Streamlit not found. Please install it with:")
        print("pip install streamlit pandas numpy plotly requests")
        return
    
    # Start streamlit with the full app
    print("Launching the full GDELT Data Visualization with ICEWS Explorer app...")
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Print info message
    print("\nThe app should open in your default web browser.")
    print("If it doesn't, you can access it at: http://localhost:8501\n")
    print("Press Ctrl+C to stop the app.")
    
    try:
        # Just wait for Ctrl+C while displaying status messages
        print("Streamlit is running...")
        print("The application should open in your web browser automatically.")
        print("If it doesn't, open http://localhost:8501 manually.")
        
        # Keep the script running until Ctrl+C or until the Streamlit process ends
        while streamlit_process.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the app...")
        streamlit_process.terminate()
        print("App has been stopped.")

if __name__ == "__main__":
    main()