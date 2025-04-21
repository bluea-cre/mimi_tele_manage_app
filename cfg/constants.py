import os

# Log file name
LOG_FILE = "logs/log_file.txt"


# Folder includes the function scripts
FUNCTIONS_DIR = "functions"
ORDER_FILE = os.path.join(FUNCTIONS_DIR, ".order")


# The file stores the last window size
WINDOW_SIZE_FILE = "window_size.json"
DEFAULT_WINDOW_SIZE = {"width": 800, "height": 600}


# Sort options list for "Sort by option"
SORT_OPTIONS = ["Sort Alphabet", "Move Checked to Top"]
