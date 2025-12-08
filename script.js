// Wait for the HTML page to fully load before running our code
document.addEventListener('DOMContentLoaded', function() {
    
    // Get references to all the HTML elements we need to work with
    const lengthSlider = document.getElementById('lengthSlider');
    const lengthValue = document.getElementById('lengthValue');
    const uppercaseCheckbox = document.getElementById('uppercase');
    const lowercaseCheckbox = document.getElementById('lowercase');
    const numbersCheckbox = document.getElementById('numbers');
    const symbolsCheckbox = document.getElementById('symbols');
    const excludeAmbiguousCheckbox = document.getElementById('excludeAmbiguous');
    const generateBtn = document.getElementById('generateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const passwordOutput = document.getElementById('passwordOutput');
    const strengthBar = document.getElementById('strengthBar');
    const strengthText = document.getElementById('strengthText');

    // Define character sets for password generation
    const UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const LOWERCASE = 'abcdefghijklmnopqrstuvwxyz';
    const NUMBERS = '0123456789';
    const SYMBOLS = '!@#$%^&*()_+-=[]{}|;:,.<>?';
    const AMBIGUOUS = '0Ol1I';  // Characters that look similar

    // Update the displayed length value when slider moves
    lengthSlider.addEventListener('input', function() {
        lengthValue.textContent = lengthSlider.value;
    });

    // Generate password when button is clicked
    generateBtn.addEventListener('click', generatePassword);

    // Copy password when copy button is clicked
    copyBtn.addEventListener('click', copyToClipboard);

    // Also generate password when Enter key is pressed
    document.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            generatePassword();
        }
    });

    /**
     * Main function to generate a password based on user settings
     */
    function generatePassword() {
        // Get current settings from the form
        const length = parseInt(lengthSlider.value);
        const useUppercase = uppercaseCheckbox.checked;
        const useLowercase = lowercaseCheckbox.checked;
        const useNumbers = numbersCheckbox.checked;
        const useSymbols = symbolsCheckbox.checked;
        const excludeAmbiguous = excludeAmbiguousCheckbox.checked;

        // Build the character pool based on selected options
        let characters = '';
        
        if (useUppercase) {
            characters += UPPERCASE;
        }
        if (useLowercase) {
            characters += LOWERCASE;
        }
        if (useNumbers) {
            characters += NUMBERS;
        }
        if (useSymbols) {
            characters += SYMBOLS;
        }

        // Remove ambiguous characters if option is selected
        if (excludeAmbiguous) {
            for (let char of AMBIGUOUS) {
                characters = characters.replace(new RegExp(char, 'g'), '');
            }
        }

        // Check if at least one option is selected
        if (characters.length === 0) {
            passwordOutput.value = 'Please select at least one option!';
            resetStrengthIndicator();
            return;
        }

        // Generate the password by randomly selecting characters
        let password = '';
        for (let i = 0; i < length; i++) {
            // Get a random index from 0 to characters.length - 1
            const randomIndex = Math.floor(Math.random() * characters.length);
            // Add the character at that random index to our password
            password += characters[randomIndex];
        }

        // Display the generated password
        passwordOutput.value = password;

        // Calculate and display password strength
        calculateStrength(password, useUppercase, useLowercase, useNumbers, useSymbols);
    }

    /**
     * Calculates the strength of the generated password
     * @param {string} password - The password to evaluate
     * @param {boolean} hasUpper - Whether uppercase letters are included
     * @param {boolean} hasLower - Whether lowercase letters are included
     * @param {boolean} hasNum - Whether numbers are included
     * @param {boolean} hasSym - Whether symbols are included
     */
    function calculateStrength(password, hasUpper, hasLower, hasNum, hasSym) {
        let strength = 0;
        const length = password.length;

        // Award points based on password length
        if (length >= 16) {
            strength += 3;
        } else if (length >= 12) {
            strength += 2;
        } else if (length >= 8) {
            strength += 1;
        }

        // Award points for character variety
        if (hasUpper) strength += 1;
        if (hasLower) strength += 1;
        if (hasNum) strength += 1;
        if (hasSym) strength += 2;  // Symbols are worth more

        // Determine strength level and update UI
        if (strength <= 3) {
            updateStrengthUI('weak', 'Strength: Weak 🔴');
        } else if (strength <= 5) {
            updateStrengthUI('medium', 'Strength: Medium 🟡');
        } else {
            updateStrengthUI('strong', 'Strength: Strong 🟢');
        }
    }

    /**
     * Updates the visual strength indicator
     * @param {string} level - The strength level ('weak', 'medium', or 'strong')
     * @param {string} text - The text to display
     */
    function updateStrengthUI(level, text) {
        // Remove all previous strength classes
        strengthBar.classList.remove('weak', 'medium', 'strong');
        strengthText.classList.remove('weak', 'medium', 'strong');

        // Add the new strength class
        strengthBar.classList.add(level);
        strengthText.classList.add(level);
        strengthText.textContent = text;
    }

    /**
     * Resets the strength indicator to default state
     */
    function resetStrengthIndicator() {
        strengthBar.classList.remove('weak', 'medium', 'strong');
        strengthText.classList.remove('weak', 'medium', 'strong');
        strengthText.textContent = 'Strength: -';
    }

    /**
     * Copies the generated password to clipboard
     */
    function copyToClipboard() {
        const password = passwordOutput.value;

        // Check if there's a valid password to copy
        if (!password || password === 'Please select at least one option!') {
            return;
        }

        // Copy to clipboard using modern API
        navigator.clipboard.writeText(password).then(function() {
            // Show visual feedback that copy was successful
            copyBtn.textContent = '✓ Copied!';
            copyBtn.classList.add('copied');

            // Reset button after 2 seconds
            setTimeout(function() {
                copyBtn.textContent = '📋 Copy';
                copyBtn.classList.remove('copied');
            }, 2000);
        }).catch(function(err) {
            // Fallback method if modern API fails
            console.error('Failed to copy:', err);
            
            // Try older method
            passwordOutput.select();
            document.execCommand('copy');
            
            copyBtn.textContent = '✓ Copied!';
            setTimeout(function() {
                copyBtn.textContent = '📋 Copy';
            }, 2000);
        });
    }

    // Generate an initial password when page loads
    generatePassword();
});