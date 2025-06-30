# Comprehensive Prompt: Build MultiStreamNews.TV from Scratch

## 1. High-Level Objective

Create a comprehensive single-page web application named "MultiStreamNews.TV" for viewing multiple YouTube videos simultaneously. This is a lightweight, user-friendly platform focused on providing an excellent multistreaming experience with built-in news channels, drag-and-drop functionality, and mobile-responsive design.

The web application features a modern, responsive design with video wall header, collapsible sections, quick-add news channel buttons, macOS-style window controls, video title display, drag-and-drop support, advanced notification system, and persistent data storage.

## 2. Core Functional Requirements

### PART A: WEB APPLICATION FEATURES

### 2.1. Header Design
* **Hero Section:** Create a prominent header with a background image using this URL: `https://images.pexels.com/photos/1779487/pexels-photo-1779487.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2`
* **Overlay:** Add a dark overlay (`bg-gray-900 opacity-60`) to ensure text readability
* **Title & Subtitle:** Display "MultiStreamNews.TV" as the main title and "Your central hub for multistream news and content." as the subtitle
* **Donation Feature:** Include a "Buy me a coffee" dropdown in the header with PayPal and Venmo options
  - Professional branded SVG icons for PayPal and Venmo
  - Hover-activated dropdown with seamless interaction (no gap between button and menu)
  - QR code modal displays when donation option is selected
  - Modal remains open until user closes it for easy mobile scanning
* **Responsive Design:** Ensure the header looks good on all screen sizes

### 2.2. Quick Add News Channels Section

* **Collapsible Interface:**
  - Create a collapsible section with a purple toggle button labeled "[Hide] Quick Add News Channels" when expanded
  - When collapsed, the button should read "[Show] Quick Add News Channels"
  - Section should be expanded by default on page load
  - Smooth 0.4-second CSS transitions for expand/collapse animations

* **Built-in News Channels:**
  - Use a built-in JavaScript array of news channels for instant loading and reliability
  - No external file dependencies - all channels embedded in the application
  - Include major outlets: Sky, NBC, ABC, CBS, CNN, Fox News, BBC, MSNBC, C-SPAN, DW, France 24, Bloomberg, Al Jazeera, Reuters, CNBC, Euronews, Global News, NASA, PBS NewsHour, CTV News, CBC News, Channel 4 News, 9 News Australia, ABC News Australia, Times Now, WION, GB News, TalkTV, 6abc

* **News Channel Buttons:**
  - Each button should have a unique color from a 12-color palette that cycles through:
    1. Blue (`bg-blue-600 hover:bg-blue-700`)
    2. Emerald (`bg-emerald-600 hover:bg-emerald-700`)
    3. Purple (`bg-purple-600 hover:bg-purple-700`)
    4. Orange (`bg-orange-600 hover:bg-orange-700`)
    5. Teal (`bg-teal-600 hover:bg-teal-700`)
    6. Red (`bg-red-600 hover:bg-red-700`)
    7. Indigo (`bg-indigo-600 hover:bg-indigo-700`)
    8. Amber (`bg-amber-600 hover:bg-amber-700`)
    9. Cyan (`bg-cyan-600 hover:bg-cyan-700`)
    10. Rose (`bg-rose-600 hover:bg-rose-700`)
    11. Lime (`bg-lime-600 hover:bg-lime-700`)
    12. Pink (`bg-pink-600 hover:bg-pink-700`)
  - Buttons should be flexbox wrapped with gap spacing
  - Clicking a button should instantly add that channel's video to the video wall

### 2.3. Drag and Drop System

* **Global Drop Zone:**
  - Make the entire page a drop zone for YouTube video links
  - Show visual feedback when dragging over the page
  - Display drag zone instruction: "Drag a video link anywhere on the page to add a new video window"
  - Hide drag zone areas on mobile devices (not functional on touch)

* **Drag Visual Feedback:**
  - Change cursor and add visual indicators when dragging
  - Highlight drop zones with color changes and animations
  - Provide clear success/error feedback after dropping

* **Smart Link Processing:**
  - Extract YouTube video IDs from various URL formats
  - Support both full YouTube URLs and youtu.be short links
  - Validate links before processing

### 2.4. Advanced Notification System

* **Non-blocking Toast Notifications:**
  - Position notifications in top-right corner of screen
  - Color-coded notification types:
    - Green: Success messages (video added successfully)
    - Orange: Duplicate warnings (video already exists)
    - Red: Error messages (invalid YouTube link)
    - Yellow: Mixed issues or general warnings
  - Auto-dismiss after 5 seconds with smooth fade animation
  - Click to dismiss manually

