# Dynamic Multi-Video Player

This is a simple yet powerful web application built with HTML, CSS (Tailwind CSS), and JavaScript that allows users to embed and manage multiple YouTube videos on a single page. It features a dynamic, responsive layout, drag-and-drop reordering, and local storage persistence for a seamless user experience.

## Features

* **Dynamic Video Embedding:** Paste one or more YouTube video URLs (separated by newlines) into the input area to add them to the page.

* **Automatic Playback & Muting:** Newly added videos automatically start playing and are muted by default.

* **Drag-and-Drop Reordering:** Easily rearrange the order of loaded video windows using a dedicated drag handle (⋮⋮⋮).

* **Close Button:** Each video window has a `[Close]` button to remove it from the page.

* **Duplicate URL Prevention:** The application prevents adding the same video URL more than once.

* **Persistent Video List:** All successfully loaded video URLs are saved to your browser's local storage and automatically reloaded when you revisit the page.

* **Collapsible Input:** The multi-URL input area can be toggled to show or hide, keeping the interface clean.

* **Loaded URLs List:** A section at the bottom of the page displays a list of all currently loaded video URLs, with a button to copy them to your clipboard.

* **Responsive Design:** The layout automatically adjusts between a single-column (for smaller screens) and a two-column grid (for wider screens, >600px).

* **Custom Alerts:** User-friendly modal alerts are used instead of native browser `alert()` for better integration.

## How to Use

1. **Open the Application:** Load the `index.html` file in your web browser.

2. **Add Videos:**

   * By default, the input area might be hidden. Click "Show Video Input" to expand it.

   * Paste one or more YouTube video URLs into the `textarea`, with each URL on a new line.

   * Click "Load Video(s)".

   * Valid videos will be added to the page, starting playback muted.

   * Invalid or duplicate URLs will trigger an alert.

3. **Rearrange Videos:**

   * For any loaded video, click and hold the `⋮⋮⋮` drag handle located at the top-left corner of its window.

   * Drag the video to your desired position. A dashed blue placeholder will indicate where it will be inserted.

   * Release the mouse/finger to drop the video into its new place.

4. **Close Videos:** Click the `[Close]` button at the top-right of any video window to remove it.

5. **View & Copy URLs:** Scroll to the bottom of the page to see a list of all currently loaded video URLs. You can click "Copy All URLs" to copy the list to your clipboard.

6. **Persistence:** Close and reopen the page. Your last set of loaded videos should automatically reappear.

## Comprehensive Prompt to Recreate This Application

Act as an expert frontend developer, data analyst, UI/UX designer, and **information architect**. Your task is to analyze a provided **Source Report** (from any domain) and generate a complete, single HTML file for a **single-page interactive web application (SPA)** that makes its content easily consumable and explorable. Your **response** and the **SPA** should be in the **Source Report** language.

**Objective:** The SPA must effectively translate the **Source Report** into an intuitive interactive experience. It should allow users to **easily explore, interact with, understand, and synthesize** all key information – quantitative data, qualitative insights, analyses, findings, text, etc. The **primary goal is user understanding and ease of navigation**, achieved through a well-designed interactive structure and dynamic presentation within a single page. **The application structure does NOT need to mirror the report's structure; instead, you should design the most logical and user-friendly structure** based on the content and potential user interactions.

**Content Focus:**
The application will present and allow interaction with the full spectrum of information found in the **specific Source Report provided**. This could include (depending on the report):

* Quantitative Data (Stats, metrics, results, financials, projections)

* Qualitative Insights (Findings, observations, themes, commentary, case studies)

* Analysis & Structure (Comparisons, trends, correlations, frameworks, processes, methodologies)

* Textual Content (Summaries, background, explanations, conclusions, recommendations)

* Interactive Elements (Filters, selectors, sliders, toggles, clickable details, search/highlight, drill-downs)

* ***CRITICAL: The application must capture the essence and key details of the Source Report, presenting them in the most effective interactive format, regardless of the report's original layout.***

**Technical Requirements:**

1. **SPA Structure:** Single HTML page. Use Tailwind CSS for a responsive layout. **Analyze the report's content and design an optimal information architecture for the SPA.** This might involve thematic sections, a dashboard layout, task-oriented views, or other structures that best facilitate user exploration and understanding. Implement this structure using appropriate HTML semantics and Tailwind layouts (e.g., grid, flexbox). Include interactive UI components (buttons, dropdowns, etc.) integrated logically within the designed structure.

   * **Chart Containers:** For charts, ensure `<canvas>` elements are wrapped in a `<div>` (e.g., `<div class="chart-container">...</div>`). This container `div` **must** act as a responsive boundary, managing the chart's size and integration within the parent Tailwind layout (e.g., a grid cell or flex item). The parent element containing the chart container might use Tailwind's flexbox or grid utilities (e.g., `flex flex-col`) to properly allocate space for the chart container, especially if the chart container is intended to fill available vertical space up to its defined `max-height`.

