#!/usr/bin/env python3
"""
Networks.txt Maintenance Script
===============================

This script maintains the Networks.txt file by:
1. Checking if YouTube streams are currently live
2. Updating viewer counts
3. Removing dead streams
4. Adding new live streams from predefined channels
5. Generating a report of changes

Usage:
    python maintain_networks.py [options]

Options:
    --check-only    Only check status without updating the file
    --add-new       Search for new live streams from known channels
    --verbose       Enable verbose output
    --help          Show this help message

Requirements:
    pip install requests beautifulsoup4 lxml
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
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REQUEST_DELAY = 2  # seconds between requests to avoid rate limiting

# Known news channels to search for live streams
KNOWN_CHANNELS = [
    ("Sky News", "@SkyNews"),
    ("BBC News", "@BBCNews"),
    ("CNN", "@CNN"),
    ("Fox News", "@FoxNews"),
    ("NBC News", "@NBCNews"),
    ("ABC News", "@ABCNews"),
    ("CBS News", "@CBSNews"),
    ("Reuters", "@Reuters"),
    ("AP News", "@AssociatedPress"),
    ("NPR", "@NPR"),
    ("PBS NewsHour", "@PBSNewsHour"),
    ("C-SPAN", "@cspan"),
    ("France 24", "@France24_en"),
    ("DW News", "@dwnews"),
    ("Al Jazeera English", "@aljazeeraenglish"),
    ("Euronews", "@euronews"),
    ("RT", "@RT"),
    ("TRT World", "@trtworld"),
    ("WION", "@WION"),
    ("Bloomberg", "@markets"),
    ("CNBC", "@CNBC"),
    ("Fox Business", "@FoxBusiness"),
]

class NetworkMaintainer:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
    def log(self, message: str, force: bool = False):
        """Log message if verbose mode is enabled or force is True"""
        if self.verbose or force:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        if 'youtube.com/watch' in url:
            parsed = urlparse(url)
            return parse_qs(parsed.query).get('v', [None])[0]
        elif 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        return None
    
    def check_stream_status(self, url: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a YouTube stream is currently live
        Returns: (is_live, viewer_count)
        """
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                return False, None
            
            # Request the YouTube page
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return False, None
            
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
            
            # Extract viewer count
            viewer_count = None
            if is_live:
                # Try to extract viewer count using various patterns
                patterns = [
                    r'(\d+(?:,\d+)*)\s+watching',
                    r'(\d+(?:\.\d+)?[KM]?)\s+watching',
                    r'"viewCount":"(\d+)"',
                    r'viewCount.*?(\d+(?:,\d+)*)',
                ]
                
                for pattern in patterns:
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
            
            return is_live, viewer_count
            
        except Exception as e:
            self.log(f"Error checking {url}: {e}")
            return False, None
    
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
            "errors": 0
        }
        
        updated_networks = []
        
        for i, network in enumerate(networks):
            url = network.get('YouTube URL', '')
            network_name = network.get('Network', 'Unknown')
            
            self.log(f"Checking {network_name} ({i+1}/{len(networks)}): {url}")
            
            is_live, viewer_count = self.check_stream_status(url)
            stats["checked"] += 1
            
            if is_live:
                stats["live"] += 1
                network['Status'] = 'LIVE'
                
                # Update viewer count if available
                old_viewers = network.get('Viewers', '')
                if viewer_count and viewer_count != old_viewers:
                    network['Viewers'] = viewer_count
                    stats["updated"] += 1
                    self.log(f"  ✓ LIVE - Updated viewers: {old_viewers} → {viewer_count}")
                else:
                    self.log(f"  ✓ LIVE - {viewer_count or 'viewer count unavailable'}")
                
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
        Search a YouTube channel for live streams
        Returns: List of live stream dictionaries
        """
        try:
            # Search for live streams from this channel
            search_url = f"https://www.youtube.com/results?search_query={channel_handle}+live&sp=EgJAAQ%253D%253D"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return []
            
            content = response.text
            
            # Extract video URLs and titles from search results
            # This is a simplified extraction - in practice, you might want to use the YouTube Data API
            video_pattern = r'{"videoId":"([^"]+)".*?"title":{"runs":\[{"text":"([^"]+)"}'
            matches = re.findall(video_pattern, content)
            
            live_streams = []
            for video_id, title in matches[:3]:  # Check first 3 results
                url = f"https://www.youtube.com/watch?v={video_id}"
                is_live, viewer_count = self.check_stream_status(url)
                
                if is_live:
                    live_streams.append({
                        'Network': channel_name,
                        'Channel': channel_name,
                        'YouTube URL': url,
                        'Status': 'LIVE',
                        'Viewers': viewer_count or 'Unknown'
                    })
                    self.log(f"  Found live stream: {title}")
                
                time.sleep(REQUEST_DELAY)
            
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
        
        for channel_name, channel_handle in KNOWN_CHANNELS:
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
        print(f"No longer live (removed): {stats.get('dead', 0)}")
        print(f"Viewer counts updated: {stats.get('updated', 0)}")
        
        if stats.get('errors', 0) > 0:
            print(f"Errors encountered: {stats.get('errors', 0)}")
        
        print("="*50)


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
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    maintainer = NetworkMaintainer(verbose=args.verbose)
    
    try:
        if args.add_new:
            maintainer.log("Searching for new live streams...", force=True)
            new_count = maintainer.add_new_streams()
            print(f"Added {new_count} new streams")
        
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
