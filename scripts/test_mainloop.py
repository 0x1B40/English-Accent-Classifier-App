#!/usr/bin/env python3
"""Test tkinter mainloop functionality."""

import sys
import threading
import time
import tkinter as tk


def test_basic_tkinter():
    """Test basic tkinter functionality."""
    try:
        print("Creating tkinter root...")
        root = tk.Tk()
        root.title("Test Window")
        root.geometry("300x200")

        print("Adding a label...")
        label = tk.Label(root, text="Hello, World!")
        label.pack(pady=20)

        print("Adding a button...")
        button = tk.Button(root, text="Close", command=root.quit)
        button.pack(pady=10)

        print("Window created successfully. Starting mainloop with timeout...")

        # Start mainloop in a separate thread with timeout
        def run_mainloop():
            try:
                root.mainloop()
            except Exception as e:
                print(f"Error in mainloop: {e}")

        mainloop_thread = threading.Thread(target=run_mainloop, daemon=True)
        mainloop_thread.start()

        # Wait a bit
        time.sleep(2)

        print("Destroying window...")
        root.quit()
        root.destroy()

        print("Test completed successfully")
        return True

    except Exception as e:
        print(f"Error during tkinter test: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_basic_tkinter()
    sys.exit(0 if success else 1)
