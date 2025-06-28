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
* **One-Click News Access**: A collapsible section with colorful quick-add buttons for major news outlets including:
  - Sky News, NBC, ABC, CBS, BBC, CNN, Fox News, MSNBC, C-SPAN
  - International: DW, France 24, Al Jazeera, Bloomberg, Reuters
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
* **Responsive Grid Layout**: Video windows are arranged in a smart grid that automatically adjusts to your screen size, adding more columns as you widen your browser window

### User Interface
* **Collapsible Sections**: Both the news channels and video input sections can be shown or hidden with toggle buttons
* **Clean Interface**: Input areas automatically close after successfully adding videos to keep the interface uncluttered  
* **Visual Feedback**: Smooth animations and hover effects provide clear user feedback
* **Mobile Responsive**: The interface adapts to different screen sizes and devices

### Data Persistence
* **Persistent Sessions**: Your video layout is automatically saved to your browser's local storage
* **Auto-Restore**: When you revisit the page, all your previously loaded videos will be restored exactly where you left them
* **URL Management**: A "Loaded Videos" section dynamically lists all active video URLs with clickable links
* **One-Click Copy**: Copy all currently loaded video URLs to your clipboard with a single button click

## How to Use

### Adding Videos via Quick Add Buttons
1. **Access News Channels**: The colorful quick-add buttons are visible by default at the top of the page
2. **Click to Add**: Simply click any news channel button to instantly add that stream to your video wall
3. **Collapse if Needed**: Use the "[Hide] Quick Add News Channels" button to minimize this section

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

## Technical Details

* **Frontend**: Built entirely with vanilla HTML, CSS, and JavaScript
* **Styling**: Utilizes **Tailwind CSS** (via CDN) for modern, responsive design with a custom color palette
* **APIs**: Uses YouTube's oEmbed API to fetch video titles
* **Persistence**: Leverages browser `localStorage` to save and retrieve video URLs between sessions
* **Performance**: Lightweight single-file application with no external frameworks
* **Analytics**: Includes Google Analytics integration for usage tracking

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
