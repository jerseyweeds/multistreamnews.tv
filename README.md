# Multi Stream News .TV

**🔴 Live at: https://www.multistreamnews.tv/**

Welcome to Multi Stream News .TV, a comprehensive news streaming platform that combines a modern single-page web application with a robust backend monitoring system. This tool is perfect for monitoring live news streams, following multiple events, or creating a custom video dashboard with automated live stream detection capabilities.

## ✨ Key Features Overview

- **🎬 Multi-Video Dashboard**: View multiple YouTube news streams simultaneously in a responsive grid
- **🔴 Live Stream Detection**: Automated backend system that monitors 21+ news networks for live streams
- **📱 Responsive Design**: Optimized for desktop, tablet, and mobile with intelligent touch detection
- **🚀 Multiple Input Methods**: Drag-and-drop, one-click news buttons, bulk "Add All Networks", or manual URL entry
- **⚡ Real-time Updates**: Automated scanning and monitoring with shell script management
- **💾 Persistent Sessions**: Auto-save video layouts with localStorage integration
- **🎨 Modern UI**: macOS-inspired window controls with Tailwind CSS styling

## 🎬 Frontend Features

### Core Video Management
* **Smart Drag & Drop**: Drag YouTube video links from anywhere on your browser directly onto the page
* **One-Click News Access**: Colorful quick-add buttons for 20 major news outlets:
  - **US Networks**: NBC, ABC, LiveNOW, 6abc, CNBC  
  - **International**: Sky News, DW, France 24, Al Jazeera, Bloomberg
  - **Government/Science**: NASA
* **Bulk Loading**: "✨ Add All Networks" button with smart duplicate prevention and progress feedback
* **Manual URL Entry**: Paste multiple YouTube URLs at once (desktop/tablet only)
* **Video Title Display**: Automatically fetches real video titles using YouTube's oEmbed API
* **Auto-Play & Mute**: New videos start playing and muted by default for seamless experience
### Advanced Window Management
* **macOS-style Controls**: Each video has familiar traffic light buttons (red/yellow/green)
  - **Red Button (Close)**: Removes video window and updates localStorage
  - **Yellow Button (Minimize)**: Hides video content while keeping title bar visible
  - **Green Button (Maximize)**: Expands to full width without interrupting playback
* **Zero-Restart Playback**: Videos continue playing seamlessly when maximized/restored using CSS-only positioning
* **Smart Positioning**: New videos placed strategically (top-left or below maximized videos)
* **Bulk Actions**: "Close All Videos" with confirmation modal

### Intelligent User Interface
* **Advanced Touch Detection**: Multi-method detection distinguishes actual touch devices from small screens
  - Drag & drop hidden only on true mobile devices
  - Desktop windows and tablets with mouse/trackpad retain full functionality
* **Three-Tier Responsive Design**: Distinct profiles for phones, tablets, and desktops
  - **Phone**: 2-column control layout, single video column, drag-and-drop hidden
  - **Tablet**: 2-column control layout, multi-video grid, drag-and-drop hidden  
  - **Desktop**: 3-column control layout, multi-video grid, drag-and-drop always visible
* **Device Profile Indicator**: Shows current view mode (Phone/Tablet/Desktop) with device detection
* **Visit Engagement**: Automatically records and displays visit count with fun milestone celebrations
  - **First Visit**: Special welcome message
  - **Early Visits (2-5)**: Shows visit number
  - **Regular Visits (6-10)**: Simple visit count
  - **Active User (11-50)**: Visit count with party emoji 🎉
  - **Power User (51-100)**: Visit count with fire emoji 🔥
  - **Super User (100+)**: Visit count with star emoji 🌟
* **Collapsible Sections**: News channels and manual input can be shown/hidden
* **Smart Footer**: "Made for you in South Jersey" with New Jersey SVG and dynamic timestamp
* **Color-Coded Notifications**: Non-blocking toast system with clear feedback
  - 🟢 Green: Success messages
  - 🟠 Orange: Duplicate warnings
  - 🔴 Red: Error messages  
  - 🟡 Yellow: Mixed issues
### Data Persistence & Management
* **Persistent Sessions**: Video layouts automatically saved to browser localStorage
* **Auto-Restore**: Previously loaded videos restored exactly where you left them
* **URL Management**: Dynamic "Loaded Videos" section with clickable links
* **One-Click Copy**: Copy all active video URLs to clipboard
* **Smart Duplicate Prevention**: Intelligent detection with clear user notifications

### Donation Support
* **Integrated Donations**: "Buy me a coffee" dropdown with multiple payment options
* **Payment Methods**: PayPal, Apple Pay, and Venmo with QR code modals
* **Professional Design**: Branded SVG icons and seamless hover interactions
* **Mobile Optimized**: QR codes for easy mobile payments

## 🔴 Backend Live Stream Detection

### Automated Monitoring System
* **Multi-Script Architecture**: 6 specialized Python scanners with different detection methods
* **Real-time Detection**: Monitors 21+ major news networks for live streams
* **Shell Script Manager**: Easy command-line interface (`live_stream_manager.sh`)
* **Continuous Monitoring**: Background monitoring with configurable intervals
* **Smart Detection**: Video-by-video live status checking for accuracy

### Scanner Scripts
* **`auto_refresh_scanner.py`**: Main automated scanner (recommended for regular use)
* **`comprehensive_live_scanner.py`**: Detailed analysis with viewer counts and metadata
* **`advanced_live_detector.py`**: Test scanner for specific channels and debugging
* **`manual_scan_live_streams.py`**: Multi-endpoint scanning approach
* **`precise_live_scanner.py`**: Pattern matching detection with high accuracy
* **`enhanced_scan_live_streams.py`**: Enhanced detection methods and fallbacks

