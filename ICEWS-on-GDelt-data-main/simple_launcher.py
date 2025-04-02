#!/usr/bin/env python3
"""
Simple launcher for the streamlit app.
"""
import subprocess
import sys
import time

def main():
    """Launch the streamlit app."""
    print("Starting the simple GDELT Data Explorer...")
    
    # Check for streamlit
    try:
        subprocess.run(["streamlit", "--version"], 
                      check=True, 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Streamlit not found. Please install it with:")
        print("pip install streamlit pandas numpy plotly requests")
        return
    
    # Start streamlit
    print("Launching streamlit app...")
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "simple_app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Print info message
    print("\nThe app should open in your default web browser.")
    print("If it doesn't, you can access it at: http://localhost:8501\n")
    print("Press Ctrl+C to stop the app.")
    
    try:
        # Just keep the script running until Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the app...")
        streamlit_process.terminate()
        print("App has been stopped.")

if __name__ == "__main__":
    main()