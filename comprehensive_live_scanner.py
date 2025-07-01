#!/usr/bin/env python3
"""
Final Comprehensive Live Stream Scanner
Uses proven video-by-video checking method that successfully detected live streams
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime

class ComprehensiveLiveStreamScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.all_live_streams = []
        
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
    
    def scan_channel_for_live_streams(self, network_name, channel_url, max_videos=15):
        """Scan a channel by checking individual videos for live status"""
        print(f"\n🔍 Scanning {network_name}")
        print(f"   URL: {channel_url}")
        
        try:
            # Get the channel page
            response = self.session.get(channel_url, timeout=20)
            response.raise_for_status()
            
            content = response.text
            print(f"   ✅ Page loaded ({len(content):,} characters)")
            
            # Extract video IDs from the page
            video_ids = self._extract_video_ids(content)
            print(f"   📹 Found {len(video_ids)} video IDs")
            
            if not video_ids:
                print(f"   ⚠️ No video IDs found - channel may be empty or use different structure")
                return []
            
            # Check videos for live status
            live_streams = []
            videos_to_check = min(max_videos, len(video_ids))
            
            print(f"   🎥 Checking first {videos_to_check} videos for live status...")
            
            for i, video_id in enumerate(video_ids[:videos_to_check]):
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                try:
                    live_info = self._check_video_live_status(video_url)
                    
                    if live_info['is_live']:
                        live_stream = {
                            'video_id': video_id,
                            'url': video_url,
                            'title': live_info['title'],
                            'viewers': live_info['viewers'],
                            'network': network_name,
                            'detected_at': datetime.now().isoformat()
                        }
                        live_streams.append(live_stream)
                        print(f"      🔴 LIVE [{i+1}/{videos_to_check}]: {live_info['title'][:60]}... ({live_info['viewers']} viewers)")
                    else:
                        # Only show first few non-live videos to avoid spam
                        if i < 3:
                            print(f"      ⚪ Not live [{i+1}/{videos_to_check}]: {live_info['title'][:50]}...")
                        elif i == 3:
                            print(f"      ⚪ (Checking remaining {videos_to_check-3} videos silently...)")
                    
                    # Small delay between video checks
                    time.sleep(0.5)
                    
                except Exception as e:
                    if i < 3:  # Only show errors for first few videos
                        print(f"      ❌ Error checking video {i+1}: {e}")
            
            if live_streams:
                print(f"   ✅ Found {len(live_streams)} live stream(s)")
                self.all_live_streams.extend(live_streams)
            else:
                print(f"   ⚪ No live streams found")
            
            return live_streams
            
        except Exception as e:
            print(f"   ❌ Error scanning channel: {e}")
            return []
    
    def _extract_video_ids(self, content):
        """Extract video IDs from channel content using multiple methods"""
        video_ids = []
        
        # Method 1: Direct regex for /watch?v= URLs
        matches = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', content)
        video_ids.extend(matches)
        
        # Method 2: JSON videoId fields
        matches = re.findall(r'"videoId"\s*:\s*"([a-zA-Z0-9_-]{11})"', content)
        video_ids.extend(matches)
        
        # Method 3: Various URL parameter patterns
        matches = re.findall(r'[?&]v=([a-zA-Z0-9_-]{11})', content)
        video_ids.extend(matches)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_video_ids = []
        for video_id in video_ids:
            if video_id not in seen:
                seen.add(video_id)
                unique_video_ids.append(video_id)
        
        return unique_video_ids
    
    def _check_video_live_status(self, video_url):
        """Check if a specific video is currently live"""
        try:
            response = self.session.get(video_url, timeout=12)
            
            if response.status_code != 200:
                return {'is_live': False, 'title': 'Unavailable', 'viewers': 0}
            
            content = response.text
            
            # Extract title
            title = self._extract_video_title(content)
            
            # Check for live indicators
            is_live = False
            viewers = 0
            
            # Primary live detection methods
            live_patterns = [
                r'"isLiveContent"\s*:\s*true',
                r'"liveBroadcastDetails"\s*:',
                r'"isLive"\s*:\s*true',
                r'isLivePlayback.*?true'
            ]
            
            for pattern in live_patterns:
                if re.search(pattern, content):
                    is_live = True
                    break
            
            # Extract viewer count if live
            if is_live:
                viewers = self._extract_viewer_count(content)
            
            # Secondary check: look for "watching now" which is a strong live indicator
            watching_match = re.search(r'(\d+(?:,\d+)*)\s+watching now', content, re.IGNORECASE)
            if watching_match:
                is_live = True
                viewers = max(viewers, int(watching_match.group(1).replace(',', '')))
            
            return {
                'is_live': is_live,
                'title': title,
                'viewers': viewers
            }
            
        except Exception as e:
            return {'is_live': False, 'title': 'Error', 'viewers': 0}
    
    def _extract_video_title(self, content):
        """Extract video title from page content"""
        # Method 1: JSON title field
        title_match = re.search(r'"title":"([^"]+)"', content)
        if title_match:
            title = title_match.group(1)
            # Decode common escape sequences
            title = title.replace('\\u0026', '&').replace('\\"', '"').replace('\\n', ' ')
            return title[:200]  # Limit length
        
        # Method 2: HTML title tag
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            return title_match.group(1)[:200]
        
        return "Unknown Title"
    
    def _extract_viewer_count(self, content):
        """Extract current viewer count from live stream"""
        viewer_patterns = [
            r'"concurrentViewers"\s*:\s*"(\d+)"',
            r'"viewCount"\s*:\s*"(\d+)"',
            r'(\d+(?:,\d+)*)\s+watching now',
            r'(\d+(?:,\d+)*)\s+viewers watching'
        ]
        
        for pattern in viewer_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                viewer_str = match.group(1).replace(',', '')
                try:
                    return int(viewer_str)
                except ValueError:
                    continue
        
        return 0
    
    def scan_all_networks(self, network_list_file):
        """Scan all networks for live streams"""
        networks = self.parse_network_list(network_list_file)
        
        print("🎯 Comprehensive Live Stream Scanner")
        print("=" * 60)
        print(f"Scanning {len(networks)} networks for live streams...")
        print("(Using proven video-by-video detection method)")
        
        failed_networks = []
        
        for i, (network_name, channel_url) in enumerate(networks):
            print(f"\n[{i+1}/{len(networks)}]")
            
            try:
                live_streams = self.scan_channel_for_live_streams(network_name, channel_url)
                
                # Delay between channels to be respectful
                if i < len(networks) - 1:  # Don't delay after the last one
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ❌ Failed to scan {network_name}: {e}")
                failed_networks.append((network_name, str(e)))
        
        # Print summary of failures
        if failed_networks:
            print(f"\n⚠️ Failed to scan {len(failed_networks)} networks:")
            for network, error in failed_networks:
                print(f"   • {network}: {error}")
        
        return self.all_live_streams
    
    def print_summary(self):
        """Print comprehensive summary of findings"""
        print("\n" + "=" * 60)
        print("🔴 COMPREHENSIVE LIVE STREAM RESULTS")
        print("=" * 60)
        
        if not self.all_live_streams:
            print("❌ No live streams detected")
            print("\nPossible reasons:")
            print("   • No channels currently live streaming")
            print("   • Channels not broadcasting at this time")
            print("   • Network-specific restrictions")
            return
        
        # Sort by viewer count
        sorted_streams = sorted(self.all_live_streams, key=lambda x: x['viewers'], reverse=True)
        
        print(f"✅ Found {len(self.all_live_streams)} live streams!")
        
        # Group by network
        by_network = {}
        for stream in self.all_live_streams:
            network = stream['network']
            if network not in by_network:
                by_network[network] = []
            by_network[network].append(stream)
        
        print(f"📊 Live streams by network:")
        for network, streams in by_network.items():
            print(f"   • {network}: {len(streams)} live stream(s)")
        
        print(f"\n🔴 Live streams (sorted by viewer count):")
        
        for i, stream in enumerate(sorted_streams, 1):
            print(f"\n{i}. 🔴 {stream['network']}")
            print(f"   📺 {stream['title']}")
            print(f"   👥 {stream['viewers']:,} viewers")
            print(f"   🔗 {stream['url']}")
        
        total_viewers = sum(s['viewers'] for s in self.all_live_streams)
        print(f"\n📈 Total viewers across all live streams: {total_viewers:,}")
        
        if total_viewers > 0:
            avg_viewers = total_viewers / len(self.all_live_streams)
            print(f"📊 Average viewers per stream: {avg_viewers:.0f}")
    
    def save_results(self, filename='comprehensive_live_streams.json'):
        """Save comprehensive results"""
        results = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'scanner_type': 'comprehensive_video_checking',
                'total_networks_scanned': len(set(s['network'] for s in self.all_live_streams)),
                'total_live_streams': len(self.all_live_streams)
            },
            'live_streams': self.all_live_streams,
            'summary': {
                'networks_with_live_content': list(set(s['network'] for s in self.all_live_streams)),
                'total_viewers': sum(s['viewers'] for s in self.all_live_streams)
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Comprehensive results saved to: {filename}")

def main():
    print("🚀 Starting Comprehensive Live Stream Detection")
    print("=" * 60)
    
    scanner = ComprehensiveLiveStreamScanner()
    
    # Scan all networks
    live_streams = scanner.scan_all_networks('network_list.txt')
    
    # Print comprehensive summary
    scanner.print_summary()
    
    # Save results
    scanner.save_results()
    
    print(f"\n✅ Comprehensive scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
