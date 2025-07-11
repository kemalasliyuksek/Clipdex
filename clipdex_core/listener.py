import time
from pynput import keyboard as pynput_keyboard
import keyboard as system_keyboard
from .snippet_manager import SnippetManager
import os
import sys
from typing import Optional
from .config_manager import ConfigManager

class ClipdexListener:
    """
    Listens for system-wide keyboard events and performs text expansion.
    """
    def __init__(self):
        self.snippet_manager = SnippetManager()
        self.config_manager = ConfigManager()
        self.snippets = self.snippet_manager.load_snippets()

        # Check for MacOS permissions
        if sys.platform == "darwin":
            self._check_macos_permissions()

        # Variables to track the current state
        self.current_shortcut = ""
        self.is_listening = False

        # Variables to track the current state
        self._awaiting_backspace = False  # Waiting for the first key after expansion
        self._last_expanded_text = ""     # The expanded text we wrote
        self._last_shortcut = ""          # Original shortcut (':' + shortcut)
        self._ignore_events = 0           # Count of keys to ignore
        # Track if the user pressed space before the ':' key
        self._prev_key_was_space = False
        self._leading_space_flag = False  # Was there a space before the ':' key?

        # Track the last modified time of the snippet file
        self._snippet_file_mtime: Optional[float] = self._get_snippet_file_mtime()

        # Prepare the pynput listener
        self.listener = pynput_keyboard.Listener(on_press=self.on_press)

    def _check_macos_permissions(self):
        """Check if the app has necessary permissions on MacOS."""
        try:
            # Try to start a test listener to check permissions
            test_listener = pynput_keyboard.Listener(on_press=lambda x: None)
            test_listener.start()
            test_listener.stop()
            print("✓ macOS keyboard permissions checked - OK")
        except Exception as e:
            print("⚠️  macOS permission issue detected!")
            print("Follow these steps to allow Clipdex to work:")
            print("1. System Preferences > Security & Privacy > Privacy > Accessibility")
            print("2. Click the '+' button and add the Clipdex application")
            print("3. Check the box next to Clipdex")
            print("4. Restart the application")
            print(f"Error details: {e}")

    def start(self):
        """Starts the listener."""
        print("Clipdex engine running...")
        try:
            self.listener.start()
            print("✓ Keyboard listener started")
        except Exception as e:
            print(f"❌ Keyboard listener could not be started: {e}")
            if sys.platform == "darwin":
                print("Check Accessibility permissions on macOS!")

    def join(self):
        """Waits for the listener thread to finish."""
        self.listener.join()

    def on_press(self, key):
        """Function triggered on every key press."""
        # Ignore keys pressed by the program
        if self._ignore_events > 0:
            self._ignore_events -= 1
            return
    
        # Check if we are waiting for the first key after expansion
        if self._awaiting_backspace:
            # If the first key is backspace, revert the expansion
            if key == pynput_keyboard.Key.backspace:
                try:
                    # The user's backspace already removed the last character.
                    # We need to remove the remaining expanded text
                    remove_count = len(self._last_expanded_text)
                    self._ignore_events += remove_count
                    for _ in range(remove_count):
                        system_keyboard.press_and_release('backspace')
                        time.sleep(0.01)

                    # 2. Write the old shortcut again (including shortcut character)
                    system_keyboard.write(self._last_shortcut)
                    self._ignore_events += len(self._last_shortcut)

                    # 3. Reset the listening state
                    self.is_listening = False
                    self.current_shortcut = ""
                finally:
                    # Now we are not waiting for the first key after expansion
                    self._awaiting_backspace = False
                return  # We have consumed this key press
            else:
                # The first key pressed was not backspace, so we can't revert the expansion
                self._awaiting_backspace = False
                # (Continue processing this key as normal)

        # Update the snippet list on every key press
        self._refresh_snippets_if_needed()

        try:
            # Get shortcut character from config
            shortcut_char = self.config_manager.get("shortcut_character", ":")
            # Shortcut character starts listening
            if isinstance(key, pynput_keyboard.KeyCode) and key.char == shortcut_char:
                self.is_listening = True
                self.current_shortcut = ""
                # Save if there was a space before the shortcut character
                self._leading_space_flag = self._prev_key_was_space
                # print("Listening started...")  # For debugging
                return

            if self.is_listening:
                # Space or Enter ends the shortcut
                trigger_pref = self.config_manager.get("trigger_key", "space").lower()
                is_trigger = (
                    (trigger_pref == "space" and key == pynput_keyboard.Key.space) or
                    (trigger_pref == "enter" and key == pynput_keyboard.Key.enter)
                )

                if is_trigger:
                    if self.current_shortcut in self.snippets:
                        # print(f"Shortcut found: {self.current_shortcut}")  # For debugging

                        # 1. Delete the typed shortcut
                        # The shortcut itself + the trigger character + the terminator ' '
                        shortcut_char = self.config_manager.get("shortcut_character", ":")
                        backspace_count = len(self.current_shortcut) + 2
                        # Ignore the backspace key events we will create
                        self._ignore_events += backspace_count
                        for _ in range(backspace_count):
                            system_keyboard.press_and_release('backspace')
                            time.sleep(0.01)  # Prevent keypress overlaps

                        # 2. Write the expanded text
                        expanded_text = self.snippets[self.current_shortcut]
                        system_keyboard.write(expanded_text)

                        # 3. Save information for reverting (undo)
                        self._awaiting_backspace = True
                        self._last_expanded_text = expanded_text
                        shortcut_char = self.config_manager.get("shortcut_character", ":")
                        self._last_shortcut = shortcut_char + self.current_shortcut
                        self._ignore_events += len(expanded_text)
                        # Save if there was a space before the ':' key (for reverting)
                        self._leading_space_for_revert = self._leading_space_flag

                    # Reset state
                    self.is_listening = False
                    self.current_shortcut = ""

                # Backspace removes a character
                elif key == pynput_keyboard.Key.backspace:
                    self.current_shortcut = self.current_shortcut[:-1]

                # Other characters are added to the shortcut
                elif isinstance(key, pynput_keyboard.KeyCode) and key.char:
                    self.current_shortcut += key.char

        except Exception as e:
            # Catch possible errors and prevent the listener from crashing
            print(f"An error occurred: {e}")
            self.is_listening = False
            self.current_shortcut = ""

        # Update the previous key was space flag for the next key
        self._prev_key_was_space = (key == pynput_keyboard.Key.space)

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def _get_snippet_file_mtime(self) -> float:
        """Returns the last modified time of the snippet file."""
        if os.path.exists(self.snippet_manager.filepath):
            return os.path.getmtime(self.snippet_manager.filepath)
        return 0.0

    def _refresh_snippets_if_needed(self):
        """Reloads the snippet list if the file has been modified."""
        try:
            current_mtime = self._get_snippet_file_mtime()
            if current_mtime != self._snippet_file_mtime:
                self.snippets = self.snippet_manager.load_snippets()
                self._snippet_file_mtime = current_mtime
                print("Snippet list updated.")
        except Exception as e:
            # If there's an error reading the file, don't crash the engine
            print(f"Snippet update error: {e}")