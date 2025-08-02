#!/usr/bin/env python3
"""
Script to run the improved Kenya Protest Tracker Dashboard
with fixed scrolling issues and tabbed interface
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def run_dashboard():
    """Run the improved dashboard with error handling"""
    try:
        print("🚀 Starting Kenya Protest Tracker Dashboard...")
        print("📱 New Features: Tabbed interface, responsive design, no more scrolling issues!")
        print("=" * 60)
        
        # Check if dashboard.py exists
        if not Path('dashboard.py').exists():
            print("❌ Error: dashboard.py not found in current directory")
            print("Please run this script from the project root directory")
            return
        
        print("📊 Dashboard will be available at:")
        print("   Main Dashboard: http://localhost:8050")
        print("   Comparative Dashboard: http://localhost:8051")
        print()
        print("🔧 Improvements made:")
        print("   ✅ Tabbed interface prevents long scrolling")
        print("   ✅ Responsive design for mobile devices")
        print("   ✅ Better chart rendering and performance")
        print("   ✅ Fixed display issues with graphs")
        print("   ✅ Improved CSS and layout")
        print()
        print("📱 Tabs available:")
        print("   📊 Analytics Dashboard - Charts and visualizations")
        print("   🗺️  Interactive Map - Geographic protest data")
        print("   🔍 Insights & Recommendations - Analysis results")
        print()
        print("Press Ctrl+C to stop the dashboard")
        print("=" * 60)
        
        # Wait a moment then open browser
        time.sleep(2)
        try:
            webbrowser.open('http://localhost:8050')
            print("🌐 Opening dashboard in browser...")
        except:
            print("💡 Please manually open http://localhost:8050 in your browser")
        
        # Run the dashboard
        subprocess.run([sys.executable, 'dashboard.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running dashboard: {e}")
        print("💡 Make sure all required packages are installed:")
        print("   pip install dash plotly pandas numpy pathlib")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def run_comparative_dashboard():
    """Run the comparative dashboard"""
    try:
        print("🚀 Starting Comparative Dashboard...")
        print("📊 Available at: http://localhost:8051")
        subprocess.run([sys.executable, 'comparative_dashboard.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Comparative dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running comparative dashboard: {e}")

if __name__ == "__main__":
    print("Kenya Protest Tracker - Dashboard Launcher")
    print("Choose which dashboard to run:")
    print("1. Main Dashboard (Improved)")
    print("2. Comparative Dashboard")
    print("3. Both (in separate terminals)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        run_dashboard()
    elif choice == "2":
        run_comparative_dashboard()
    elif choice == "3":
        print("🔧 To run both dashboards:")
        print("Terminal 1: python dashboard.py")
        print("Terminal 2: python comparative_dashboard.py")
        print("Or run them in the background with &")
    else:
        print("❌ Invalid choice. Running main dashboard by default...")
        run_dashboard()