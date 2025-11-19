#!/usr/bin/env python3
"""
Test Runner for AI Study Buddy

Simple script to run all tests with proper configuration and reporting.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run all tests with proper configuration."""
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("🧪 Running AI Study Buddy Test Suite")
    print("=" * 50)
    
    # Run pytest with verbose output
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short",
        "--color=yes"
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n❌ Some tests failed (exit code: {result.returncode})")
            
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
