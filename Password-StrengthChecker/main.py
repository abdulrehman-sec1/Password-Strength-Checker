"""Interactive Command-Line Application Shell Entry point."""

import getpass
import sys
from typing import List, Dict, Any
import utils
import password_checker

# Application Session State
SESSION_HISTORY: List[Dict[str, Any]] = []
LAST_ANALYSIS: Dict[str, Any] = {}

def render_menu() -> None:
    """Draws text alignment decoration markers."""
    print("\n" + "=" * 35)
    utils.colored_print("     Password Strength Checker", "cyan")
    print("=" * 35)
    print("1. Check Password")
    print("2. Generate Secure Password")
    print("3. Export Reports (Last Run)")
    print("4. View History & Session Stats")
    print("5. Help Documentation")
    print("6. Exit")
    print("=" * 35)

def handle_check() -> None:
    global LAST_ANALYSIS
    print("\nEnter your password securely below:")
    raw = getpass.getpass("Password: ")
    
    if not raw:
        utils.colored_print("Password cannot be blank!", "red")
        return
        
    analysis = password_checker.analyze_password(raw)
    LAST_ANALYSIS = analysis
    SESSION_HISTORY.append(analysis)
    
    # Display Results beautifully
    print("\n--- Evaluation Results ---")
    print(f"Score: {analysis['score']}/100")
    
    color_map = {"Very Weak": "red", "Weak": "magenta", "Medium": "yellow", "Strong": "blue", "Very Strong": "green"}
    utils.colored_print(f"Category: {analysis['category']}", color_map.get(analysis['category'], "white"))
    print(f"Entropy: {analysis['entropy']:.2f} bits")
    print(f"Crack Time Estimate: {analysis['crack_time']}")
    
    if analysis['suggestions']:
        utils.colored_print("\nSuggestions:", "yellow")
        for sug in analysis['suggestions']:
            print(f" * {sug}")
    else:
        utils.colored_print("\nExcellent! Your password meets safety metrics.", "green")

def handle_generate() -> None:
    print("\nEnter desired length (default 16, min 8):")
    raw_len = input("Length: ").strip()
    length = 16
    if raw_len:
        parsed = utils.validate_input(raw_len, 8, 128)
        if parsed != -1:
            length = parsed
        else:
            utils.colored_print("Invalid length fallback to 16.", "yellow")
            
    secure_pw = utils.generate_password(length)
    print("\nGenerated Secure Password:")
    utils.colored_print(secure_pw, "green")
    print("(Copy the value safely. It is not saved to history files)")

def handle_save() -> None:
    if not LAST_ANALYSIS:
        utils.colored_print("\nNo analysis history found from this session yet. Run option 1 first.", "red")
        return
        
    base_name = input("\nEnter output file prefix name (e.g. 'report'): ").strip()
    if not base_name:
        base_name = "password_report"
        
    json_path = f"{base_name}.json"
    txt_path = f"{base_name}.txt"
    
    if utils.save_json(json_path, LAST_ANALYSIS) and utils.export_report(txt_path, LAST_ANALYSIS):
        utils.colored_print(f"\nSuccessfully created logs:\n -> {json_path}\n -> {txt_path}", "green")

def handle_stats() -> None:
    if not SESSION_HISTORY:
        utils.colored_print("\nNo entries stored in history during this runtime execution loop.", "yellow")
        return
    print(f"\n--- History Stats ({len(SESSION_HISTORY)} checked) ---")
    avg_score = sum(item['score'] for item in SESSION_HISTORY) / len(SESSION_HISTORY)
    print(f"Average Session Score: {avg_score:.1f}/100")
    
    categories = [item['category'] for item in SESSION_HISTORY]
    print("Breakdown by categories:")
    for cat in ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]:
        if categories.count(cat) > 0:
            print(f" - {cat}: {categories.count(cat)}")

def handle_help() -> None:
    print("\n=== Application Manual Help ===")
    print("Entropy measures the true mathematical unpredictability of standard characters.")
    print("Higher variations among uppercase, numeric positions, and non-alphanumeric lengths")
    print("yield larger resistance against dictionary brute-force dictionary attack arrays.")

def main() -> None:
    while True:
        try:
            render_menu()
            choice_raw = input("Select an option (1-6): ").strip()
            choice = utils.validate_input(choice_raw, 1, 6)
            
            if choice == 1: handle_check()
            elif choice == 2: handle_generate()
            elif choice == 3: handle_save()
            elif choice == 4: handle_stats()
            elif choice == 5: handle_help()
            elif choice == 6:
                utils.colored_print("\nExiting. Stay secure!", "cyan")
                sys.exit(0)
            else:
                utils.colored_print("Invalid selection option. Use integer choices from 1 to 6.", "red")
        except KeyboardInterrupt:
            utils.colored_print("\nSession interrupted. Exiting gracefully.", "magenta")
            sys.exit(0)

if __name__ == "__main__":
    main()