* **Specific User Feedback:**
  - "Video added successfully" for successful additions
  - "This video is already loaded in the video wall" for duplicates
  - "Not a valid YouTube video link" for invalid URLs
  - Clear, actionable messages that help users understand what happened

### 2.5. Manual Video Input Section (Desktop/Tablet Only)

* **Collapsible Input Interface:**
  - Blue toggle button with text "[Hide] Paste URLs" when expanded, "[Show] Paste URLs" when collapsed
  - Section hidden by default on page load
  - Hide entire section on mobile devices (`hidden md:block`)
  - Smooth CSS transitions matching the news channels section

* **URL Input:**
  - Textarea for users to paste multiple YouTube video URLs (one per line)
  - Placeholder text: "https://www.youtube.com/watch?v=VIDEO_ID"
  - Green "Load Video(s)" button to process the input
  - Label: "Paste YouTube Video URL(s) here, one per line:"

* **Processing Logic:**
  - Process each unique, valid YouTube URL from the textarea
  - Use notification system for user feedback
  - Auto-collapse input section after successfully adding videos
  - Clear textarea after successful video addition

### 2.6. Video Title Integration

* **Automatic Title Fetching:**
  - Use YouTube's oEmbed API to fetch real video titles: `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`
  - Make the `addVideo()` function async to handle title fetching
  - Display fetched titles in the video window title bars
  - Fallback to "YouTube Video" if title fetch fails
  - Handle API errors gracefully with try/catch

* **Title Display:**
  - Show video titles in the macOS-style title bar
  - Center the title text and truncate long titles with ellipsis
  - Add a `title` attribute for hover tooltips showing full titles
  - Use appropriate text styling (`text-gray-600 text-sm font-medium`)

### 2.5. Video Window Management

* **Dynamic Video Creation:**
  - Each valid video URL creates a new embedded video window
  - Videos auto-play and start muted by default
  - Use iframe embed format: `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&enablejsapi=1`

* **macOS-style Window Controls:**
  - **Red Button (Close):** Removes the video window and updates localStorage
  - **Yellow Button (Minimize):** Toggles video content visibility (title bar remains)
  - **Green Button (Maximize):** 
    - Toggles maximized state (spans full grid width)
    - **IMPORTANT:** When maximizing, unmute the video by reloading iframe without `&mute=1` parameter
    - When un-maximizing, re-mute the video by adding `&mute=1` back
    - Move maximized videos to top of grid container

* **Window Styling:**
  - macOS-inspired title bar with linear gradient background
  - Traffic light buttons with proper colors and hover effects
  - 16:9 aspect ratio video containers with responsive design
  - Rounded corners and shadow effects

### 2.6. Responsive Grid Layout

* **CSS Grid Implementation:**
  - Mobile-first responsive design with progressive enhancement
  - Mobile (default): Single column layout with small side margins (4px)
  - Small screens (640px+): Single column with increased margins (8px)
  - Medium screens (768px+): Multi-column grid with `minmax(350px, 1fr)`, 12px margins
  - Large screens (1024px+): Multi-column grid with `minmax(400px, 1fr)`, 16px margins
  - Extra large (1280px+): Maximum margins (20px) for optimal viewing
  - Responsive gap spacing: 1rem on mobile, scaling to 1.5rem on desktop
  - Videos have max-height of 720px (removed when maximized)
  - Maximized videos span full width: `grid-column: 1 / -1`

* **Mobile Optimization:**
  - Prevent horizontal overflow with `min-width: 0` and `max-width: 100%`
  - Maintain 16:9 aspect ratio across all screen sizes
  - Touch-friendly button spacing with responsive gaps
  - Container padding scales from 8px (mobile) to 32px (desktop)

### 2.7. Data Persistence & URL Management

* **localStorage Integration:**
  - Save all current video URLs to localStorage on any change
  - Auto-restore videos on page load from localStorage
  - Default to Sky and NBC videos if localStorage is empty

* **Loaded Videos Section:**
  - Display list of all currently loaded video URLs at bottom of page
  - Hide section when no videos are loaded
  - Clickable links that open videos in new tabs
  - "Copy All URLs" button with clipboard functionality
  - Visual confirmation ("Copied!") that fades after 2 seconds

