# YouTube Live Feed Scanner (Python Version)

A desktop Python tool to scan YouTube channel live tabs and extract feed metadata. This is the command-line version of the web-based `get_feeds.html` tool.

## Features

- 🔍 **Scan YouTube Channels** - Extract live stream metadata from any YouTube channel
- 📊 **Structured Data Extraction** - Parse YouTube's internal data structures for accurate results
- 📝 **Multiple Export Formats** - Export to CSV, JSON, or plain text
- 🖥️ **Command Line Interface** - Easy to use from terminal/command prompt
- 🌐 **CORS Proxy Support** - Bypass browser restrictions with proxy services
- 📋 **Clipboard Integration** - Copy URLs directly to clipboard
- 🎯 **Flexible Output** - Display results in terminal or export to files

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make the script executable (optional):**
   ```bash
   chmod +x get_feeds.py
   ```

## Usage

### Basic Usage
```bash
python get_feeds.py "https://www.youtube.com/channel/UC4R8DWoMoI7CAwX8_LjQHig/live"
```

### Export to CSV
```bash
python get_feeds.py "https://www.youtube.com/@CNN" --export-csv
```

### Export to JSON
```bash
python get_feeds.py "https://www.youtube.com/c/SkyNews" --export-json
```

### Get URLs Only
```bash
python get_feeds.py "https://www.youtube.com/user/BBCNews" --urls-only
```

### Use with Proxy
```bash
python get_feeds.py "https://www.youtube.com/@FoxNews" --use-proxy
```

### Copy URLs to Clipboard
```bash
python get_feeds.py "https://www.youtube.com/@AlJazeera" --copy-urls
```

### Quiet Mode (minimal output)
```bash
python get_feeds.py "https://www.youtube.com/@DWNews" --quiet --urls-only
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `channel_url` | YouTube channel URL (positional argument) |
| `--use-proxy` | Use CORS proxy to bypass restrictions |
| `--proxy-url` | Custom proxy URL |
| `--export-csv` | Export results to CSV file |
| `--export-json` | Export results to JSON file |
| `--csv-file` | Custom CSV filename |
| `--json-file` | Custom JSON filename |
| `--urls-only` | Output only URLs, one per line |
| `--copy-urls` | Copy URLs to clipboard |
| `--quiet` | Quiet mode - minimal output |

## Supported URL Formats

The tool automatically converts various YouTube URL formats to live tab URLs:

- `https://www.youtube.com/channel/CHANNEL_ID` → `https://www.youtube.com/channel/CHANNEL_ID/live`
- `https://www.youtube.com/c/CHANNEL_NAME` → `https://www.youtube.com/c/CHANNEL_NAME/live`
- `https://www.youtube.com/user/USERNAME` → `https://www.youtube.com/user/USERNAME/live`
- `https://www.youtube.com/@HANDLE` → `https://www.youtube.com/@HANDLE/live`

## Output Format

The tool displays results in a formatted table showing:

- **Status**: Live status indicator (🔴 LIVE or ⏰ UPCOMING)
- **Title**: Stream title
- **Channel**: Channel name
- **Viewers**: Current viewer count
- **Duration**: Stream duration or "Live"
- **URL**: Direct link to the stream

## Export Formats

### CSV Export
Exports all feed data to a CSV file with columns:
- status, title, channel_name, view_count, view_count_text, duration, url, video_id, extracted_at

### JSON Export
Exports structured data as JSON with complete metadata for each feed.

## Examples

### Scan Sky News Live Feeds
```bash
python get_feeds.py "https://www.youtube.com/channel/UC4R8DWoMoI7CAwX8_LjQHig/live"
```

### Export CNN Live Feeds to CSV
```bash
python get_feeds.py "https://www.youtube.com/@CNN" --export-csv --csv-file "cnn_feeds.csv"
```

### Get BBC News URLs Only
```bash
python get_feeds.py "https://www.youtube.com/user/BBCNews" --urls-only > bbc_urls.txt
```

### Scan Multiple Channels (using shell loop)
```bash
for channel in "https://www.youtube.com/@CNN" "https://www.youtube.com/@BBCNews" "https://www.youtube.com/@SkyNews"; do
    echo "Scanning $channel"
    python get_feeds.py "$channel" --quiet --urls-only
done
```

## Technical Details

### Data Extraction Methods

1. **Primary Method**: Extracts YouTube's `ytInitialData` JSON structure from the HTML
2. **Fallback Method**: Uses regex patterns to find video IDs and metadata
3. **Proxy Support**: Can use CORS proxy services to bypass browser restrictions

### Parsing Strategy

The tool attempts to parse YouTube's internal data structures in this order:
1. Extract `ytInitialData` from script tags
2. Navigate through the tab structure to find live content
3. Extract metadata from video renderers
4. Fall back to regex-based extraction if structured data is unavailable

### Error Handling

- Validates YouTube URLs before processing
- Handles network timeouts and HTTP errors
- Provides detailed error messages for troubleshooting
- Continues processing even if individual feeds fail to parse

## Limitations

- **Rate Limiting**: YouTube may rate limit requests if used too frequently
- **Structure Changes**: YouTube occasionally changes their internal data structure
- **Geographic Restrictions**: Some streams may not be available in all regions
- **Proxy Dependency**: Direct access may be limited due to CORS policies

## Dependencies

- **requests**: HTTP library for fetching web pages
- **pyperclip**: Clipboard integration (optional)
- **json**: JSON parsing (built-in)
- **re**: Regular expressions (built-in)
- **csv**: CSV export functionality (built-in)

## Troubleshooting

### Common Issues

1. **No feeds found**: The channel may not have any live streams, or the URL format may be incorrect
2. **Network errors**: Try using `--use-proxy` option
3. **Parsing errors**: YouTube may have changed their page structure
4. **Permission errors**: Ensure you have write permissions for export files

### Debug Tips

- Use `--quiet` flag to reduce output noise
- Check the converted live URL in the output
- Try different proxy services if the default doesn't work
- Verify the channel actually has live content by visiting it manually

## Integration with MultiStreamNews.TV

This Python tool complements the web-based `get_feeds.html` and can be used to:
- Batch process multiple channels
- Schedule automated scans
- Integrate with other tools and scripts
- Export data for analysis

## License

Part of the MultiStreamNews.TV project. See main project README for license information.

---

*Last Updated: January 2, 2025*
