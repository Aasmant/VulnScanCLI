"""
Unit Tests for VulnScanCLI - Network Security Automation Tool
"""

import unittest
import tempfile
import os
from VulnScanCLI.scanner.nmap_scanner import NmapScanner
from VulnScanCLI.reporting.report_generator import ReportGenerator
from VulnScanCLI.database.sqlite_db import ScanDatabase


class TestNmapScanner(unittest.TestCase):
    """Test Nmap scanning functionality"""
    
    def setUp(self):
        self.scanner = NmapScanner()
    
    def test_scanner_initialization(self):
        """Test scanner initializes correctly"""
        self.assertIsNotNone(self.scanner)
    
    def test_common_vulnerabilities_available(self):
        """Test that common vulnerabilities are available"""
        vulns = self.scanner.get_common_vulnerabilities('SSH', '2.2.2')
        self.assertIsInstance(vulns, list)


class TestReportGenerator(unittest.TestCase):
    """Test report generation functionality"""
    
    def setUp(self):
        self.generator = ReportGenerator()
        # Sample scan with correct data structure for report_generator
        self.sample_scan = {
            'id': 1,
            'target': '127.0.0.1',
            'ports': '22,80,443',
            'status': 'completed',
            'created_at': '2026-05-10',
            'results': {
                'target': '127.0.0.1',
                'hosts': [
                    {
                        'ip': '127.0.0.1',
                        'hostname': 'localhost',
                        'state': 'up',
                        'services': [
                            {'port': 22, 'state': 'open', 'service': 'ssh', 'product': 'OpenSSH', 'version': '7.4'}
                        ]
                    }
                ]
            }
        }
    
    def test_json_report_generation(self):
        """Test JSON report generation"""
        report = self.generator.generate(self.sample_scan, format='json')
        self.assertIsNotNone(report)
        self.assertIn('scan_id', report)
    
    def test_html_report_generation(self):
        """Test HTML report generation"""
        report = self.generator.generate(self.sample_scan, format='html')
        self.assertIsNotNone(report)
        self.assertIn('<html', report.lower())
    
    def test_text_report_generation(self):
        """Test text report generation"""
        report = self.generator.generate(self.sample_scan, format='text')
        self.assertIsNotNone(report)
        self.assertIn('127.0.0.1', report)


class TestScanDatabase(unittest.TestCase):
    """Test SQLite database operations"""
    
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        self.db = ScanDatabase(self.db_path)
        self.db.init_db()
    
    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_database_initialization(self):
        """Test database initializes correctly"""
        self.assertTrue(os.path.exists(self.db_path))
    
    def test_scan_creation(self):
        """Test creating a scan record"""
        result = self.db.create_scan(
            target='127.0.0.1',
            ports='22,80',
            results={'hosts': []}
        )
        
        self.assertIsNotNone(result)
        self.assertIn('id', result)
    
    def test_scan_retrieval(self):
        """Test retrieving a scan record"""
        created = self.db.create_scan(
            target='127.0.0.1',
            ports='22,80',
            results={'hosts': []}
        )
        
        retrieved = self.db.get_scan(created['id'])
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['target'], '127.0.0.1')
    
    def test_scan_listing(self):
        """Test listing all scans"""
        self.db.create_scan('127.0.0.1', '22', {'hosts': []})
        self.db.create_scan('192.168.1.1', '80', {'hosts': []})
        
        scans = self.db.list_scans()
        self.assertGreaterEqual(len(scans), 2)


if __name__ == '__main__':
    unittest.main()
