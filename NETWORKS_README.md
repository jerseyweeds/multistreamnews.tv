# Networks.txt Maintenance System

This directory contains scripts to automatically maintain the `Networks.txt` file, which provides an optional live stream database for the MultiStreamNews.TV application. The application uses built-in channels by default for reliability and speed, with Networks.txt available as an enhanced option via toggle button.

## Files

- **`Networks.txt`** - Main database of live news streams (tab-delimited)
- **`network_list.txt`** - List of YouTube channels for stream discovery
- **`maintain_networks.py`** - Python script for checking and updating streams
- **`update_networks.sh`** - Shell script for automation and scheduling
- **`requirements.txt`** - Python dependencies
- **`NETWORKS_README.md`** - This documentation file

## Stream Filtering

The maintenance system now includes **24-hour filtering**:
- Only streams that have been live for **over 24 hours** are included
- Short-lived streams (under 24 hours) are automatically filtered out
- This ensures only stable, continuous news streams are displayed

## Quick Start

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run a quick check:**
   ```bash
   ./update_networks.sh check
   ```

3. **Update existing streams:**
   ```bash
   ./update_networks.sh quick
   ```

4. **Full refresh from channel list:**
   ```bash
   ./update_networks.sh refresh
   ```

## Usage

### Shell Script (Recommended)

The `update_networks.sh` script provides five modes:

- **`quick`** (default) - Updates existing streams, applies 24h filter
- **`full`** - Updates existing streams and searches for new ones (24h+ only)
- **`refresh`** - Complete rebuild from `network_list.txt` (24h+ only)
- **`check`** - Checks status without modifying files
- **`--test-mode`** - Limits processing to 10 URLs per channel (for development/testing)

```bash
# Quick update (default)
./update_networks.sh
./update_networks.sh quick

# Full update with new stream search
./update_networks.sh full

# Complete rebuild from network_list.txt
./update_networks.sh refresh

# Check only (no file changes)
./update_networks.sh check

# Test mode (limits processing for development/testing)
./update_networks.sh quick --test-mode
./update_networks.sh full --test-mode
```

### Python Script (Direct)

For more control, use the Python script directly:

```bash
# Check status without updating
python3 maintain_networks.py --check-only --verbose

# Update existing streams
python3 maintain_networks.py --verbose

# Search for new streams and update
python3 maintain_networks.py --add-new --verbose

# Full refresh from network list
python3 maintain_networks.py --refresh --verbose

# Test mode (limits to 10 URLs per channel for testing code changes)
python3 maintain_networks.py --test-mode --verbose --check-only
```

## Automation

### Cron Jobs

To automatically maintain the networks list, add a cron job:

```bash
# Edit crontab
crontab -e

# Add one of these lines:

# Every 30 minutes (quick update)
*/30 * * * * cd /path/to/multistreamnews.tv && ./update_networks.sh quick >> networks_update.log 2>&1

# Every 2 hours (full update)
0 */2 * * * cd /path/to/multistreamnews.tv && ./update_networks.sh full >> networks_update.log 2>&1

# Every hour during business hours (9 AM - 6 PM)
0 9-18 * * * cd /path/to/multistreamnews.tv && ./update_networks.sh quick >> networks_update.log 2>&1
```

### Systemd Timer (Linux)

Create a systemd service and timer for more advanced scheduling:

```ini
# /etc/systemd/system/networks-update.service
[Unit]
Description=Update Networks.txt file
After=network.target

[Service]
Type=oneshot
User=your-username
WorkingDirectory=/path/to/multistreamnews.tv
ExecStart=/path/to/multistreamnews.tv/update_networks.sh quick
```

```ini
# /etc/systemd/system/networks-update.timer
[Unit]
Description=Run networks update every 30 minutes
Requires=networks-update.service

[Timer]
OnCalendar=*:0/30
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl enable networks-update.timer
sudo systemctl start networks-update.timer
```

## Features

### Automatic Verification
- Checks if YouTube streams are currently live
- Updates viewer counts in real-time
- Removes dead/offline streams automatically

### Backup System
- Creates timestamped backups before updates
- Keeps the 5 most recent backups
- Automatic cleanup of old backups

### Logging
- Comprehensive logging to `networks_update.log`
- Automatic log rotation when files get large
- Timestamps and status reporting

### Error Handling
- Graceful handling of network errors
- Rate limiting to avoid YouTube blocking
- Retry logic for temporary failures

### New Stream Discovery
- Searches known news channels for new live streams
- Configurable list of channels to monitor
- Prevents duplicate entries

## Configuration

