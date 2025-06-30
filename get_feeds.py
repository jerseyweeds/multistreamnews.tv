#!/usr/bin/env python3
"""
YouTube Live Feed Scanner - Desktop Version
Part of MultiStreamNews.TV

A Python tool to scan YouTube channel live tabs and extract feed metadata.
Usage: python get_feeds.py [channel_url]
"""

import requests
import json
import re
import sys
import argparse
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import csv
import os

class YouTubeFeedScanner:
    def __init__(self):
        self.feeds = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scan_channel(self, channel_url, use_proxy=False, proxy_url=None):
        """
        Scan a YouTube channel for live feeds
        
        Args:
            channel_url (str): YouTube channel URL
            use_proxy (bool): Whether to use a CORS proxy
            proxy_url (str): Custom proxy URL
        
        Returns:
            list: List of feed dictionaries
        """
        print(f"🔍 Scanning channel: {channel_url}")
        
        if not self.is_valid_youtube_url(channel_url):
            raise ValueError("Invalid YouTube channel URL")
        
        # Convert to live tab URL if needed
        live_url = self.convert_to_live_url(channel_url)
        print(f"📺 Live tab URL: {live_url}")
        
        try:
            html = self.fetch_page(live_url, use_proxy, proxy_url)
            feeds = self.parse_feeds(html)
            self.feeds = feeds
            
            print(f"✅ Found {len(feeds)} live feed(s)")
            return feeds
            
        except Exception as e:
            print(f"❌ Error scanning channel: {str(e)}")
            raise
    
    def is_valid_youtube_url(self, url):
        """Check if URL is a valid YouTube URL"""
        try:
            parsed = urlparse(url)
            return parsed.hostname in ['www.youtube.com', 'youtube.com', 'youtu.be']
        except:
            return False
    
    def convert_to_live_url(self, url):
        """Convert various YouTube URLs to live tab format"""
        parsed = urlparse(url)
        
        # Extract channel ID or username
        if '/channel/' in url:
            channel_id = url.split('/channel/')[1].split('/')[0]
            return f"https://www.youtube.com/channel/{channel_id}/live"
        elif '/c/' in url:
            channel_name = url.split('/c/')[1].split('/')[0]
            return f"https://www.youtube.com/c/{channel_name}/live"
        elif '/user/' in url:
            username = url.split('/user/')[1].split('/')[0]
            return f"https://www.youtube.com/user/{username}/live"
        elif '/@' in url:
            handle = url.split('/@')[1].split('/')[0]
            return f"https://www.youtube.com/@{handle}/live"
        
        # If it's already a live URL, return as is
        if '/live' in url or '/streams' in url:
            return url
        
        # Default: assume it's a base channel URL and add /live
        return f"{url.rstrip('/')}/live"
    
    def fetch_page(self, url, use_proxy=False, proxy_url=None):
        """Fetch the YouTube page content"""
        target_url = url
        
        if use_proxy:
            if proxy_url:
                if 'allorigins' in proxy_url:
                    target_url = f"{proxy_url}{requests.utils.quote(url, safe='')}"
                else:
                    target_url = f"{proxy_url}{url}"
            else:
                # Default proxy
                target_url = f"https://api.allorigins.win/get?url={requests.utils.quote(url, safe='')}"
        
        print(f"🌐 Fetching: {target_url}")
        
        response = self.session.get(target_url, timeout=30)
        response.raise_for_status()
        
        if use_proxy and 'allorigins' in (proxy_url or target_url):
            data = response.json()
            return data.get('contents', '')
        else:
            return response.text
    
    def parse_feeds(self, html):
        """Parse YouTube HTML to extract live feed metadata"""
        feeds = []
        
        try:
            # Try to extract ytInitialData
            yt_data = self.extract_yt_initial_data(html)
            if yt_data:
                feeds.extend(self.extract_feeds_from_yt_data(yt_data))
            
            # Fallback: regex-based extraction
            if not feeds:
                feeds.extend(self.extract_feeds_from_regex(html))
            
        except Exception as e:
            print(f"⚠️  Parsing error: {str(e)}")
        
        return feeds
    
    def extract_yt_initial_data(self, html):
        """Extract YouTube's initial data JSON from HTML"""
        patterns = [
            r'var ytInitialData\s*=\s*({.*?});',
            r'window\["ytInitialData"\]\s*=\s*({.*?});',
            r'ytInitialData["\']\s*[:=]\s*({.*?});'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except:
                    continue
        
        return None
    
    def extract_feeds_from_yt_data(self, yt_data):
        """Extract feeds from YouTube's structured data"""
        feeds = []
        
        try:
            # Navigate through YouTube's data structure
            contents = yt_data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
            
            for tab in contents:
                tab_renderer = tab.get('tabRenderer', {})
                
                # Look for Live tab
                if (tab_renderer.get('title') == 'Live' or 
                    'live' in str(tab_renderer.get('endpoint', {}))):
                    
                    content = tab_renderer.get('content', {})
                    section_list = content.get('sectionListRenderer', {}).get('contents', [])
                    
                    for section in section_list:
                        items = (section.get('itemSectionRenderer', {}).get('contents', []) or
                                section.get('videoListRenderer', {}).get('contents', []) or
                                section.get('gridRenderer', {}).get('items', []))
                        
                        for item in items:
                            feed = self.extract_feed_from_item(item)
                            if feed:
                                feeds.append(feed)
        
        except Exception as e:
            print(f"⚠️  Error extracting from structured data: {str(e)}")
        
        return feeds
    
    def extract_feed_from_item(self, item):
        """Extract feed data from a YouTube item"""
        try:
            video_renderer = item.get('videoRenderer') or item.get('gridVideoRenderer')
            if not video_renderer:
                return None
            
            video_id = video_renderer.get('videoId')
            if not video_id:
                return None
            
            # Extract title
            title_data = video_renderer.get('title', {})
            title = (title_data.get('runs', [{}])[0].get('text') or 
                    title_data.get('simpleText') or 
                    'Unknown Title')
            
            # Extract channel name
            owner_data = video_renderer.get('ownerText', {})
            channel_name = (owner_data.get('runs', [{}])[0].get('text') or 
                           'Unknown Channel')
            
            # Check if live
            badges = video_renderer.get('badges', [])
            is_live = any(badge.get('metadataBadgeRenderer', {}).get('style') == 'BADGE_STYLE_TYPE_LIVE_NOW' 
                         for badge in badges)
            
            # Extract view count
            view_count_data = video_renderer.get('viewCountText', {})
            view_count_text = (view_count_data.get('simpleText') or 
                              video_renderer.get('shortViewCountText', {}).get('simpleText') or 
                              '0 viewers')
            
            # Extract duration
            length_data = video_renderer.get('lengthText', {})
            duration = length_data.get('simpleText') or 'Live'
            
            # If no duration from lengthText, check thumbnailOverlays
            if duration == 'Live':
                overlays = video_renderer.get('thumbnailOverlays', [])
                for overlay in overlays:
                    time_status = overlay.get('thumbnailOverlayTimeStatusRenderer', {})
                    if time_status:
                        duration = time_status.get('text', {}).get('simpleText', 'Live')
                        break
            
            return {
                'video_id': video_id,
                'title': title,
                'channel_name': channel_name,
                'view_count': self.parse_view_count(view_count_text),
                'view_count_text': view_count_text,
                'duration': duration,
                'is_live': is_live,
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'status': 'live' if is_live else 'upcoming',
                'extracted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️  Error extracting feed item: {str(e)}")
            return None
    
    def extract_feeds_from_regex(self, html):
        """Fallback regex-based extraction"""
        feeds = []
        
        try:
            # Look for video IDs and titles
            video_pattern = r'/watch\?v=([a-zA-Z0-9_-]{11})'
            title_pattern = r'"title":\s*"([^"]+)"'
            
            video_matches = re.findall(video_pattern, html)
            title_matches = re.findall(title_pattern, html)
            
            # Remove duplicates while preserving order
            video_ids = list(dict.fromkeys(video_matches))
            
            for i, video_id in enumerate(video_ids[:10]):  # Limit to first 10
                title = title_matches[i] if i < len(title_matches) else 'Unknown Title'
                
                feeds.append({
                    'video_id': video_id,
                    'title': title,
                    'channel_name': 'Unknown Channel',
                    'view_count': 0,
                    'view_count_text': 'Unknown',
                    'duration': 'Live',
                    'is_live': True,
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'status': 'live',
                    'extracted_at': datetime.now().isoformat()
                })
        
        except Exception as e:
            print(f"⚠️  Error in regex extraction: {str(e)}")
        
        return feeds
    
    def parse_view_count(self, view_count_text):
        """Parse view count text to number"""
        if not view_count_text:
            return 0
        
        text = view_count_text.lower()
        number_match = re.search(r'([\d.]+)', text)
        
        if not number_match:
            return 0
        
        number = float(number_match.group(1))
        
        if 'k' in text:
            return int(number * 1000)
        elif 'm' in text:
            return int(number * 1000000)
        elif 'b' in text:
            return int(number * 1000000000)
        
        return int(number)
    
    def display_feeds(self, feeds=None):
        """Display feeds in a formatted table"""
        if feeds is None:
            feeds = self.feeds
        
        if not feeds:
            print("No feeds found.")
            return
        
        # Print header
        print("\n" + "="*120)
        print(f"{'Status':<8} {'Title':<40} {'Channel':<20} {'Viewers':<12} {'Duration':<10} {'URL':<25}")
        print("="*120)
        
        # Print feeds
        for feed in feeds:
            status = "🔴 LIVE" if feed['is_live'] else "⏰ UPCOMING"
            title = feed['title'][:37] + "..." if len(feed['title']) > 40 else feed['title']
            channel = feed['channel_name'][:17] + "..." if len(feed['channel_name']) > 20 else feed['channel_name']
            viewers = f"{feed['view_count']:,}" if feed['view_count'] > 0 else feed['view_count_text']
            duration = feed['duration']
            url = feed['url'][:22] + "..." if len(feed['url']) > 25 else feed['url']
            
            print(f"{status:<8} {title:<40} {channel:<20} {viewers:<12} {duration:<10} {url:<25}")
        
        print("="*120)
        print(f"Total: {len(feeds)} feed(s)")
    
    def export_to_csv(self, filename=None, feeds=None):
        """Export feeds to CSV file"""
        if feeds is None:
            feeds = self.feeds
        
        if not feeds:
            print("No feeds to export.")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"youtube_feeds_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['status', 'title', 'channel_name', 'view_count', 'view_count_text', 
                             'duration', 'url', 'video_id', 'extracted_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for feed in feeds:
                    writer.writerow(feed)
            
            print(f"✅ Exported {len(feeds)} feed(s) to {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {str(e)}")
    
    def export_to_json(self, filename=None, feeds=None):
        """Export feeds to JSON file"""
        if feeds is None:
            feeds = self.feeds
        
        if not feeds:
            print("No feeds to export.")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"youtube_feeds_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(feeds, jsonfile, indent=2, ensure_ascii=False)
            
            print(f"✅ Exported {len(feeds)} feed(s) to {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting to JSON: {str(e)}")
    
    def get_urls_only(self, feeds=None):
        """Get only the URLs from feeds"""
        if feeds is None:
            feeds = self.feeds
        
        return [feed['url'] for feed in feeds]
    
    def copy_urls_to_clipboard(self, feeds=None):
        """Copy URLs to clipboard (requires pyperclip)"""
        try:
            import pyperclip
            urls = self.get_urls_only(feeds)
            if urls:
                pyperclip.copy('\n'.join(urls))
                print(f"✅ Copied {len(urls)} URL(s) to clipboard")
            else:
                print("No URLs to copy")
        except ImportError:
            print("⚠️  pyperclip not installed. Install with: pip install pyperclip")
            print("URLs not copied to clipboard.")

def main():
    parser = argparse.ArgumentParser(
        description='YouTube Live Feed Scanner - Extract live stream metadata from YouTube channels',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python get_feeds.py "https://www.youtube.com/channel/UC4R8DWoMoI7CAwX8_LjQHig/live"
  python get_feeds.py "https://www.youtube.com/@CNN" --export-csv
  python get_feeds.py "https://www.youtube.com/c/SkyNews" --use-proxy --export-json
  python get_feeds.py "https://www.youtube.com/user/BBCNews" --quiet --urls-only
        """
    )
    
    parser.add_argument('channel_url', nargs='?', 
                       default='https://www.youtube.com/channel/UC4R8DWoMoI7CAwX8_LjQHig/live',
                       help='YouTube channel URL (default: Sky News)')
    
    parser.add_argument('--use-proxy', action='store_true',
                       help='Use CORS proxy to bypass restrictions')
    
    parser.add_argument('--proxy-url', type=str,
                       help='Custom proxy URL')
    
    parser.add_argument('--export-csv', action='store_true',
                       help='Export results to CSV file')
    
    parser.add_argument('--export-json', action='store_true',
                       help='Export results to JSON file')
    
    parser.add_argument('--csv-file', type=str,
                       help='Custom CSV filename')
    
    parser.add_argument('--json-file', type=str,
                       help='Custom JSON filename')
    
    parser.add_argument('--urls-only', action='store_true',
                       help='Output only URLs, one per line')
    
    parser.add_argument('--copy-urls', action='store_true',
                       help='Copy URLs to clipboard (requires pyperclip)')
    
    parser.add_argument('--quiet', action='store_true',
                       help='Quiet mode - minimal output')
    
    args = parser.parse_args()
    
    if not args.quiet:
        print("🎬 YouTube Live Feed Scanner")
        print("=" * 50)
    
    scanner = YouTubeFeedScanner()
    
    try:
        feeds = scanner.scan_channel(
            args.channel_url, 
            use_proxy=args.use_proxy,
            proxy_url=args.proxy_url
        )
        
        if args.urls_only:
            for url in scanner.get_urls_only(feeds):
                print(url)
        elif not args.quiet:
            scanner.display_feeds(feeds)
        
        # Export options
        if args.export_csv:
            scanner.export_to_csv(args.csv_file, feeds)
        
        if args.export_json:
            scanner.export_to_json(args.json_file, feeds)
        
        if args.copy_urls:
            scanner.copy_urls_to_clipboard(feeds)
        
        if not args.quiet:
            print(f"\n🎯 Scan completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
