#!/usr/bin/env python3
"""
Precise YouTube Live Stream Detection Scanner
Focuses on actual livestreaming content using specific HTML markers
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
from urllib.parse import urljoin

class PreciseLiveStreamScanner:
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
        self.live_streams = []
        
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
    
    def detect_live_streams_precise(self, network_name, channel_url):
        """Precisely detect live streams using specific YouTube live indicators"""
        print(f"\n🔍 Scanning {network_name}")
        print(f"   URL: {channel_url}")
        
        live_streams = []
        
        try:
            response = self.session.get(channel_url, timeout=15)
            response.raise_for_status()
            
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            
            print(f"   📄 Analyzing page content...")
            
            # Method 1: Look for "Live now" section in HTML
            live_now_streams = self._find_live_now_section(soup, content)
            live_streams.extend(live_now_streams)
            
            # Method 2: Look for LIVE overlay badges
            live_badge_streams = self._find_live_badge_streams(soup, content)
            live_streams.extend(live_badge_streams)
            
            # Method 3: Look for JSON data with live indicators
            json_live_streams = self._find_live_streams_in_json(content)
            live_streams.extend(json_live_streams)
            
            # Remove duplicates based on video ID
            unique_streams = self._remove_duplicate_streams(live_streams)
            
            if unique_streams:
                print(f"   ✅ Found {len(unique_streams)} live stream(s)")
                
                # Verify each stream is actually live
                verified_streams = []
                for stream in unique_streams:
                    if self._verify_stream_is_live(stream):
                        verified_streams.append({
                            **stream,
                            'network': network_name,
                            'detected_at': datetime.now().isoformat()
                        })
                        print(f"   🔴 Confirmed: {stream['title']} ({stream.get('viewers', 'N/A')} viewers)")
                    else:
                        print(f"   ❌ Not live: {stream['title']}")
                
                self.live_streams.extend(verified_streams)
                return verified_streams
            else:
                print(f"   ⚪ No live streams detected")
                
        except Exception as e:
            print(f"   ❌ Error scanning: {e}")
        
        return []
    
    def _find_live_now_section(self, soup, content):
        """Find streams in the 'Live now' section"""
        live_streams = []
        
        try:
            # Look for "Live now" text in the HTML
            live_now_elements = soup.find_all(text=re.compile(r'Live now', re.IGNORECASE))
            
            for element in live_now_elements:
                print(f"     🔍 Found 'Live now' section")
                
                # Find the parent container
                parent = element.parent if hasattr(element, 'parent') else None
                
                # Look for video links near the "Live now" text
                for i in range(5):  # Check up to 5 parent levels
                    if parent:
                        video_links = parent.find_all('a', href=re.compile(r'/watch\?v='))
                        
                        for link in video_links:
                            video_id = self._extract_video_id(link.get('href', ''))
                            if video_id:
                                title = self._extract_title_from_link(link)
                                
                                # Check for LIVE badge near this link
                                has_live_badge = self._check_live_badge_near_element(link)
                                
                                if has_live_badge:
                                    live_streams.append({
                                        'video_id': video_id,
                                        'title': title,
                                        'url': f'https://www.youtube.com/watch?v={video_id}',
                                        'detection_method': 'live_now_section',
                                        'has_live_badge': True
                                    })
                                    print(f"       ✅ Found live stream in Live now: {title}")
                        
                        parent = parent.parent
                    else:
                        break
        
        except Exception as e:
            print(f"     ⚠️ Error in live now section detection: {e}")
        
        return live_streams
    
    def _find_live_badge_streams(self, soup, content):
        """Find streams with LIVE overlay badges"""
        live_streams = []
        
        try:
            # Method 1: Look for overlay-style="LIVE"
            live_overlays = soup.find_all(attrs={'overlay-style': 'LIVE'})
            print(f"     🔍 Found {len(live_overlays)} overlay-style='LIVE' elements")
            
            for overlay in live_overlays:
                video_link = self._find_video_link_near_element(overlay)
                if video_link:
                    video_id = self._extract_video_id(video_link.get('href', ''))
                    title = self._extract_title_from_link(video_link)
                    
                    if video_id:
                        live_streams.append({
                            'video_id': video_id,
                            'title': title,
                            'url': f'https://www.youtube.com/watch?v={video_id}',
                            'detection_method': 'live_overlay',
                            'has_live_badge': True
                        })
                        print(f"       ✅ Found via LIVE overlay: {title}")
            
            # Method 2: Look for <div class="badge-shape-wiz__text">LIVE</div>
            live_badges = soup.find_all('div', class_='badge-shape-wiz__text', text='LIVE')
            print(f"     🔍 Found {len(live_badges)} badge-shape-wiz__text LIVE elements")
            
            for badge in live_badges:
                video_link = self._find_video_link_near_element(badge)
                if video_link:
                    video_id = self._extract_video_id(video_link.get('href', ''))
                    title = self._extract_title_from_link(video_link)
                    
                    if video_id:
                        live_streams.append({
                            'video_id': video_id,
                            'title': title,
                            'url': f'https://www.youtube.com/watch?v={video_id}',
                            'detection_method': 'live_badge',
                            'has_live_badge': True
                        })
                        print(f"       ✅ Found via LIVE badge: {title}")
            
            # Method 3: Look for any element containing "LIVE" with video nearby
            live_elements = soup.find_all(text=re.compile(r'^LIVE$'))
            print(f"     🔍 Found {len(live_elements)} standalone LIVE text elements")
            
            for live_text in live_elements:
                parent = live_text.parent if hasattr(live_text, 'parent') else None
                if parent:
                    video_link = self._find_video_link_near_element(parent)
                    if video_link:
                        video_id = self._extract_video_id(video_link.get('href', ''))
                        title = self._extract_title_from_link(video_link)
                        
                        if video_id:
                            live_streams.append({
                                'video_id': video_id,
                                'title': title,
                                'url': f'https://www.youtube.com/watch?v={video_id}',
                                'detection_method': 'live_text',
                                'has_live_badge': True
                            })
                            print(f"       ✅ Found via LIVE text: {title}")
        
        except Exception as e:
            print(f"     ⚠️ Error in live badge detection: {e}")
        
        return live_streams
    
    def _find_live_streams_in_json(self, content):
        """Find live streams in YouTube's JSON data"""
        live_streams = []
        
        try:
            # Look for ytInitialData
            json_match = re.search(r'var ytInitialData = ({.*?});', content, re.DOTALL)
            if json_match:
                print(f"     🔍 Analyzing YouTube JSON data...")
                
                try:
                    data = json.loads(json_match.group(1))
                    live_streams.extend(self._extract_live_from_json_data(data))
                except json.JSONDecodeError as e:
                    print(f"     ⚠️ JSON decode error: {e}")
        
        except Exception as e:
            print(f"     ⚠️ Error in JSON live stream detection: {e}")
        
        return live_streams
    
    def _extract_live_from_json_data(self, data):
        """Extract live streams from JSON data structure"""
        live_streams = []
        
        def find_live_renderers(obj, path=""):
            """Recursively find video renderers with live indicators"""
            if isinstance(obj, dict):
                # Check if this object has live indicators
                if self._is_live_renderer(obj):
                    video_id = obj.get('videoId')
                    if video_id:
                        title = self._extract_title_from_renderer(obj)
                        viewers = self._extract_viewers_from_renderer(obj)
                        
                        live_streams.append({
                            'video_id': video_id,
                            'title': title,
                            'url': f'https://www.youtube.com/watch?v={video_id}',
                            'viewers': viewers,
                            'detection_method': 'json_data',
                            'has_live_badge': True
                        })
                        print(f"       ✅ Found in JSON: {title} ({viewers} viewers)")
                
                # Recurse into nested objects
                for key, value in obj.items():
                    find_live_renderers(value, f"{path}.{key}")
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_live_renderers(item, f"{path}[{i}]")
        
        find_live_renderers(data)
        return live_streams
    
    def _is_live_renderer(self, renderer):
        """Check if a renderer represents a live stream"""
        # Check for live badges
        badges = renderer.get('badges', [])
        for badge in badges:
            badge_renderer = badge.get('metadataBadgeRenderer', {})
            if badge_renderer.get('label', '').upper() == 'LIVE':
                return True
            if badge_renderer.get('style', '') == 'BADGE_STYLE_TYPE_LIVE_NOW':
                return True
        
        # Check for live broadcast details
        if 'liveBroadcastDetails' in renderer:
            return True
        
        # Check for live content indicator
        if renderer.get('isLiveContent') is True:
            return True
        
        return False
    
    def _extract_title_from_renderer(self, renderer):
        """Extract title from a video renderer"""
        title_obj = renderer.get('title', {})
        
        if 'runs' in title_obj:
            return ''.join(run.get('text', '') for run in title_obj['runs'])
        elif 'simpleText' in title_obj:
            return title_obj['simpleText']
        
        return "Unknown Title"
    
    def _extract_viewers_from_renderer(self, renderer):
        """Extract viewer count from a live stream renderer"""
        # Look for view count in various places
        view_keys = ['viewCountText', 'shortViewCountText']
        
        for key in view_keys:
            if key in renderer:
                view_obj = renderer[key]
                
                if 'simpleText' in view_obj:
                    text = view_obj['simpleText']
                elif 'runs' in view_obj:
                    text = ''.join(run.get('text', '') for run in view_obj['runs'])
                else:
                    continue
                
                # Extract number from text like "1,234 watching now"
                if 'watching' in text.lower():
                    numbers = re.findall(r'(\d+(?:,\d+)*)', text)
                    if numbers:
                        return int(numbers[0].replace(',', ''))
        
        return 0
    
    def _check_live_badge_near_element(self, element):
        """Check if there's a LIVE badge near an element"""
        # Check the element itself and its nearby siblings/parents
        for level in range(3):  # Check 3 levels up/down
            if element:
                # Check current element
                if element.get_text and 'LIVE' in element.get_text():
                    return True
                
                # Check for overlay-style attribute
                if element.get('overlay-style') == 'LIVE':
                    return True
                
                # Check for LIVE badge classes
                live_badges = element.find_all('div', class_='badge-shape-wiz__text', text='LIVE')
                if live_badges:
                    return True
                
                # Move to parent
                element = element.parent
            else:
                break
        
        return False
    
    def _find_video_link_near_element(self, element):
        """Find a video link near a given element"""
        # Check current element and parents
        current = element
        for level in range(10):  # Check up to 10 levels
            if current:
                # Check for video link in current element
                video_link = current.find('a', href=re.compile(r'/watch\?v='))
                if video_link:
                    return video_link
                
                # Check siblings
                if hasattr(current, 'parent') and current.parent:
                    for sibling in current.parent.find_all('a', href=re.compile(r'/watch\?v=')):
                        return sibling
                
                # Move to parent
                current = current.parent if hasattr(current, 'parent') else None
            else:
                break
        
        return None
    
    def _extract_video_id(self, href):
        """Extract video ID from YouTube URL"""
        if not href:
            return None
        
        match = re.search(r'v=([a-zA-Z0-9_-]{11})', href)
        return match.group(1) if match else None
    
    def _extract_title_from_link(self, link):
        """Extract title from a video link element"""
        # Try various attributes and text content
        title = (link.get('title') or 
                link.get('aria-label') or 
                link.get_text(strip=True) or 
                "Unknown Title")
        
        return title[:100]  # Limit title length
    
    def _remove_duplicate_streams(self, streams):
        """Remove duplicate streams based on video ID"""
        seen_ids = set()
        unique_streams = []
        
        for stream in streams:
            video_id = stream.get('video_id')
            if video_id and video_id not in seen_ids:
                seen_ids.add(video_id)
                unique_streams.append(stream)
        
        return unique_streams
    
    def _verify_stream_is_live(self, stream):
        """Verify that a stream is actually live by checking the video page"""
        try:
            print(f"     🔍 Verifying: {stream['title']}")
            
            response = self.session.get(stream['url'], timeout=10)
            if response.status_code != 200:
                return False
            
            content = response.text
            
            # Look for definitive live indicators
            live_indicators = [
                r'"isLiveContent":true',
                r'"isLive":true',
                r'"liveBroadcastDetails"',
                r'watching now',
                r'viewers watching now'
            ]
            
            for pattern in live_indicators:
                if re.search(pattern, content, re.IGNORECASE):
                    # Try to extract viewer count
                    viewer_match = re.search(r'(\d+(?:,\d+)*)\s+watching now', content, re.IGNORECASE)
                    if viewer_match:
                        stream['viewers'] = int(viewer_match.group(1).replace(',', ''))
                    
                    return True
            
            return False
        
        except Exception as e:
            print(f"     ⚠️ Verification error: {e}")
            return False
    
    def scan_all_channels(self, network_list_file):
        """Scan all channels for precise live stream detection"""
        networks = self.parse_network_list(network_list_file)
        
        print("🎯 Precise YouTube Live Stream Scanner")
        print("=" * 60)
        print(f"Scanning {len(networks)} networks for ACTUAL live streams...")
        
        all_live_streams = []
        
        for i, (network_name, channel_url) in enumerate(networks):
            print(f"\n[{i+1}/{len(networks)}]")
            
            try:
                streams = self.detect_live_streams_precise(network_name, channel_url)
                all_live_streams.extend(streams)
                
                time.sleep(2)  # Be respectful to YouTube
                
            except Exception as e:
                print(f"   ❌ Failed to scan {network_name}: {e}")
        
        return all_live_streams
    
    def print_summary(self, live_streams):
        """Print summary of found live streams"""
        print("\n" + "=" * 60)
        print("🔴 PRECISE LIVE STREAMS DETECTED")
        print("=" * 60)
        
        if not live_streams:
            print("❌ No active live streams found")
            print("\nThis indicates either:")
            print("   • No channels are currently live streaming")
            print("   • The detection method needs further refinement")
            return
        
        # Group by network
        by_network = {}
        for stream in live_streams:
            network = stream['network']
            if network not in by_network:
                by_network[network] = []
            by_network[network].append(stream)
        
        # Sort by viewer count
        sorted_streams = sorted(live_streams, key=lambda x: x.get('viewers', 0), reverse=True)
        
        for i, stream in enumerate(sorted_streams, 1):
            print(f"\n{i}. 🔴 {stream['network']}")
            print(f"   📺 {stream['title']}")
            print(f"   👥 {stream.get('viewers', 'N/A')} viewers")
            print(f"   🔗 {stream['url']}")
            print(f"   🎯 Detection: {stream.get('detection_method', 'unknown')}")
        
        print(f"\n📊 Summary:")
        print(f"   • Total live streams: {len(live_streams)}")
        print(f"   • Networks with live content: {len(by_network)}")
        
        total_viewers = sum(s.get('viewers', 0) for s in live_streams if isinstance(s.get('viewers'), int))
        if total_viewers > 0:
            print(f"   • Total viewers: {total_viewers:,}")
    
    def save_results(self, filename='precise_live_streams.json'):
        """Save results to JSON file"""
        results = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'scanner_type': 'precise_live_detection',
                'total_streams': len(self.live_streams)
            },
            'live_streams': self.live_streams
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {filename}")

def main():
    print("🎯 Precise YouTube Live Stream Detection")
    print("=" * 60)
    
    scanner = PreciseLiveStreamScanner()
    
    # Scan all channels
    live_streams = scanner.scan_all_channels('network_list.txt')
    
    # Print summary
    scanner.print_summary(live_streams)
    
    # Save results
    scanner.save_results()
    
    print(f"\n✅ Precise scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
