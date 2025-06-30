# MultiStreamNews.TV

https://www.multistreamnews.tv/

Welcome to MultiStreamNews.TV, a single-page web application designed for viewing multiple YouTube videos simultaneously. This tool is perfect for monitoring live news streams, following multiple events, or creating a custom video dashboard. Built with pure HTML, Tailwind CSS, and vanilla JavaScript, it's a lightweight and powerful solution for multistreaming.

## Features

### Core Video Management
* **Multiple Input Methods**: Add videos via drag-and-drop anywhere on the page, quick-add news channel buttons, or manual URL entry
* **Smart Drag & Drop**: Drag YouTube video links anywhere on the page to instantly add them to your video wall
* **Direct YouTube Video Support**: Paste YouTube video URLs (watch?v= format) into the input area to dynamically load them onto the page
* **Video Title Display**: Each video window automatically fetches and displays the actual video title in the title bar using YouTube's oEmbed API
* **Auto-Play & Mute**: All newly added videos automatically start playing and are muted by default to provide a seamless viewing experience
* **Smart Duplicate Prevention**: The application intelligently prevents duplicate URLs with clear user notifications
* **Intelligent Positioning**: New videos are placed at the top-left, or below maximized videos to maintain focus
* **Non-blocking Notifications**: Color-coded notification system provides clear feedback for all user actions:
  - Green: Success messages
  - Orange: Duplicate video warnings  
  - Red: Invalid video errors
  - Yellow: Mixed issues

### Quick Add News Channels
* **Built-in News Channels**: Curated collection of major news outlets with one-click access
* **One-Click News Access**: Colorful quick-add buttons for major news outlets including:
  - Sky News, NBC, ABC, CBS, BBC, CNN, Fox News, MSNBC, C-SPAN, PBS NewsHour
  - International: DW, France 24, Al Jazeera, Bloomberg, Reuters, Euronews
  - Canadian: CBC News, CTV News, Global News
  - Australian: ABC News Australia, 9 News Australia
  - Regional: 6abc, NASA, and more
* **Color-Coded Buttons**: Each news channel button has a unique color from a 12-color palette for easy visual identification
* **Expandable Interface**: The news channels section can be collapsed to save space when not needed

### Window Management
* **macOS-style Window Controls**: Each video player is housed in a clean, macOS-inspired window with familiar traffic light controls:
  - **Red Button (Close)**: Instantly removes the video window from the player
  - **Yellow Button (Minimize)**: Collapses the video content, leaving only the title bar visible to save space
  - **Green Button (Maximize)**: Expands the video to the full width of the container and moves it to the top of the grid for focused viewing
    - **Seamless Playback**: Video continues playing without interruption or restarting
    - **No Audio Disruption**: Maintains current playback position and audio state
    - **Smart Positioning**: When maximizing, moves to top; when restoring, maintains current position
* **Close All Videos**: Red button with confirmation modal to close all video windows at once
* **Responsive Grid Layout**: Video windows are arranged in a smart grid that automatically adjusts to your screen size:
  - **Mobile**: Single column with small side margins to prevent edge-to-edge display
  - **Tablet**: Multi-column layout with 350px minimum width per video
  - **Desktop**: Multi-column layout with 400px minimum width per video
  - **Large screens**: Additional spacing and margins for optimal viewing

### User Interface
* **Mobile-Optimized Design**: Streamlined interface for mobile devices:
  - Drag and drop zones hidden on mobile (not functional on touch devices)
  - Manual URL input hidden on mobile for cleaner interface
  - Focus on Quick Add News Channels for easy mobile interaction
* **Collapsible Sections**: News channels section can be shown or hidden with toggle buttons
* **Visual Feedback**: Smooth animations and hover effects provide clear user feedback
* **Confirmation Modals**: Important actions like "Close All Videos" require user confirmation
* **Non-blocking Notifications**: Toast-style notifications provide feedback without interrupting workflow
* **Clean Interface**: Input areas automatically close after successfully adding videos to keep the interface uncluttered
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
* **Bulk Actions**: Close all videos at once with confirmation modal to prevent accidental data loss

## How to Use

### Supporting the Project
The page includes a "Buy me a coffee" donation feature in the header:
1. **Access Donations**: Hover over the "Like this? Buy me a coffee" button to see PayPal and Venmo options
2. **Choose Payment Method**: Click either PayPal or Venmo to open a QR code modal
3. **Scan QR Code**: Use your mobile device to scan the displayed QR code for easy payment
4. **Close Modal**: Click the X button or outside the modal to close it

### Adding Videos - Multiple Methods

#### Method 1: Drag and Drop (Desktop/Tablet)
1. **Drag from anywhere**: Simply drag a YouTube video link from any browser window, email, or document
2. **Drop anywhere on the page**: The entire page acts as a drop zone - drag the link anywhere on the page
3. **Instant feedback**: Get immediate visual feedback and notifications about success, duplicates, or invalid links

#### Method 2: Quick Add News Channels (All Devices)
1. **Access News Channels**: The colorful quick-add buttons are visible by default at the top of the page
2. **Click to Add**: Simply click any news channel button to instantly add that stream to your video wall
3. **Collapse if Needed**: Use the "[Hide] Quick Add News Channels" button to minimize this section

#### Method 3: Manual URL Input (Desktop/Tablet)
1. **Show the Input**: Click the "[Show] Paste URLs" button to expand the input panel (hidden on mobile)
2. **Add Videos**: Paste one or more YouTube video URLs into the text area (one URL per line)
3. **Load Videos**: Click the "Load Video(s)" button - videos will appear in the grid and the input panel will automatically close

### Managing Your Video Wall
1. **Control Individual Videos**: Use the red, yellow, and green buttons on each video's title bar to close, minimize, or maximize windows
2. **Close All Videos**: Use the red "Close All Videos" button with confirmation modal to clear your entire video wall
3. **Interact with Videos**: Click directly on any video to use YouTube's native controls (play, pause, volume, etc.)
4. **Copy Your Setup**: Scroll to the bottom and click "Copy All URLs" to save your current video list for sharing or backup

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

## Technical Details

* **Frontend**: Built entirely with vanilla HTML, CSS, and JavaScript
* **Styling**: Utilizes **Tailwind CSS** (via CDN) for modern, responsive design with a custom color palette
* **Responsive Design**: Mobile-first approach with progressive enhancement:
  - CSS Grid with responsive breakpoints (640px, 768px, 1024px, 1280px)
  - Mobile-optimized interface with hidden drag zones and URL input (not practical on mobile)
  - Progressive multi-column layout for tablets and desktop
  - Maintains video aspect ratios across all device sizes
* **APIs**: Uses YouTube's oEmbed API to fetch video titles
* **Persistence**: Leverages browser `localStorage` to save and retrieve video URLs between sessions
* **Performance**: Lightweight single-file application with no external frameworks
* **Analytics**: Includes Google Analytics integration for usage tracking
* **User Experience**: Advanced notification system, confirmation modals, intelligent video positioning, and seamless maximize/restore without video interruption

## Installation & Setup

Simply download and open `index.html` in any modern web browser. No additional setup required!

## File Structure

```
multistreamnews.tv/
├── index.html              # Main web application (single file)
├── README.md              # This documentation
├── prompt.md              # Development prompt/specifications
└── Todolist.txt           # Development notes and tasks
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
