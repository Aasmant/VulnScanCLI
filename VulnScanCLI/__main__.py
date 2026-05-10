"""
VulnScanCLI - Python Security Automation CLI
Entry point for running as: python -m VulnScanCLI
"""

from VulnScanCLI.cli import main
import sys

if __name__ == '__main__':
    sys.exit(main())
