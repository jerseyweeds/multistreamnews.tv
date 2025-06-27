# Comprehensive Prompt: Recreate the Dynamic Multi-Video Player

## 1. High-Level Objective

Create a single-page interactive web application (SPA) named "Dynamic Multi-Video Player." The application allows users to dynamically add, manage, and view multiple embedded YouTube videos on a single page. It must feature a professional, modern design with a header, responsive video grid, macOS-style window controls, and persistent data storage.

## 2. Core Functional Requirements

### 2.1. Video Input and Loading

* **Collapsible Input Section:**
    * There must be a main toggle button with the text "Show Video Input."
    * Clicking this button should smoothly expand or collapse a dedicated input section. The button text must dynamically update to "Hide Video Input" when the section is open.
    * This section should be **collapsed by default** on page load.
* **URL Input:**
    * Inside the collapsible section, provide a `<textarea>` for users to paste multiple YouTube video URLs. Each URL should be on a new line.
    * A "Load Video(s)" button must be present to trigger the loading process.
* **Processing Logic:**
    * When "Load Video(s)" is clicked, the application must process each unique, valid YouTube URL from the input.
    * **Silent Duplicate Rejection:** If a URL is already present on the page, it must be silently ignored. Do not show an error message.
    * **Invalid URL Handling:** If a URL is not a valid YouTube link, display a custom modal alert.
    * **Auto-Close on Success:** After successfully adding at least one new video, the input section must automatically collapse.

### 2.2. Video Window Management

* **Dynamic Creation:** For every valid video added, a new video window must be dynamically created and embedded in the main content grid.
* **Playback:** New videos must automatically start playing and be **muted** by default.
* **macOS-style Controls:** Each video window must have a title bar with three clickable "traffic light" buttons on the left:
    * **Red Button (Close):** Removes the specific video window from the page.
    * **Yellow Button (Minimize):** Toggles the visibility of the video content, collapsing the window to show only the title bar.
    * **Green Button (Maximize):** Toggles a "maximized" state. When maximized, the window should span the full width of the grid container and be **moved to the top-most position** in the grid.

### 2.3. Data and Session Persistence

* **Local Storage:** All unique, valid YouTube video URLs that are currently loaded must be saved to the browser's `localStorage`.
* **Automatic Reload:** When the application is reloaded or revisited, it must automatically read the URLs from `localStorage` and display the corresponding videos in their last-known order.
* **State Updates:** Any action that changes the videos on the page (adding, closing, maximizing/moving to top) must trigger an update to `localStorage`.

### 2.4. URL List Display

* **Dynamic List:** At the bottom of the page, include a section titled "Loaded Videos." This section should display a list of all currently loaded video URLs.
* **Visibility:** This section should be hidden if no videos are loaded.
* **Copy Functionality:** A "Copy All URLs" button must be available to copy all listed URLs (one per line) to the user's clipboard. A temporary "Copied!" confirmation message should appear after a successful copy.

## 3. Visual Design & Layout (Styling)

### 3.1. Overall Theme & Header

* **Color Palette:** Use a dark, modern theme. The page background should be a dark gray (`#353E43`), and the main content container should be a slightly lighter shade (`#5A6F7B`).
* **Header Section:**
    * The page must start with a prominent header section that has a background image.
    * Use the following image URL for the background: `https://images.pexels.com/photos/1779487/pexels-photo-1779487.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2`
    * The image should have a dark overlay (`opacity-60`) to ensure text is readable.
    * Display the title "Dynamic Multi-Video Player" and a subtitle like "Your central hub for multistream news and content." centered over the header.

### 3.2. Video Grid Layout

* **CSS Grid:** The main container for the video windows (`#videoPlayersContainer`) must use a CSS Grid layout.
* **Responsive Columns:** The grid should be fully responsive, automatically adjusting the number of columns based on available space. Use `grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));`.
* **Video Window Sizing:**
    * Each video window should have a `max-height` of `720px`.
    * This `max-height` constraint must be removed when a video is in its "maximized" state.

### 3.3. macOS Window Styling

* **Title Bar:** The title bar should have a light gray linear-gradient background and a subtle bottom border/shadow to create a sense of depth.
* **Buttons:** The traffic light buttons should be small, circular, and colored appropriately (red, yellow, green) with hover effects.

## 4. Technical Specifications

* **File Structure:** The entire application must be contained within a **single HTML file**.
* **Frameworks/Libraries:**
    * Use **vanilla JavaScript** for all application logic. No frameworks like React, Vue, or Angular.
    * Use **Tailwind CSS** via CDN for all styling.
* **No Drag-and-Drop:** Do not implement any drag-and-drop functionality for reordering videos.