* **Footer with Last Updated Timestamp:**
  - Display last updated date and time at bottom of page
  - Shows when the application was last committed/updated
  - Helps users know how current their version is
  - Format: "Last Updated: [Date] at [Time] [Timezone]"

### PART B: LIVE STREAM MAINTENANCE SYSTEM

### 2.9. Networks.txt Database

* **File Structure:**
  - Tab-delimited text file with columns: Network, Channel, YouTube URL, Status, Viewers, Duration
  - Contains verified live YouTube streams from major English-speaking news networks
  - Only includes streams that have been live for 24+ hours to ensure stability
  - Automatically deduplicated to prevent duplicate entries
  - **Optional Enhancement**: Available via toggle - built-in channels used by default
  - Example format:
    ```
    Network	Channel	YouTube URL	Status	Viewers	Duration
    Sky News	Sky News	https://www.youtube.com/watch?v=YDvsBbKfLPA	LIVE	3.9K watching	2d
    NBC News NOW	NBC News	https://www.youtube.com/watch?v=DfwpCn9347w	LIVE	1.2K watching	5h
    ```

* **Content Requirements:**
  - Include 15+ major news networks
  - Cover US, UK, Australian, Canadian, and international outlets
  - Only include streams that are currently live and broadcasting for 24+ hours
  - Real-time viewer count and duration information
  - Automatic deduplication to maintain database integrity
  - **Usage**: Secondary source accessed via toggle button for live stream data

### 2.9.1. network_list.txt Channel Database

* **Purpose:** Master list of news channel pages for automated stream discovery
* **File Structure:**
  - Tab-delimited text file with columns: Network Name, Channel Handle/ID
  - Contains main YouTube channel pages (not individual videos)
  - Used by maintenance scripts to discover live streams
  - Example format:
    ```
    Network Name	Channel Handle/ID
    Sky News	@SkyNews
    NBC News	@NBCNews
    BBC News	@BBCNews
    CNN	@CNN
    ```

* **Integration:**
  - Used by maintain_networks.py with --add-new or --refresh modes
  - Scripts automatically search these channels for live streams
  - Enables dynamic discovery of new streams without manual URL updates
  - Supports both @handle and channel ID formats

### 2.10. Python Maintenance Script (maintain_networks.py)

* **Core Functionality:**
  - **Stream Verification:** Check if each YouTube URL is currently live
  - **Viewer Count Updates:** Extract and update current viewer counts
  - **Duration Tracking:** Extract and track how long each stream has been live
  - **Quality Filtering:** Remove streams that have been live for less than 24 hours
  - **Dead Stream Removal:** Remove streams that are no longer live
  - **New Stream Discovery:** Search known channels from network_list.txt for new live streams
  - **Deduplication:** Ensure no duplicate URLs in the database
  - **Report Generation:** Provide detailed statistics on maintenance operations

* **Technical Requirements:**
  - Python 3.7+ compatibility
  - Async HTTP requests with proper error handling
  - Rate limiting to avoid YouTube blocking (2-second delays)
  - User-Agent spoofing for reliable access
  - Command-line arguments: `--check-only`, `--add-new`, `--verbose`, `--test-mode`, `--refresh`
  - Test mode: Process max 10 URLs per channel (for development/testing)
  - Production mode: Process max 50 URLs per channel (default)

* **Stream Detection Logic:**
  - Parse YouTube video pages for live indicators
  - Extract viewer counts using multiple regex patterns
  - Extract live duration from stream metadata
  - Handle various viewer count formats (1.2K, 1,234, etc.)
  - Parse duration formats (minutes, hours, days)
  - Graceful handling of network errors and API limitations

* **Network List Integration:**
  - Uses network_list.txt as source for channel discovery
  - Tab-delimited format: Network Name, Channel Handle/ID
  - Supports both @channel and channel ID formats
  - Easy configuration for adding new channels

### 2.11. Shell Automation Script (update_networks.sh)

* **Operation Modes:**
  - **Quick Mode:** Update existing streams only (default, fastest)
  - **Full Mode:** Update existing streams + search for new ones from network_list.txt
  - **Refresh Mode:** Complete rebuild of Networks.txt from network_list.txt
  - **Check Mode:** Verify status without making file changes
  - **Test Mode:** Use --test-mode flag to limit processing (10 URLs per channel for development)

