"""Example pipeline script illustrating direct headless modular operations."""

from password_checker import analyze_password
from utils import generate_password

def run_pipeline_demo():
    print("--- 1. Automated Dynamic Password Checking ---")
    sample_passwords = ["123456", "P@ss1234!", "qW8v#mZ9!pLxR2tK"]
    
    for pwd in sample_passwords:
        result = analyze_password(pwd)
        print(f"Password: {pwd:<18} | Score: {result['score']:<3} | Tier: {result['category']}")
        
    print("\n--- 2. Standalone Code Generation Framework ---")
    auto_gen = generate_password(20)
    print(f"Generated a secure 20-character variant: {auto_gen}")
    
    verification = analyze_password(auto_gen)
    print(f"Verification Score: {verification['score']}/100 ({verification['category']})")

if __name__ == "__main__":
    run_pipeline_demo()