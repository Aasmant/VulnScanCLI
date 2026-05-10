"""
Simple SQLite database for storing scan results.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class ScanDatabase:
    """SQLite database for scan storage."""
    
    def __init__(self, db_path: str = "VulnScanCLI_scans.db"):
        self.db_path = Path(db_path)
        self.init_db()
    
    def init_db(self):
        """Initialize database with schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create scans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                ports TEXT,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                results TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def reset_db(self):
        """Reset database (delete all data)."""
        if self.db_path.exists():
            self.db_path.unlink()
        self.init_db()
    
    def create_scan(self, target: str, ports: str, results: Dict) -> Dict:
        """
        Create a new scan record.
        
        Args:
            target: Target being scanned
            ports: Ports scanned
            results: Scan results dictionary
            
        Returns:
            Scan record with ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        results_json = json.dumps(results)
        
        cursor.execute("""
            INSERT INTO scans (target, ports, results, status)
            VALUES (?, ?, ?, 'completed')
        """, (target, ports, results_json))
        
        conn.commit()
        scan_id = cursor.lastrowid
        conn.close()
        
        return {
            'id': scan_id,
            'target': target,
            'ports': ports,
            'status': 'completed',
            'results': results
        }
    
    def get_scan(self, scan_id: int) -> Optional[Dict]:
        """Get a scan by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, target, ports, status, created_at, results
            FROM scans WHERE id = ?
        """, (scan_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'id': row[0],
            'target': row[1],
            'ports': row[2],
            'status': row[3],
            'created_at': row[4],
            'results': json.loads(row[5])
        }
    
    def list_scans(self, limit: int = 10) -> List[Dict]:
        """List recent scans."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, target, ports, status, created_at, results
            FROM scans
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        scans = []
        for row in rows:
            scans.append({
                'id': row[0],
                'target': row[1],
                'ports': row[2],
                'status': row[3],
                'created_at': row[4],
                'results': json.loads(row[5])
            })
        
        return scans
    
    def get_info(self) -> Dict:
        """Get database information."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM scans")
        scan_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'path': str(self.db_path.absolute()),
            'scan_count': scan_count,
            'created_at': datetime.now().isoformat()
        }
