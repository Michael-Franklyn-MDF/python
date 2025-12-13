import pyperclip  # For copying to clipboard (install: pip install pyperclip)
import logic
import sys

def get_yes_no(prompt, default=True):
    """
    Asks a yes/no question and returns True or False.
    Default parameter sets what happens if user just presses Enter.
    """
    
    # Show [Y/n] or [y/N] based on default
    suffix = " [Y/n]: " if default else " [y/N]: "
    
    while True:
        response = input(prompt + suffix).strip().lower()
        
        # If user just presses Enter, use default
        if response == "":
            return default
        
        # Check for yes/no responses
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'")

def get_number(prompt, min_val, max_val, default):
    """
    Asks for a number within a specific range.
    Keeps asking until valid input is received.
    """
    
    while True:
        response = input(f"{prompt} [{min_val}-{max_val}] (default: {default}): ").strip()
        
        # If user just presses Enter, use default
        if response == "":
            return default
        
        # Try to convert to integer
        try:
            number = int(response)
            if min_val <= number <= max_val:
                return number
            else:
                print(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("Please enter a valid number")

def main():
    """
    Main function that runs the password generator program.
    This creates the interactive menu and handles user input.
    """
    
    # Print a nice header
    print("\n" + "="*50)
    print("🔐  PASSWORD GENERATOR  🔐".center(50))
    print("="*50 + "\n")
    
    # Keep generating passwords until user wants to quit
    while True:
        print("Configure your password settings:\n")
        
        # Get user preferences
        length = get_number("Password length", 8, 64, 16)
        use_uppercase = get_yes_no("Include uppercase letters (A-Z)?", True)
        use_lowercase = get_yes_no("Include lowercase letters (a-z)?", True)
        use_numbers = get_yes_no("Include numbers (0-9)?", True)
        use_symbols = get_yes_no("Include symbols (!@#$%)?", True)
        exclude_ambiguous = get_yes_no("Exclude ambiguous characters (0, O, l, 1, I)?", False)
        
        try:
            # Generate the password
            password = logic.generate_password(
                length=length, 
                use_uppercase=use_uppercase, 
                use_lowercase=use_lowercase, 
                use_numbers=use_numbers, 
                use_symbols=use_symbols, 
                exclude_ambiguous=exclude_ambiguous
            )
            
            # Calculate strength
            score, strength_text, color_code = logic.calculate_strength(password)
            reset_color = "\033[0m"  # Reset color back to normal
            
            # Display the result
            print("\n" + "-"*50)
            print(f"Generated Password: {color_code}{password}{reset_color}")
            print(f"Strength: {color_code}{strength_text}{reset_color} (Score: {score}/8)")
            print("-"*50 + "\n")
            
            # Try to copy to clipboard
            try:
                pyperclip.copy(password)
                print("✅ Password copied to clipboard!\n")
            except:
                print("⚠️  Could not copy to clipboard. Install pyperclip: pip install pyperclip\n")
                
        except logic.GenerationError as e:
            print(f"\n❌ Error: {str(e)}\n")
        
        # Ask if user wants to generate another password
        if not get_yes_no("\nGenerate another password?", True):
            print("\n👋 Thanks for using Password Generator! Stay secure!\n")
            break

# This is the entry point of the program
# It only runs if you execute this file directly
if __name__ == "__main__":
    main()