# MultiStreamNews.TV

https://www.multistreamnews.tv/

Welcome to MultiStreamNews.TV, a single-page web application designed for viewing multiple YouTube videos simultaneously. This tool is perfect for monitoring live news streams, following multiple events, or creating a custom video dashboard. Built with pure HTML, Tailwind CSS, and vanilla JavaScript, it's a lightweight and powerful solution for multistreaming.

## Features

### Core Video Management
* **Direct YouTube Video Support**: Paste YouTube video URLs (watch?v= format) into the input area to dynamically load them onto the page. Each video appears in its own manageable window.
* **Video Title Display**: Each video window automatically fetches and displays the actual video title in the title bar using YouTube's oEmbed API.
* **Auto-Play & Mute**: All newly added videos automatically start playing and are muted by default to provide a seamless viewing experience without auditory overload.
* **Smart Duplicate Prevention**: The application intelligently ignores duplicate URLs, preventing the same video from being added more than once.

### Quick Add News Channels
* **Dynamic Source Management**: Choose between Built-in (default) or Networks.txt (live database) with a toggle button
* **One-Click News Access**: A collapsible section with colorful quick-add buttons for major news outlets including:
  - Sky News, NBC, ABC, CBS, BBC, CNN, Fox News, MSNBC, C-SPAN
  - International: DW, France 24, Al Jazeera, Bloomberg, Reuters
  - Canadian: CBC News, CTV News, Global News
  - Australian: ABC News Australia, 9 News Australia
  - Regional: 6abc, NASA, and more
* **Color-Coded Buttons**: Each news channel button has a unique color from a 12-color palette for easy visual identification
* **Expandable Interface**: The news channels section can be collapsed to save space when not needed
* **Reliable Default**: Uses built-in channels for instant loading, with Networks.txt available via toggle
* **Smart Fallback**: Networks.txt loads in background and is available when toggle is switched

### Window Management
* **macOS-style Window Controls**: Each video player is housed in a clean, macOS-inspired window with familiar traffic light controls:
  - **Red Button (Close)**: Instantly removes the video window from the player
  - **Yellow Button (Minimize)**: Collapses the video content, leaving only the title bar visible to save space
  - **Green Button (Maximize)**: Expands the video to the full width of the container and moves it to the top of the grid for focused viewing
* **Responsive Grid Layout**: Video windows are arranged in a smart grid that automatically adjusts to your screen size:
  - **Mobile**: Single column with small side margins to prevent edge-to-edge display
  - **Tablet**: Multi-column layout with 350px minimum width per video
  - **Desktop**: Multi-column layout with 400px minimum width per video
  - **Large screens**: Additional spacing and margins for optimal viewing

### User Interface
* **Collapsible Sections**: Both the news channels and video input sections can be shown or hidden with toggle buttons
* **Clean Interface**: Input areas automatically close after successfully adding videos to keep the interface uncluttered  
* **Visual Feedback**: Smooth animations and hover effects provide clear user feedback
* **Error Handling**: User-friendly error messages with 5-second auto-dismiss for temporary notifications
* **Mobile Responsive**: Fully responsive design with mobile-optimized video windows
  - Single-column layout on mobile devices with appropriate side margins (4px)
  - Progressive multi-column grid on larger screens (350px minimum on tablets, 400px on desktop)
  - Responsive breakpoints at 640px, 768px, 1024px, and 1280px screen widths
  - Video windows maintain 16:9 aspect ratio at all screen sizes
* **Source Toggle**: Switch between Built-in (default) and Networks.txt sources with a small toggle button
* **Donation Support**: "Buy me a coffee" dropdown in the header with PayPal and Venmo options
  - PayPal and Venmo branded SVG icons for professional appearance
  - QR code modal displays when donation option is selected
  - Modal remains open until user closes it for easy scanning
  - Seamless hover-to-select dropdown with no gap issues

