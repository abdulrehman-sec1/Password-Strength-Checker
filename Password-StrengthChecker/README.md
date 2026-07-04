# Password Strength Checker

An interactive, modular, and production-grade Python CLI application to analyze, grade, score, and generate cryptographically sound credentials.

## Features
* **Secure Input Masking**: Uses internal native system masking arrays during entry.
* **Multi-Criteria Auditing**: Assesses minimum length, upper/lowercase bounds, digit presence, and custom special punctuation symbols.
* **Attack Sequence Recognition**: Flags standard vocabulary lists, repeating characters, and keyboard walk patterns.
* **Entropy Modeling**: Displays computational density scores (in bits) along with human-readable brute force timelines.
* **Automated Document Exports**: Serializes report models straight to plain text `.txt` and structured `.json` formats.
* **Integrated Generation Engine**: Builds randomized sequences using cryptographically secure primitives (`secrets`).

## Folder Structure
```text
Password-Strength-Checker/
│
├── main.py
├── password_checker.py
├── utils.py
├── config.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── tests/
│   ├── test_password_checker.py
│   └── __init__.py
│
├── examples/
│   └── sample_usage.py
│
└── docs/
    └── project_overview.md

```
## Installation
Clone the repository:

Bash
```
git clone https://github.com/abdulrehman-sec1/Password-Strength-Checker.git
```
```
cd Password-Strength-Checker

```
## Install dependencies:

Bash
```
pip install -r requirements.txt
```
```
```
# Usage
Run the main application interface:

Bash
```
python main.py
```
Run test coverage modules:
```
Bash
```
python -m unittest discover tests
```

```
# How Scoring Works
The engine evaluates scoring criteria out of 100 total maximum points:

Length Constraints Matched: +25 Points

Character Matrix Distributions: Up to +65 Points (split among casing formats, digits, and special characters).

Entropy Modifiers: High bits yield bonus weights.

Penalties: Common words or pattern strings subtract value dynamically.
```

```
# Strength Levels
0–20: Very Weak

21–40: Weak

41–60: Medium

61–80: Strong

81–100: Very Strong
```
```
# Technologies Used
Python 3 (Core Platform)

Colorama (Terminal Styles)

Unittest (Testing Harness)
```
```
# Future Improvements
Add visual desktop layouts using Tkinter.

Build lightweight endpoints using FastAPI.

Incorporate real-time external breach checking via the HaveIBeenPwned API.
```