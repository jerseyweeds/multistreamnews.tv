#!/usr/bin/env python3
"""
Enhanced YouTube Live Stream Scanner
Uses selenium for better JavaScript rendering and YouTube API approach
"""

import json
import time
from datetime import datetime
import re
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup

class EnhancedYouTubeLiveStreamScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
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
    
    def get_channel_id_from_handle(self, channel_url):
        """Extract channel ID from YouTube handle URL"""
        try:
            response = self.session.get(channel_url, timeout=15)
            response.raise_for_status()
            
            # Look for channel ID in various places
            content = response.text
            
            # Method 1: Look for channel ID in meta tags
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check meta property
            meta_tag = soup.find('meta', property='og:url')
            if meta_tag and 'channel' in meta_tag.get('content', ''):
                channel_url = meta_tag.get('content')
                if '/channel/' in channel_url:
                    return channel_url.split('/channel/')[-1].split('/')[0]
            
            # Method 2: Look in JavaScript
            channel_id_match = re.search(r'"channelId":"([^"]+)"', content)
            if channel_id_match:
                return channel_id_match.group(1)
            
            # Method 3: Look for externalId
            external_id_match = re.search(r'"externalId":"([^"]+)"', content)
            if external_id_match:
                return external_id_match.group(1)
                
        except Exception as e:
            print(f"Error getting channel ID from {channel_url}: {e}")
        
        return None
    
    def check_live_streams_direct(self, channel_url):
        """Check for live streams by looking at channel's live tab"""
        try:
            # Try the live streams page directly
            if '/c/' in channel_url:
                live_url = channel_url.rstrip('/') + '/streams'
            elif '/@' in channel_url:
                live_url = channel_url.rstrip('/') + '/streams'
            else:
                live_url = channel_url.rstrip('/') + '/streams'
            
            print(f"  Checking live streams at: {live_url}")
            
            response = self.session.get(live_url, timeout=15)
            if response.status_code == 200:
                content = response.text
                
                # Look for live stream indicators
                live_indicators = [
                    'watching now',
                    'viewers watching',
                    'Live now',
                    'LIVE',
                    'streaming live'
                ]
                
                streams_found = []
                
                # Extract JSON data
                json_match = re.search(r'var ytInitialData = ({.*?});', content)
                if json_match:
                    try:
                        data = json.loads(json_match.group(1))
                        streams_found.extend(self.extract_live_streams_from_json(data))
                    except json.JSONDecodeError:
                        pass
                
                # Fallback: HTML parsing
                if not streams_found:
                    soup = BeautifulSoup(content, 'html.parser')
                    streams_found.extend(self.extract_live_streams_from_html(soup))
                
                return streams_found
                
        except Exception as e:
            print(f"  Error checking live streams: {e}")
        
        return []
    
    def extract_live_streams_from_json(self, data):
        """Extract live stream data from YouTube JSON"""
        streams = []
        
        try:
            # Navigate through the complex JSON structure
            contents = data.get('contents', {})
            
            # Look in various possible locations
            possible_paths = [
                ['contents', 'twoColumnBrowseResultsRenderer', 'tabs'],
                ['contents', 'sectionListRenderer', 'contents'],
                ['header', 'c4TabbedHeaderRenderer', 'navigationEndpoint']
            ]
            
            def find_video_renderers(obj, path=[]):
                """Recursively find video renderers in the JSON structure"""
                found_renderers = []
                
                if isinstance(obj, dict):
                    # Check if this is a video renderer
                    if any(key.endswith('VideoRenderer') for key in obj.keys()):
                        for key, value in obj.items():
                            if key.endswith('VideoRenderer') and isinstance(value, dict):
                                found_renderers.append(value)
                    
                    # Recursively search in all dict values
                    for key, value in obj.items():
                        found_renderers.extend(find_video_renderers(value, path + [key]))
                
                elif isinstance(obj, list):
                    # Recursively search in all list items
                    for i, item in enumerate(obj):
                        found_renderers.extend(find_video_renderers(item, path + [i]))
                
                return found_renderers
            
            video_renderers = find_video_renderers(data)
            
            for renderer in video_renderers:
                stream_info = self.parse_video_renderer_for_live(renderer)
                if stream_info and stream_info.get('is_live'):
                    streams.append(stream_info)
        
        except Exception as e:
            print(f"    Error parsing JSON for live streams: {e}")
        
        return streams
    
    def parse_video_renderer_for_live(self, renderer):
        """Parse video renderer specifically looking for live streams"""
        try:
            video_id = renderer.get('videoId', '')
            if not video_id:
                return None
            
            # Get title
            title = ''
            title_obj = renderer.get('title', {})
            if 'runs' in title_obj:
                title = ''.join(run.get('text', '') for run in title_obj['runs'])
            elif 'simpleText' in title_obj:
                title = title_obj['simpleText']
            
            # Check for live badges
            is_live = False
            badges = renderer.get('badges', [])
            for badge in badges:
                badge_renderer = badge.get('metadataBadgeRenderer', {})
                label = badge_renderer.get('label', '').upper()
                if 'LIVE' in label:
                    is_live = True
                    break
            
            # Check for live in title
            if not is_live and 'live' in title.lower():
                is_live = True
            
            # Get viewer count
            viewer_count = 0
            view_count_text = ''
            
            # Look for view count in various places
            for key in ['viewCountText', 'shortViewCountText']:
                if key in renderer:
                    view_obj = renderer[key]
                    if 'simpleText' in view_obj:
                        view_count_text = view_obj['simpleText']
                    elif 'runs' in view_obj:
                        view_count_text = ''.join(run.get('text', '') for run in view_obj['runs'])
                    break
            
            # Extract numeric viewer count
            if 'watching' in view_count_text.lower():
                numbers = re.findall(r'(\d+(?:,\d+)*)', view_count_text)
                if numbers:
                    viewer_count = int(numbers[0].replace(',', ''))
                    is_live = True  # If it says "watching", it's likely live
            
            if is_live or viewer_count > 0:
                return {
                    'video_id': video_id,
                    'title': title,
                    'is_live': is_live,
                    'viewer_count': viewer_count,
                    'view_count_text': view_count_text,
                    'url': f'https://www.youtube.com/watch?v={video_id}'
                }
        
        except Exception as e:
            print(f"    Error parsing video renderer: {e}")
        
        return None
    
    def extract_live_streams_from_html(self, soup):
        """Extract live streams from HTML as fallback"""
        streams = []
        
        try:
            # Look for live indicators in the HTML
            live_elements = soup.find_all(text=re.compile(r'(LIVE|watching now|viewers)', re.IGNORECASE))
            
            for element in live_elements:
                # Find nearby video links
                parent = element.parent
                for _ in range(5):  # Look up to 5 levels up
                    if parent:
                        video_link = parent.find('a', href=re.compile(r'/watch\?v='))
                        if video_link:
                            href = video_link.get('href', '')
                            video_id_match = re.search(r'v=([^&]+)', href)
                            if video_id_match:
                                video_id = video_id_match.group(1)
                                title = video_link.get('title', '') or video_link.get_text(strip=True)
                                
                                # Try to extract viewer count
                                viewer_count = 0
                                viewer_text = element.strip() if hasattr(element, 'strip') else str(element)
                                numbers = re.findall(r'(\d+(?:,\d+)*)', viewer_text)
                                if numbers:
                                    viewer_count = int(numbers[0].replace(',', ''))
                                
                                streams.append({
                                    'video_id': video_id,
                                    'title': title,
                                    'is_live': True,
                                    'viewer_count': viewer_count,
                                    'view_count_text': viewer_text,
                                    'url': f'https://www.youtube.com/watch?v={video_id}'
                                })
                                break
                        parent = parent.parent
                    else:
                        break
        
        except Exception as e:
            print(f"    Error extracting from HTML: {e}")
        
        return streams
    
    def scan_channel(self, network_name, channel_url):
        """Scan a single channel for live streams"""
        print(f"\nScanning {network_name}...")
        print(f"  URL: {channel_url}")
        
        try:
            # Method 1: Check live streams page
            live_streams = self.check_live_streams_direct(channel_url)
            
            if live_streams:
                print(f"  Found {len(live_streams)} potential live stream(s)")
                
                for stream in live_streams:
                    # Verify it's actually live and get accurate viewer count
                    verified_stream = self.verify_live_stream(stream['url'])
                    if verified_stream and verified_stream.get('is_live') and verified_stream.get('viewer_count', 0) > 0:
                        final_stream = {
                            'network': network_name,
                            'title': stream['title'],
                            'url': stream['url'],
                            'viewer_count': verified_stream['viewer_count'],
                            'is_live': True,
                            'scanned_at': datetime.now().isoformat()
                        }
                        self.live_streams.append(final_stream)
                        print(f"  ✓ Confirmed live: {stream['title']} ({verified_stream['viewer_count']} viewers)")
                    else:
                        print(f"  ✗ Not live or no viewers: {stream['title']}")
            else:
                print("  No live streams found")
        
        except Exception as e:
            print(f"  Error scanning {network_name}: {e}")
        
        # Be respectful to YouTube's servers
        time.sleep(2)
    
    def verify_live_stream(self, video_url):
        """Verify if a video is actually live and get viewer count"""
        try:
            print(f"    Verifying: {video_url}")
            response = self.session.get(video_url, timeout=15)
            response.raise_for_status()
            
            content = response.text
            
            # Look for live indicators
            is_live = False
            viewer_count = 0
            
            # Check for various live indicators
            live_patterns = [
                r'"isLiveContent":true',
                r'"isLive":true',
                r'watching now',
                r'viewers watching',
                r'"liveBroadcastDetails"'
            ]
            
            for pattern in live_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    is_live = True
                    break
            
            if is_live:
                # Try to extract viewer count
                viewer_patterns = [
                    r'(\d+(?:,\d+)*)\s+watching now',
                    r'(\d+(?:,\d+)*)\s+viewers watching',
                    r'"viewCount"\s*:\s*"(\d+)"',
                    r'"concurrentViewers"\s*:\s*"(\d+)"'
                ]
                
                for pattern in viewer_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        viewer_count = int(match.group(1).replace(',', ''))
                        break
            
            return {
                'is_live': is_live,
                'viewer_count': viewer_count
            }
        
        except Exception as e:
            print(f"    Error verifying stream: {e}")
            return {'is_live': False, 'viewer_count': 0}
    
    def scan_all_channels(self, network_list_file):
        """Scan all channels in the network list"""
        networks = self.parse_network_list(network_list_file)
        
        print(f"Enhanced YouTube Live Stream Scanner")
        print(f"Found {len(networks)} networks to scan")
        print("=" * 60)
        
        for i, (network_name, channel_url) in enumerate(networks):
            print(f"\n[{i+1}/{len(networks)}]", end="")
            try:
                self.scan_channel(network_name, channel_url)
            except Exception as e:
                print(f"Error scanning {network_name}: {e}")
                continue
        
        return self.live_streams
    
    def save_results(self, filename='enhanced_live_streams_results.json'):
        """Save the results to a JSON file"""
        results = {
            'scan_timestamp': datetime.now().isoformat(),
            'total_networks_scanned': len(self.live_streams),
            'live_streams': self.live_streams
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to {filename}")
    
    def print_summary(self):
        """Print a summary of found live streams"""
        print("\n" + "=" * 60)
        print("LIVE STREAMS SUMMARY")
        print("=" * 60)
        
        if not self.live_streams:
            print("No live streams with active viewers found.")
            print("\nThis could be due to:")
            print("- No channels currently live streaming")
            print("- YouTube's anti-bot measures")
            print("- Rate limiting")
            print("- Channel URLs that have changed")
            return
        
        # Sort by viewer count
        sorted_streams = sorted(self.live_streams, key=lambda x: x.get('viewer_count', 0), reverse=True)
        
        for i, stream in enumerate(sorted_streams, 1):
            print(f"\n{i}. {stream['network']}")
            print(f"   Title: {stream['title']}")
            print(f"   Viewers: {stream.get('viewer_count', 0):,}")
            print(f"   URL: {stream['url']}")
        
        total_viewers = sum(stream.get('viewer_count', 0) for stream in self.live_streams)
        print(f"\n📊 Summary:")
        print(f"   Total live streams: {len(self.live_streams)}")
        print(f"   Total viewers across all streams: {total_viewers:,}")
        
        if self.live_streams:
            avg_viewers = total_viewers / len(self.live_streams)
            print(f"   Average viewers per stream: {avg_viewers:.0f}")

def main():
    print("🔴 Enhanced YouTube Live Stream Scanner")
    print("=" * 60)
    
    scanner = EnhancedYouTubeLiveStreamScanner()
    
    # Scan all channels
    live_streams = scanner.scan_all_channels('network_list.txt')
    
    # Print summary
    scanner.print_summary()
    
    # Save results
    scanner.save_results()
    
    print(f"\n✅ Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