### Data Persistence
* **Persistent Sessions**: Your video layout is automatically saved to your browser's local storage
* **Auto-Restore**: When you revisit the page, all your previously loaded videos will be restored exactly where you left them
* **URL Management**: A "Loaded Videos" section dynamically lists all active video URLs with clickable links
* **One-Click Copy**: Copy all currently loaded video URLs to your clipboard with a single button click

## How to Use

### Supporting the Project
The page includes a "Buy me a coffee" donation feature in the header:
1. **Access Donations**: Hover over the "Like this? Buy me a coffee" button to see PayPal and Venmo options
2. **Choose Payment Method**: Click either PayPal or Venmo to open a QR code modal
3. **Scan QR Code**: Use your mobile device to scan the displayed QR code for easy payment
4. **Close Modal**: Click the X button or outside the modal to close it

### Adding Videos via Quick Add Buttons
1. **Access News Channels**: The colorful quick-add buttons are visible by default at the top of the page
2. **Choose Source**: Use the small toggle button to switch between "Built-in" (default) and "Networks.txt" (live database)
3. **Click to Add**: Simply click any news channel button to instantly add that stream to your video wall
4. **Collapse if Needed**: Use the "[Hide] Quick Add News Channels" button to minimize this section

### Adding Videos via URL Input
1. **Show the Input**: Click the "[Show] Video Input" button to expand the input panel
2. **Add Videos**: Paste one or more YouTube video URLs into the text area (one URL per line)
3. **Load Videos**: Click the "Load Video(s)" button - videos will appear in the grid and the input panel will automatically close

### Managing Your Video Wall
4. **Control Individual Videos**: Use the red, yellow, and green buttons on each video's title bar to close, minimize, or maximize windows
5. **Interact with Videos**: Click directly on any video to use YouTube's native controls (play, pause, volume, etc.)
6. **Copy Your Setup**: Scroll to the bottom and click "Copy All URLs" to save your current video list for sharing or backup

## Supported URL Formats

The application supports standard YouTube video URLs:
* **Full URLs**: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
* **Short URLs**: `https://youtu.be/dQw4w9WgXcQ`

**Note**: Channel URLs, playlist URLs, and live stream channel URLs are not supported. Please use direct video URLs only.

## News Channels Included

The quick-add section includes buttons for these major news outlets:
- **US Networks**: NBC, ABC, CBS, CNN, Fox News, MSNBC, C-SPAN, PBS NewsHour, CNBC
- **UK/Europe**: Sky News, BBC, Channel 4 News, DW, France 24, Euronews, GB News, TalkTV
- **International**: Al Jazeera, Reuters, Bloomberg, Times Now, WION
- **Canadian**: CBC News, CTV News, Global News
- **Australian**: ABC News Australia, 9 News Australia
- **Regional/Other**: 6abc Philadelphia, NASA

## Live Stream Database

MultiStreamNews.TV includes an automated system for maintaining a database of currently live YouTube news streams:

### Networks.txt File
* **Live Stream Database**: `Networks.txt` contains verified live YouTube streams from major English-speaking news networks
* **Optional Enhancement**: Available via toggle button - built-in channels are used by default for reliability
* **Real-time Updates**: Stream status, viewer counts, and live duration are automatically verified and updated
* **Duration Tracking**: Includes live duration column (e.g., "2d", "5h", "45m") for each stream
* **Quality Filtering**: Only includes streams that have been live for 24+ hours to ensure stability
* **18+ Major Networks**: Includes Sky News, NBC, ABC, CNN, Fox News, BBC, Al Jazeera, Bloomberg, DW News, and more
* **Tab-delimited Format**: Easy to read and integrate with other applications with columns: Network, Channel, YouTube URL, Status, Viewers, Duration
* **Deduplication**: Automatically removes duplicate streams to maintain database integrity

### Maintenance System
* **Automated Verification**: Python script (`maintain_networks.py`) checks stream status, updates viewer counts, and tracks live duration
* **Smart Discovery**: Automatically finds new live streams from known news channels using `network_list.txt`
* **Quality Filtering**: Removes streams live for less than 24 hours and filters out offline streams
* **Deduplication**: Ensures no duplicate streams in the database
* **Test & Production Modes**: Configurable URL limits for testing (10 URLs) vs production (50 URLs per channel)
* **Backup System**: Creates timestamped backups before making changes
* **Comprehensive Logging**: Detailed logs of all maintenance operations

