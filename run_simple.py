#!/usr/bin/env python3
"""
Simple Flask runner for Virtual IHC Analysis System
Run this instead of main.py for better stability
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("Starting Virtual IHC Analysis System...")
    print("Server will be available at: http://0.0.0.0:5000")
    
    # Run with minimal configuration for stability
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )