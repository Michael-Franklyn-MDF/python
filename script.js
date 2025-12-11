// Wait for the HTML page to fully load before running our code
document.addEventListener('DOMContentLoaded', function() {
        // ========== DARK MODE FUNCTIONALITY - START ==========
        
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const body = document.body;
        
        // Load saved theme from localStorage on page load
        function loadTheme() {
            const savedTheme = localStorage.getItem('theme');
            
            if (savedTheme === 'dark') {
                body.classList.add('dark-mode');
                themeIcon.textContent = '☀️';
            } else {
                body.classList.remove('dark-mode');
                themeIcon.textContent = '🌙';
            }
        }
        
        // Toggle between light and dark mode
        function toggleTheme() {
            body.classList.toggle('dark-mode');
            
            // Update icon and save preference
            if (body.classList.contains('dark-mode')) {
                themeIcon.textContent = '☀️';
                localStorage.setItem('theme', 'dark');
            } else {
                themeIcon.textContent = '🌙';
                localStorage.setItem('theme', 'light');
            }
        }
        
        // Add click event to toggle button
        themeToggle.addEventListener('click', toggleTheme);
        
        // Load theme when page first loads
        loadTheme();
        
        // ========== DARK MODE FUNCTIONALITY - END ==========

        // Load theme when page first loads
    loadTheme();
    
    // ========== DARK MODE FUNCTIONALITY - END ==========
    
    // ========== PASSWORD HISTORY FUNCTIONALITY - START ==========
    
    const historyContainer = document.getElementById('historyContainer');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    const MAX_HISTORY_ITEMS = 10; // Store up to 10 passwords
    
    /**
     * Load password history from localStorage
     * @returns {Array} Array of password history objects
     */
    function loadHistory() {
        try {
            const history = localStorage.getItem('passwordHistory');
            return history ? JSON.parse(history) : [];
        } catch (error) {
            console.error('Error loading history:', error);
            return [];
        }
    }
    
    /**
     * Save password history to localStorage
     * @param {Array} history - Array of password objects to save
     */
    function saveHistory(history) {
        try {
            localStorage.setItem('passwordHistory', JSON.stringify(history));
        } catch (error) {
            console.error('Error saving history:', error);
            // Handle quota exceeded error
            if (error.name === 'QuotaExceededError') {
                alert('Storage limit reached. Clearing old passwords...');
                // Keep only the last 5 items
                const trimmedHistory = history.slice(0, 5);
                localStorage.setItem('passwordHistory', JSON.stringify(trimmedHistory));
            }
        }
    }
    
    /**
     * Add a new password to history
     * @param {string} password - The generated password
     * @param {number} length - Password length
     * @param {string} strength - Password strength (weak, medium, strong)
     */
    function addToHistory(password, length, strength) {
        const history = loadHistory();
        
        // Create new history item
        const historyItem = {
            id: Date.now(), // Unique ID using timestamp
            password: password,
            timestamp: new Date().toISOString(),
            length: length,
            strength: strength
        };
        
        // Add to beginning of array (newest first)
        history.unshift(historyItem);
        
        // Keep only MAX_HISTORY_ITEMS
        if (history.length > MAX_HISTORY_ITEMS) {
            history.pop(); // Remove oldest item
        }
        
        // Save and update display
        saveHistory(history);
        displayHistory();
    }
    
    /**
     * Format timestamp to readable format (e.g., "2 mins ago")
     * @param {string} timestamp - ISO timestamp string
     * @returns {string} Formatted time difference
     */
    function formatTimestamp(timestamp) {
        const now = new Date();
        const past = new Date(timestamp);
        const diffMs = now - past;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
        if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    }
    
    /**
     * Get strength emoji based on strength level
     * @param {string} strength - Strength level (weak, medium, strong)
     * @returns {string} Emoji representing strength
     */
    function getStrengthEmoji(strength) {
        switch(strength) {
            case 'weak': return '🔴';
            case 'medium': return '🟡';
            case 'strong': return '🟢';
            default: return '⚪';
        }
    }
    
    /**
     * Display password history in the UI
     */
    function displayHistory() {
        const history = loadHistory();
        
        // Clear container
        historyContainer.innerHTML = '';
        
        // Show empty state if no history
        if (history.length === 0) {
            historyContainer.innerHTML = '<p class="history-empty">No passwords generated yet. Generate your first password!</p>';
            return;
        }
        
        // Create history items
        history.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.dataset.id = item.id;
            
            historyItem.innerHTML = `
                <div class="history-password">
                    <div class="history-password-text">${item.password}</div>
                    <div class="history-meta">
                        <span class="history-timestamp">🕐 ${formatTimestamp(item.timestamp)}</span>
                        <span class="history-length">📏 ${item.length} chars</span>
                    </div>
                </div>
                <span class="history-strength" title="Strength: ${item.strength}">${getStrengthEmoji(item.strength)}</span>
                <div class="history-actions">
                    <button class="history-copy-btn" data-password="${item.password}">📋 Copy</button>
                    <button class="history-delete-btn" data-id="${item.id}">🗑️</button>
                </div>
            `;
            
            historyContainer.appendChild(historyItem);
        });
        
        // Add event listeners to copy buttons
        document.querySelectorAll('.history-copy-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const password = this.dataset.password;
                copyPasswordFromHistory(password, this);
            });
        });
        
        // Add event listeners to delete buttons
        document.querySelectorAll('.history-delete-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = parseInt(this.dataset.id);
                deleteHistoryItem(id);
            });
        });
    }
    
    /**
     * Copy password from history to clipboard
     * @param {string} password - Password to copy
     * @param {HTMLElement} button - The button element that was clicked
     */
    function copyPasswordFromHistory(password, button) {
        navigator.clipboard.writeText(password).then(function() {
            // Visual feedback
            const originalText = button.textContent;
            button.textContent = '✓ Copied!';
            button.classList.add('copied');
            
            // Reset after 2 seconds
            setTimeout(function() {
                button.textContent = originalText;
                button.classList.remove('copied');
            }, 2000);
        }).catch(function(err) {
            console.error('Failed to copy:', err);
            alert('Failed to copy password');
        });
    }
    
    /**
     * Delete a single history item
     * @param {number} id - ID of the item to delete
     */
    function deleteHistoryItem(id) {
        let history = loadHistory();
        history = history.filter(item => item.id !== id);
        saveHistory(history);
        displayHistory();
    }
    
    /**
     * Clear all history
     */
    function clearAllHistory() {
        if (confirm('Are you sure you want to clear all password history?')) {
            localStorage.removeItem('passwordHistory');
            displayHistory();
        }
    }
    
    // Event listener for clear all button
    clearHistoryBtn.addEventListener('click', clearAllHistory);
    
    // Display history on page load
    displayHistory();
    
    // ========== PASSWORD HISTORY FUNCTIONALITY - END ==========
    
    // ========== PASSPHRASE WORD LIST - START ==========
    
    const WORD_LIST = [
        // Animals
        'cat', 'dog', 'lion', 'tiger', 'bear', 'wolf', 'eagle', 'shark', 'dragon', 'phoenix',
        'rabbit', 'horse', 'elephant', 'dolphin', 'penguin', 'falcon', 'panther', 'leopard',
        'cheetah', 'rhino', 'zebra', 'giraffe', 'monkey', 'gorilla', 'whale', 'octopus',
        
        // Colors
        'red', 'blue', 'green', 'purple', 'orange', 'silver', 'gold', 'crimson', 'azure',
        'emerald', 'violet', 'amber', 'coral', 'ivory', 'jade', 'ruby', 'topaz', 'onyx',
        
        // Nature
        'ocean', 'mountain', 'forest', 'river', 'cloud', 'storm', 'thunder', 'sunset',
        'rainbow', 'garden', 'meadow', 'valley', 'canyon', 'desert', 'glacier', 'volcano',
        'spring', 'summer', 'autumn', 'winter', 'breeze', 'wind', 'rain', 'snow',
        
        // Objects
        'table', 'chair', 'laptop', 'phone', 'camera', 'robot', 'rocket', 'castle',
        'bridge', 'tower', 'diamond', 'crystal', 'mirror', 'lamp', 'clock', 'compass',
        'anchor', 'shield', 'sword', 'arrow', 'crown', 'throne', 'wagon', 'ship',
        
        // Actions/Verbs
        'jump', 'run', 'dance', 'swim', 'fly', 'create', 'build', 'dream', 'think',
        'laugh', 'smile', 'sing', 'write', 'paint', 'climb', 'explore', 'discover',
        
        // Adjectives
        'quick', 'brave', 'wise', 'happy', 'strong', 'bright', 'swift', 'bold',
        'calm', 'fierce', 'gentle', 'mighty', 'noble', 'royal', 'silent', 'wild',
        
        // Food
        'pizza', 'coffee', 'apple', 'bread', 'honey', 'berry', 'mango', 'lemon',
        'cherry', 'peach', 'grape', 'melon', 'banana', 'orange', 'coconut',
        
        // Tech/Modern
        'cyber', 'digital', 'quantum', 'neural', 'binary', 'data', 'pixel', 'byte',
        'code', 'cloud', 'network', 'signal', 'pulse', 'matrix', 'nexus', 'core',
        
        // Abstract/Misc
        'magic', 'shadow', 'light', 'star', 'moon', 'sun', 'time', 'space', 'future',
        'power', 'energy', 'spirit', 'soul', 'cosmos', 'zenith', 'echo', 'mystic',
        'legend', 'myth', 'hero', 'quest', 'journey', 'destiny', 'fortune', 'glory',
        
        // Places
        'city', 'town', 'village', 'island', 'temple', 'palace', 'fortress', 'harbor',
        'square', 'avenue', 'street', 'plaza', 'market', 'academy', 'library', 'arena',
        
        // Elements
        'fire', 'water', 'earth', 'metal', 'stone', 'wood', 'ice', 'flame', 'frost',
        'spark', 'blaze', 'steam', 'smoke', 'mist', 'fog', 'dew', 'ash',
        
        // Celestial
        'comet', 'meteor', 'planet', 'galaxy', 'nebula', 'cosmos', 'stellar', 'lunar',
        'solar', 'astral', 'orbit', 'eclipse', 'aurora', 'zenith', 'nova',
        
        // Emotions/States
        'joy', 'peace', 'hope', 'faith', 'truth', 'trust', 'courage', 'honor',
        'grace', 'charm', 'valor', 'pride', 'glory', 'victory', 'triumph'
    ];
    
    // ========== PASSPHRASE WORD LIST - END ==========
       
    // Get references to all the HTML elements we need to work with
    const lengthSlider = document.getElementById('lengthSlider');
    // ... rest of your existing code continues here
    // Get references to HTML elements
    const lengthValue = document.getElementById('lengthValue');
    const uppercaseCheckbox = document.getElementById('uppercaseCheck');
    const lowercaseCheckbox = document.getElementById('lowercaseCheck');
    const numbersCheckbox = document.getElementById('numbersCheck');
    const symbolsCheckbox = document.getElementById('symbolsCheck');
    const excludeAmbiguousCheckbox = document.getElementById('excludeAmbiguous');
    const generateBtn = document.getElementById('generateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const passwordOutput = document.getElementById('passwordOutput');
    const strengthBar = document.getElementById('strengthBar');
    const strengthText = document.getElementById('strengthText');

    // ========== NEW: PASSPHRASE ELEMENT REFERENCES - START ==========
    const randomTab = document.getElementById('randomTab');
    const passphraseTab = document.getElementById('passphraseTab');
    const randomSettings = document.getElementById('randomSettings');
    const passphraseSettings = document.getElementById('passphraseSettings');
    const wordCountSlider = document.getElementById('wordCountSlider');
    const wordCountValue = document.getElementById('wordCountValue');
    const passphraseNumbersCheck = document.getElementById('passphraseNumbers');
    const passphraseSymbolsCheck = document.getElementById('passphraseSymbols');
    const exampleText = document.getElementById('exampleText');
    
    // Track current mode
    let currentMode = 'random'; // 'random' or 'passphrase'
    // ========== NEW: PASSPHRASE ELEMENT REFERENCES - END ==========

    // ========== MODE SWITCHING FUNCTIONALITY - START ==========
    
    /**
     * Switch between Random and Passphrase modes
     * @param {string} mode - 'random' or 'passphrase'
     */
    function switchMode(mode) {
        currentMode = mode;
        
        // Update tab buttons
        if (mode === 'random') {
            randomTab.classList.add('active');
            passphraseTab.classList.remove('active');
            randomSettings.style.display = 'block';
            passphraseSettings.style.display = 'none';
            generateBtn.textContent = 'Generate Password';
        } else {
            passphraseTab.classList.add('active');
            randomTab.classList.remove('active');
            passphraseSettings.style.display = 'block';
            randomSettings.style.display = 'none';
            generateBtn.textContent = 'Generate Passphrase';
            updatePassphraseExample();
        }
        
        // Clear current password and reset strength
        passwordOutput.value = '';
        resetStrengthIndicator();
    }
    
    // Add click events to tabs
    randomTab.addEventListener('click', () => switchMode('random'));
    passphraseTab.addEventListener('click', () => switchMode('passphrase'));
    
    // ========== MODE SWITCHING FUNCTIONALITY - END ==========
    
        // ========== PASSPHRASE GENERATION FUNCTIONALITY - START ==========
    
    /**
     * Update the word count display when slider moves
     */
    wordCountSlider.addEventListener('input', function() {
        wordCountValue.textContent = wordCountSlider.value;
        updatePassphraseExample();
    });
    
    /**
     * Update example when any passphrase setting changes
     */
    document.querySelectorAll('input[name="separator"]').forEach(radio => {
        radio.addEventListener('change', updatePassphraseExample);
    });
    
    document.querySelectorAll('input[name="capitalize"]').forEach(radio => {
        radio.addEventListener('change', updatePassphraseExample);
    });
    
    passphraseNumbersCheck.addEventListener('change', updatePassphraseExample);
    passphraseSymbolsCheck.addEventListener('change', updatePassphraseExample);
    
    /**
     * Generate example passphrase preview
     */
    function updatePassphraseExample() {
        const wordCount = parseInt(wordCountSlider.value);
        const separator = document.querySelector('input[name="separator"]:checked').value;
        const capitalize = document.querySelector('input[name="capitalize"]:checked').value;
        const addNumbers = passphraseNumbersCheck.checked;
        const addSymbols = passphraseSymbolsCheck.checked;
        
        // Generate example (client-side, just for preview)
        const exampleWords = [];
        for (let i = 0; i < wordCount; i++) {
            const randomWord = WORD_LIST[Math.floor(Math.random() * WORD_LIST.length)];
            exampleWords.push(randomWord);
        }
        
        // Apply capitalization
        let processedWords = exampleWords.map(word => {
            if (capitalize === 'title') return word.charAt(0).toUpperCase() + word.slice(1);
            if (capitalize === 'upper') return word.toUpperCase();
            return word.toLowerCase();
        });
        
        // Build example
        let example = processedWords.join(separator);
        if (addNumbers) example += '42';
        if (addSymbols) example += '!';
        
        exampleText.textContent = example;
    }
    
    /**
     * Generate passphrase using backend API
     */
    function generatePassphrase() {
        const wordCount = parseInt(wordCountSlider.value);
        const separator = document.querySelector('input[name="separator"]:checked').value;
        const capitalize = document.querySelector('input[name="capitalize"]:checked').value;
        const addNumbers = passphraseNumbersCheck.checked;
        const addSymbols = passphraseSymbolsCheck.checked;
        
        // Call backend API
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        
        fetch('/api/generate-passphrase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                wordCount,
                separator,
                addNumbers,
                addSymbols,
                capitalize
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to generate passphrase');
            }
            return response.json();
        })
        .then(data => {
            const passphrase = data.passphrase || '';
            passwordOutput.value = passphrase;
            
            // Calculate strength for passphrase
            const strength = calculatePassphraseStrength(passphrase, wordCount, addNumbers, addSymbols);
            updateStrengthUI(strength, `Strength: ${strength.charAt(0).toUpperCase() + strength.slice(1)} ${strength === 'weak' ? '🔴' : strength === 'medium' ? '🟡' : '🟢'}`);
            
            // Add to history
            addToHistory(passphrase, passphrase.length, strength);
        })
        .catch(error => {
            console.error(error);
            passwordOutput.value = 'Error generating passphrase';
            resetStrengthIndicator();
        })
        .finally(() => {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Passphrase';
        });
    }
    
    /**
     * Calculate strength for passphrases
     * @param {string} passphrase - The passphrase to evaluate
     * @param {number} wordCount - Number of words
     * @param {boolean} hasNumbers - Has numbers
     * @param {boolean} hasSymbols - Has symbols
     * @returns {string} 'weak', 'medium', or 'strong'
     */
    function calculatePassphraseStrength(passphrase, wordCount, hasNumbers, hasSymbols) {
        let strength = 0;
        
        // Word count is most important for passphrases
        if (wordCount >= 5) strength += 3;
        else if (wordCount >= 4) strength += 2;
        else strength += 1;
        
        // Length bonus
        if (passphrase.length >= 30) strength += 2;
        else if (passphrase.length >= 20) strength += 1;
        
        // Additional character types
        if (hasNumbers) strength += 1;
        if (hasSymbols) strength += 1;
        
        // Determine overall strength
        if (strength <= 3) return 'weak';
        if (strength <= 5) return 'medium';
        return 'strong';
    }
    
    // ========== PASSPHRASE GENERATION FUNCTIONALITY - END ==========


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
     * Main function to generate password or passphrase based on current mode
     */
    function generatePassword() {
        // Check which mode we're in
        if (currentMode === 'passphrase') {
            generatePassphrase();
            return;
        }
        
        // Original random password generation
        const length = parseInt(lengthSlider.value);
        const useUppercase = uppercaseCheckbox.checked;
        const useLowercase = lowercaseCheckbox.checked;
        const useNumbers = numbersCheckbox.checked;
        const useSymbols = symbolsCheckbox.checked;
        const excludeAmbiguous = excludeAmbiguousCheckbox.checked;

        // Check if at least one option is selected
        if (!useUppercase && !useLowercase && !useNumbers && !useSymbols) {
            passwordOutput.value = 'Please select at least one option!';
            resetStrengthIndicator();
            return;
        }

        // Call backend API to generate password
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';

        fetch('/api/generate-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                length,
                useUppercase,
                useLowercase,
                useNumbers,
                useSymbols,
                excludeAmbiguous
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to generate password');
            }
            return response.json();
        })
        .then(data => {
            const password = data.password || '';
            passwordOutput.value = password;
            calculateStrength(password, useUppercase, useLowercase, useNumbers, useSymbols);

            // Get the current strength level from the UI
            const strengthLevel = strengthText.textContent.includes('Weak') ? 'weak' :
                                 strengthText.textContent.includes('Medium') ? 'medium' : 'strong';
            
            // Add to history
            addToHistory(password, length, strengthLevel);
        })
        .catch(error => {
            console.error(error);
            passwordOutput.value = 'Error generating password';
            resetStrengthIndicator();
        })
        .finally(() => {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Password';
        });
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
    
    // Initialize passphrase example
    updatePassphraseExample();
});
