"""Graphical User Interface for the English Accent Classifier."""

import tkinter as tk
from tkinter import messagebox
import logging
from typing import Callable

from .audio_processor import AudioProcessor
from .accent_classifier import AccentClassifier
from .exceptions import AccentClassifierError
from .config import get_config

logger = logging.getLogger(__name__)


class AccentClassifierGUI:
    """GUI application for English accent classification."""

    def __init__(self):
        """Initialize the GUI application."""
        try:
            self.audio_processor = AudioProcessor()
            self.classifier = AccentClassifier()
        except Exception as e:
            logger.error(f"Failed to initialize audio processor or classifier: {str(e)}")
            raise RuntimeError(f"Failed to initialize application components: {str(e)}")

        # GUI elements
        self.root: tk.Tk = None
        self.url_entry: tk.Entry = None
        self.process_button: tk.Button = None
        self.status_label: tk.Label = None
        self.result_text: tk.Text = None
        self.scrollbar: tk.Scrollbar = None

    def create_gui(self) -> tk.Tk:
        """Create and configure the GUI elements.

        Returns:
            tk.Tk: The root window of the application.
        """
        config = get_config()

        self.root = tk.Tk()
        self.root.title(config.get('gui.title'))
        width = config.get('gui.width')
        height = config.get('gui.height')
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, True)

        # Create widgets
        self._create_widgets()
        self._layout_widgets()

        return self.root

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        config = get_config()

        # URL input
        font_family = config.get('gui.font_family')
        font_size = config.get('gui.font_size')
        tk.Label(self.root, text="Enter YouTube Video URL:",
                font=(font_family, font_size + 2)).pack(pady=(20, 5))

        self.url_entry = tk.Entry(self.root, width=60, font=(font_family, font_size))
        self.url_entry.pack(pady=(0, 20))

        # Process button
        self.process_button = tk.Button(
            self.root,
            text="Analyze Accent",
            command=self._process_video,
            font=(font_family, font_size + 2, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.process_button.pack(pady=(0, 20))

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to analyze accents...",
            font=(font_family, font_size),
            fg="#666666"
        )
        self.status_label.pack(pady=(0, 10))

        # Results text area
        tk.Label(self.root, text="Classification Results:",
                font=(font_family, font_size + 2)).pack(pady=(10, 5))

        # Create a frame for text area and scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=(0, 20), padx=20)

        # Scrollbar for text area
        self.scrollbar = tk.Scrollbar(text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text = tk.Text(
            text_frame,
            height=15,
            width=70,
            font=("Courier", font_size),
            wrap=tk.WORD,
            yscrollcommand=self.scrollbar.set
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.result_text.yview)

    def _layout_widgets(self) -> None:
        """Layout the GUI widgets (currently using pack layout)."""
        pass  # Using pack layout, no additional layout needed

    def _process_video(self) -> None:
        """Process the video URL and display results."""
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        try:
            # Update UI
            self._set_processing_state(True)
            self.status_label.config(text="Downloading and processing audio...",
                                   fg="#FF9800")
            self.root.update()

            # Process audio
            logger.info(f"Processing URL: {url}")
            wav_path = self.audio_processor.download_and_convert_to_wav(url)

            try:
                # Classify accent
                result, most_probable_accent = self.classifier.classify_accent(wav_path)

                # Update UI with results
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, result)
                self.status_label.config(
                    text=f"Most probable accent: {most_probable_accent}",
                    fg="#4CAF50"
                )

                logger.info(f"Classification complete: {most_probable_accent}")

            finally:
                # Clean up temporary file
                self.audio_processor.cleanup_temp_file(wav_path)

        except AccentClassifierError as e:
            logger.error(f"Processing failed: {str(e)}")
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="Processing failed", fg="#F44336")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.status_label.config(text="Unexpected error", fg="#F44336")
        finally:
            self._set_processing_state(False)

    def _set_processing_state(self, processing: bool) -> None:
        """Set the processing state of the GUI.

        Args:
            processing: True if processing, False otherwise.
        """
        state = "disabled" if processing else "normal"
        self.process_button.config(state=state)
        self.url_entry.config(state=state)

    def run(self) -> None:
        """Run the GUI application."""
        try:
            root = self.create_gui()
            logger.info("GUI initialized successfully, starting main loop")
            root.mainloop()
        except Exception as e:
            logger.error(f"Failed to start GUI: {str(e)}")
            # Since GUI failed to start, we can't show a messagebox
            # Just log the error and let the program exit
            print(f"Error: Failed to start GUI application: {str(e)}")
            raise


def run_gui() -> None:
    """Run the English Accent Classifier GUI application."""
    try:
        config = get_config()
        print("Configuration loaded successfully")

        # Configure logging
        log_level = config.get('logging.level', 'INFO')
        log_format = config.get('logging.format')
        log_file = config.get('logging.file')

        # Convert string level to logging level
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)

        log_config = {
            'level': numeric_level,
            'format': log_format
        }

        if log_file:
            log_config['filename'] = log_file

        logging.basicConfig(**log_config)
        logger.info("Logging configured successfully")

        # Test tkinter functionality
        print("Testing tkinter compatibility...")
        try:
            test_root = tk.Tk()
            test_root.withdraw()  # Hide the window
            test_root.quit()
            test_root.destroy()
            print("Tkinter test successful")
        except Exception as tk_error:
            print(f"Tkinter not available or not properly configured: {tk_error}")
            print("This might be due to running in an environment without GUI support.")
            print("Try running this application on a desktop environment with GUI support.")
            return

        # Create and run GUI
        print("Creating GUI application...")
        gui = AccentClassifierGUI()
        print("GUI application created, starting main loop...")
        gui.run()

    except Exception as e:
        # If we get here, logging might not be set up yet
        print(f"Error starting GUI application: {e}")
        import traceback
        traceback.print_exc()
        raise
