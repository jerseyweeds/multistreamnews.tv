Dynamic Multi-Video PlayerThis is a simple yet powerful web application built with HTML, CSS (Tailwind CSS), and JavaScript that allows users to embed and manage multiple YouTube videos on a single page. It features a dynamic, responsive layout, drag-and-drop reordering, and local storage persistence for a seamless user experience.FeaturesDynamic Video Embedding: Paste one or more YouTube video URLs (separated by newlines) into the input area to add them to the page.Automatic Playback & Muting: Newly added videos automatically start playing and are muted by default.Drag-and-Drop Reordering: Easily rearrange the order of loaded video windows using a dedicated drag handle (⋮⋮⋮).Close Button: Each video window has a [Close] button to remove it from the page.Duplicate URL Prevention: The application prevents adding the same video URL more than once.Persistent Video List: All successfully loaded video URLs are saved to your browser's local storage and automatically reloaded when you revisit the page.Collapsible Input: The multi-URL input area can be toggled to show or hide, keeping the interface clean.Loaded URLs List: A section at the bottom of the page displays a list of all currently loaded video URLs, with a button to copy them to your clipboard.Responsive Design: The layout automatically adjusts between a single-column (for smaller screens) and a two-column grid (for wider screens, >600px).Custom Alerts: User-friendly modal alerts are used instead of native browser alert() for better integration.How to UseOpen the Application: Load the index.html file in your web browser.Add Videos:By default, the input area might be hidden. Click "Show Video Input" to expand it.Paste one or more YouTube video URLs into the textarea, with each URL on a new line.Click "Load Video(s)".Valid videos will be added to the page, starting playback muted.Invalid or duplicate URLs will trigger an alert.Rearrange Videos:For any loaded video, click and hold the ⋮⋮⋮ drag handle located at the top-left corner of its window.Drag the video to your desired position. A dashed blue placeholder will indicate where it will be inserted.Release the mouse/finger to drop the video into its new place.Close Videos: Click the [Close] button at the top-right of any video window to remove it.View & Copy URLs: Scroll to the bottom of the page to see a list of all currently loaded video URLs. You can click "Copy All URLs" to copy the list to your clipboard.Persistence: Close and reopen the page. Your last set of loaded videos should automatically reappear.Comprehensive Prompt to Recreate This ApplicationCreate a single-page web application using HTML, Tailwind CSS, and vanilla JavaScript.

The application should function as a dynamic multi-video player for YouTube videos, allowing users to embed, rearrange, and manage videos.

Here are the specific requirements:

**1. Overall Layout & Responsiveness:**
   - The page should have a clean, modern design using Tailwind CSS.
   - It must be fully responsive:
     - For browser widths up to 600px, it should display a single-column layout.
     - For browser widths greater than 600px, it should transition to a two-column grid layout for video windows.
   - The main content container should always utilize the full available width of the page, without fixed maximum widths (e.g., no `max-w-6xl` on the main container).
   - Use the 'Inter' font.

**2. Video Input Section:**
   - At the top of the page, there should be a `textarea` labeled "Paste YouTube Video URL(s) here, one per line".
   - Below the `textarea`, there should be a "Load Video(s)" button.
   - This entire input section (textarea + button) must be **collapsible**:
     - It should start in a collapsed (hidden) state when the page loads.
     - There must be a toggle button (e.g., "Show/Hide Video Input") above this section to expand/collapse it. The button text should dynamically reflect its current action (e.g., "Show Video Input" or "Hide Video Input").
   - When URLs are pasted into this `textarea` and the "Load Video(s)" button is clicked:
     - It should process each URL on a new line.
     - Invalid YouTube URLs should be skipped and noted with a custom alert.
     - Duplicate URLs (already loaded) should be skipped and noted with a custom alert.
     - Valid and unique URLs should then be added as new video windows.
     - The `textarea` should be cleared after processing.

**3. Dynamic Video Windows:**
   - Each successfully loaded video URL should create a new "video window".
   - These video windows should be dynamically added to a container below the main input section.
   - Each new video window should contain:
     - The embedded YouTube video (`<iframe>`).
     - A `[Close]` button positioned at the top-right of the video window.
     - A drag handle (represented by `⋮⋮⋮`) positioned at the top-left of the video window.
   - When a video window is added, the video within it must **automatically start playing and be muted**.
   - Video windows should adapt to the responsive layout (single or two columns).
   - Video windows that are empty input slots (before a URL is loaded into them) should *not* display the video iframe, the drag handle, or the close button. They should only show the input field and a "Load Video" button.

**4. Video Window Controls & Interactions:**
   - **Close Button:** Clicking the `[Close]` button on a video window should remove that specific window from the page.
   - **Drag-and-Drop Reordering:**
     - Users must be able to reorder the *loaded* video windows using drag-and-drop.
     - The drag action should be initiated by clicking and dragging the `⋮⋮⋮` icon (drag handle). The rest of the video window should not directly initiate the drag.
     - When dragging, the dragged video should become semi-transparent (`opacity: 0.5`), and a blue dashed border placeholder should appear at the potential drop location to guide the user.
     - Drag and drop should work symmetrically (moving up or down should behave consistently).

**5. Persistence (Local Storage):**
   - The list of all unique, loaded video URLs should be saved to the browser's local storage.
   - When the page is reopened, the application should automatically load the videos from the saved URLs.
   - This persistence should update whenever a video is added or removed.

**6. Loaded URLs List:**
   - At the bottom of the page, there should be a section titled "Loaded Videos".
   - This section should display a dynamic, clickable list of all currently unique, loaded video URLs.
   - This list should automatically hide if there are no loaded videos.
   - Include a "Copy All URLs" button next to this list. Clicking it should copy all the listed URLs (each on a new line) to the user's clipboard. A temporary "Copied!" confirmation message should appear after copying.

**7. Error Handling & User Feedback:**
   - Use a custom, styled modal alert system instead of the browser's native `alert()` for all messages (e.g., invalid URL, duplicate URL, copy confirmation).

**Technical Constraints:**
   - Use vanilla HTML, CSS (Tailwind CSS), and JavaScript. No external JavaScript frameworks (like React, Vue, Angular) are allowed.
   - YouTube video embedding should use the IFrame Player API for control (e.g., `autoplay=1&mute=1`).
   - The solution must be self-contained within a single HTML file.
