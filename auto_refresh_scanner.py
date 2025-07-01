#!/usr/bin/env python3
"""
Automated Live Stream Refresh System
Provides multiple ways to refresh and monitor live streams continuously
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import schedule
import threading
from datetime import datetime, timedelta
import argparse
import os

class AutoRefreshLiveStreamScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self.latest_results = []
        self.scan_count = 0
        self.start_time = datetime.now()
        
    def parse_network_list(self, filename):
        """Parse the network list file to extract channel URLs"""
        networks = []
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            line = line.strip()
            # Skip first line (header) and any empty lines
            if i == 0 or not line:
                continue
            # Process lines with tab-separated values
            if '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    network_name = parts[0].strip()
                    url = parts[1].strip()
                    if url.startswith('https://www.youtube.com/'):
                        networks.append((network_name, url))
        
        return networks
    
    def quick_scan_network(self, network_name, channel_url, max_videos=5):
        """Quick scan of a network (fewer videos for faster refresh)"""
        try:
            response = self.session.get(channel_url, timeout=15)
            response.raise_for_status()
            
            content = response.text
            video_ids = self._extract_video_ids(content)
            
            live_streams = []
            videos_to_check = min(max_videos, len(video_ids))
            
            for video_id in video_ids[:videos_to_check]:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                live_info = self._check_video_live_status(video_url)
                
                if live_info['is_live']:
                    live_streams.append({
                        'video_id': video_id,
                        'url': video_url,
                        'title': live_info['title'],
                        'viewers': live_info['viewers'],
                        'network': network_name,
                        'detected_at': datetime.now().isoformat()
                    })
                
                time.sleep(0.3)  # Faster between videos for refresh
            
            return live_streams
            
        except Exception as e:
            print(f"   ⚠️ Error scanning {network_name}: {e}")
            return []
    
    def _extract_video_ids(self, content):
        """Extract video IDs from channel content"""
        video_ids = []
        
        # Multiple extraction methods
        patterns = [
            r'/watch\?v=([a-zA-Z0-9_-]{11})',
            r'"videoId"\s*:\s*"([a-zA-Z0-9_-]{11})"',
            r'[?&]v=([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            video_ids.extend(matches)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_ids = []
        for vid_id in video_ids:
            if vid_id not in seen:
                seen.add(vid_id)
                unique_ids.append(vid_id)
        
        return unique_ids
    
    def _check_video_live_status(self, video_url):
        """Check if a video is live"""
        try:
            response = self.session.get(video_url, timeout=8)
            
            if response.status_code != 200:
                return {'is_live': False, 'title': 'Unavailable', 'viewers': 0}
            
            content = response.text
            
            # Extract title
            title_match = re.search(r'"title":"([^"]+)"', content)
            title = title_match.group(1) if title_match else "Unknown Title"
            title = title.replace('\\u0026', '&').replace('\\"', '"')
            
            # Check for live indicators
            is_live = False
            viewers = 0
            
            live_patterns = [
                r'"isLiveContent"\s*:\s*true',
                r'"liveBroadcastDetails"\s*:',
                r'"isLive"\s*:\s*true'
            ]
            
            for pattern in live_patterns:
                if re.search(pattern, content):
                    is_live = True
                    break
            
            # Extract viewer count
            if is_live:
                viewer_patterns = [
                    r'"concurrentViewers"\s*:\s*"(\d+)"',
                    r'(\d+(?:,\d+)*)\s+watching now'
                ]
                
                for pattern in viewer_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        viewers = int(match.group(1).replace(',', ''))
                        break
            
            return {
                'is_live': is_live,
                'title': title[:150],  # Limit title length
                'viewers': viewers
            }
            
        except Exception:
            return {'is_live': False, 'title': 'Error', 'viewers': 0}
    
    def perform_refresh_scan(self, quick_mode=True):
        """Perform a refresh scan of all networks"""
        print(f"\n🔄 Refresh Scan #{self.scan_count + 1} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        networks = self.parse_network_list('network_list.txt')
        all_live_streams = []
        
        max_videos = 5 if quick_mode else 15
        
        for i, (network_name, channel_url) in enumerate(networks):
            print(f"[{i+1}/{len(networks)}] {network_name}...", end=" ")
            
            live_streams = self.quick_scan_network(network_name, channel_url, max_videos)
            
            if live_streams:
                print(f"✅ {len(live_streams)} live")
                all_live_streams.extend(live_streams)
            else:
                print("⚪ none")
            
            time.sleep(1)  # Brief delay between networks
        
        self.latest_results = all_live_streams
        self.scan_count += 1
        
        # Save results with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'live_streams_refresh_{timestamp}.json'
        
        results = {
            'scan_info': {
                'scan_number': self.scan_count,
                'timestamp': datetime.now().isoformat(),
                'scan_type': 'quick' if quick_mode else 'full',
                'total_live_streams': len(all_live_streams),
                'total_networks': len(networks)
            },
            'live_streams': all_live_streams
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Also save as latest.json for easy access
        with open('latest_live_streams.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self._print_refresh_summary(all_live_streams)
        
        return all_live_streams
    
    def _print_refresh_summary(self, live_streams):
        """Print a summary of the refresh results"""
        if not live_streams:
            print("\n❌ No live streams found in this refresh")
            return
        
        print(f"\n✅ Found {len(live_streams)} live streams")
        
        # Group by network
        by_network = {}
        for stream in live_streams:
            network = stream['network']
            if network not in by_network:
                by_network[network] = []
            by_network[network].append(stream)
        
        print(f"📊 Networks with live content: {len(by_network)}")
        for network, streams in by_network.items():
            total_viewers = sum(s['viewers'] for s in streams)
            print(f"   • {network}: {len(streams)} stream(s) ({total_viewers:,} viewers)")
        
        # Top streams
        sorted_streams = sorted(live_streams, key=lambda x: x['viewers'], reverse=True)
        print(f"\n🔴 Top 5 live streams:")
        for i, stream in enumerate(sorted_streams[:5], 1):
            print(f"   {i}. {stream['network']}: {stream['viewers']:,} viewers")
    
    def continuous_monitoring(self, interval_minutes=15):
        """Run continuous monitoring with specified interval"""
        print(f"🚀 Starting continuous monitoring (every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.perform_refresh_scan(quick_mode=True)
                
                print(f"\n⏰ Next scan in {interval_minutes} minutes...")
                print(f"📊 Total scans completed: {self.scan_count}")
                print(f"🕐 Running since: {self.start_time.strftime('%H:%M:%S')}")
                
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Monitoring stopped after {self.scan_count} scans")
            print(f"📊 Total runtime: {datetime.now() - self.start_time}")
    
    def scheduled_monitoring(self):
        """Set up scheduled monitoring at specific times"""
        print("📅 Setting up scheduled monitoring...")
        
        # Schedule scans every 15 minutes during peak hours
        schedule.every(15).minutes.do(lambda: self.perform_refresh_scan(quick_mode=True))
        
        # Schedule full scans every 2 hours
        schedule.every(2).hours.do(lambda: self.perform_refresh_scan(quick_mode=False))
        
        # Schedule daily summary at midnight
        schedule.every().day.at("00:00").do(self.daily_summary)
        
        print("📋 Schedule configured:")
        print("   • Quick scan: Every 15 minutes")
        print("   • Full scan: Every 2 hours") 
        print("   • Daily summary: Midnight")
        print("\nPress Ctrl+C to stop scheduled monitoring")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n🛑 Scheduled monitoring stopped")
    
    def daily_summary(self):
        """Generate a daily summary report"""
        print("\n📊 DAILY SUMMARY REPORT")
        print("=" * 40)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Total scans today: {self.scan_count}")
        
        if self.latest_results:
            total_viewers = sum(s['viewers'] for s in self.latest_results)
            print(f"Current live streams: {len(self.latest_results)}")
            print(f"Total viewers: {total_viewers:,}")
    
    def compare_with_previous(self, previous_file='latest_live_streams.json'):
        """Compare current results with previous scan"""
        if not os.path.exists(previous_file):
            print("No previous scan found for comparison")
            return
        
        try:
            with open(previous_file, 'r') as f:
                previous_data = json.load(f)
            
            previous_streams = previous_data.get('live_streams', [])
            current_streams = self.latest_results
            
            # Compare counts
            prev_count = len(previous_streams)
            curr_count = len(current_streams)
            
            print(f"\n📈 COMPARISON WITH PREVIOUS SCAN:")
            print(f"   Previous: {prev_count} live streams")
            print(f"   Current:  {curr_count} live streams")
            print(f"   Change:   {curr_count - prev_count:+d}")
            
            # Find new and ended streams
            prev_video_ids = set(s['video_id'] for s in previous_streams)
            curr_video_ids = set(s['video_id'] for s in current_streams)
            
            new_streams = curr_video_ids - prev_video_ids
            ended_streams = prev_video_ids - curr_video_ids
            
            if new_streams:
                print(f"\n🆕 New live streams: {len(new_streams)}")
            if ended_streams:
                print(f"🔚 Ended streams: {len(ended_streams)}")
            
        except Exception as e:
            print(f"Error comparing with previous scan: {e}")

def main():
    parser = argparse.ArgumentParser(description='Live Stream Refresh System')
    parser.add_argument('--mode', choices=['single', 'continuous', 'scheduled'], 
                       default='single', help='Refresh mode')
    parser.add_argument('--interval', type=int, default=15, 
                       help='Interval in minutes for continuous mode')
    parser.add_argument('--quick', action='store_true', 
                       help='Use quick scan (fewer videos per channel)')
    
    args = parser.parse_args()
    
    scanner = AutoRefreshLiveStreamScanner()
    
    if args.mode == 'single':
        print("🔄 Single Refresh Scan")
        scanner.perform_refresh_scan(quick_mode=args.quick)
        scanner.compare_with_previous()
        
    elif args.mode == 'continuous':
        scanner.continuous_monitoring(interval_minutes=args.interval)
        
    elif args.mode == 'scheduled':
        scanner.scheduled_monitoring()

if __name__ == "__main__":
    main()
