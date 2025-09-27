// Avatar Controller Script
// This script handles the connection between the web interface and Avatar.py

class AvatarController {
    constructor() {
        this.isRunning = false;
        this.avatarProcess = null;
    }

    async startAvatar() {
        if (this.isRunning) {
            console.log('Avatar is already running');
            return;
        }

        try {
            // Show loading indicator
            this.showLoading(true);
            
            // Make a request to start the Python Avatar script
            const response = await fetch('/start-avatar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'start',
                    script_path: '../6.2/Avatar.py'
                })
            });

            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    this.isRunning = true;
                    this.showStatus('Avatar started successfully!', 'success');
                    // Redirect to the Avatar interface after 2 seconds
                    setTimeout(() => {
                        window.location.href = '../6.2/index.html';
                    }, 2000);
                } else {
                    this.showStatus('Failed to start Avatar: ' + result.error, 'error');
                }
            } else {
                this.showStatus('Server error: Unable to start Avatar', 'error');
            }
        } catch (error) {
            console.error('Error starting Avatar:', error);
            this.showStatus('Error: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    showLoading(show) {
        const loadingElement = document.getElementById('loading-indicator');
        if (loadingElement) {
            loadingElement.style.display = show ? 'block' : 'none';
        }
    }

    showStatus(message, type) {
        const statusElement = document.getElementById('status-message');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `status-message ${type}`;
            statusElement.style.display = 'block';
            
            // Hide after 5 seconds
            setTimeout(() => {
                statusElement.style.display = 'none';
            }, 5000);
        }
    }

    // Alternative method: Direct redirect to Avatar server
    async startAvatarDirect() {
        try {
            this.showLoading(true);
            this.showStatus('Starting Sam, your AI teacher...', 'info');
            
            // Redirect to the Avatar web server
            setTimeout(() => {
                this.showStatus('Redirecting to Sam Avatar interface...', 'success');
                setTimeout(() => {
                    window.location.href = 'http://localhost:5000';
                }, 1500);
            }, 2000);
            
        } catch (error) {
            console.error('Error:', error);
            this.showStatus('Error starting Avatar: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }
}

// Initialize the controller when the page loads
document.addEventListener('DOMContentLoaded', function() {
    window.avatarController = new AvatarController();
    
    // Add event listeners to Start button
    const startButton = document.querySelector('.frame');
    if (startButton) {
        startButton.onclick = function(e) {
            e.preventDefault();
            window.avatarController.startAvatarDirect();
        };
    }
});

// Utility functions for server interaction
async function checkPythonDependencies() {
    const dependencies = [
        'azure-ai-voicelive',
        'pyaudio', 
        'python-dotenv',
        'azure-core',
        'azure-identity'
    ];
    
    console.log('Required Python dependencies:');
    dependencies.forEach(dep => console.log(`- ${dep}`));
    
    return dependencies;
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AvatarController;
}