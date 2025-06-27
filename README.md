Dynamic Multi-Video Player
Welcome to the Dynamic Multi-Video Player, a single-page web application designed for viewing multiple YouTube video streams simultaneously. This tool is perfect for monitoring live news, following multiple events, or creating a custom video dashboard. Built with pure HTML, Tailwind CSS, and vanilla JavaScript, it's a lightweight and powerful solution for multistreaming.

Features
Dynamic Video Embedding: Paste one or more YouTube URLs into the input area to dynamically load them onto the page. Each video appears in its own manageable window.

Auto-Play & Mute: All newly added videos automatically start playing and are muted by default to provide a seamless viewing experience without auditory overload.

macOS-style Window Management: Each video player is housed in a clean, macOS-inspired window with familiar controls:

Red Button (Close): Instantly removes the video window from the player.

Yellow Button (Minimize): Collapses the video content, leaving only the title bar visible to save space.

Green Button (Maximize): Expands the video to the full width of the container and moves it to the top of the grid for focused viewing.

Persistent Sessions: Your layout is automatically saved to your browser's local storage. When you revisit the page, all your previously loaded videos will be right where you left them.

Responsive Grid Layout: The video windows are arranged in a smart grid that automatically adjusts to your screen size. It adds more columns as you widen your browser window for optimal use of space.

Collapsible Input: The URL input area can be shown or hidden with a single click, keeping the interface clean. It also automatically closes after you successfully add videos.

Silent Duplicate Handling: The application intelligently ignores duplicate URLs, preventing the same video from being added more than once.

URL List Management: A "Loaded Videos" section at the bottom dynamically lists all active video URLs and allows you to copy them all to your clipboard with a single click.

How to Use
Show the Input: Click the "Show Video Input" button to expand the input panel.

Add Videos: Paste one or more YouTube video URLs into the text area (one URL per line).

Load Videos: Click the "Load Video(s)" button. The videos will appear in the grid below, and the input panel will automatically close.

Manage Windows:

Use the red, yellow, and green buttons on each video's title bar to close, minimize, or maximize it.

Click directly on a video to use YouTube's native controls (play, pause, volume, etc.).

Copy URLs: To save your current list of videos, scroll to the bottom and click the "Copy All URLs" button.

Technical Details
Frontend: Built entirely with vanilla HTML, CSS, and JavaScript.

Styling: Utilizes Tailwind CSS (via CDN) for a modern, responsive, and utility-first design.

Persistence: Leverages browser localStorage to save and retrieve the list of video URLs between sessions.

No Dependencies: This is a pure, single-file application with no external frameworks or libraries beyond Tailwind CSS.

Enjoy your multistreaming experience!
