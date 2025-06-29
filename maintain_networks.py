#!/usr/bin/env python3
"""
Networks.txt Maintenance Script
===============================

This script maintains the Networks.txt file by:
1. Checking if YouTube streams are currently live
2. Updating viewer counts
3. Removing dead streams
4. Adding new live streams from channels listed in network_list.txt
5. Performing full refresh from network_list.txt
6. Generating a report of changes

Usage:
    python maintain_networks.py [options]

Options:
    --check-only    Only check status without updating the file
    --add-new       Search for new live streams from channels in network_list.txt
    --refresh       Perform full refresh from network_list.txt (rebuilds Networks.txt)
    --verbose       Enable verbose output
    --help          Show this help message

Requirements:
    pip install requests beautifulsoup4 lxml
    
Files:
    network_list.txt - Tab-delimited list of network names and YouTube channel URLs
    Networks.txt     - Tab-delimited list of live streams (auto-generated)
"""

import argparse
import csv
import re
import requests
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse, parse_qs

# Configuration
NETWORKS_FILE = "Networks.txt"
NETWORK_LIST_FILE = "network_list.txt"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REQUEST_DELAY = 2  # seconds between requests to avoid rate limiting

class NetworkMaintainer:
    def __init__(self, verbose: bool = False, test_mode: bool = False):
        self.verbose = verbose
        self.test_mode = test_mode  # Limit URLs when testing code changes
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
    def log(self, message: str, force: bool = False):
        """Log message if verbose mode is enabled or force is True"""
        if self.verbose or force:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
    
    def load_network_list(self) -> List[Tuple[str, str]]:
        """Load network list from network_list.txt file"""
        networks = []
        try:
            with open(NETWORK_LIST_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                for row in reader:
                    network_name = row.get('Network', '').strip()
                    channel_url = row.get('YouTube Channel URL', '').strip()
                    if network_name and channel_url:
                        # Extract channel handle from URL (e.g., @SkyNews from https://www.youtube.com/@SkyNews)
                        if '@' in channel_url:
                            channel_handle = '@' + channel_url.split('@')[-1].rstrip('/')
                        else:
                            channel_handle = channel_url
                        networks.append((network_name, channel_handle))
            self.log(f"Loaded {len(networks)} networks from {NETWORK_LIST_FILE}")
        except FileNotFoundError:
            self.log(f"Network list file {NETWORK_LIST_FILE} not found, using fallback list", force=True)
            # Fallback to a minimal list if file not found
            networks = [
                ("Sky News", "@SkyNews"),
                ("NBC News", "@NBCNews"),
                ("ABC News", "@ABCNews"),
                ("CNN", "@CNN"),
                ("Fox News", "@FoxNews"),
            ]
        except Exception as e:
            self.log(f"Error loading network list: {e}", force=True)
            networks = []
        
        return networks
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        if 'youtube.com/watch' in url:
            parsed = urlparse(url)
            return parse_qs(parsed.query).get('v', [None])[0]
        elif 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        return None
    
    def check_stream_status(self, url: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check if a YouTube stream is currently live
        Returns: (is_live, viewer_count, duration)
        """
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                return False, None, None
            
            # Request the YouTube page
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return False, None, None
            
            content = response.text
            
            # Check for live indicators
            live_indicators = [
                '"isLiveContent":true',
                '"isLive":true',
                'LIVE',
                'watching now',
                'viewers watching'
            ]
            
            is_live = any(indicator in content for indicator in live_indicators)
            
            # Extract viewer count and duration
            viewer_count = None
            duration = None
            
            if is_live:
                # Try to extract viewer count using various patterns
                viewer_patterns = [
                    r'(\d+(?:,\d+)*)\s+watching',
                    r'(\d+(?:\.\d+)?[KM]?)\s+watching',
                    r'"viewCount":"(\d+)"',
                    r'viewCount.*?(\d+(?:,\d+)*)',
                ]
                
                for pattern in viewer_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        viewer_count = match.group(1)
                        if viewer_count.isdigit():
                            # Format large numbers
                            count = int(viewer_count)
                            if count >= 1000000:
                                viewer_count = f"{count/1000000:.1f}M"
                            elif count >= 1000:
                                viewer_count = f"{count/1000:.1f}K"
                            else:
                                viewer_count = str(count)
                        viewer_count += " watching"
                        break
                
                # Extract live duration
                duration = self.extract_live_duration(content)
            
            return is_live, viewer_count, duration
            
        except Exception as e:
            self.log(f"Error checking {url}: {e}")
            return False, None, None
    
    def extract_live_duration(self, content: str) -> Optional[str]:
        """
        Extract live stream duration from YouTube page content
        Returns: Duration string (e.g., "2h 30m", "45m", "1d 5h") or None if can't determine
        """
        try:
            # Look for "Started streaming" text patterns - most reliable method
            streaming_patterns = [
                r'Started streaming (\d+) (minute|hour|day)s? ago',
                r'Live for (\d+) (minute|hour|day)s?',
                r'(\d+) (minute|hour|day)s? ago',
            ]
            
            for pattern in streaming_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if len(match) == 2:
                        try:
                            value = int(match[0])
                            unit = match[1].lower()
                            
                            if unit.startswith('minute'):
                                total_minutes = value
                            elif unit.startswith('hour'):
                                total_minutes = value * 60
                            elif unit.startswith('day'):
                                total_minutes = value * 60 * 24
                            else:
                                continue
                            
                            # Only return duration if it seems reasonable (under 30 days)
                            if total_minutes <= 43200:  # 30 days max
                                return self.format_duration(total_minutes)
                        except:
                            continue
            
            # If we can't find reliable duration info, return "Unknown"
            # This is better than showing incorrect durations
            return "Unknown"
            
        except Exception as e:
            self.log(f"Error extracting duration: {e}")
            return "Unknown"
    
    def format_duration(self, total_minutes: int) -> str:
        """
        Format duration in minutes to human-readable string
        Returns: Formatted duration (e.g., "2h 30m", "45m", "1d 5h")
        """
        if total_minutes < 60:
            return f"{total_minutes}m"
        elif total_minutes < 1440:  # Less than 24 hours
            hours = total_minutes // 60
            minutes = total_minutes % 60
            if minutes > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{hours}h"
        else:  # 24 hours or more
            days = total_minutes // 1440
            remaining_minutes = total_minutes % 1440
            hours = remaining_minutes // 60
            if hours > 0:
                return f"{days}d {hours}h"
            else:
                return f"{days}d"
    
    def is_duration_over_24_hours(self, duration_str: Optional[str]) -> bool:
        """
        Check if duration string represents more than 24 hours
        Returns: True if duration is over 24 hours, False otherwise
        """
        if not duration_str or duration_str == "Unknown":
            # If we can't determine duration, assume it's a long-running stream
            # and include it (many news streams don't show duration info)
            return True
        
        try:
            total_minutes = 0
            
            # Parse duration string (e.g., "2d 5h", "25h", "1500m")
            if 'd' in duration_str:
                days_match = re.search(r'(\d+)d', duration_str)
                if days_match:
                    total_minutes += int(days_match.group(1)) * 1440
            
            if 'h' in duration_str:
                hours_match = re.search(r'(\d+)h', duration_str)
                if hours_match:
                    total_minutes += int(hours_match.group(1)) * 60
            
            if 'm' in duration_str and 'h' not in duration_str.split(duration_str.split('m')[0])[-1]:
                # Only count minutes if they're not part of "Xh Ym" format
                minutes_match = re.search(r'(\d+)m', duration_str)
                if minutes_match and 'h' not in duration_str:
                    total_minutes += int(minutes_match.group(1))
            
            # 24 hours = 1440 minutes
            return total_minutes >= 1440
            
        except Exception as e:
            self.log(f"Error parsing duration '{duration_str}': {e}")
            # If we can't parse it, assume it's valid (many news streams are long-running)
            return True
    
    def load_networks(self) -> List[Dict[str, str]]:
        """Load networks from the Networks.txt file"""
        networks = []
        try:
            with open(NETWORKS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                for row in reader:
                    networks.append(dict(row))
        except FileNotFoundError:
            self.log(f"Networks file {NETWORKS_FILE} not found", force=True)
        except Exception as e:
            self.log(f"Error loading networks: {e}", force=True)
        
        return networks
    
    def save_networks(self, networks: List[Dict[str, str]]):
        """Save networks to the Networks.txt file"""
        if not networks:
            self.log("No networks to save", force=True)
            return
        
        try:
            with open(NETWORKS_FILE, 'w', encoding='utf-8', newline='') as f:
                if networks:
                    fieldnames = networks[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
                    writer.writeheader()
                    writer.writerows(networks)
            self.log(f"Saved {len(networks)} networks to {NETWORKS_FILE}", force=True)
        except Exception as e:
            self.log(f"Error saving networks: {e}", force=True)
    
    def update_networks(self, check_only: bool = False) -> Dict[str, int]:
        """
        Update the networks list by checking live status
        Only includes streams that have been live for over 24 hours
        Returns: Statistics dictionary
        """
        networks = self.load_networks()
        if not networks:
            return {"error": 1}
        
        stats = {
            "total": len(networks),
            "checked": 0,
            "live": 0,
            "dead": 0,
            "updated": 0,
            "filtered_short": 0,
            "errors": 0
        }
        
        updated_networks = []
        
        for i, network in enumerate(networks):
            url = network.get('YouTube URL', '')
            network_name = network.get('Network', 'Unknown')
            
            self.log(f"Checking {network_name} ({i+1}/{len(networks)}): {url}")
            
            is_live, viewer_count, duration = self.check_stream_status(url)
            stats["checked"] += 1
            
            if is_live:
                stats["live"] += 1
                
                # Check if stream has been live for over 24 hours
                if not self.is_duration_over_24_hours(duration):
                    stats["filtered_short"] += 1
                    self.log(f"  ⏰ LIVE but under 24h ({duration or 'unknown duration'}) - Filtering out")
                    continue
                
                network['Status'] = 'LIVE'
                
                # Update viewer count if available
                old_viewers = network.get('Viewers', '')
                if viewer_count and viewer_count != old_viewers:
                    network['Viewers'] = viewer_count
                    stats["updated"] += 1
                
                # Update duration
                old_duration = network.get('Duration', '')
                if duration and duration != old_duration:
                    network['Duration'] = duration
                    if old_duration:
                        stats["updated"] += 1
                elif not network.get('Duration'):
                    network['Duration'] = duration or 'Unknown'
                
                self.log(f"  ✓ LIVE (24h+) - Duration: {duration or 'unknown'}, Viewers: {viewer_count or 'unknown'}")
                updated_networks.append(network)
            else:
                stats["dead"] += 1
                self.log(f"  ✗ NOT LIVE - Removing from list")
            
            # Rate limiting
            if i < len(networks) - 1:
                time.sleep(REQUEST_DELAY)
        
        if not check_only and updated_networks:
            self.save_networks(updated_networks)
        
        return stats
    
    def search_channel_for_live_streams(self, channel_name: str, channel_handle: str) -> List[Dict[str, str]]:
        """
        Search a YouTube channel for live streams that have been live for over 24 hours
        Limits testing to max 10 URLs only when in test_mode
        Returns: List of live stream dictionaries
        """
        try:
            live_streams = []
            found_urls = set()  # Track URLs to avoid duplicates
            
            # Set URL limit based on mode
            max_urls = 10 if self.test_mode else 50  # Limit only during testing
            
            # Method 1: Check channel page directly for live streams
            if channel_handle.startswith('@'):
                channel_url = f"https://www.youtube.com/{channel_handle}/streams"
            else:
                channel_url = channel_handle + "/streams"
            
            self.log(f"  Checking channel streams page: {channel_url}")
            response = self.session.get(channel_url, timeout=15)
            
            if response.status_code == 200:
                content = response.text
                
                # Look for live stream indicators and video IDs
                video_patterns = [
                    r'"videoId":"([a-zA-Z0-9_-]{11})"',
                    r'/watch\?v=([a-zA-Z0-9_-]{11})',
                    r'videoId\\u003d([a-zA-Z0-9_-]{11})'
                ]
                
                found_video_ids = set()
                for pattern in video_patterns:
                    matches = re.findall(pattern, content)
                    found_video_ids.update(matches)
                
                self.log(f"  Found {len(found_video_ids)} potential video IDs")
                
                # Test URLs up to the limit
                test_count = 0
                for video_id in found_video_ids:
                    if test_count >= max_urls:
                        if self.test_mode:
                            self.log(f"  Reached test limit of {max_urls} URLs")
                        break
                        
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    # Skip if we've already checked this URL
                    if url in found_urls:
                        continue
                    found_urls.add(url)
                    
                    is_live, viewer_count, duration = self.check_stream_status(url)
                    test_count += 1
                    
                    if is_live:
                        # Check if stream has been live for over 24 hours
                        if self.is_duration_over_24_hours(duration):
                            live_streams.append({
                                'Network': channel_name,
                                'Channel': channel_name,
                                'YouTube URL': url,
                                'Status': 'LIVE',
                                'Viewers': viewer_count or 'Unknown',
                                'Duration': duration or 'Unknown'
                            })
                            self.log(f"  ✓ Found live stream (24h+): {url} - Duration: {duration}")
                        else:
                            self.log(f"  ⏰ Found live stream but under 24h ({duration}) - Skipping: {url}")
                    
                    time.sleep(REQUEST_DELAY)
            
            # Method 2: Search approach as fallback (only if we found < 3 streams and under URL limit)
            if len(live_streams) < 3 and test_count < max_urls:
                self.log(f"  Trying search approach for {channel_name}")
                search_url = f"https://www.youtube.com/results?search_query={channel_handle.replace('@', '')}+live&sp=EgJAAQ%253D%253D"
                
                response = self.session.get(search_url, timeout=10)
                if response.status_code == 200:
                    content = response.text
                    
                    # Extract video IDs from search results
                    video_pattern = r'"videoId":"([a-zA-Z0-9_-]{11})"'
                    matches = re.findall(video_pattern, content)
                    
                    for video_id in matches:
                        if test_count >= max_urls:
                            if self.test_mode:
                                self.log(f"  Reached test limit of {max_urls} URLs")
                            break
                            
                        url = f"https://www.youtube.com/watch?v={video_id}"
                        
                        # Skip if we've already checked this URL
                        if url in found_urls:
                            continue
                        found_urls.add(url)
                        
                        is_live, viewer_count, duration = self.check_stream_status(url)
                        test_count += 1
                        
                        if is_live:
                            if self.is_duration_over_24_hours(duration):
                                live_streams.append({
                                    'Network': channel_name,
                                    'Channel': channel_name,
                                    'YouTube URL': url,
                                    'Status': 'LIVE',
                                    'Viewers': viewer_count or 'Unknown',
                                    'Duration': duration or 'Unknown'
                                })
                                self.log(f"  ✓ Found live stream via search (24h+): {url} - Duration: {duration}")
                            else:
                                self.log(f"  ⏰ Found live stream via search but under 24h ({duration}) - Skipping: {url}")
                        
                        time.sleep(REQUEST_DELAY)
            
            mode_info = f" (test mode: {max_urls} URL limit)" if self.test_mode else ""
            self.log(f"  Tested {test_count} URLs, found {len(live_streams)} valid streams{mode_info}")
            return live_streams
            
        except Exception as e:
            self.log(f"Error searching {channel_name}: {e}")
            return []
    
    def add_new_streams(self) -> int:
        """
        Search for new live streams from known channels
        Returns: Number of new streams added
        """
        existing_networks = self.load_networks()
        existing_urls = {network.get('YouTube URL', '') for network in existing_networks}
        
        new_streams = []
        known_channels = self.load_network_list()
        
        for channel_name, channel_handle in known_channels:
            self.log(f"Searching for live streams from {channel_name}...")
            
            channel_streams = self.search_channel_for_live_streams(channel_name, channel_handle)
            
            for stream in channel_streams:
                if stream['YouTube URL'] not in existing_urls:
                    new_streams.append(stream)
                    existing_urls.add(stream['YouTube URL'])
            
            time.sleep(REQUEST_DELAY)
        
        if new_streams:
            all_networks = existing_networks + new_streams
            self.save_networks(all_networks)
            self.log(f"Added {len(new_streams)} new live streams", force=True)
        else:
            self.log("No new live streams found", force=True)
        
        return len(new_streams)
    
    def generate_report(self, stats: Dict[str, int]):
        """Generate a status report"""
        print("\n" + "="*50)
        print("NETWORKS MAINTENANCE REPORT")
        print("="*50)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total networks checked: {stats.get('total', 0)}")
        print(f"Currently live: {stats.get('live', 0)}")
        print(f"Live 24+ hours (kept): {stats.get('live', 0) - stats.get('filtered_short', 0)}")
        print(f"Live under 24h (filtered): {stats.get('filtered_short', 0)}")
        print(f"No longer live (removed): {stats.get('dead', 0)}")
        print(f"Data updates made: {stats.get('updated', 0)}")
        
        if stats.get('errors', 0) > 0:
            print(f"Errors encountered: {stats.get('errors', 0)}")
        
        print("="*50)
    
    def full_refresh_from_network_list(self) -> Dict[str, int]:
        """
        Perform a full refresh of Networks.txt based on network_list.txt
        This will search all channels and rebuild the networks file with current live streams
        Removes duplicate URLs and ensures only 24h+ streams are included
        Returns: Statistics dictionary
        """
        self.log("Starting full refresh from network list...", force=True)
        
        known_channels = self.load_network_list()
        if not known_channels:
            return {"error": 1}
        
        stats = {
            "channels_checked": len(known_channels),
            "live_streams_found": 0,
            "duplicates_removed": 0,
            "errors": 0
        }
        
        all_live_streams = []
        seen_urls = set()  # Track URLs to avoid duplicates
        
        for channel_name, channel_handle in known_channels:
            try:
                self.log(f"Searching {channel_name} for live streams...")
                
                channel_streams = self.search_channel_for_live_streams(channel_name, channel_handle)
                
                if channel_streams:
                    # Add only unique URLs
                    unique_streams = []
                    for stream in channel_streams:
                        url = stream.get('YouTube URL', '')
                        if url and url not in seen_urls:
                            seen_urls.add(url)
                            unique_streams.append(stream)
                        else:
                            stats["duplicates_removed"] += 1
                    
                    all_live_streams.extend(unique_streams)
                    stats["live_streams_found"] += len(unique_streams)
                    self.log(f"  Found {len(unique_streams)} unique live stream(s)")
                    if len(channel_streams) > len(unique_streams):
                        self.log(f"  Removed {len(channel_streams) - len(unique_streams)} duplicate(s)")
                else:
                    self.log(f"  No live streams found")
                
                time.sleep(REQUEST_DELAY)
                
            except Exception as e:
                self.log(f"Error processing {channel_name}: {e}")
                stats["errors"] += 1
        
        if all_live_streams:
            self.save_networks(all_live_streams)
            self.log(f"Full refresh complete: {len(all_live_streams)} unique live streams saved", force=True)
            if stats["duplicates_removed"] > 0:
                self.log(f"Removed {stats['duplicates_removed']} duplicate URLs", force=True)
        else:
            self.log("No live streams found during full refresh", force=True)
        
        return stats


def main():
    parser = argparse.ArgumentParser(
        description="Maintain the Networks.txt file with live YouTube streams"
    )
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Only check status without updating the file'
    )
    parser.add_argument(
        '--add-new',
        action='store_true',
        help='Search for new live streams from known channels'
    )
    parser.add_argument(
        '--refresh',
        action='store_true',
        help='Perform full refresh from network_list.txt (rebuilds Networks.txt)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Enable test mode (limits to 10 URLs per channel for testing code changes)'
    )
    
    args = parser.parse_args()
    
    maintainer = NetworkMaintainer(verbose=args.verbose, test_mode=args.test_mode)
    
    try:
        if args.refresh:
            maintainer.log("Performing full refresh from network list...", force=True)
            stats = maintainer.full_refresh_from_network_list()
            if 'error' not in stats:
                print(f"\nFull refresh completed:")
                print(f"Channels checked: {stats.get('channels_checked', 0)}")
                print(f"Live streams found: {stats.get('live_streams_found', 0)}")
                if stats.get('duplicates_removed', 0) > 0:
                    print(f"Duplicates removed: {stats.get('duplicates_removed', 0)}")
                if stats.get('errors', 0) > 0:
                    print(f"Errors: {stats.get('errors', 0)}")
            else:
                print("Error: Could not load network list file")
                sys.exit(1)
        elif args.add_new:
            maintainer.log("Searching for new live streams...", force=True)
            new_count = maintainer.add_new_streams()
            print(f"Added {new_count} new streams")
        
        if not args.refresh:  # Don't run regular update if we did a full refresh
            maintainer.log("Checking existing networks...", force=True)
            stats = maintainer.update_networks(check_only=args.check_only)
            
            if 'error' not in stats:
                maintainer.generate_report(stats)
            else:
                print("Error: Could not load networks file")
                sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