* **Advanced Features:**
  - **Automatic Backups:** Create timestamped backups before changes
  - **Backup Rotation:** Keep 5 most recent backups, delete older ones
  - **Comprehensive Logging:** All operations logged to `networks_update.log`
  - **Log Rotation:** Automatic log file rotation when size exceeds 1MB
  - **Dependency Checking:** Verify Python version and install requirements
  - **Error Handling:** Graceful failure handling with detailed error messages
  - **Duration Tracking:** Extracts and tracks live stream duration
  - **Quality Control:** Filters out streams live for less than 24 hours

* **Command Examples:**
  ```bash
  ./update_networks.sh quick       # Quick update (default)
  ./update_networks.sh full        # Full update with discovery
  ./update_networks.sh refresh     # Complete rebuild
  ./update_networks.sh check       # Check only, no changes
  ./update_networks.sh quick --test-mode  # Test mode with limited processing
  ```

* **Cron Integration:**
  - Ready for crontab scheduling
  - Example cron entries provided in documentation
  - Supports both quick (frequent) and full (periodic) updates

### 2.8. User Interface & UX

* **Modal System:**
  - Custom modal for error messages and confirmations
  - Click outside modal or close button to dismiss
  - Auto-hide option with 5-second display duration for temporary messages
  - Improved user feedback for CORS/file access issues
  - QR code modal for donation system with PayPal and Venmo QR codes
  - Modal remains open until user closes it for easy mobile device scanning

* **Donation System:**
  - "Buy me a coffee" dropdown in header with hover activation
  - PayPal and Venmo options with professional branded SVG icons
  - Seamless dropdown interaction with no gap between button and menu
  - QR code modal displays payment-specific QR codes
  - Mobile-optimized for easy scanning and payment processing
  - Clean, professional styling that matches the overall design

* **Color Scheme:**
  - Dark theme: body `#353E43`, main container `#5A6F7B`
  - Video windows: `#4a5e62` background
  - Use Tailwind CSS gray-800/700 for UI components

* **Responsive Design:**
  - Mobile-friendly interface with responsive grid layout
  - Progressive enhancement from mobile-first single column to desktop multi-column
  - Responsive breakpoints at 640px, 768px, 1024px, and 1280px
  - Video windows maintain aspect ratio and prevent horizontal overflow
  - Touch-friendly button and control sizing
  - Appropriate margins and padding for different screen sizes
  - Collapsible sections to save space on smaller screens
  - Flexible grid that adapts to screen size with appropriate minimum widths

## 3. Technical Implementation Requirements

### PART A: WEB APPLICATION IMPLEMENTATION

### 3.1. File Structure & Dependencies
* **Single HTML File:** Entire application in one HTML file
* **Vanilla JavaScript:** No frameworks (React, Vue, etc.)
* **Tailwind CSS:** Use CDN version for all styling
* **Google Fonts:** Inter font family via CDN
* **Google Analytics:** Include GA4 tracking code

### 3.2. Code Organization

* **News Channels Configuration:**
```javascript
const newsChannels = [
    { label: 'Sky', url: 'https://www.youtube.com/watch?v=VIDEO_ID' },
    { label: 'NBC', url: 'https://www.youtube.com/watch?v=VIDEO_ID' },
    // ... more channels
];
```

* **Key Functions to Implement:**
  - `getYouTubeVideoId(url)` - Extract video ID from various YouTube URL formats
  - `createEmbedUrl(videoId, muted = true)` - Generate embed URL with conditional mute parameter
  - `getVideoTitle(videoId)` - Async function to fetch video title from oEmbed API
  - `addVideo(url, shouldSave = true)` - Async function to add videos with title fetching
  - `createVideoWindow(url, videoId, videoTitle)` - Generate video window HTML
  - `createNewsChannelButtons()` - Generate colored news channel buttons
  - `saveUrlsToStorage()` / `getUrlsFromStorage()` - localStorage management
  - `loadInitialVideos()` - Async function to restore saved videos on page load
  - `showQRModal(service)` - Display QR code modal for PayPal or Venmo donations
  - `closeQRModal()` - Close the QR code modal

### 3.3. CSS Requirements

* **Responsive Grid System:**
```css
#videoPlayersContainer {
    display: grid;
    gap: 1rem; /* Mobile: smaller gap */
    grid-template-columns: 1fr; /* Mobile: single column */
    padding: 0 4px; /* Mobile: small margins */
}

@media (min-width: 640px) {
    #videoPlayersContainer {
        gap: 1.25rem;
        padding: 0 8px;
    }
}

@media (min-width: 768px) {
    #videoPlayersContainer {
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 1.5rem;
        padding: 0 12px;
    }
}

@media (min-width: 1024px) {
    #videoPlayersContainer {
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        padding: 0 16px;
    }
}
```

