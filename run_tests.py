"""
Test runner script for the ML project.

This script provides an easy way to run all tests with proper configuration.
"""
import sys
import os
import subprocess
import argparse

def run_tests(test_path=None, verbose=False, coverage=False):
    """
    Run tests using pytest.
    
    Args:
        test_path: Specific test file or directory to run (optional)
        verbose: Enable verbose output
        coverage: Enable coverage reporting
    """
    # Add src directory to Python path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Build pytest command
    cmd = ['python', '-m', 'pytest']
    
    if verbose:
        cmd.append('-v')
    
    if coverage:
        cmd.extend(['--cov=src', '--cov-report=html', '--cov-report=term'])
    
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append('tests/')
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest")
        return 1

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Run tests for the ML project')
    parser.add_argument('--test', '-t', help='Specific test file or directory to run')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--coverage', '-c', action='store_true', help='Enable coverage reporting')
    
    args = parser.parse_args()
    
    return run_tests(
        test_path=args.test,
        verbose=args.verbose,
        coverage=args.coverage
    )

if __name__ == "__main__":
    sys.exit(main())
