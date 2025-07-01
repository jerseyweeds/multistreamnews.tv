#!/usr/bin/env python3
"""
Alternative YouTube Live Stream Scanner
Checks main channel pages and videos for live content with manual verification
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
from urllib.parse import urljoin

class ManualYouTubeLiveStreamScanner:
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
        self.results = []
        
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
    
    def check_channel_for_live_content(self, network_name, channel_url):
        """Check multiple endpoints for live content"""
        print(f"\n🔍 Checking {network_name}")
        print(f"   Channel: {channel_url}")
        
        results = {
            'network': network_name,
            'channel_url': channel_url,
            'live_streams': [],
            'recent_videos': [],
            'status': 'checked',
            'timestamp': datetime.now().isoformat()
        }
        
        # Check multiple endpoints
        endpoints_to_check = [
            ('Main Page', channel_url),
            ('Videos Page', f"{channel_url.rstrip('/')}/videos"),
            ('Live Page', f"{channel_url.rstrip('/')}/streams"),
            ('Community Page', f"{channel_url.rstrip('/')}/community")
        ]
        
        for endpoint_name, url in endpoints_to_check:
            try:
                print(f"   📄 Checking {endpoint_name}...")
                response = self.session.get(url, timeout=12)
                
                if response.status_code == 200:
                    # Look for live content indicators
                    content = response.text.lower()
                    
                    # Count various live indicators
                    live_indicators = {
                        'live_now': content.count('live now'),
                        'watching_now': content.count('watching now'),
                        'viewers_watching': content.count('viewers watching'),
                        'streaming_live': content.count('streaming live'),
                        'live_badge': content.count('live'),
                        'concurrent_viewers': content.count('concurrent')
                    }
                    
                    total_indicators = sum(live_indicators.values())
                    
                    if total_indicators > 5:  # Threshold for likely live content
                        print(f"   ✅ {endpoint_name}: Found {total_indicators} live indicators")
                        
                        # Try to extract specific video URLs
                        video_urls = self.extract_video_urls_from_content(response.text)
                        
                        for video_url in video_urls[:5]:  # Check top 5 videos
                            live_info = self.check_specific_video_for_live(video_url)
                            if live_info and live_info.get('is_live'):
                                results['live_streams'].append(live_info)
                                print(f"   🔴 Found live stream: {live_info.get('title', 'Unknown')} ({live_info.get('viewers', 0)} viewers)")
                    else:
                        print(f"   ⚪ {endpoint_name}: {total_indicators} live indicators (below threshold)")
                        
                        # Still check recent videos
                        video_urls = self.extract_video_urls_from_content(response.text)
                        for video_url in video_urls[:3]:
                            video_info = self.get_basic_video_info(video_url)
                            if video_info:
                                results['recent_videos'].append(video_info)
                
                else:
                    print(f"   ❌ {endpoint_name}: HTTP {response.status_code}")
                
                time.sleep(1)  # Be respectful
                
            except Exception as e:
                print(f"   ⚠️  {endpoint_name}: Error - {e}")
        
        self.results.append(results)
        return results
    
    def extract_video_urls_from_content(self, content):
        """Extract video URLs from page content"""
        video_urls = []
        
        # Look for video URLs in various formats
        patterns = [
            r'"/watch\?v=([a-zA-Z0-9_-]{11})"',
            r'"videoId":"([a-zA-Z0-9_-]{11})"',
            r'/watch\?v=([a-zA-Z0-9_-]{11})',
        ]
        
        video_ids = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            video_ids.update(matches)
        
        for video_id in list(video_ids)[:10]:  # Limit to 10 videos
            video_urls.append(f"https://www.youtube.com/watch?v={video_id}")
        
        return video_urls
    
    def check_specific_video_for_live(self, video_url):
        """Check if a specific video is currently live"""
        try:
            print(f"     🎥 Checking video: {video_url}")
            response = self.session.get(video_url, timeout=10)
            
            if response.status_code != 200:
                return None
            
            content = response.text
            
            # Look for live indicators
            is_live = False
            viewer_count = 0
            title = "Unknown"
            
            # Extract title
            title_match = re.search(r'"title":"([^"]+)"', content)
            if title_match:
                title = title_match.group(1)
            
            # Check for live status
            live_patterns = [
                r'"isLiveContent":true',
                r'"isLive":true',
                r'isLivePlayback.*?true',
                r'"liveBroadcastDetails"'
            ]
            
            for pattern in live_patterns:
                if re.search(pattern, content):
                    is_live = True
                    break
            
            # Extract viewer count if live
            if is_live:
                viewer_patterns = [
                    r'"viewCount":"(\d+)"',
                    r'(\d+(?:,\d+)*)\s+watching now',
                    r'(\d+(?:,\d+)*)\s+viewers'
                ]
                
                for pattern in viewer_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        viewer_count = int(match.group(1).replace(',', ''))
                        break
            
            if is_live:
                return {
                    'url': video_url,
                    'title': title,
                    'is_live': True,
                    'viewers': viewer_count,
                    'checked_at': datetime.now().isoformat()
                }
        
        except Exception as e:
            print(f"     ⚠️  Error checking video: {e}")
        
        return None
    
    def get_basic_video_info(self, video_url):
        """Get basic info about a video"""
        try:
            response = self.session.get(video_url, timeout=8)
            if response.status_code == 200:
                content = response.text
                
                title_match = re.search(r'"title":"([^"]+)"', content)
                title = title_match.group(1) if title_match else "Unknown"
                
                view_match = re.search(r'"viewCount":"(\d+)"', content)
                views = int(view_match.group(1)) if view_match else 0
                
                return {
                    'url': video_url,
                    'title': title,
                    'views': views,
                    'checked_at': datetime.now().isoformat()
                }
        except:
            pass
        
        return None
    
    def scan_all_channels(self, network_list_file):
        """Scan all channels"""
        networks = self.parse_network_list(network_list_file)
        
        print("🎯 Manual YouTube Live Stream Scanner")
        print("=" * 60)
        print(f"Scanning {len(networks)} news networks for live streams...")
        
        live_streams_found = []
        
        for i, (network_name, channel_url) in enumerate(networks):
            print(f"\n[{i+1}/{len(networks)}]")
            
            try:
                result = self.check_channel_for_live_content(network_name, channel_url)
                
                if result['live_streams']:
                    live_streams_found.extend([
                        {**stream, 'network': network_name} 
                        for stream in result['live_streams']
                    ])
                
                time.sleep(2)  # Be respectful to servers
                
            except Exception as e:
                print(f"   ❌ Failed to scan {network_name}: {e}")
        
        return live_streams_found
    
    def print_summary(self, live_streams):
        """Print scan summary"""
        print("\n" + "=" * 60)
        print("📊 SCAN RESULTS SUMMARY")
        print("=" * 60)
        
        if not live_streams:
            print("❌ No live streams found")
            print("\n🤔 Possible reasons:")
            print("   • No channels currently live")
            print("   • YouTube's anti-scraping measures")
            print("   • Channels may be geo-blocked")
            print("   • Rate limiting in effect")
        else:
            print(f"✅ Found {len(live_streams)} live streams!")
            
            # Sort by viewer count
            sorted_streams = sorted(live_streams, key=lambda x: x.get('viewers', 0), reverse=True)
            
            for i, stream in enumerate(sorted_streams, 1):
                print(f"\n{i}. 🔴 {stream['network']}")
                print(f"   📺 {stream['title']}")
                print(f"   👥 {stream.get('viewers', 0):,} viewers")
                print(f"   🔗 {stream['url']}")
            
            total_viewers = sum(s.get('viewers', 0) for s in live_streams)
            print(f"\n📈 Total viewers across all streams: {total_viewers:,}")
        
        # Channel summary
        print(f"\n📋 Channel Summary:")
        networks_with_content = len([r for r in self.results if r['live_streams'] or r['recent_videos']])
        print(f"   • Networks scanned: {len(self.results)}")
        print(f"   • Networks with content: {networks_with_content}")
        print(f"   • Networks with live streams: {len(set(s['network'] for s in live_streams))}")
    
    def save_detailed_results(self, filename='detailed_scan_results.json'):
        """Save detailed results"""
        output = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'total_networks': len(self.results),
                'total_live_streams': sum(len(r['live_streams']) for r in self.results)
            },
            'results_by_network': self.results,
            'summary': {
                'live_streams': [
                    {**stream, 'network': result['network']}
                    for result in self.results
                    for stream in result['live_streams']
                ]
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: {filename}")

def main():
    scanner = ManualYouTubeLiveStreamScanner()
    
    print("🚀 Starting comprehensive YouTube live stream scan...")
    live_streams = scanner.scan_all_channels('network_list.txt')
    
    scanner.print_summary(live_streams)
    scanner.save_detailed_results()
    
    print(f"\n✅ Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
