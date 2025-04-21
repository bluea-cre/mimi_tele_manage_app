from tkinter import ttk
from typing import Optional


class CustomFrame(ttk.Frame):
    """A custom frame with configurable background color."""

    def __init__(self, parent, background: Optional[str] = None, **kwargs):
        """Initialize the custom frame.

        Args:
            parent: The parent widget.
            background: Initial background color (e.g., 'blue', '#FF0000'). If None, uses default.
            **kwargs: Additional arguments passed to ttk.Frame.
        """
        super().__init__(parent, **kwargs)
        self._style = ttk.Style()
        self._style_name = f"CustomFrame_{id(self)}.TFrame"

        # Configure initial style
        if background:
            self._configure_background(background)
        else:
            self._configure_background("SystemButtonFace")  # Default system background

        # Apply style to frame
        self.configure(style=self._style_name)

    def set_background(self, color: str) -> None:
        """Change the background color of the frame.

        Args:
            color: The new background color (e.g., 'blue', '#FF0000').
        """
        self._configure_background(color)
        self.configure(style=self._style_name)

    def _configure_background(self, color: str) -> None:
        """Configure the style with the specified background color."""
        self._style.configure(self._style_name, background=color)
