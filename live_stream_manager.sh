#!/bin/bash
# Live Stream Manager - Easy management of YouTube live stream detection
# Usage: ./live_stream_manager.sh [command] [options]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="python3"
AUTO_SCANNER="auto_refresh_scanner.py"
ADVANCED_DETECTOR="advanced_live_detector.py"
COMPREHENSIVE_SCANNER="comprehensive_live_scanner.py"
RESULTS_FILE="latest_live_streams.json"
QUICK_RESULTS_FILE="quick_live_test_results.json"

# Function to print colored output
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}🔴 Live Stream Manager${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Check dependencies
check_dependencies() {
    print_info "Checking dependencies..."
    
    # Check Python
    if ! command -v $PYTHON_CMD &> /dev/null; then
        print_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
    
    # Check required Python packages
    $PYTHON_CMD -c "import requests, bs4, schedule" 2>/dev/null || {
        print_warning "Installing required Python packages..."
        pip3 install requests beautifulsoup4 schedule
    }
    
    # Check if scripts exist
    for script in "$AUTO_SCANNER" "$ADVANCED_DETECTOR" "$COMPREHENSIVE_SCANNER"; do
        if [[ ! -f "$script" ]]; then
            print_error "Required script not found: $script"
            exit 1
        fi
    done
    
    print_success "All dependencies satisfied"
}

# Quick scan function
quick_scan() {
    print_header
    print_info "Starting quick scan (2-3 minutes)..."
    echo ""
    
    $PYTHON_CMD "$AUTO_SCANNER" --mode single --quick
    
    if [[ -f "$RESULTS_FILE" ]]; then
        echo ""
        print_success "Quick scan completed!"
        show_summary
    else
        print_error "Scan failed - no results file generated"
    fi
}

# Full scan function
full_scan() {
    print_header
    print_info "Starting comprehensive scan (5-10 minutes)..."
    echo ""
    
    $PYTHON_CMD "$COMPREHENSIVE_SCANNER"
    
    if [[ -f "comprehensive_live_streams.json" ]]; then
        echo ""
        print_success "Comprehensive scan completed!"
        show_comprehensive_summary
    else
        print_error "Scan failed - no results file generated"
    fi
}

# Test scan with advanced detector
test_scan() {
    print_header
    print_info "Running advanced detector test on known channels..."
    echo ""
    
    $PYTHON_CMD "$ADVANCED_DETECTOR"
    
    if [[ -f "$QUICK_RESULTS_FILE" ]]; then
        echo ""
        print_success "Test scan completed!"
        show_test_summary
    else
        print_error "Test scan failed - no results file generated"
    fi
}

# Continuous monitoring
monitor() {
    local interval=${1:-15}
    print_header
    print_info "Starting continuous monitoring (every $interval minutes)"
    print_warning "Press Ctrl+C to stop monitoring"
    echo ""
    
    $PYTHON_CMD "$AUTO_SCANNER" --mode continuous --interval "$interval"
}

# Scheduled monitoring
schedule_monitor() {
    print_header
    print_info "Starting scheduled monitoring (every 30 minutes)"
    print_warning "Press Ctrl+C to stop monitoring"
    echo ""
    
    $PYTHON_CMD "$AUTO_SCANNER" --mode scheduled
}

# Show summary of results
show_summary() {
    if [[ -f "$RESULTS_FILE" ]]; then
        local live_count=$(jq '.live_streams_found // 0' "$RESULTS_FILE" 2>/dev/null || echo "0")
        local networks_count=$(jq '.networks_with_live_content // 0' "$RESULTS_FILE" 2>/dev/null || echo "0")
        
        echo ""
        echo -e "${PURPLE}📊 SUMMARY:${NC}"
        echo -e "   Live Streams Found: ${GREEN}$live_count${NC}"
        echo -e "   Networks with Live Content: ${GREEN}$networks_count${NC}"
        echo ""
        
        if command -v jq &> /dev/null; then
            echo -e "${PURPLE}🔴 Top 5 Live Streams:${NC}"
            jq -r '.live_streams[]? | select(.viewers > 0) | "   • \(.network): \(.title) (\(.viewers) viewers)"' "$RESULTS_FILE" 2>/dev/null | head -5
        fi
    fi
}

show_comprehensive_summary() {
    if [[ -f "comprehensive_live_streams.json" ]]; then
        local live_count=$(jq '.total_live_streams // 0' "comprehensive_live_streams.json" 2>/dev/null || echo "0")
        local networks_count=$(jq '.networks_with_live | length' "comprehensive_live_streams.json" 2>/dev/null || echo "0")
        
        echo ""
        echo -e "${PURPLE}📊 COMPREHENSIVE SUMMARY:${NC}"
        echo -e "   Live Streams Found: ${GREEN}$live_count${NC}"
        echo -e "   Networks with Live Content: ${GREEN}$networks_count${NC}"
        echo ""
        
        if command -v jq &> /dev/null; then
            echo -e "${PURPLE}🔴 Top Networks:${NC}"
            jq -r '.networks_with_live[]? | "   • \(.network): \(.live_streams) stream(s)"' "comprehensive_live_streams.json" 2>/dev/null | head -10
        fi
    fi
}

show_test_summary() {
    if [[ -f "$QUICK_RESULTS_FILE" ]]; then
        local live_count=$(jq '.live_streams_found // 0' "$QUICK_RESULTS_FILE" 2>/dev/null || echo "0")
        local channels_tested=$(jq '.channels_tested // 0' "$QUICK_RESULTS_FILE" 2>/dev/null || echo "0")
        
        echo ""
        echo -e "${PURPLE}📊 TEST SUMMARY:${NC}"
        echo -e "   Channels Tested: ${GREEN}$channels_tested${NC}"
        echo -e "   Live Streams Found: ${GREEN}$live_count${NC}"
        echo ""
        
        if command -v jq &> /dev/null && [[ "$live_count" -gt 0 ]]; then
            echo -e "${PURPLE}🔴 Live Streams Detected:${NC}"
            jq -r '.live_streams[]? | "   • \(.network): \(.title) (\(.viewers) viewers)"' "$QUICK_RESULTS_FILE" 2>/dev/null
        fi
    fi
}

# View latest results
view_results() {
    print_header
    
    if [[ -f "$RESULTS_FILE" ]]; then
        print_info "Latest scan results:"
        
        if command -v jq &> /dev/null; then
            local timestamp=$(jq -r '.scan_timestamp // "Unknown"' "$RESULTS_FILE" 2>/dev/null)
            echo -e "${CYAN}Scan Time: $timestamp${NC}"
            show_summary
            
            echo ""
            echo -e "${PURPLE}📄 Full results saved in: $RESULTS_FILE${NC}"
        else
            print_warning "Install 'jq' for formatted output: brew install jq"
            echo ""
            echo "Raw results:"
            cat "$RESULTS_FILE"
        fi
    else
        print_warning "No results file found. Run a scan first."
    fi
}

# Clean old result files
cleanup() {
    print_header
    print_info "Cleaning up old result files..."
    
    local cleaned=0
    
    # Remove old timestamped files
    find . -name "*live_streams_*.json" -mtime +7 -delete 2>/dev/null && cleaned=1
    find . -name "*scan_results_*.json" -mtime +7 -delete 2>/dev/null && cleaned=1
    
    if [[ $cleaned -eq 1 ]]; then
        print_success "Cleaned up old result files (older than 7 days)"
    else
        print_info "No old files to clean up"
    fi
}

# Show status
status() {
    print_header
    
    print_info "Live Stream Detection System Status"
    echo ""
    
    # Check if monitoring is running
    if pgrep -f "$AUTO_SCANNER" > /dev/null; then
        print_success "Monitoring is currently RUNNING"
        echo -e "${CYAN}   Process ID: $(pgrep -f "$AUTO_SCANNER")${NC}"
    else
        print_info "No monitoring currently running"
    fi
    
    # Check latest scan time
    if [[ -f "$RESULTS_FILE" ]]; then
        local timestamp=$(jq -r '.scan_timestamp // "Unknown"' "$RESULTS_FILE" 2>/dev/null)
        echo -e "${CYAN}   Last scan: $timestamp${NC}"
        
        local live_count=$(jq '.live_streams_found // 0' "$RESULTS_FILE" 2>/dev/null || echo "0")
        echo -e "${CYAN}   Live streams found: $live_count${NC}"
    else
        print_warning "No previous scan results found"
    fi
    
    # Check disk space for results
    local disk_usage=$(du -sh . 2>/dev/null | cut -f1 || echo "Unknown")
    echo -e "${CYAN}   Directory size: $disk_usage${NC}"
}

# Stop monitoring
stop_monitor() {
    print_header
    
    local pids=$(pgrep -f "$AUTO_SCANNER" 2>/dev/null || true)
    
    if [[ -n "$pids" ]]; then
        print_info "Stopping monitoring processes..."
        echo "$pids" | xargs kill 2>/dev/null || true
        sleep 2
        
        # Force kill if still running
        local still_running=$(pgrep -f "$AUTO_SCANNER" 2>/dev/null || true)
        if [[ -n "$still_running" ]]; then
            echo "$still_running" | xargs kill -9 2>/dev/null || true
            print_warning "Force stopped monitoring processes"
        else
            print_success "Monitoring stopped gracefully"
        fi
    else
        print_info "No monitoring processes found running"
    fi
}

# Show help
show_help() {
    print_header
    echo ""
    echo -e "${YELLOW}USAGE:${NC}"
    echo "  ./live_stream_manager.sh [command] [options]"
    echo ""
    echo -e "${YELLOW}COMMANDS:${NC}"
    echo -e "  ${GREEN}quick${NC}              Quick scan (2-3 minutes, fewer videos per channel)"
    echo -e "  ${GREEN}full${NC}               Comprehensive scan (5-10 minutes, thorough)"
    echo -e "  ${GREEN}test${NC}               Test scan on known channels"
    echo -e "  ${GREEN}monitor [interval]${NC} Continuous monitoring (default: every 15 minutes)"
    echo -e "  ${GREEN}schedule${NC}           Scheduled monitoring (every 30 minutes)"
    echo -e "  ${GREEN}view${NC}               View latest results"
    echo -e "  ${GREEN}status${NC}             Show system status"
    echo -e "  ${GREEN}stop${NC}               Stop any running monitoring"
    echo -e "  ${GREEN}cleanup${NC}            Clean up old result files"
    echo -e "  ${GREEN}help${NC}               Show this help message"
    echo ""
    echo -e "${YELLOW}EXAMPLES:${NC}"
    echo "  ./live_stream_manager.sh quick          # Run quick scan"
    echo "  ./live_stream_manager.sh monitor 10     # Monitor every 10 minutes"
    echo "  ./live_stream_manager.sh view           # View latest results"
    echo "  ./live_stream_manager.sh stop           # Stop monitoring"
    echo ""
    echo -e "${YELLOW}FILES:${NC}"
    echo -e "  ${CYAN}$RESULTS_FILE${NC}        Latest scan results"
    echo -e "  ${CYAN}$QUICK_RESULTS_FILE${NC}  Test scan results"
    echo -e "  ${CYAN}comprehensive_live_streams.json${NC}  Full scan results"
    echo ""
}

# Main script logic
main() {
    cd "$SCRIPT_DIR"
    
    # Check dependencies first
    check_dependencies
    
    case "${1:-help}" in
        "quick")
            quick_scan
            ;;
        "full")
            full_scan
            ;;
        "test")
            test_scan
            ;;
        "monitor")
            monitor "${2:-15}"
            ;;
        "schedule")
            schedule_monitor
            ;;
        "view")
            view_results
            ;;
        "status")
            status
            ;;
        "stop")
            stop_monitor
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
