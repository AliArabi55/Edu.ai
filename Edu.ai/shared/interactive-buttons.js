// Interactive Buttons JavaScript - Edu.ai
// This script adds hover and click effects to all buttons and clickable elements

document.addEventListener('DOMContentLoaded', function() {
    // Function to add interactive effects to elements
    function makeElementInteractive(element) {
        // Add transition effect
        element.style.transition = 'all 0.3s ease';
        element.style.cursor = 'pointer';
        
        // Store original styles
        const originalBoxShadow = element.style.boxShadow || 'none';
        
        // Mouse enter effect (hover) - بدون zoom
        element.addEventListener('mouseenter', function() {
            element.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
            element.style.filter = 'brightness(1.1)';
        });
        
        // Mouse leave effect
        element.addEventListener('mouseleave', function() {
            element.style.boxShadow = originalBoxShadow;
            element.style.filter = 'brightness(1)';
        });
        
        // Mouse down effect (click start) - بدون zoom
        element.addEventListener('mousedown', function() {
            element.style.boxShadow = '0 3px 10px rgba(0, 0, 0, 0.2)';
            element.style.filter = 'brightness(0.9)';
        });
        
        // Mouse up effect (click end)
        element.addEventListener('mouseup', function() {
            element.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
            element.style.filter = 'brightness(1.1)';
        });
    }
    
    // Find and make all buttons interactive
    const buttonSelectors = [
        'button',
        '.button',
        '.btn',
        '.frame',
        '.frame-2',
        '.frame-3',
        '.frame-4',
        '.frame-5',
        '.frame-6',
        '.frame-7',
        '.div-wrapper',
        '.group',
        '.text-wrapper',
        '.text-wrapper-2',
        '.text-wrapper-3',
        '.text-wrapper-4',
        '.text-wrapper-5',
        '.text-wrapper-6',
        '.text-wrapper-7',
        '.text-wrapper-8',
        '.text-wrapper-9',
        '.text-wrapper-10',
        '.text-wrapper-11',
        '.text-wrapper-12',
        '.text-wrapper-13',
        '.text-wrapper-14',
        '.text-wrapper-15',
        '.text-wrapper-16',
        '.text-wrapper-17',
        '.text-wrapper-18',
        '.text-wrapper-19',
        '.text-wrapper-20',
        '.text-wrapper-21',
        '.text-wrapper-22',
        '.text-wrapper-23',
        '.text-wrapper-24',
        '.text-wrapper-25',
        '.text-wrapper-26',
        '.text-wrapper-27',
        '.text-wrapper-28',
        '.text-wrapper-29',
        '.text-wrapper-30',
        '.text-wrapper-31',
        '.text-wrapper-32',
        '.text-wrapper-33',
        '.text-wrapper-34',
        '.text-wrapper-35',
        '.text-wrapper-36',
        '.text-wrapper-37',
        '.text-wrapper-38',
        '.text-wrapper-39',
        '.text-wrapper-40',
        '.text-wrapper-41',
        '.text-wrapper-42',
        '.text-wrapper-43',
        '.text-wrapper-44',
        '.text-wrapper-45',
        '.text-wrapper-46',
        '.text-wrapper-47',
        '.text-wrapper-48',
        '.text-wrapper-49',
        '.text-wrapper-50',
        '.text-wrapper-51',
        '.text-wrapper-52',
        '.text-wrapper-53',
        '.text-wrapper-54',
        '.text-wrapper-55',
        '[onclick]'
    ];
    
    // Apply interactive effects to all matching elements
    buttonSelectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            // Only make interactive if it has onclick or is a button
            if (element.onclick || element.tagName === 'BUTTON' || element.classList.contains('button') || element.classList.contains('btn') || element.hasAttribute('onclick')) {
                makeElementInteractive(element);
            }
        });
    });
    
    // Special effects for specific button types
    
    // Primary buttons (main action buttons)
    const primaryButtons = document.querySelectorAll('.frame, .div-wrapper, button, .button');
    primaryButtons.forEach(button => {
        if (button.onclick || button.hasAttribute('onclick')) {
            button.addEventListener('mouseenter', function() {
                this.style.background = 'linear-gradient(45deg, #4CAF50, #45a049)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.background = '';
            });
        }
    });
    
    // Navigation buttons
    const navButtons = document.querySelectorAll('.text-wrapper, .text-wrapper-2, .text-wrapper-3, .text-wrapper-4, .text-wrapper-5');
    navButtons.forEach(button => {
        if (button.onclick || button.hasAttribute('onclick')) {
            button.addEventListener('mouseenter', function() {
                this.style.color = '#4CAF50';
                this.style.fontWeight = 'bold';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.color = '';
                this.style.fontWeight = '';
            });
        }
    });
    
    // Add ripple effect for click
    function createRipple(event) {
        const button = event.currentTarget;
        const circle = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;
        
        circle.style.width = circle.style.height = diameter + 'px';
        circle.style.left = (event.clientX - button.offsetLeft - radius) + 'px';
        circle.style.top = (event.clientY - button.offsetTop - radius) + 'px';
        circle.classList.add('ripple');
        
        // Add ripple styles
        circle.style.position = 'absolute';
        circle.style.borderRadius = '50%';
        circle.style.transform = 'scale(0)';
        circle.style.animation = 'ripple 0.6s linear';
        circle.style.backgroundColor = 'rgba(255, 255, 255, 0.6)';
        circle.style.pointerEvents = 'none';
        
        const ripple = button.getElementsByClassName('ripple')[0];
        if (ripple) {
            ripple.remove();
        }
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(circle);
        
        setTimeout(() => {
            circle.remove();
        }, 600);
    }
    
    // Add ripple effect to all interactive buttons
    document.querySelectorAll('[onclick], button, .button, .btn').forEach(button => {
        button.addEventListener('click', createRipple);
    });
    
    // Add CSS animation for ripple effect - بدون zoom
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .interactive-button {
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .interactive-button:hover {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            filter: brightness(1.1);
        }
        
        .interactive-button:active {
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
            filter: brightness(0.9);
        }
        
        /* Glow effect for important buttons */
        .glow-button {
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from {
                box-shadow: 0 0 5px #4CAF50, 0 0 10px #4CAF50, 0 0 15px #4CAF50;
            }
            to {
                box-shadow: 0 0 10px #4CAF50, 0 0 20px #4CAF50, 0 0 30px #4CAF50;
            }
        }
        
        /* Pulse animation for call-to-action buttons - بدون zoom */
        .pulse-button {
            animation: pulse-glow 2s infinite;
        }
        
        @keyframes pulse-glow {
            0% {
                box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
            }
            50% {
                box-shadow: 0 0 20px rgba(0, 123, 255, 0.8);
            }
            100% {
                box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
            }
        }
        
        /* Bounce effect for success buttons */
        .bounce-button {
            animation: bounce 1s ease infinite;
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }
    `;
    document.head.appendChild(style);
    
    // Add special effects to specific buttons based on their content
    setTimeout(() => {
        // Glow effect for "Start" buttons
        const startButtons = document.querySelectorAll('*');
        startButtons.forEach(button => {
            const text = button.textContent.trim().toLowerCase();
            if (text.includes('start') || text.includes('begin') || text.includes('ابدأ')) {
                button.classList.add('glow-button');
            }
            
            // Pulse effect for main CTA buttons
            if (text.includes('today') || text.includes('now') || text.includes('الآن') || text.includes('اليوم')) {
                button.classList.add('pulse-button');
            }
            
            // Bounce effect for success/completion buttons
            if (text.includes('complete') || text.includes('finish') || text.includes('done') || text.includes('تم') || text.includes('انتهى')) {
                button.classList.add('bounce-button');
            }
        });
    }, 1000);
    
    console.log('🎉 Interactive buttons loaded successfully!');
});