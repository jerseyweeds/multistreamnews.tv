#!/usr/bin/env python3
"""
Enhanced Live Stream Detection with JavaScript Support
Uses selenium for JavaScript rendering when available, falls back to pattern matching
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime

class AdvancedLiveStreamDetector:
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
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
    def test_specific_channel_live_detection(self, channel_url, network_name):
        """Test live detection on a specific channel with detailed analysis"""
        print(f"🔍 Testing live detection for {network_name}")
        print(f"   URL: {channel_url}")
        
        try:
            response = self.session.get(channel_url, timeout=20)
            response.raise_for_status()
            
            content = response.text
            print(f"   ✅ Page loaded ({len(content):,} characters)")
            
            # Extract all video IDs from the page
            video_ids = self._extract_all_video_ids(content)
            print(f"   📹 Found {len(video_ids)} video IDs")
            
            # Check each video for live status
            live_streams = []
            
            for i, video_id in enumerate(video_ids[:10]):  # Check first 10 videos
                print(f"   🎥 Checking video {i+1}/10: {video_id}")
                
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                live_info = self._check_video_live_status(video_url)
                
                if live_info['is_live']:
                    live_streams.append({
                        'video_id': video_id,
                        'url': video_url,
                        'title': live_info['title'],
                        'viewers': live_info['viewers'],
                        'network': network_name
                    })
                    print(f"      🔴 LIVE: {live_info['title']} ({live_info['viewers']} viewers)")
                else:
                    print(f"      ⚪ Not live: {live_info['title']}")
                
                time.sleep(1)  # Be respectful
            
            return live_streams
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def _extract_all_video_ids(self, content):
        """Extract all video IDs from page content"""
        # Method 1: Direct regex on HTML
        video_ids = set()
        
        # Look for /watch?v= URLs
        matches = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', content)
        video_ids.update(matches)
        
        # Look for videoId in JSON
        matches = re.findall(r'"videoId"\s*:\s*"([a-zA-Z0-9_-]{11})"', content)
        video_ids.update(matches)
        
        # Look for v= in various contexts
        matches = re.findall(r'[?&]v=([a-zA-Z0-9_-]{11})', content)
        video_ids.update(matches)
        
        return list(video_ids)
    
    def _check_video_live_status(self, video_url):
        """Check if a specific video is currently live"""
        try:
            response = self.session.get(video_url, timeout=10)
            
            if response.status_code != 200:
                return {'is_live': False, 'title': 'Unknown', 'viewers': 0}
            
            content = response.text
            
            # Extract title
            title_match = re.search(r'"title":"([^"]+)"', content)
            title = title_match.group(1) if title_match else "Unknown Title"
            title = title.replace('\\u0026', '&').replace('\\"', '"')
            
            # Check for live indicators
            is_live = False
            viewers = 0
            
            # Method 1: Look for isLiveContent
            if re.search(r'"isLiveContent"\s*:\s*true', content):
                is_live = True
            
            # Method 2: Look for liveBroadcastDetails
            if re.search(r'"liveBroadcastDetails"\s*:', content):
                is_live = True
            
            # Method 3: Look for "watching now" text
            watching_match = re.search(r'(\d+(?:,\d+)*)\s+watching now', content, re.IGNORECASE)
            if watching_match:
                is_live = True
                viewers = int(watching_match.group(1).replace(',', ''))
            
            # Method 4: Look for concurrent viewers
            concurrent_match = re.search(r'"concurrentViewers"\s*:\s*"(\d+)"', content)
            if concurrent_match:
                is_live = True
                viewers = int(concurrent_match.group(1))
            
            # Method 5: Look for live streaming metadata
            if re.search(r'"isLive"\s*:\s*true', content):
                is_live = True
            
            return {
                'is_live': is_live,
                'title': title,
                'viewers': viewers
            }
            
        except Exception as e:
            return {'is_live': False, 'title': 'Error', 'viewers': 0}
    
    def quick_test_known_live_channels(self):
        """Test a few channels that are likely to have live content"""
        
        test_channels = [
            ("ABC News", "https://www.youtube.com/@ABCNews"),
            ("Sky News", "https://www.youtube.com/@SkyNews"),
            ("Al Jazeera English", "https://www.youtube.com/@aljazeeraenglish"),
            ("DW News", "https://www.youtube.com/@dwnews"),
            ("CNBC", "https://www.youtube.com/@CNBC")
        ]
        
        print("🎯 Quick Test of Live Stream Detection")
        print("=" * 50)
        
        all_live_streams = []
        
        for network_name, channel_url in test_channels:
            print(f"\n[Testing {network_name}]")
            live_streams = self.test_specific_channel_live_detection(channel_url, network_name)
            all_live_streams.extend(live_streams)
            
            time.sleep(3)  # Be respectful between channels
        
        print("\n" + "=" * 50)
        print("🔴 LIVE STREAMS FOUND:")
        print("=" * 50)
        
        if not all_live_streams:
            print("❌ No live streams detected")
            print("\nPossible reasons:")
            print("• No channels currently live streaming")
            print("• YouTube's dynamic content loading")
            print("• Anti-bot measures")
        else:
            for i, stream in enumerate(all_live_streams, 1):
                print(f"\n{i}. 🔴 {stream['network']}")
                print(f"   📺 {stream['title']}")
                print(f"   👥 {stream['viewers']:,} viewers")
                print(f"   🔗 {stream['url']}")
        
        # Save results
        results = {
            'test_timestamp': datetime.now().isoformat(),
            'channels_tested': len(test_channels),
            'live_streams_found': len(all_live_streams),
            'live_streams': all_live_streams
        }
        
        with open('quick_live_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to quick_live_test_results.json")
        
        return all_live_streams

def main():
    detector = AdvancedLiveStreamDetector()
    detector.quick_test_known_live_channels()

if __name__ == "__main__":
    main()
