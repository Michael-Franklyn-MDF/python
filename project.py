import tkinter as tk
from tkinter import ttk
import random
import string

# This function generates the actual password based on user preferences
def generate_password():
    # Get the desired length from the slider
    length = int(length_slider.get())
    
    # Create an empty string to store available characters
    characters = ""
    
    # Check which checkboxes are selected and add those character types
    if uppercase_var.get():
        characters += string.ascii_uppercase  # Adds A-Z
    if lowercase_var.get():
        characters += string.ascii_lowercase  # Adds a-z
    if numbers_var.get():
        characters += string.digits  # Adds 0-9
    if symbols_var.get():
        characters += string.punctuation  # Adds !@#$%^&* etc.
    
    # If user wants to exclude ambiguous characters
    if exclude_ambiguous_var.get():
        # Remove characters that look similar: 0, O, l, 1, I
        ambiguous = "0Ol1I"
        for char in ambiguous:
            characters = characters.replace(char, "")
    
    # Check if user selected at least one character type
    if not characters:
        result_text.delete(0, tk.END)
        result_text.insert(0, "Please select at least one option!")
        return
    
    # Generate the password by randomly selecting characters
    password = ''.join(random.choice(characters) for _ in range(length))
    
    # Display the password in the text box
    result_text.delete(0, tk.END)
    result_text.insert(0, password)
    
    # Calculate and display password strength
    calculate_strength(password)

# This function evaluates how strong the password is
def calculate_strength(password):
    strength = 0
    feedback = ""
    
    # Check various criteria and add points for each
    if len(password) >= 12:
        strength += 2
    elif len(password) >= 8:
        strength += 1
    
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 2
    
    # Determine strength level based on points
    if strength <= 2:
        feedback = "Weak"
        color = "red"
    elif strength <= 4:
        feedback = "Medium"
        color = "orange"
    else:
        feedback = "Strong"
        color = "green"
    
    # Update the strength label with color
    strength_label.config(text=f"Strength: {feedback}", foreground=color)

# This function copies the password to clipboard
def copy_to_clipboard():
    password = result_text.get()
    if password and password != "Please select at least one option!":
        window.clipboard_clear()
        window.clipboard_append(password)
        copy_button.config(text="Copied!")
        # Reset button text after 2 seconds
        window.after(2000, lambda: copy_button.config(text="Copy"))

# Create the main window
window = tk.Tk()
window.title("Password Generator")
window.geometry("450x500")
window.resizable(False, False)

# Create a main frame for better organization
main_frame = ttk.Frame(window, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Title label
title_label = ttk.Label(main_frame, text="Password Generator", font=("Arial", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Password length section
length_label = ttk.Label(main_frame, text="Password Length:", font=("Arial", 11))
length_label.grid(row=1, column=0, sticky=tk.W, pady=5)

# Display current length value
length_value_label = ttk.Label(main_frame, text="12", font=("Arial", 11, "bold"))
length_value_label.grid(row=1, column=1, sticky=tk.E, pady=5)

# Slider to select password length (8 to 32 characters)
length_slider = ttk.Scale(main_frame, from_=8, to=32, orient=tk.HORIZONTAL, length=300,
                          command=lambda v: length_value_label.config(text=str(int(float(v)))))
length_slider.set(12)  # Default value
length_slider.grid(row=2, column=0, columnspan=2, pady=(0, 20))

# Character options section
options_label = ttk.Label(main_frame, text="Include:", font=("Arial", 11, "bold"))
options_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

# Create variables to store checkbox states (True/False)
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
exclude_ambiguous_var = tk.BooleanVar(value=False)

# Create checkboxes for each option
uppercase_check = ttk.Checkbutton(main_frame, text="Uppercase Letters (A-Z)", variable=uppercase_var)
uppercase_check.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=3)

lowercase_check = ttk.Checkbutton(main_frame, text="Lowercase Letters (a-z)", variable=lowercase_var)
lowercase_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=3)

numbers_check = ttk.Checkbutton(main_frame, text="Numbers (0-9)", variable=numbers_var)
numbers_check.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=3)

symbols_check = ttk.Checkbutton(main_frame, text="Symbols (!@#$%^&*)", variable=symbols_var)
symbols_check.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=3)

exclude_check = ttk.Checkbutton(main_frame, text="Exclude Ambiguous (0, O, l, 1, I)", variable=exclude_ambiguous_var)
exclude_check.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=3)

# Generate button
generate_button = ttk.Button(main_frame, text="Generate Password", command=generate_password)
generate_button.grid(row=9, column=0, columnspan=2, pady=(20, 10))

# Result section
result_frame = ttk.Frame(main_frame)
result_frame.grid(row=10, column=0, columnspan=2, pady=10)

# Text box to display the generated password
result_text = ttk.Entry(result_frame, width=35, font=("Courier", 12))
result_text.grid(row=0, column=0, padx=(0, 5))

# Copy button
copy_button = ttk.Button(result_frame, text="Copy", command=copy_to_clipboard, width=8)
copy_button.grid(row=0, column=1)

# Strength indicator label
strength_label = ttk.Label(main_frame, text="Strength: -", font=("Arial", 11, "bold"))
strength_label.grid(row=11, column=0, columnspan=2, pady=(5, 0))

# Start the application
window.mainloop()




