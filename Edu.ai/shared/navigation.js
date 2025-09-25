// Enhanced navigation system for Edu.ai platform - Original Design Buttons Only
class EduaiNavigation {
    constructor() {
        this.pages = [
            { id: 1, name: "Landing Page", path: "../1.Land page/index.html" },
            { id: 2, name: "Login", path: "../2.Login/index.html" },
            { id: 3, name: "Sign Up", path: "../3.Sign up/index.html" },
            { id: 4, name: "Select Language", path: "../4.select language/index.html" },
            { id: 5, name: "Courses", path: "../5.courses/index.html" },
            { id: 6, name: "Start Lesson", path: "../6.Start Lesson/index.html" },
            { id: 7, name: "Quiz 1", path: "../7.Quiz 1/index.html" },
            { id: 8, name: "Score", path: "../8.Score/index.html" }
        ];
        
        this.currentPage = this.getCurrentPageId();
        this.init();
    }

    getCurrentPageId() {
        const path = window.location.pathname;
        const pathSegments = path.split('/');
        
        // Extract page number from folder name
        for (let segment of pathSegments) {
            if (segment.includes('.')) {
                const match = segment.match(/(\d+)\./);
                if (match) {
                    return parseInt(match[1]);
                }
            }
        }
        
        return 1; // Default to first page
    }

    init() {
        // Only add page transitions and utility functions
        // NO floating navigation buttons
        this.addPageTransition();
        this.handleKeyboardNavigation();
        this.enhanceOriginalButtons();
    }

    enhanceOriginalButtons() {
        // Add smooth transitions to all clickable elements
        const clickableElements = document.querySelectorAll('[onclick], [href], button, .frame, .component');
        clickableElements.forEach(element => {
            element.style.transition = 'all 0.3s ease';
        });
    }

    addPageTransition() {
        // Add entrance animation
        document.addEventListener('DOMContentLoaded', () => {
            document.body.style.opacity = '0';
            document.body.style.transform = 'translateY(20px)';
            document.body.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                document.body.style.opacity = '1';
                document.body.style.transform = 'translateY(0)';
            }, 100);
        });
    }

    handleKeyboardNavigation() {
        // Keep keyboard shortcuts for power users
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey) {
                switch(e.key) {
                    case 'ArrowLeft':
                        e.preventDefault();
                        if (this.currentPage > 1) {
                            this.navigateToPage(this.currentPage - 1);
                        }
                        break;
                    case 'ArrowRight':
                        e.preventDefault();
                        if (this.currentPage < this.pages.length) {
                            this.navigateToPage(this.currentPage + 1);
                        }
                        break;
                    case 'Home':
                        e.preventDefault();
                        this.navigateToPage(1);
                        break;
                    case 'End':
                        e.preventDefault();
                        this.navigateToPage(this.pages.length);
                        break;
                }
            }
        });
    }

    navigateToPage(pageId) {
        if (pageId < 1 || pageId > this.pages.length) {
            return;
        }

        const targetPage = this.pages[pageId - 1];
        
        // Add page transition effect
        document.body.style.opacity = '0.7';
        document.body.style.transform = 'scale(0.98)';
        document.body.style.transition = 'all 0.3s ease';

        setTimeout(() => {
            window.location.href = targetPage.path;
        }, 300);
    }
}

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const navigation = new EduaiNavigation();
});

// Utility functions for enhanced interactivity
window.EduaiUtils = {
    // Show notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#2563eb'};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-family: 'Poppins', sans-serif;
            font-size: 14px;
            z-index: 2000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            animation: slideDown 0.3s ease;
        `;
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideUp 0.3s ease';
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    },

    // Add loading state to any element
    addLoadingState(element) {
        element.classList.add('loading');
        return () => element.classList.remove('loading');
    },

    // Smooth scroll to element
    scrollToElement(selector) {
        const element = document.querySelector(selector);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    }
};

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from { transform: translateX(-50%) translateY(-100%); opacity: 0; }
        to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
    
    @keyframes slideUp {
        from { transform: translateX(-50%) translateY(0); opacity: 1; }
        to { transform: translateX(-50%) translateY(-100%); opacity: 0; }
    }
`;
document.head.appendChild(style);