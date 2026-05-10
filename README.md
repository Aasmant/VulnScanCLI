# VulnScanCLI - Python Security Automation Tool

**Status**: Simple Python CLI tool for network scanning and vulnerability reporting  
**Built for**: Learning and practicing security automation  
**Free & Open Source**: Yes ✅

---

## What This Is

A **simple Python automation tool** I built to learn:

✅ Network scanning (Nmap integration)  
✅ Vulnerability identification  
✅ Report generation (JSON/HTML)  
✅ Python CLI applications  
✅ SQLite database usage  

**What it's NOT:**
- ❌ Enterprise vulnerability scanner (too basic)
- ❌ Replacement for Nessus/OpenVAS
- ❌ Complex full-stack application
- ❌ Production-ready security tool

---

## Quick Start (30 seconds)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run a scan (local network example)
python -m VulnScanCLI scan 192.168.1.0/24

# 3. Generate report
python -m VulnScanCLI report --scan-id 1 --format json

# 4. View all scans
python -m VulnScanCLI list
```

---

## How It Works

### 1. **Network Scanning**
```bash
python -m VulnScanCLI scan 192.168.1.0/24
# Discovers live hosts on network
```

### 2. **Port Scanning** (Optional)
```bash
python -m VulnScanCLI scan -p 22,80,443 192.168.1.1
# Scans specific ports on a target
```

### 3. **Report Generation**
```bash
# JSON report (machine-readable)
python -m VulnScanCLI report --scan-id 1 --format json

# HTML report (human-readable)
python -m VulnScanCLI report --scan-id 1 --format html -o report.html

# Text report (console-friendly)
python -m VulnScanCLI report --scan-id 1 --format text
```

### 4. **Scan History**
```bash
# List all scans
python -m VulnScanCLI list

# Check scan status
python -m VulnScanCLI status 1
```

---

## Project Structure

```
VulnScanCLI/
├── scanner/
│   └── nmap_scanner.py         # Nmap integration
├── reporting/
│   └── report_generator.py     # Report generation (JSON/HTML/text)
├── database/
│   └── sqlite_db.py            # SQLite scan storage
├── cli.py                       # Command-line interface
└── __main__.py                  # Entry point
```

---

## What It Does

### Scanning Phase
1. Takes a target (IP or CIDR range)
2. Uses Nmap to discover live hosts
3. Optionally scans specific ports
4. Saves results to local SQLite database

### Reporting Phase
1. Retrieves scan from database
2. Generates report in requested format
3. Outputs to console or file

### Simple Vulnerability Detection
- Basic service-based vulnerability suggestions
- Local database (not connected to NVD/CISA)
- Educational only

---

## Technology Stack

| Component | Choice | Why |
|-----------|--------|-----|
| **Language** | Python | Security field standard |
| **Scanning** | Nmap | Industry standard tool |
| **Database** | SQLite | No server dependency, simple |
| **CLI** | argparse | Built-in Python, lightweight |
| **Reporting** | JSON/HTML | Standard formats, no dependencies |

---

## What I Learned Building This

✅ Network discovery with Nmap  
✅ Python subprocess integration  
✅ SQLite for local data storage  
✅ JSON for data interchange  
✅ CLI design with argparse  
✅ Report generation patterns  
✅ Python package structure  

---

## Limitations (Intentional)

- No external API calls (NVD/CISA) → Keep it simple
- Local database only → No network requirements  
- Basic vulnerability detection → Learning project, not enterprise tool
- Single-threaded scanning → Simplicity over performance
- No GUI dashboard → CLI is cleaner for learning

---

## Why This Approach?

Instead of building a "fancy full-stack app", I focused on:

✅ **Understanding security workflows** through automation  
✅ **Clean Python code** with proper structure  
✅ **Real tools** (Nmap) that security pros use  
✅ **Honest scope** - this is what it is, nothing more  
✅ **Portfolio value** - shows I can automate, not just fetch data  

---

## Example Workflow

```bash
# 1. Scan your local network
$ python -m VulnScanCLI scan 192.168.1.0/24
🔍 Starting scan of 192.168.1.0/24...
✅ Scan complete! Scan ID: 1
   Found 5 hosts

# 2. View the results
$ python -m VulnScanCLI list
ID    Target              Date                 Status
───────────────────────────────────────────────────────
1     192.168.1.0/24      2024-05-08 10:30:45  completed

# 3. Generate a report
$ python -m VulnScanCLI report --scan-id 1 --format text
╔════════════════════════════════════════════════════════════════╗
║                   VulnScanCLI SCAN REPORT                      ║
╚════════════════════════════════════════════════════════════════╝

Scan ID:        1
Target:         192.168.1.0/24
Date:           2024-05-08 10:30:45
Status:         completed

SUMMARY
───────────────────────────────────────────────────────────────
Total Hosts:    5
Total Services: 12
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Nmap installed on your system:
  ```bash
  # macOS
  brew install nmap
  brew upgrade nmap
  
  # Ubuntu/Debian
  sudo apt-get install nmap
  ```

### Install VulnScanCLI
```bash
git clone https://github.com/yourusername/VulnScanCLI.git
cd VulnScanCLI
pip install -r requirements.txt
python -m VulnScanCLI db init
```

### First Scan
```bash
python -m VulnScanCLI scan 192.168.1.0/24
```

---

## Legal Notice

⚠️ **Warning**: Only scan networks you own or have written permission to scan.

---

## License

MIT License - Free to use and modify

---

**This is a learning project. Simple, honest, human-made. 🔍**
