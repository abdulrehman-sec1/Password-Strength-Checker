"""Utility and helper functions including formatting, generation, and file I/O."""

import json
import random
import secrets
import string
from typing import Dict, Any
from colorama import init, Fore, Style
import config

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

def colored_print(text: str, color: str, end: str = "\n") -> None:
    """Prints text in a specific color using colorama."""
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE
    }
    selected_color = color_map.get(color.lower(), Fore.WHITE)
    print(f"{selected_color}{text}{Style.RESET_ALL}", end=end)

def generate_password(length: int = 16) -> str:
    """Generates a cryptographically secure random password."""
    if length < 8:
        length = 8
        
    alphabet = string.ascii_letters + string.digits + config.SYMBOLS
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        # Ensure it meets basic composition requirements
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in config.SYMBOLS for c in password)):
            return password

def save_json(filepath: str, data: Dict[str, Any]) -> bool:
    """Saves analysis data dictionary to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except IOError as e:
        colored_print(f"Error saving JSON file: {e}", "red")
        return False

def export_report(filepath: str, data: Dict[str, Any]) -> bool:
    """Exports a formatted plain text analysis report."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 40 + "\n")
            f.write("      PASSWORD SECURITY REPORT\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Score: {data['score']}/100\n")
            f.write(f"Category: {data['category']}\n")
            f.write(f"Entropy: {data['entropy']:.2f} bits\n")
            f.write(f"Estimated Crack Time: {data['crack_time']}\n\n")
            
            f.write("Analysis Details:\n")
            for metric, passed in data['metrics'].items():
                status = "PASS" if passed else "FAIL"
                f.write(f" - {metric.replace('_', ' ').title()}: {status}\n")
                
            if data['suggestions']:
                f.write("\nSuggestions for Improvement:\n")
                for sug in data['suggestions']:
                    f.write(f" * {sug}\n")
        return True
    except IOError as e:
        colored_print(f"Error exporting TXT report: {e}", "red")
        return False

def validate_input(choice_str: str, min_val: int, max_val: int) -> int:
    """Validates that a string input is an integer within a given range."""
    try:
        val = int(choice_str)
        if min_val <= val <= max_val:
            return val
    except ValueError:
        pass
    return -1