### Adding New Channels

Edit the `network_list.txt` file to add new channels:

```
Network	YouTube Channel URL
Sky News	https://www.youtube.com/@SkyNews
NBC News	https://www.youtube.com/@NBCNews
New Channel	https://www.youtube.com/@newchannel
Another Channel	https://www.youtube.com/@anotherchannel
```

The YouTube Channel URL should be the full channel URL:
- Format: `https://www.youtube.com/@channelname`
- Handle format: `https://www.youtube.com/@channelname`
- Legacy format: `https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxx`

After adding channels, run a refresh to discover their live streams:
```bash
./update_networks.sh refresh
```

### Adjusting Rate Limits

Modify the `REQUEST_DELAY` constant in `maintain_networks.py`:

```python
REQUEST_DELAY = 2  # seconds between requests
```

### Log File Size

Adjust the maximum log file size in `update_networks.sh`:

```bash
MAX_LOG_SIZE=1048576  # 1MB
```

## Networks.txt Format

The file uses tab-delimited format with these columns:

- **Network** - Display name of the news network
- **Channel** - YouTube channel name  
- **YouTube URL** - Full YouTube watch URL
- **Status** - Current status (LIVE/OFFLINE)
- **Viewers** - Current viewer count (e.g., "1.2K watching")
- **Duration** - How long the stream has been live (e.g., "2d", "5h", "45m")

**Note:** Only streams that have been live for **over 24 hours** are included.

Example:
```
Network	Channel	YouTube URL	Status	Viewers	Duration
Sky News	Sky News	https://www.youtube.com/watch?v=YDvsBbKfLPA	LIVE	3.9K watching	2d
NBC News NOW	NBC News	https://www.youtube.com/watch?v=DfwpCn9347w	LIVE	1.2K watching	25h
```

## network_list.txt Format

The `network_list.txt` file contains the master list of YouTube channels to monitor for live streams. It uses tab-delimited format with these columns:

- **Network** - Display name of the news network
- **YouTube Channel URL** - Full YouTube channel URL

Example:
```
Network	YouTube Channel URL
Sky News	https://www.youtube.com/@SkyNews
NBC News	https://www.youtube.com/@NBCNews
BBC News	https://www.youtube.com/@BBCNews
CNN	https://www.youtube.com/@CNN
Fox News	https://www.youtube.com/@FoxNews
```

This file is used by the maintenance scripts when discovering new live streams (modes: `full`, `refresh`).

## Troubleshooting

### Common Issues

1. **"Networks.txt not found"**
   - Ensure you're running the script from the correct directory
   - Check that the Networks.txt file exists

2. **"Python dependencies not installed"**
   - Run: `pip3 install -r requirements.txt`

3. **"Permission denied"**
   - Make script executable: `chmod +x update_networks.sh`

4. **"No streams found"**
   - YouTube may be rate-limiting requests
   - Try increasing the `REQUEST_DELAY` value
   - Check your internet connection

### Debugging

Enable verbose output for detailed information:

```bash
./update_networks.sh check  # Shows detailed status
python3 maintain_networks.py --verbose --check-only
```

Check the log file:
```bash
tail -f networks_update.log
```

## Integration with MultiStreamNews.TV

The maintenance system works as an optional enhancement to the main application:

1. **Default Operation** - App uses built-in channels for instant, reliable loading
2. **Enhanced Mode** - Networks.txt provides live stream data when toggled by user
3. **Background Loading** - Networks.txt loads silently without blocking the UI
4. **Seamless Toggle** - Users can switch between built-in and live data sources
5. **Clean Data** - Dead streams are removed automatically when Networks.txt is used
6. **Fresh Content** - New live streams are discovered and added regularly

The web application will automatically use the updated Networks.txt file when the user toggles to it, without requiring any changes to the code.

## Best Practices

1. **Regular Updates** - Run updates every 30-60 minutes during peak hours for optimal live data
2. **Monitor Logs** - Check logs regularly for errors or issues
3. **Backup Strategy** - Keep backups of working Networks.txt files
4. **Rate Limiting** - Don't make requests too frequently to avoid blocking
5. **Testing** - Use `--check-only` mode to test before making changes
6. **Optional Usage** - Remember that the main app works perfectly with built-in channels when Networks.txt is unavailable

## Support

For issues or questions:

1. Check the log files for error messages
2. Run in verbose mode to see detailed output
3. Verify all dependencies are installed
4. Check internet connectivity and YouTube accessibility

The maintenance system is designed to be robust and handle most common scenarios automatically, but manual intervention may be needed for complex issues.