2. **JavaScript Logic (Mandatory Use):**

   * **Core Interaction Handling:** Vanilla JS for event listeners, input handling, data processing/filtering, and dynamic updates of **both visualizations and textual content blocks** based on user actions and application state, supporting the designed interactive flow.

   * **Functional Navigation:** Implement functional navigation code for all navigation and sub-navigation elements.

   * **State Management:** Simple JS variables/objects for current state.

   * **Data Storage:** Store base data (numeric and textual snippets) in JS arrays/objects.

3. **JavaScript Libraries (Mandatory Use):**

   * **Chart.js:** For standard dynamic charts. Ensure responsiveness (including setting `maintainAspectRatio: false` in chart options so they respect their container's dimensions), Canvas rendering, label wrapping (16-char logic), required tooltip config. Dynamically updatable. Load via CDN.

   * **Plotly.js:** Optional, for sophisticated interactive plots (Canvas/WebGL only). Dynamically updatable. AVOID SVG. Load via CDN.

   * **--- NO MERMAID JS ---**

4. **Graphics:**

   * **--- NO SVG ---**

   * Use **Canvas** (Chart.js/Plotly.js) for charts.

   * Use **structured HTML/CSS with Tailwind**, **Unicode characters/icons**, or **Canvas** for icons, diagrams, visual elements. Avoid raster images.

**Styling Requirements:**

1. **CSS Framework:** **Tailwind CSS**, loaded via CDN. Responsive layout.

   * **Chart Container Styling:** Chart containers (the `div` wrapping a `<canvas>`) are crucial for managing chart dimensions and preventing layout issues. They **must** be styled to:

     * **Occupy Full Parent Width:** Take `100%` of the width of their parent layout column (e.g., using Tailwind `w-full`).

     * **Have a Maximum Width:** Include a `max-width` (e.g., Tailwind `max-w-xl`, `max-w-2xl`, or an explicit pixel value like `max-width: 600px` via embedded CSS for a class like `.chart-container`) to prevent charts from becoming excessively wide on larger screens and to maintain readability.

     * **Be Centered Horizontally:** If the `max-width` is less than the parent column's width, the chart container should be centered horizontally (e.g., Tailwind `mx-auto`).

     * **Have Controlled Height:** Possess a defined responsive height (e.g., Tailwind `h-[40vh]` or `h-96`) and a maximum height (e.g., `max-h-[400px]` or `max-h-96`) to prevent vertical overflow. Consider adjusting these heights for different screen sizes (e.g., smaller heights on mobile using Tailwind's responsive prefixes like `sm:h-80 md:h-96`).

     * **Prevent Overflow:** The container itself should effectively constrain the chart canvas, preventing the canvas from overflowing its bounds (both horizontally and vertically). `position: relative;` on the container is also recommended for child element positioning (like tooltips).

     * **Implementation:** Achieve this primarily with Tailwind classes. If highly specific or responsive values are needed beyond standard Tailwind, use a minimal embedded `<style>` tag for a dedicated chart container class (e.g., `.chart-container`). For example: `<style>.chart-container { position: relative; width: 100%; max-width: 600px; margin-left: auto; margin-right: auto; height: 300px; /* Base height, adjust with media queries or use Tailwind for responsive heights */ max-height: 400px; } @media (min-width: 768px) { .chart-container { height: 350px; } }</style>`. Ensure any embedded CSS is minimal and directly supports these chart container requirements.

2. **Layout & Spacing:**

   * Clean, professional, and visually appealing.

   * Use a container that centers content with appropriate horizontal padding that adjusts for screen size.

   * Utilize flexbox and grid for layout structures (e.g., for navigation, about section columns, portfolio gallery).

**Overall Design and Interactivity Requirements:**

1. **High-Quality Design:** Employ clean aesthetics, appropriate typography, and engaging visual elements (icons, color schemes, layout) to make the information accessible, appealing, and aligned with the tone of the \[Document/Report Topic\]. The background must always be a light color.

2. **Data Clarity:** Ensure that all data visualizations (charts, maps, etc.) are clearly labeled, easy to understand, and accurately reflect the data points and information from the source document. Add brief explanatory text for context where needed.

3. **Accessibility & Responsiveness:** The application should be designed with accessibility in mind and be fully responsive, providing an excellent user experience across various devices (desktop, tablet, mobile). Prevent horizontal scrolling on all devices.

4. **Engagement:** When appropriate, incorporate elements that encourage users to click, hover, explore, and interact with the information, fostering active learning rather than passive consumption. The goal is to make the story of the \[Document/Report Topic\] unfold interactively. Don't overuse them

5. **"Wow" Factor/Impact:** Where appropriate, incorporate innovative visualization techniques, smooth transitions, or unique interactive elements to make the experience memorable, impactful, and effective in conveying the core messages of the \[Document/Report Topic\]. The aim is not just to present data and information, but to teach and engage the user effectively through interactive storytelling.

**Inspiration:**
Adapt ideas for layout, content presentation, and interactivity, focusing on creating the best user experience for the specific report content:

* `colour combinations`: The app's color scheme should be minimalistic and create a sense of calm harmony. Think a palette grounded in warm neutrals as the main background. Then, find complimentary colors for the rest of the components and for secondary areas. Accent colors should be very subtle, used sparingly for calls to action or highlights. The colors must work together to feel supportive and integrated. Keep the total number of colors used to a minimum.

* `The Impact of Data Visualization` / `INFOGRAPHIC of INFOGRAPHICS`: Use for ideas on grouping related text and visuals, sectioning content logically (but not necessarily mirroring the report), and mixing content types.

* **Modern Web Dashboards & Interactive Reports:** Inspire UI/UX patterns for filters, navigation, and dynamic content presentation that support an optimal, potentially non-linear, exploration path.

* `Infographic Charts - How to Choose`: Guide for base visualization selection (NO SVG, add interaction).

**Interactive Element & Visualization Selection Guide (Domain-Agnostic, NO SVG, Interaction-Focused):**

* **Goal: Inform:** Dynamic Stats, Key Findings Lists, Simple Proportions (Donut/Pie - Chart.js/Canvas), Progress Indicators (HTML/CSS/Canvas), Contextual Text Blocks (JS show/hide/update).

* **Goal: Compare:** Interactive Bar/Stacked Bar/Bubble Charts (Chart.js/Canvas), Comparison Tables (HTML + JS filter/sort), Side-by-Side Layouts (Grid/Flex + JS updates).

* **Goal: Change:** Interactive Line/Area Charts (Chart.js/Canvas + time controls), Timelines/Process Flows (HTML/CSS/Tailwind + JS highlight). Trend Description Text (JS update).

* **Goal: Organize:** Interactive Lists/Tables (HTML + JS filter/sort), Diagrams (Flowcharts, Org Charts, Concept Maps - **HTML/CSS/Tailwind + JS interaction**), Matrix Layouts (HTML Grid/Flex + JS detail display), Hierarchies (Styled HTML + limited JS interaction). **NO SVG/Mermaid.**

* **Goal: Relationships:** Interactive Scatter/Distribution Plots (Chart.js/Plotly Canvas/WebGL), Simple Network Maps (HTML/CSS/JS - limited), Cross-filtering (JS connecting multiple elements).

**Output Constraint:**

* **Single HTML file ONLY.**

* **NO explanatory text outside HTML tags.**

* **CRITICAL: NO HTML comments, CSS comments, or JavaScript comments, *except* for the required placeholders below.**

* **Placeholder Comments Required:**

  * `<!-- Chosen Palette: [Name of selected palette] -->`

  * `<!-- Application Structure Plan: [Summary of the DESIGNED interactive structure (e.g., thematic sections, dashboard approach), key interactions, and user flow, explaining WHY this structure was chosen for usability based on the report's content.] -->`

  * `<!-- Visualization & Content Choices: [Summary: Report Info -> Goal -> Viz/Presentation Method -> Interaction -> Justification -> Library/Method - Confirming NO SVG/Mermaid, supporting the DESIGNED structure.] -->`

  * `<!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->`

**Source Material Integration (CRITICAL PROCESS):**

1. **Analyze Source Report:** Deeply understand the report's content, goals, data, insights, and target audience. Identify the core message and key pieces of information.

2. **Design Application Structure & Flow:** **Synthesize the report's content and devise the most effective interactive structure for the SPA.** Consider user tasks, logical groupings of information, and intuitive navigation. This structure might be thematic, functional, or dashboard-like, prioritizing ease of consumption over mirroring the report's chapters. Document the rationale for the chosen structure in the placeholder comment (`<!-- Application Structure Plan: ... -->`).

3. **Select Optimal Presentation & Interactions:** For each key piece of information from the report:

   * Determine its *goal* within the context of the designed application structure.

   * Choose the best presentation method (chart, text, diagram, interactive element) adhering to **NO SVG/Mermaid**.

   * Define interactions that enhance exploration within the designed structure.

   * Justify choices based on usability and clarity. Document in the placeholder comment (`<!-- Visualization & Content Choices: ... -->`).

4. **Implement & Populate:** Generate the single HTML file:

   * **HTML Structure:** Build the **designed application layout** using Tailwind.

   * **CSS Styling:** Apply the theme consistently to the designed structure.

   * **Chart/Diagram Implementation:** Use appropriate methods supporting the design, including properly constrained chart containers as specified in "Styling Requirements."

   * **JavaScript Implementation:** Implement logic to power the interactions and dynamic updates within the **designed structure**.

   * **Content:** Populate with data and text from the source report, placed logically within the **designed structure**.

   * **Layout & Sizing:** Ensure responsiveness and appropriate sizing for the designed layout. Specifically, ensure chart visualizations are strictly constrained within their designated, styled containers, respecting both width and height limits, and do not cause any overflow (horizontal or vertical) or an excessively long page scroll.

   * **CRITICAL CONTEXT REQUIREMENT:**

     * **Every element MUST have clear context within the application's designed structure.** Explain what it shows (linking back to report concepts), how to interact, and the key takeaways.

     * **Each major section of the DESIGNED application MUST have an introductory paragraph.** Explain the purpose of that section within the app, what kind of information/interactions the user will find there (referencing the source content it contains), and how it contributes to understanding the report's overall message.
