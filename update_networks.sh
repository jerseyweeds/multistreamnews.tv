#!/bin/bash

# Networks.txt Maintenance Automation Script
# ==========================================
# 
# This script automates the maintenance of the Networks.txt file.
# It can be run manually or scheduled via cron.
#
# Usage:
#   ./update_networks.sh [quick|full|refresh|check]
#
# Modes:
#   quick   - Update existing streams only (default)
#   full    - Update existing streams and search for new ones
#   refresh - Perform full refresh from network_list.txt (rebuilds Networks.txt)
#   check   - Check status without updating files
#
# Cron example (run every 30 minutes):
#   */30 * * * * cd /path/to/multistreamnews.tv && ./update_networks.sh quick >> networks_update.log 2>&1

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/networks_update.log"
MAX_LOG_SIZE=1048576  # 1MB
PYTHON_CMD="python3"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    log "ERROR: $1"
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}$1${NC}"
    log "SUCCESS: $1"
}

# Warning message
warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
    log "WARNING: $1"
}

# Info message
info() {
    echo -e "${BLUE}INFO: $1${NC}"
    log "INFO: $1"
}

# Rotate log file if it gets too large
rotate_log() {
    if [[ -f "$LOG_FILE" && $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0) -gt $MAX_LOG_SIZE ]]; then
        mv "$LOG_FILE" "${LOG_FILE}.old"
        info "Log file rotated"
    fi
}

# Check if Python is available
check_python() {
    if ! command -v $PYTHON_CMD &> /dev/null; then
        error_exit "Python 3 is not installed or not in PATH"
    fi
    
    # Check Python version
    python_version=$($PYTHON_CMD --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    major_version=$(echo $python_version | cut -d. -f1)
    minor_version=$(echo $python_version | cut -d. -f2)
    
    if [[ $major_version -lt 3 || ($major_version -eq 3 && $minor_version -lt 7) ]]; then
        error_exit "Python 3.7 or higher is required. Found: $python_version"
    fi
    
    info "Using Python $python_version"
}

# Install Python dependencies
install_dependencies() {
    if [[ -f "$SCRIPT_DIR/requirements.txt" ]]; then
        info "Installing Python dependencies..."
        if $PYTHON_CMD -m pip install -r "$SCRIPT_DIR/requirements.txt" --quiet; then
            success "Dependencies installed successfully"
        else
            error_exit "Failed to install Python dependencies"
        fi
    else
        warning "requirements.txt not found, skipping dependency installation"
    fi
}

# Check if networks file exists
check_networks_file() {
    if [[ ! -f "$SCRIPT_DIR/Networks.txt" ]]; then
        error_exit "Networks.txt file not found in $SCRIPT_DIR"
    fi
}

# Backup networks file
backup_networks() {
    local backup_file="$SCRIPT_DIR/Networks.txt.backup.$(date '+%Y%m%d_%H%M%S')"
    if cp "$SCRIPT_DIR/Networks.txt" "$backup_file"; then
        info "Created backup: $(basename "$backup_file")"
        
        # Keep only the 5 most recent backups
        ls -t "$SCRIPT_DIR"/Networks.txt.backup.* 2>/dev/null | tail -n +6 | xargs rm -f
    else
        warning "Failed to create backup"
    fi
}

# Run the maintenance script
run_maintenance() {
    local mode="$1"
    local python_args=""
    
    case "$mode" in
        "check")
            python_args="--check-only --verbose"
            info "Running in check-only mode..."
            ;;
        "full")
            python_args="--add-new --verbose"
            info "Running full maintenance (including search for new streams)..."
            backup_networks
            ;;
        "refresh")
            python_args="--refresh --verbose"
            info "Running full refresh from network_list.txt (rebuilding Networks.txt)..."
            backup_networks
            ;;
        "quick"|*)
            python_args="--verbose"
            info "Running quick maintenance (existing streams only)..."
            backup_networks
            ;;
    esac
    
    cd "$SCRIPT_DIR"
    
    if $PYTHON_CMD maintain_networks.py $python_args; then
        success "Maintenance completed successfully"
        
        # Show current status
        if [[ -f "Networks.txt" ]]; then
            local live_count=$(tail -n +2 "Networks.txt" | wc -l | tr -d ' ')
            info "Current live streams: $live_count"
        fi
    else
        error_exit "Maintenance script failed"
    fi
}

# Show usage
show_usage() {
    cat << EOF
Usage: $0 [mode]

Modes:
  quick   - Update existing streams only (default)
  full    - Update existing streams and search for new ones  
  refresh - Perform full refresh from network_list.txt (rebuilds Networks.txt)
  check   - Check status without updating files

Examples:
  $0 quick     # Quick update (default)
  $0 full      # Full update with new stream search
  $0 refresh   # Rebuild Networks.txt from network_list.txt
  $0 check     # Check only, no file changes

This script maintains the Networks.txt file by checking YouTube live streams
and updating their status and viewer counts. The refresh mode will completely
rebuild Networks.txt by searching all channels listed in network_list.txt.

Files:
  Networks.txt        - Main networks database
  Networks.txt.backup.* - Automatic backups
  networks_update.log - Operation log

Cron example (every 30 minutes):
  */30 * * * * cd $SCRIPT_DIR && ./update_networks.sh quick >> networks_update.log 2>&1
EOF
}

# Main execution
main() {
    local mode="${1:-quick}"
    
    # Handle help
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    # Validate mode
    case "$mode" in
        "quick"|"full"|"refresh"|"check")
            ;;
        *)
            echo -e "${RED}Invalid mode: $mode${NC}"
            show_usage
            exit 1
            ;;
    esac
    
    rotate_log
    log "Starting networks maintenance - Mode: $mode"
    
    # Pre-flight checks
    check_python
    check_networks_file
    
    # Install dependencies if needed
    if [[ "$mode" != "check" ]]; then
        install_dependencies
    fi
    
    # Run maintenance
    run_maintenance "$mode"
    
    log "Networks maintenance completed - Mode: $mode"
}

# Run main function with all arguments
main "$@"
