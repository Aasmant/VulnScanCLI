#!/usr/bin/env python3
"""
VulnScanCLI - Simple Network Security Scanner
A Python automation tool for vulnerability assessment and network scanning.
"""

import sys
import argparse
import json
from pathlib import Path

from VulnScanCLI.scanner.nmap_scanner import NmapScanner
from VulnScanCLI.reporting.report_generator import ReportGenerator
from VulnScanCLI.database.sqlite_db import ScanDatabase

def main():
    parser = argparse.ArgumentParser(
        prog='VulnScanCLI',
        description='VulnScanCLI - Python Security Automation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    VulnScanCLI scan 192.168.1.0/24              # Scan a network
    VulnScanCLI scan -p 22,80,443 192.168.1.1    # Scan specific ports
    VulnScanCLI report --scan-id 1 --format json  # Generate report
    VulnScanCLI list                              # List all scans
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan a target')
    scan_parser.add_argument('target', help='Target IP/CIDR range')
    scan_parser.add_argument('-p', '--ports', help='Ports to scan (e.g., 22,80,443)')
    scan_parser.add_argument('--timeout', type=int, default=300, help='Scan timeout in seconds')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate scan report')
    report_parser.add_argument('--scan-id', type=int, required=True, help='Scan ID')
    report_parser.add_argument('--format', choices=['json', 'html', 'text'], default='json', help='Report format')
    report_parser.add_argument('-o', '--output', help='Output file')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all scans')
    list_parser.add_argument('--limit', type=int, default=10, help='Number of scans to show')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check scan status')
    status_parser.add_argument('scan_id', type=int, help='Scan ID')
    
    # Database command
    db_parser = subparsers.add_parser('db', help='Database operations')
    db_parser.add_argument('action', choices=['init', 'reset', 'info'], help='Database action')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize database
    db = ScanDatabase()
    
    try:
        if args.command == 'scan':
            return cmd_scan(args, db)
        elif args.command == 'report':
            return cmd_report(args, db)
        elif args.command == 'list':
            return cmd_list(args, db)
        elif args.command == 'status':
            return cmd_status(args, db)
        elif args.command == 'db':
            return cmd_db(args, db)
        else:
            parser.print_help()
            return 1
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_scan(args, db):
    """Execute a scan."""
    print(f"🔍 Starting scan of {args.target}...")
    
    scanner = NmapScanner()
    ports = args.ports if args.ports else None
    
    # Run scan
    results = scanner.scan(args.target, ports=ports, timeout=args.timeout)
    
    # Save to database
    scan_record = db.create_scan(
        target=args.target,
        ports=ports or 'all',
        results=results
    )
    
    print(f"✅ Scan complete! Scan ID: {scan_record['id']}")
    print(f"   Found {len(results.get('hosts', []))} hosts")
    print(f"\n   Generate report: VulnScanCLI report --scan-id {scan_record['id']}")
    
    return 0


def cmd_report(args, db):
    """Generate a scan report."""
    scan = db.get_scan(args.scan_id)
    
    if not scan:
        print(f"❌ Scan {args.scan_id} not found")
        return 1
    
    print(f"📄 Generating {args.format} report for scan {args.scan_id}...")
    
    generator = ReportGenerator()
    report = generator.generate(scan, format=args.format)
    
    if args.output:
        Path(args.output).write_text(report)
        print(f"✅ Report saved to {args.output}")
    else:
        print(report)
    
    return 0


def cmd_list(args, db):
    """List all scans."""
    scans = db.list_scans(limit=args.limit)
    
    if not scans:
        print("No scans found")
        return 0
    
    print(f"\n{'ID':<5} {'Target':<20} {'Date':<20} {'Status':<10}")
    print("─" * 60)
    
    for scan in scans:
        print(f"{scan['id']:<5} {scan['target']:<20} {scan['created_at']:<20} {scan['status']:<10}")
    
    return 0


def cmd_status(args, db):
    """Check scan status."""
    scan = db.get_scan(args.scan_id)
    
    if not scan:
        print(f"❌ Scan {args.scan_id} not found")
        return 1
    
    print(f"\nScan {args.scan_id}:")
    print(f"  Target: {scan['target']}")
    print(f"  Status: {scan['status']}")
    print(f"  Created: {scan['created_at']}")
    print(f"  Hosts found: {len(scan['results'].get('hosts', []))}")
    
    return 0


def cmd_db(args, db):
    """Database operations."""
    if args.action == 'init':
        db.init_db()
        print("✅ Database initialized")
        return 0
    elif args.action == 'reset':
        db.reset_db()
        print("✅ Database reset")
        return 0
    elif args.action == 'info':
        info = db.get_info()
        print(f"\nDatabase info:")
        print(f"  Path: {info['path']}")
        print(f"  Scans: {info['scan_count']}")
        print(f"  Created: {info['created_at']}")
        return 0


if __name__ == '__main__':
    sys.exit(main())