* **Mobile-Optimized Video Windows:**
```css
.video-window {
    min-width: 0;
    width: 100%;
    max-width: 100%;
    overflow: hidden;
}

.video-content-wrapper iframe {
    width: 100%;
    height: 100%;
    max-width: 100%;
}
```

* **Collapsible Sections:**
```css
.section {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease-out;
}
.section.expanded {
    max-height: 800px; /* Adjust based on content */
    transition: max-height 0.4s ease-in;
}
```

* **macOS Window Styling:**
```css
.title-bar {
    background-image: linear-gradient(to bottom, #ececec, #dcdcdc);
    box-shadow: inset 0px 1px 0px rgba(255,255,255,0.7), 0px 1px 1px rgba(0,0,0,0.1);
}
```

* **Donation Dropdown Styling:**
```css
.coffee-dropdown {
    position: relative;
    display: inline-block;
}

.coffee-dropdown-content {
    display: none;
    position: absolute;
    right: 0;
    top: 100%;
    background-color: #374151;
    min-width: 200px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    border-radius: 0.5rem;
    z-index: 1000;
    /* No margin-top to eliminate gap */
}

.coffee-dropdown:hover .coffee-dropdown-content {
    display: block;
}
```

* **QR Modal Styling:**
```css
.qr-modal {
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
    padding: 1rem;
}
```

### 3.4. YouTube URL Support
* Support standard formats: `https://www.youtube.com/watch?v=VIDEO_ID`
* Support short formats: `https://youtu.be/VIDEO_ID`
* **Do NOT support:** Channel URLs, playlist URLs, or live stream channel URLs
* Extract 11-character video IDs using regex patterns

### 3.5. Error Handling
* Graceful handling of API failures (video title fetching)
* Invalid URL detection and user feedback
* Network error handling for embed failures
* Clipboard API error handling with fallback messages
* Smart CORS/file access restriction detection and user notification
* Improved error message duration (5 seconds) for better user experience
* Robust toggle logic with failure state tracking to prevent unnecessary retries

### PART B: MAINTENANCE SYSTEM IMPLEMENTATION

### 3.6. Python Dependencies & Requirements

* **Dependencies (requirements.txt):**
  ```
  requests>=2.28.0
  beautifulsoup4>=4.11.0
  lxml>=4.9.0
  ```

* **Python Script Structure:**
  - `NetworkMaintainer` class with modular methods
  - Session management with proper headers
  - Configurable constants (delays, user agents, etc.)
  - Comprehensive error logging and reporting

### 3.7. Key Python Functions

* **Core Methods:**
  - `extract_video_id(url)` - Extract YouTube video ID from various URL formats
  - `check_stream_status(url)` - Verify if stream is live and get viewer count
  - `load_networks()` / `save_networks()` - CSV/TSV file handling
  - `update_networks()` - Main update logic with statistics
  - `search_channel_for_live_streams()` - Discover new streams
  - `generate_report()` - Format and display operation results

* **Error Handling:**
  - Network timeouts and connection errors
  - YouTube page parsing failures
  - File I/O errors and permission issues
  - Rate limiting and service blocking detection

### 3.8. Shell Script Implementation

* **Script Structure:**
  - Bash script with proper error handling (`set -e`)
  - Color-coded output for better UX
  - Modular functions for each operation
  - Comprehensive logging with timestamps

* **Key Shell Functions:**
  - `check_python()` - Verify Python version and availability
  - `install_dependencies()` - Handle pip installation
  - `backup_networks()` - Create and manage backups
  - `run_maintenance()` - Execute Python script with appropriate arguments
  - `rotate_log()` - Manage log file sizes

### 3.9. File Structure & Organization

```
multistreamnews.tv/
├── index.html                 # Main web application
├── Networks.txt               # Live stream database (with Duration column)
├── network_list.txt           # Channel list for stream discovery
├── maintain_networks.py       # Python maintenance script with duration tracking
├── update_networks.sh         # Shell automation script with multiple modes
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── prompt.md                  # This comprehensive build guide
├── NETWORKS_README.md         # Maintenance system documentation
└── networks_update.log        # Auto-generated operation logs
```

## 4. Advanced Features & Polish