### Automation Scripts
* **`update_networks.sh`**: Shell script for easy automation with multiple modes:
  - **Quick**: Update existing streams only (recommended for frequent runs)
  - **Full**: Update existing streams and search for new ones from network_list.txt
  - **Refresh**: Complete rebuild of Networks.txt from network_list.txt
  - **Check**: Verify status without making changes
  - **Test Mode**: Use `--test-mode` flag to limit processing for development/testing
* **Network List Management**: Uses `network_list.txt` for discovering live streams from known channel pages
* **Cron Integration**: Ready for scheduling with crontab for automatic updates
* **Error Handling**: Robust error handling and rate limiting to avoid service blocks
* **Duration Tracking**: Extracts and tracks how long each stream has been live
* **Quality Control**: Automatically filters out short-duration streams (< 24 hours)

### Usage
```bash
# Quick update (recommended for regular use)
./update_networks.sh quick

# Full update with new stream discovery
./update_networks.sh full

# Complete rebuild from network_list.txt
./update_networks.sh refresh

# Check status without making changes
./update_networks.sh check

# Test mode with limited processing (for development)
./update_networks.sh quick --test-mode
./update_networks.sh full --test-mode
```

For detailed documentation, see `NETWORKS_README.md`.

## Technical Details

* **Frontend**: Built entirely with vanilla HTML, CSS, and JavaScript
* **Styling**: Utilizes **Tailwind CSS** (via CDN) for modern, responsive design with a custom color palette
* **Responsive Design**: Mobile-first approach with progressive enhancement:
  - CSS Grid with responsive breakpoints (640px, 768px, 1024px, 1280px)
  - Mobile-optimized single-column layout with appropriate margins
  - Progressive multi-column layout for tablets and desktop
  - Maintains video aspect ratios across all device sizes
* **APIs**: Uses YouTube's oEmbed API to fetch video titles
* **Persistence**: Leverages browser `localStorage` to save and retrieve video URLs between sessions
* **Performance**: Lightweight single-file application with no external frameworks
* **Analytics**: Includes Google Analytics integration for usage tracking
* **Stream Maintenance**: Python-based automation system for maintaining live stream database
* **User Support**: Integrated donation system with PayPal and Venmo QR code modals

## Installation & Setup

### Basic Usage (Web App Only)
Simply download and open `index.html` in any modern web browser. No additional setup required!

### Advanced Setup (With Stream Maintenance)
For automated live stream database maintenance:

1. **Install Python Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Test the Maintenance System**:
   ```bash
   # Check current stream status
   ./update_networks.sh check
   
   # Update existing streams
   ./update_networks.sh quick
   ```

3. **Set Up Automation** (Optional):
   ```bash
   # Edit crontab for automatic updates
   crontab -e
   
   # Add this line for updates every 30 minutes:
   */30 * * * * cd /path/to/multistreamnews.tv && ./update_networks.sh quick >> networks_update.log 2>&1
   ```

## File Structure

```
multistreamnews.tv/
├── index.html              # Main web application
├── Networks.txt            # Live stream database (tab-delimited with Duration column)
├── network_list.txt        # Channel list for stream discovery (tab-delimited)
├── maintain_networks.py    # Python maintenance script with duration tracking
├── update_networks.sh      # Shell automation script with multiple modes
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
├── prompt.md              # Development prompt/specifications
├── NETWORKS_README.md     # Detailed maintenance system docs
└── networks_update.log    # Maintenance operation logs (created automatically)
```

## Customization

To add or modify news channels, simply edit the `newsChannels` array in the JavaScript section:

```javascript
const newsChannels = [
    {
        label: 'Your Channel Name',
        url: 'https://www.youtube.com/watch?v=VIDEO_ID'
    },
    // Add more channels here...
];
```

The color palette will automatically cycle through the available colors for new channels.

Enjoy your multistreaming experience!
