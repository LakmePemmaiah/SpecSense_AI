# All Helper functions are defined in this file. 
# These functions can be used across the project/ other Folders.
import logging
import json
from pathlib import Path
from typing import Any


def get_logger(name: str) -> logging.Logger:  #Logging object is returned from the function
    """Get a simple logger for the given name."""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s' # many other Levels are available like below
        # (INFO, DEBUG,WARNING, ERROR, CRITICAL)
    )
    return logging.getLogger(name)

def extract_json_from_text(text: str) -> Any:
    """Extract JSON from text string (Raw LLM output).

    Returns the first JSON object/array found, or a list of all JSON values found in the text.
    If only one JSON value is present, a single parsed value is returned. If multiple values are found,
    the function returns a list containing all of them.
    """
    if not text:
        return {}

    decoder = json.JSONDecoder()
    parsed_values = []
    seen_positions = set()

    for index, char in enumerate(text):
        if char not in '{[':
            continue

        if index in seen_positions:
            continue

        try:
            parsed, end = decoder.raw_decode(text[index:])
            parsed_values.append(parsed)
            seen_positions.add(index)

            # Skip ahead so we don't repeatedly parse the same JSON from an overlapping substring.
            for next_index in range(index + 1, index + end):
                seen_positions.add(next_index)
        except json.JSONDecodeError:
            continue

    if not parsed_values:
        return {}
    if len(parsed_values) == 1:
        return parsed_values[0]
    return parsed_values

def load_file(file_path: str) -> str:
    """Load and return file contents as string."""
    return Path(file_path).read_text().strip()
