# YouTube Live Stream Scanners Documentation

This document explains how to use the various YouTube live stream detection tools available in this project.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Shell Script Manager](#shell-script-manager)
- [Python Scanner Scripts](#python-scanner-scripts)
- [Network List Configuration](#network-list-configuration)
- [Output Files](#output-files)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### For Immediate Results (Recommended)
```bash
# Quick scan (2-3 minutes)
./live_stream_manager.sh quick

# View latest results
./live_stream_manager.sh view
```

### For Continuous Monitoring
```bash
# Monitor every 15 minutes
./live_stream_manager.sh monitor 15

# Stop monitoring
./live_stream_manager.sh stop
```

---

## 🛠️ Shell Script Manager

The `live_stream_manager.sh` script provides an easy-to-use interface for all scanning operations.

### Prerequisites
```bash
# Make script executable (one-time setup)
chmod +x live_stream_manager.sh

# Install required Python packages
pip3 install requests beautifulsoup4 schedule
```

### Available Commands

| Command | Description | Duration | Use Case |
|---------|-------------|----------|----------|
| `quick` | Fast scan (fewer videos per channel) | 2-3 min | Regular updates |
| `full` | Comprehensive scan (more thorough) | 5-10 min | Detailed analysis |
| `test` | Test scan on known channels | 1-2 min | Verify system works |
| `monitor [interval]` | Continuous monitoring | Ongoing | Background monitoring |
| `schedule` | Scheduled monitoring (every 30 min) | Ongoing | Automated scanning |
| `view` | View latest results | Instant | Check current live streams |
| `status` | Show system status | Instant | Check if monitoring is running |
| `stop` | Stop any running monitoring | Instant | Stop background processes |
| `cleanup` | Clean up old result files | Instant | Maintenance |
| `help` | Show help message | Instant | Get usage information |

### Examples

```bash
# Basic usage
./live_stream_manager.sh quick                    # Quick scan
./live_stream_manager.sh full                     # Full scan
./live_stream_manager.sh test                     # Test scan

# Monitoring
./live_stream_manager.sh monitor 10               # Monitor every 10 minutes
./live_stream_manager.sh monitor 30               # Monitor every 30 minutes
./live_stream_manager.sh schedule                 # Scheduled monitoring

# Management
./live_stream_manager.sh view                     # View results
./live_stream_manager.sh status                   # Check status
./live_stream_manager.sh stop                     # Stop monitoring
./live_stream_manager.sh cleanup                  # Clean old files
```

---

## 🐍 Python Scanner Scripts

### 1. Auto Refresh Scanner (Recommended)
**File:** `auto_refresh_scanner.py`  
**Best for:** Regular updates and automation

```bash
# Single scans
python3 auto_refresh_scanner.py --mode single --quick           # Quick scan
python3 auto_refresh_scanner.py --mode single                   # Full scan

# Continuous monitoring
python3 auto_refresh_scanner.py --mode continuous --interval 15 # Every 15 minutes
python3 auto_refresh_scanner.py --mode continuous --interval 30 # Every 30 minutes

# Scheduled monitoring
python3 auto_refresh_scanner.py --mode scheduled                # Every 30 minutes
```

### 2. Comprehensive Live Scanner
**File:** `comprehensive_live_scanner.py`  
**Best for:** Detailed analysis with full results

```bash
python3 comprehensive_live_scanner.py
```

**Features:**
- Checks 15 videos per channel
- Detailed viewer count analysis
- Comprehensive JSON output
- Network-by-network breakdown

### 3. Advanced Live Detector
**File:** `advanced_live_detector.py`  
**Best for:** Testing specific channels

```bash
python3 advanced_live_detector.py
```

**Features:**
- Tests 5 known channels
- Video-by-video live detection
- Detailed debugging output
- Quick verification

### 4. Manual Scan Live Streams
**File:** `manual_scan_live_streams.py`  
**Best for:** Multi-endpoint checking

```bash
python3 manual_scan_live_streams.py
```

**Features:**
- Checks multiple endpoints per channel
- Manual verification approach
- Detailed scan results
- Threshold-based detection

### 5. Precise Live Scanner
**File:** `precise_live_scanner.py`  
**Best for:** Precise detection with specific patterns

```bash
python3 precise_live_scanner.py
```

**Features:**
- Targets specific "Live now" indicators
- HTML badge detection
- Precise pattern matching
- Detailed logging

### 6. Enhanced Scan Live Streams
**File:** `enhanced_scan_live_streams.py`  
**Best for:** Enhanced detection methods

```bash
python3 enhanced_scan_live_streams.py
```

**Features:**
- Multiple detection methods
- Channel ID extraction
- Enhanced pattern matching
- Comprehensive analysis

---

## 📝 Network List Configuration

### File Format
All scanners read from `network_list.txt` with this format:

```tsv
Network	YouTube Channel URL

6abc Philadelphia	https://www.youtube.com/@6abcActionNews
ABC News Australia	https://www.youtube.com/@abcnewsaustralia
ABC News Live	https://www.youtube.com/@ABCNews
Al Jazeera English	https://www.youtube.com/@aljazeeraenglish
...
```

### Adding New Networks
1. Open `network_list.txt`
2. Add new line with: `Network Name[TAB]https://www.youtube.com/@channel`
3. Save the file
4. All scanners will automatically use the updated list

### Current Networks (21 total)
- 6abc Philadelphia
- ABC News Australia
- ABC News Live
- Al Jazeera English
- Bloomberg Television
- CBS News 24/7
- CNBC
- CNBC-TV18
- CNN-News18
- DW News
- Euronews English
- FOX Weather
- FRANCE 24 English
- GB News
- LiveNOW from FOX
- NASA ISS Live
- NBC News NOW
- Sky News
- Times Now
- TRT World
- WION

---

## 📊 Output Files

### Primary Results
| File | Description | Updated By |
|------|-------------|------------|
| `latest_live_streams.json` | Latest scan results | auto_refresh_scanner.py |
| `comprehensive_live_streams.json` | Detailed comprehensive results | comprehensive_live_scanner.py |
| `quick_live_test_results.json` | Quick test results | advanced_live_detector.py |
| `detailed_scan_results.json` | Manual scan results | manual_scan_live_streams.py |

### Result Structure Example
```json
{
  "scan_timestamp": "2025-06-30T18:54:17.123456",
  "total_networks": 21,
  "live_streams_found": 33,
  "networks_with_live_content": 14,
  "live_streams": [
    {
      "network": "Al Jazeera English",
      "title": "Al Jazeera English | Live",
      "url": "https://www.youtube.com/watch?v=abc123",
      "viewers": 396135782,
      "video_id": "abc123"
    }
  ]
}
```

### Viewing Results
```bash
# Pretty print JSON results
cat latest_live_streams.json | python3 -m json.tool

# View with jq (if installed)
jq '.live_streams[] | {network, title, viewers}' latest_live_streams.json

# Use shell script manager
./live_stream_manager.sh view
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Permission Denied
```bash
chmod +x live_stream_manager.sh
```

#### 2. Python Module Not Found
```bash
pip3 install requests beautifulsoup4 schedule
```

#### 3. No Results Found
- Check network connectivity
- Verify `network_list.txt` format
- Try different scanner scripts
- Check for rate limiting

#### 4. Monitoring Not Working
```bash
# Check if monitoring is running
./live_stream_manager.sh status

# Stop any stuck processes
./live_stream_manager.sh stop

# Restart monitoring
./live_stream_manager.sh monitor 15
```

### Debug Mode
```bash
# Run with verbose output
python3 -u auto_refresh_scanner.py --mode single --quick

# Check specific network
python3 -c "
from auto_refresh_scanner import AutoRefreshLiveStreamScanner
scanner = AutoRefreshLiveStreamScanner()
networks = scanner.parse_network_list('network_list.txt')
print(f'Found {len(networks)} networks')
for name, url in networks[:3]:
    print(f'  {name}: {url}')
"
```

### Performance Tips

#### For Fast Updates
- Use `./live_stream_manager.sh quick`
- Use `--quick` flag with auto_refresh_scanner.py
- Monitor at 15-30 minute intervals

#### For Accuracy
- Use `./live_stream_manager.sh full`
- Use `comprehensive_live_scanner.py`
- Allow 5-10 minutes for complete scans

#### For Automation
- Use scheduled monitoring: `./live_stream_manager.sh schedule`
- Set up cron jobs for regular scans
- Monitor log files for errors

---

## 📈 Best Practices

### Regular Monitoring
```bash
# Set up continuous monitoring
./live_stream_manager.sh monitor 20

# Or use scheduled monitoring
./live_stream_manager.sh schedule
```

### Maintenance
```bash
# Weekly cleanup
./live_stream_manager.sh cleanup

# Check system status
./live_stream_manager.sh status
```

### Rate Limiting
- Don't run multiple scanners simultaneously
- Use appropriate intervals (15+ minutes)
- Monitor for 429 (Too Many Requests) errors

### Data Management
- Results are automatically timestamped
- Old files are cleaned up by `cleanup` command
- JSON files can be processed with standard tools

---

## 📞 Support

### Quick Help
```bash
./live_stream_manager.sh help
```

### Verify Installation
```bash
# Test parsing
python3 -c "from auto_refresh_scanner import AutoRefreshLiveStreamScanner; print('✅ Installation OK')"

# Test shell script
./live_stream_manager.sh status
```

### Log Files
- Scanner output is displayed in real-time
- Use `tee` to save output: `./live_stream_manager.sh quick | tee scan.log`
- Check system logs for background processes

---

*Last updated: June 30, 2025*
