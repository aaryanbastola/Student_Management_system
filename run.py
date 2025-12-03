# run.py - ADDITIONAL RUN SCRIPT FOR EASY START
import os
import sys
import webbrowser
from threading import Timer
from app import app

def open_browser():
    """Open browser to the app after a short delay"""
    Timer(1.5, lambda: webbrowser.open('http://localhost:5000')).start()

if __name__ == '__main__':
    # Create static folder if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Create templates folder if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Open browser automatically
    if len(sys.argv) > 1 and sys.argv[1] == '--open':
        open_browser()
    
    print("🚀 Starting Student Management System...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("\n" + "="*50)
    
    app.run(debug=True, port=5000)
