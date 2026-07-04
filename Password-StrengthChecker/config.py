"""Configuration file containing constraints, thresholds, and constants."""

MIN_LENGTH = 8
RECOMMENDED_LENGTH = 12

# Strength thresholds based on score (0-100)
THRESHOLDS = {
    "Very Weak": 20,
    "Weak": 40,
    "Medium": 60,
    "Strong": 80,
    "Very Strong": 100,
}

SYMBOLS = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

# Commonly used weak passwords to check against
COMMON_PASSWORDS = [
    "123456", "password", "123456789", "qwerty", "12345678", 
    "111111", "links123", "password123", "admin", "welcome", 
    "letmein", "iloveyou", "secret", "monkey", "charlie"
]

# Common keyboard sequences for detection
SEQUENCES = [
    "abcdefghijklmnopqrstuvwxyz",
    "01234567890",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]