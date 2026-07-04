"""Core cryptographic and complexity parsing engine for password checking."""

import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import config

@dataclass
class PasswordResult:
    score: int
    category: str
    entropy: float
    crack_time: str
    metrics: Dict[str, bool]
    suggestions: List[str]

def check_length(password: str) -> bool:
    return len(password) >= config.MIN_LENGTH

def check_uppercase(password: str) -> bool:
    return any(c.isupper() for c in password)

def check_lowercase(password: str) -> bool:
    return any(c.islower() for c in password)

def check_digits(password: str) -> bool:
    return any(c.isdigit() for c in password)

def check_special_characters(password: str) -> bool:
    return any(c in config.SYMBOLS for c in password)

def detect_common_password(password: str) -> bool:
    return password.lower() in config.COMMON_PASSWORDS

def detect_repeated_characters(password: str) -> bool:
    """Returns True if any character repeats more than 3 times consecutively."""
    count = 1
    for i in range(1, len(password)):
        if password[i] == password[i-1]:
            count += 1
            if count > 3:
                return True
        else:
            count = 1
    return False

def detect_sequences(password: str) -> bool:
    """Returns True if common keyboard/alphabetical sequences >= 4 steps exist."""
    lower_pw = password.lower()
    if len(lower_pw) < 4:
        return False
    for i in range(len(lower_pw) - 3):
        sub = lower_pw[i:i+4]
        for seq in config.SEQUENCES:
            if sub in seq or sub in seq[::-1]:
                return True
    return False

def calculate_entropy(password: str) -> float:
    """Calculates information entropy metric in bits."""
    if not password:
        return 0.0
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(c in config.SYMBOLS for c in password): pool += len(config.SYMBOLS)
    
    # Check for custom/outside characters if pool is still 0
    if pool == 0: 
        pool = 256
        
    return len(password) * math.log2(pool)

def estimate_crack_time(entropy: float) -> str:
    """Translates entropy thresholds into logical human timelines."""
    # Assuming 10 billion guesses per second (high-end consumer/mid GPU array)
    guesses_per_sec = 1e10
    total_combinations = 2 ** entropy
    seconds = total_combinations / guesses_per_sec
    
    if seconds < 1: return "Instantly"
    if seconds < 60: return f"{int(seconds)} seconds"
    
    minutes = seconds / 60
    if minutes < 60: return f"{int(minutes)} minutes"
    
    hours = minutes / 60
    if hours < 24: return f"{int(hours)} hours"
    
    days = hours / 24
    if days < 365: return f"{int(days)} days"
    
    years = days / 365
    if years < 1000: return f"{int(years)} years"
    if years < 1e6: return f"{int(years/1000)} millennia"
    return "Eons"

def calculate_strength(metrics: Dict[str, bool], entropy: float) -> tuple[int, str]:
    """Calculates points up to 100 and classifies the tier."""
    score = 0
    # Length metrics
    if metrics["length_ok"]: score += 25
    if metrics["highly_common"]: score -= 40
    if metrics["repeated_chars"]: score -= 10
    if metrics["sequential_chars"]: score -= 10
    
    # Base variations
    if metrics["has_upper"]: score += 15
    if metrics["has_lower"]: score += 15
    if metrics["has_digits"]: score += 15
    if metrics["has_special"]: score += 20

    # Dynamic Entropy modifier adjustments
    if entropy > 60: score += 10
    
    score = max(0, min(100, score))
    
    category = "Very Weak"
    for name, top_limit in config.THRESHOLDS.items():
        if score <= top_limit:
            category = name
            break
            
    return score, category

def analyze_password(password: str) -> Dict[str, Any]:
    """Orchestrates validation tasks to compile structural results."""
    metrics = {
        "length_ok": check_length(password),
        "has_upper": check_uppercase(password),
        "has_lower": check_lowercase(password),
        "has_digits": check_digits(password),
        "has_special": check_special_characters(password),
        "highly_common": detect_common_password(password),
        "repeated_chars": detect_repeated_characters(password),
        "sequential_chars": detect_sequences(password)
    }
    
    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)
    score, category = calculate_strength(metrics, entropy)
    
    suggestions = []
    if not metrics["length_ok"]: suggestions.append(f"Make password at least {config.MIN_LENGTH} characters.")
    if not metrics["has_upper"]: suggestions.append("Add uppercase letters.")
    if not metrics["has_lower"]: suggestions.append("Add lowercase letters.")
    if not metrics["has_digits"]: suggestions.append("Add numeric digits.")
    if not metrics["has_special"]: suggestions.append("Add symbols or special characters.")
    if metrics["highly_common"]: suggestions.append("Avoid standard or widely guessed default phrases.")
    if metrics["repeated_chars"]: suggestions.append("Reduce long consecutive repeating identical characters.")
    if metrics["sequential_chars"]: suggestions.append("Avoid logical runs (like '1234' or 'abcd').")

    res = PasswordResult(score, category, entropy, crack_time, metrics, suggestions)
    return asdict(res)