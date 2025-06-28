# Networks.txt Maintenance System

This directory contains scripts to automatically maintain the `Networks.txt` file, which contains live YouTube news streams for the MultiStreamNews.TV application.

## Files

- **`Networks.txt`** - Main database of live news streams (tab-delimited)
- **`maintain_networks.py`** - Python script for checking and updating streams
- **`update_networks.sh`** - Shell script for automation and scheduling
- **`requirements.txt`** - Python dependencies
- **`NETWORKS_README.md`** - This documentation file

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

4. **Full update with new stream search:**
   ```bash
   ./update_networks.sh full
   ```

## Usage

### Shell Script (Recommended)

The `update_networks.sh` script provides three modes:

- **`quick`** (default) - Updates existing streams only
- **`full`** - Updates existing streams and searches for new ones
- **`check`** - Checks status without modifying files

```bash
# Quick update (default)
./update_networks.sh
./update_networks.sh quick

# Full update with new stream search
./update_networks.sh full

# Check only (no file changes)
./update_networks.sh check
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

Edit the `KNOWN_CHANNELS` list in `maintain_networks.py`:

```python
KNOWN_CHANNELS = [
    ("Channel Name", "@channel_handle"),
    ("New Channel", "@newchannel"),
    # Add more channels here
]
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

Example:
```
Network	Channel	YouTube URL	Status	Viewers
Sky News	Sky News	https://www.youtube.com/watch?v=YDvsBbKfLPA	LIVE	3.9K watching
NBC News NOW	NBC News	https://www.youtube.com/watch?v=DfwpCn9347w	LIVE	1.2K watching
```

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

The maintenance system works seamlessly with the main application:

1. **Real-time Updates** - Streams are verified and updated regularly
2. **Clean Data** - Dead streams are removed automatically  
3. **Fresh Content** - New live streams are discovered and added
4. **Reliable Sources** - Only verified live streams are included

The web application will automatically use the updated Networks.txt file without requiring any changes to the code.

## Best Practices

1. **Regular Updates** - Run updates every 30-60 minutes during peak hours
2. **Monitor Logs** - Check logs regularly for errors or issues
3. **Backup Strategy** - Keep backups of working Networks.txt files
4. **Rate Limiting** - Don't make requests too frequently to avoid blocking
5. **Testing** - Use `--check-only` mode to test before making changes

## Support

For issues or questions:

1. Check the log files for error messages
2. Run in verbose mode to see detailed output
3. Verify all dependencies are installed
4. Check internet connectivity and YouTube accessibility

The maintenance system is designed to be robust and handle most common scenarios automatically, but manual intervention may be needed for complex issues.
