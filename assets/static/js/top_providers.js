// Top Providers JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {

    // Animate progress bars
    function animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-fill');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const targetWidth = progressBar.getAttribute('data-progress') + '%';

                    // Reset width to 0 first
                    progressBar.style.width = '0%';

                    // Animate to target width after a short delay
                    setTimeout(() => {
                        progressBar.style.width = targetWidth;
                    }, 200);

                    // Unobserve after animation starts
                    observer.unobserve(progressBar);
                }
            });
        }, {
            threshold: 0.5,
            rootMargin: '0px 0px -50px 0px'
        });

        progressBars.forEach(bar => {
            observer.observe(bar);
        });
    }

    // Animate order numbers
    function animateOrderNumbers() {
        const statNumbers = document.querySelectorAll('.top-providers-container .stat-number');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const numberElement = entry.target;
                    const targetNumber = parseInt(numberElement.textContent.replace(/,/g, ''));

                    animateNumber(numberElement, targetNumber);
                    observer.unobserve(numberElement);
                }
            });
        }, {
            threshold: 0.5
        });

        statNumbers.forEach(number => {
            observer.observe(number);
        });
    }

    // Number animation function
    function animateNumber(element, target, duration = 1500) {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            element.textContent = Math.floor(current).toLocaleString();

            if (current >= target) {
                element.textContent = target.toLocaleString();
                clearInterval(timer);
            }
        }, 16);
    }

    // Add hover effects to provider items
    function addHoverEffects() {
        const providerItems = document.querySelectorAll('.provider-item');

        providerItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                const avatar = this.querySelector('.provider-avatar');
                const progressFill = this.querySelector('.progress-fill');

                if (avatar) {
                    avatar.style.transform = 'scale(1.1) rotate(5deg)';
                    avatar.style.background = 'rgba(255, 255, 255, 0.3)';
                }

                if (progressFill) {
                    progressFill.style.background = 'linear-gradient(90deg, #10b981, #059669)';
                }
            });

            item.addEventListener('mouseleave', function() {
                const avatar = this.querySelector('.provider-avatar');
                const progressFill = this.querySelector('.progress-fill');

                if (avatar) {
                    avatar.style.transform = 'scale(1) rotate(0deg)';
                    avatar.style.background = 'rgba(255, 255, 255, 0.2)';
                }

                if (progressFill) {
                    progressFill.style.background = 'linear-gradient(90deg, #4ade80, #22c55e)';
                }
            });

            // Add click effect
            item.addEventListener('click', function() {
                this.style.transform = 'translateY(-2px) scale(0.98)';
                setTimeout(() => {
                    this.style.transform = 'translateY(-2px) scale(1)';
                }, 150);
            });
        });
    }

    // Initialize all animations and effects
    function initializeProviders() {
        animateProgressBars();
        animateOrderNumbers();
        addHoverEffects();
    }

    // Start initialization
    initializeProviders();

    // Optional: Add real-time updates simulation
    function simulateRealTimeUpdates() {
        const statNumbers = document.querySelectorAll('.top-providers-container .stat-number');

        setInterval(() => {
            if (Math.random() > 0.8) { // 20% chance of update
                const randomIndex = Math.floor(Math.random() * statNumbers.length);
                const element = statNumbers[randomIndex];
                const currentValue = parseInt(element.textContent.replace(/,/g, ''));
                const increase = Math.floor(Math.random() * 10) + 1;

                element.style.color = '#4ade80';
                element.textContent = (currentValue + increase).toLocaleString();

                setTimeout(() => {
                    element.style.color = 'white';
                }, 2000);
            }
        }, 15000); // Update every 15 seconds
    }

    // Uncomment to enable real-time simulation
    // simulateRealTimeUpdates();
});
