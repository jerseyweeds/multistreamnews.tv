# Comprehensive Prompt: Build MultiStreamNews.TV from Scratch

## 1. High-Level Objective

Create a comprehensive multi-streaming news platform consisting of:
1. **Single-page web application (SPA)** named "MultiStreamNews.TV" for viewing multiple YouTube videos simultaneously
2. **Automated live stream maintenance system** for managing a database of currently live YouTube news streams
3. **Professional deployment-ready package** with documentation and automation scripts

The web application features a modern, responsive design with video wall header, collapsible sections, quick-add news channel buttons, macOS-style window controls, video title display, and persistent data storage. The maintenance system ensures the live stream database stays current and accurate.

## 2. Core Functional Requirements

### PART A: WEB APPLICATION FEATURES

### 2.1. Header Design
* **Hero Section:** Create a prominent header with a background image using this URL: `https://images.pexels.com/photos/1779487/pexels-photo-1779487.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2`
* **Overlay:** Add a dark overlay (`bg-gray-900 opacity-60`) to ensure text readability
* **Title & Subtitle:** Display "MultiStreamNews.TV" as the main title and "Your central hub for multistream news and content." as the subtitle
* **Responsive Design:** Ensure the header looks good on all screen sizes

### 2.2. Quick Add News Channels Section

* **Collapsible Interface:**
  - Create a collapsible section with a purple toggle button labeled "[Hide] Quick Add News Channels" when expanded
  - When collapsed, the button should read "[Show] Quick Add News Channels"
  - Section should be expanded by default on page load
  - Smooth 0.4-second CSS transitions for expand/collapse animations

* **Dynamic Source Management:**
  - Include a small toggle button to switch between "Networks.txt" and "Built-in" sources
  - Primary method: Load channels from Networks.txt file (live database)
  - Backup method: Use built-in JavaScript array when Networks.txt unavailable
  - Graceful fallback with user notification when source switching fails
  - Smart retry logic that prevents unnecessary reload attempts

* **News Channel Buttons:**
  - Create an array of news channels with labels and YouTube video URLs
  - Include major outlets: Sky, NBC, ABC, CBS, CNN, Fox News, BBC, MSNBC, C-SPAN, DW, France 24, Bloomberg, Al Jazeera, Reuters, CNBC, Euronews, Global News, NASA, PBS NewsHour, CTV News, CBC News, Channel 4 News, 9 News Australia, ABC News Australia, Times Now, WION, GB News, TalkTV, 6abc
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

### 2.3. Manual Video Input Section

* **Collapsible Input Interface:**
  - Blue toggle button with text "[Hide] Video Input" when expanded, "[Show] Video Input" when collapsed
  - Section expanded by default on page load
  - Smooth CSS transitions matching the news channels section

* **URL Input:**
  - Textarea for users to paste multiple YouTube video URLs (one per line)
  - Placeholder text: "https://www.youtube.com/watch?v=VIDEO_ID"
  - Green "Load Video(s)" button to process the input
  - Label: "Paste YouTube Video URL(s) here, one per line:"

* **Processing Logic:**
  - Process each unique, valid YouTube URL from the textarea
  - Silent duplicate rejection (no error messages for duplicates)
  - Show modal alert for invalid YouTube URLs
  - Auto-collapse input section after successfully adding videos
  - Clear textarea after successful video addition

### 2.4. Video Title Integration

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
  - Use CSS Grid for video container: `grid-template-columns: repeat(auto-fit, minmax(400px, 1fr))`
  - 1.5rem gap between video windows
  - Videos have max-height of 720px (removed when maximized)
  - Maximized videos span full width: `grid-column: 1 / -1`

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

### PART B: LIVE STREAM MAINTENANCE SYSTEM

### 2.9. Networks.txt Database

* **File Structure:**
  - Tab-delimited text file with columns: Network, Channel, YouTube URL, Status, Viewers
  - Contains verified live YouTube streams from major English-speaking news networks
  - Example format:
    ```
    Network	Channel	YouTube URL	Status	Viewers
    Sky News	Sky News	https://www.youtube.com/watch?v=YDvsBbKfLPA	LIVE	3.9K watching
    NBC News NOW	NBC News	https://www.youtube.com/watch?v=DfwpCn9347w	LIVE	1.2K watching
    ```

* **Content Requirements:**
  - Include 15+ major news networks
  - Cover US, UK, Australian, Canadian, and international outlets
  - Only include streams that are currently live and broadcasting
  - Real-time viewer count information

### 2.10. Python Maintenance Script (maintain_networks.py)

* **Core Functionality:**
  - **Stream Verification:** Check if each YouTube URL is currently live
  - **Viewer Count Updates:** Extract and update current viewer counts
  - **Dead Stream Removal:** Remove streams that are no longer live
  - **New Stream Discovery:** Search known channels for new live streams
  - **Report Generation:** Provide detailed statistics on maintenance operations

* **Technical Requirements:**
  - Python 3.7+ compatibility
  - Async HTTP requests with proper error handling
  - Rate limiting to avoid YouTube blocking (2-second delays)
  - User-Agent spoofing for reliable access
  - Command-line arguments: `--check-only`, `--add-new`, `--verbose`

* **Stream Detection Logic:**
  - Parse YouTube video pages for live indicators
  - Extract viewer counts using multiple regex patterns
  - Handle various viewer count formats (1.2K, 1,234, etc.)
  - Graceful handling of network errors and API limitations

* **Known Channels Array:**
  - Predefined list of 20+ major news channels with handles
  - Include: Sky News, BBC, CNN, Fox News, NBC, ABC, CBS, Reuters, etc.
  - Support both @channel and channel ID formats
  - Easy configuration for adding new channels

### 2.11. Shell Automation Script (update_networks.sh)

* **Operation Modes:**
  - **Quick Mode:** Update existing streams only (default, fastest)
  - **Full Mode:** Update existing streams + search for new ones
  - **Check Mode:** Verify status without making file changes

* **Advanced Features:**
  - **Automatic Backups:** Create timestamped backups before changes
  - **Backup Rotation:** Keep 5 most recent backups, delete older ones
  - **Comprehensive Logging:** All operations logged to `networks_update.log`
  - **Log Rotation:** Automatic log file rotation when size exceeds 1MB
  - **Dependency Checking:** Verify Python version and install requirements
  - **Error Handling:** Graceful failure handling with detailed error messages

* **Command Examples:**
  ```bash
  ./update_networks.sh quick    # Quick update (default)
  ./update_networks.sh full     # Full update with discovery
  ./update_networks.sh check    # Check only, no changes
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

* **Color Scheme:**
  - Dark theme: body `#353E43`, main container `#5A6F7B`
  - Video windows: `#4a5e62` background
  - Use Tailwind CSS gray-800/700 for UI components

* **Responsive Design:**
  - Mobile-friendly interface with proper padding/margins
  - Collapsible sections to save space on smaller screens
  - Flexible grid that adapts to screen size

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

### 3.3. CSS Requirements

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
├── Networks.txt               # Live stream database
├── maintain_networks.py       # Python maintenance script  
├── update_networks.sh         # Shell automation script
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

### 4.3. Cross-Browser Compatibility
* Modern browser support (Chrome, Firefox, Safari, Edge)
* Fallbacks for older browsers where reasonable
* Responsive design for mobile devices

## 5. Expected User Workflows

### 5.1. Web Application Usage

1. **Page Load:** User sees header, expanded quick-add buttons, and expanded input section
2. **Quick Add:** User clicks colorful news channel buttons to instantly add streams
3. **Manual Add:** User pastes YouTube URLs in textarea and clicks "Load Video(s)"
4. **Video Management:** User controls videos with macOS-style window buttons
5. **Maximize for Audio:** User clicks green button to maximize and unmute a video
6. **Session Persistence:** User's video selection automatically saves and restores
7. **URL Management:** User can copy all current URLs for sharing or backup

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
* **User Experience:** Intuitive interface with clear visual feedback
* **Performance:** Fast loading and smooth interactions
* **Reliability:** Robust error handling and graceful degradation

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

This comprehensive system provides both immediate usability (web app) and long-term maintainability (automation system) for a complete professional news streaming platform.