### 4.1. Performance Considerations
* Async/await for all API calls and video loading
* Efficient DOM manipulation
* Minimal re-renders and smooth animations

### 4.2. Accessibility
* Proper ARIA labels and semantic HTML
* Keyboard navigation support
* Screen reader friendly structure
* High contrast for text readability

### 4.3. Cross-Browser Compatibility & Mobile Support
* Modern browser support (Chrome, Firefox, Safari, Edge)
* Fallbacks for older browsers where reasonable
* Fully responsive design optimized for mobile devices:
  - Touch-friendly interface with appropriate button sizes
  - Single-column layout on mobile with proper margins
  - Progressive enhancement for tablets and desktop
  - Maintains video quality and functionality across all screen sizes
  - Prevents horizontal scrolling on any device
  - Optimized for both portrait and landscape orientations

## 5. Expected User Workflows

### 5.1. Web Application Usage

1. **Page Load:** User sees header with donation option, expanded quick-add buttons (built-in channels), and expanded input section
2. **Quick Add:** User clicks colorful news channel buttons to instantly add streams using built-in channels
3. **Toggle Source:** User can switch to Networks.txt via toggle button for live stream database
4. **Manual Add:** User pastes YouTube URLs in textarea and clicks "Load Video(s)"
5. **Video Management:** User controls videos with macOS-style window buttons
6. **Maximize for Audio:** User clicks green button to maximize and unmute a video
7. **Session Persistence:** User's video selection automatically saves and restores
8. **URL Management:** User can copy all current URLs for sharing or backup
9. **Support Project:** User can hover over "Buy me a coffee" and select PayPal or Venmo to see QR code for donations

### 5.2. Maintenance System Workflows

#### Developer/Administrator Workflow:
1. **Initial Setup:** Install Python dependencies with `pip3 install -r requirements.txt`
2. **Test Run:** Execute `./update_networks.sh check` to verify system functionality
3. **Regular Updates:** Set up cron job for automatic updates every 30 minutes
4. **Monitor Logs:** Check `networks_update.log` for any issues or statistics
5. **Manual Intervention:** Run `./update_networks.sh full` when major news events occur

#### Automated System Workflow:
1. **Scheduled Execution:** Cron triggers maintenance script at regular intervals
2. **Stream Verification:** Script checks each stream's live status and viewer count
3. **Database Update:** Updates Networks.txt with current information
4. **Backup Creation:** Creates timestamped backup before making changes
5. **New Stream Discovery:** Searches known channels for new live streams (full mode)
6. **Report Generation:** Logs statistics and any issues encountered
7. **Error Handling:** Gracefully handles network issues and service limitations

## 6. Quality Standards & Deliverables

### 6.1. Web Application Standards
* **Clean Code:** Well-organized, commented JavaScript with logical separation
* **Modern CSS:** Efficient use of Tailwind utilities with custom CSS where needed
* **User Experience:** Intuitive interface with clear visual feedback and seamless donation system
* **Performance:** Fast loading and smooth interactions
* **Reliability:** Robust error handling and graceful degradation
* **Mobile Optimization:** Fully responsive design with mobile-friendly donation QR codes

### 6.2. Maintenance System Standards
* **Production Ready:** Robust error handling, logging, and backup systems
* **Documentation:** Comprehensive README files with usage examples
* **Automation:** Ready for cron scheduling with minimal configuration
* **Monitoring:** Detailed logging and reporting for system health
* **Extensibility:** Easy to add new channels and modify configurations

### 6.3. Complete Deliverables Package

#### Core Application Files:
- `index.html` - Complete single-page web application
- `Networks.txt` - Initial database of 18+ verified live streams

#### Maintenance System:
- `maintain_networks.py` - Full-featured Python maintenance script
- `update_networks.sh` - Shell automation script with three operation modes
- `requirements.txt` - Python dependencies specification

#### Documentation:
- `README.md` - Complete user and deployment documentation
- `prompt.md` - This comprehensive build specification
- `NETWORKS_README.md` - Detailed maintenance system documentation

#### Features Integration:
- Automatic backup system with rotation
- Comprehensive logging with auto-rotation
- Cron-ready automation scripts
- Error handling and recovery
- Real-time stream verification
- New stream discovery
- Professional reporting and statistics
- User-friendly donation system with PayPal and Venmo QR codes
- Mobile-optimized interface with seamless donation experience

This comprehensive system provides both immediate usability (web app) and long-term maintainability (automation system) for a complete professional news streaming platform.
