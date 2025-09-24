// Navigation system for Edu.ai platform
class EduaiNavigation {
    constructor() {
        this.pages = [
            { id: 1, name: "الصفحة الرئيسية", path: "../1.Land page/index.html" },
            { id: 2, name: "تسجيل الدخول", path: "../2.Login/index.html" },
            { id: 3, name: "إنشاء حساب", path: "../3.Sign up/index.html" },
            { id: 4, name: "اختيار اللغة", path: "../4.select language/index.html" },
            { id: 5, name: "الكورسات", path: "../5.courses/index.html" },
            { id: 6, name: "بدء الدرس", path: "../6.Start Lesson/index.html" },
            { id: 7, name: "اختبار 1", path: "../7.Quiz 1/index.html" },
            { id: 8, name: "النتيجة", path: "../8.Score/index.html" }
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
        this.createNavigationButtons();
        this.addPageTransition();
        this.handleKeyboardNavigation();
    }

    createNavigationButtons() {
        // Remove existing navigation if present
        const existingNav = document.querySelector('.page-navigation');
        if (existingNav) {
            existingNav.remove();
        }

        const navContainer = document.createElement('div');
        navContainer.className = 'page-navigation';

        // Previous button
        if (this.currentPage > 1) {
            const prevButton = this.createButton('السابق', () => {
                this.navigateToPage(this.currentPage - 1);
            }, 'secondary');
            navContainer.appendChild(prevButton);
        }

        // Next button
        if (this.currentPage < this.pages.length) {
            const nextButton = this.createButton('التالي', () => {
                this.navigateToPage(this.currentPage + 1);
            }, 'primary');
            navContainer.appendChild(nextButton);
        }

        // Page indicator
        const pageIndicator = document.createElement('div');
        pageIndicator.className = 'page-indicator';
        pageIndicator.innerHTML = `
            <span style="
                background: rgba(255, 255, 255, 0.9);
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 500;
                color: #374151;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                margin-left: 10px;
            ">
                ${this.currentPage} من ${this.pages.length}
            </span>
        `;
        navContainer.appendChild(pageIndicator);

        document.body.appendChild(navContainer);
    }

    createButton(text, onClick, type = 'primary') {
        const button = document.createElement('button');
        button.className = `nav-button ${type}`;
        button.textContent = text;
        button.onclick = onClick;
        
        // Add loading state functionality
        button.addEventListener('click', () => {
            button.classList.add('loading');
            setTimeout(() => {
                button.classList.remove('loading');
            }, 1000);
        });

        return button;
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

    // Method to add quick jump menu
    addQuickJumpMenu() {
        const menuButton = document.createElement('button');
        menuButton.className = 'nav-button secondary';
        menuButton.style.position = 'fixed';
        menuButton.style.top = '30px';
        menuButton.style.right = '30px';
        menuButton.innerHTML = '☰';
        menuButton.title = 'قائمة التنقل السريع';

        const dropdown = document.createElement('div');
        dropdown.style.cssText = `
            position: absolute;
            top: 100%;
            right: 0;
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            padding: 8px 0;
            min-width: 200px;
            display: none;
            z-index: 1000;
            margin-top: 8px;
        `;

        this.pages.forEach(page => {
            const option = document.createElement('button');
            option.style.cssText = `
                width: 100%;
                padding: 12px 16px;
                text-align: right;
                border: none;
                background: ${page.id === this.currentPage ? '#f3f4f6' : 'transparent'};
                color: ${page.id === this.currentPage ? '#2563eb' : '#374151'};
                font-family: inherit;
                font-size: 14px;
                cursor: pointer;
            `;
            option.textContent = `${page.id}. ${page.name}`;
            option.onclick = () => {
                if (page.id !== this.currentPage) {
                    this.navigateToPage(page.id);
                }
                dropdown.style.display = 'none';
            };
            
            option.onmouseover = () => {
                if (page.id !== this.currentPage) {
                    option.style.backgroundColor = '#f9fafb';
                }
            };
            
            option.onmouseout = () => {
                if (page.id !== this.currentPage) {
                    option.style.backgroundColor = 'transparent';
                }
            };
            
            dropdown.appendChild(option);
        });

        menuButton.appendChild(dropdown);
        
        menuButton.onclick = (e) => {
            e.stopPropagation();
            dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
        };

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            dropdown.style.display = 'none';
        });

        menuButton.style.position = 'relative';
        document.body.appendChild(menuButton);
    }
}

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const navigation = new EduaiNavigation();
    
    // Add quick jump menu after a delay
    setTimeout(() => {
        navigation.addQuickJumpMenu();
    }, 1000);
});

// Add some utility functions for enhanced interactivity
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
                document.body.removeChild(notification);
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