### Network Coverage
The system monitors these major news outlets:
- **US Networks**: NBC, ABC, CBS, CNN, FOX, 6abc, CNBC
- **International**: Sky News, BBC, DW, France 24, Al Jazeera
- **Business**: Bloomberg, CNBC-TV18
- **Government**: NASA ISS Live
- **Regional**: Various international and local news sources

## 🚀 Quick Start Guide

### Using the Web Application
1. **Visit**: https://www.multistreamnews.tv/
2. **Add Videos**: Choose from three methods:
   - **Quick Add**: Click any colored news channel button
   - **Bulk Add**: Click "✨ Add All Networks" for instant news wall
   - **Drag & Drop**: Drag YouTube links from anywhere onto the page (desktop)
   - **Manual Entry**: Click "[Show] Paste URLs" and enter URLs (desktop/tablet)
3. **Manage Videos**: Use red/yellow/green buttons on each video window
4. **Copy Setup**: Use "Copy All URLs" to save or share your configuration

### Backend Monitoring (Optional)
```bash
# Quick setup
chmod +x live_stream_manager.sh

# Quick scan (2-3 minutes)
./live_stream_manager.sh quick

# View results
./live_stream_manager.sh view

# Continuous monitoring every 15 minutes
./live_stream_manager.sh monitor 15
```

## 📋 Supported URL Formats

* **Full URLs**: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
* **Short URLs**: `https://youtu.be/dQw4w9WgXcQ`

## 🛠️ Technical Architecture

### Frontend Stack
* **Core**: Pure HTML5, vanilla JavaScript (ES6+), and CSS3
* **Styling**: Tailwind CSS (CDN) with custom responsive breakpoints
* **APIs**: YouTube oEmbed API for video title fetching
* **Storage**: Browser localStorage for session persistence  
* **Analytics**: Google Analytics (GA4) integration

### Backend System (Optional)
* **Languages**: Python 3.7+ with requests, BeautifulSoup4, schedule
* **Architecture**: Modular scanner system with unified network configuration
* **Management**: Shell script interface for easy automation
* **Output**: Timestamped JSON results with comprehensive metadata
* **Monitoring**: Continuous background scanning with configurable intervals

### Responsive Design Philosophy
* **Mobile-First**: Progressive enhancement from mobile to desktop
* **Smart Detection**: Advanced touch device detection using multiple methods
* **Device-Aware**: Features hidden based on capabilities, not screen size
* **Breakpoints**: 640px, 768px, 1024px, 1280px with optimized layouts

### Performance Optimizations
* **Single File Deployment**: Entire frontend in one HTML file
* **Lightweight**: No external frameworks or heavy dependencies
* **Async Operations**: Non-blocking API calls and video loading
* **Smart Caching**: Efficient use of browser localStorage
* **Debounced Operations**: Optimized user interactions and bulk operations

## 📁 Project Structure

```
multistreamnews.tv/
├── 🌐 Frontend/
│   └── index.html                      # Complete web application (single file)
│
├── 🔴 Backend Scanners/
│   ├── auto_refresh_scanner.py         # Main automated scanner (recommended)
│   ├── comprehensive_live_scanner.py   # Detailed analysis with viewer counts
│   ├── advanced_live_detector.py       # Test scanner for debugging
│   ├── manual_scan_live_streams.py     # Multi-endpoint scanning
│   ├── precise_live_scanner.py         # Pattern matching detection
│   └── enhanced_scan_live_streams.py   # Enhanced detection methods
│
├── 🛠️ Management/
│   ├── live_stream_manager.sh          # Shell script interface
│   └── requirements.txt                # Python dependencies
│
├── 📊 Data & Config/
│   ├── network_list.txt                # News network URLs (21 networks)
│   └── *.json                          # Generated scan results
│
└── 📚 Documentation/
    ├── README.md                       # This comprehensive guide
    ├── Scanners.md                     # Detailed scanner documentation  
    ├── prompt.md                       # Complete technical specifications
    ├── monetization_ideas.md           # Business development ideas
    └── LLM_notes.md                    # Development history and decisions
```

## 🎨 Customization

### Adding News Channels
Edit the `newsChannels` array in `index.html`:

```javascript
const newsChannels = [
    {
        label: 'Your Channel Name',
        url: 'https://www.youtube.com/watch?v=VIDEO_ID'
    },
    // Color palette automatically cycles through 12 colors
];
```

### Backend Network Configuration
Edit `network_list.txt` for scanner system:
```
Network Name	https://www.youtube.com/@channelname
```

## 🚀 Deployment

### Web Application
1. **GitHub Pages**: Already configured with CNAME for multistreamnews.tv
2. **Single File**: Upload `index.html` to any web server
3. **CDN**: All dependencies loaded via CDN (Tailwind, fonts)
4. **No Build Process**: Ready to deploy as-is

### Backend System
1. **Dependencies**: `pip3 install requests beautifulsoup4 schedule`
2. **Permissions**: `chmod +x live_stream_manager.sh`
3. **Automation**: Set up cron jobs or systemd services for monitoring

## 📈 Analytics & Monitoring

The platform includes comprehensive analytics:
- **User Interactions**: Video additions, button clicks, feature usage
- **Performance Metrics**: Load times, error rates, device compatibility
- **Backend Monitoring**: Live stream detection accuracy, scan performance
- **Error Monitoring**: Automatic error reporting and diagnostics

---

**Last Updated**: July 3, 2025  
**Version**: 2.2.0  
**Status**: Production Ready ✅

Enjoy your multistreaming experience! 🎬
