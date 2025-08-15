#!/usr/bin/env python3
"""
Personal Expense Tracker Pro
A professional-grade command-line expense management system.

Usage:
    python main.py

Requirements:
    pip install rich

Author: Enhanced by Claude
Version: 2.0.0
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path so modules can be imported
sys.path.append(str(Path(__file__).parent))

try:
    from enhanced_ui import ExpenseUI
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all files are in the same directory:")
    print("- main.py")
    print("- enhanced_expense_manager.py")
    print("- enhanced_ui.py")
    sys.exit(1)

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import rich
        return True
    except ImportError:
        print("=" * 60)
        print("OPTIONAL DEPENDENCY MISSING")
        print("=" * 60)
        print("For the best experience, install the 'rich' library:")
        print("  pip install rich")
        print()
        print("The application will work without it, but with basic formatting.")
        print("=" * 60)
        input("Press Enter to continue with basic mode...")
        return False

def main():
    """Main application entry point."""
    print("🚀 Starting Personal Expense Tracker Pro...")
    
    # Check dependencies
    has_rich = check_dependencies()
    
    try:
        # Initialize and run the application
        app = ExpenseUI()
        app.run()
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("\nIf this error persists, please check:")
        print("1. All required files are present")
        print("2. You have write permissions in the current directory")
        print("3. Your Python version is 3.7 or higher")
        
        if has_rich:
            print("4. Rich library is properly installed")

if __name__ == "__main__":
    main()
