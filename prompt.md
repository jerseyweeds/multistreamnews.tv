# Comprehensive Prompt: Build MultiStreamNews.TV from Scratch

## 1. High-Level Objective

Create a single-page interactive web application (SPA) named "MultiStreamNews.TV." The application allows users to dynamically add, manage, and view multiple embedded YouTube videos simultaneously on a single page. It must feature a professional, modern design with a video wall header, collapsible sections, quick-add news channel buttons, macOS-style window controls, video title display, and persistent data storage.

## 2. Core Functional Requirements

### 2.1. Header Design
* **Hero Section:** Create a prominent header with a background image using this URL: `https://images.pexels.com/photos/1779487/pexels-photo-1779487.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2`
* **Overlay:** Add a dark overlay (`bg-gray-900 opacity-60`) to ensure text readability
* **Title & Subtitle:** Display "MultiStreamNews.TV" as the main title and "Your central hub for multistream news and content." as the subtitle
* **Responsive Design:** Ensure the header looks good on all screen sizes

### 2.2. Quick Add News Channels Section

* **Collapsible Interface:**
  - Create a collapsible section with a purple toggle button labeled "Hide Quick Add News Channels" when expanded
  - When collapsed, the button should read "Show Quick Add News Channels"
  - Section should be expanded by default on page load
  - Smooth 0.4-second CSS transitions for expand/collapse animations

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
  - Blue toggle button with text "Hide Video Input" when expanded, "Show Video Input" when collapsed
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

### 2.8. User Interface & UX

* **Modal System:**
  - Custom modal for error messages and confirmations
  - Click outside modal or close button to dismiss
  - Auto-hide option for temporary messages

* **Color Scheme:**
  - Dark theme: body `#353E43`, main container `#5A6F7B`
  - Video windows: `#4a5e62` background
  - Use Tailwind CSS gray-800/700 for UI components

* **Responsive Design:**
  - Mobile-friendly interface with proper padding/margins
  - Collapsible sections to save space on smaller screens
  - Flexible grid that adapts to screen size

## 3. Technical Implementation Requirements

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

## 5. Expected User Workflow

1. **Page Load:** User sees header, expanded quick-add buttons, and expanded input section
2. **Quick Add:** User clicks colorful news channel buttons to instantly add streams
3. **Manual Add:** User pastes YouTube URLs in textarea and clicks "Load Video(s)"
4. **Video Management:** User controls videos with macOS-style window buttons
5. **Maximize for Audio:** User clicks green button to maximize and unmute a video
6. **Session Persistence:** User's video selection automatically saves and restores
7. **URL Management:** User can copy all current URLs for sharing or backup

## 6. Quality Standards

* **Clean Code:** Well-organized, commented JavaScript with logical separation
* **Modern CSS:** Efficient use of Tailwind utilities with custom CSS where needed
* **User Experience:** Intuitive interface with clear visual feedback
* **Performance:** Fast loading and smooth interactions
* **Reliability:** Robust error handling and graceful degradation

This comprehensive prompt should enable recreation of the complete MultiStreamNews.TV application with all current features and functionality.
