// Top Cards JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {

    // Counter animation function
    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const increment = target / (duration / 16); // 60 FPS
        let current = start;

        const timer = setInterval(() => {
            current += increment;

            // Format number based on the element
            let displayValue;
            if (element.closest('.payments-card')) {
                // Format as currency
                displayValue = '$' + Math.floor(current).toLocaleString();
            } else {
                // Format as regular number
                displayValue = Math.floor(current).toLocaleString();
            }

            element.textContent = displayValue;

            if (current >= target) {
                // Ensure final value is exactly the target
                if (element.closest('.payments-card')) {
                    element.textContent = '$' + target.toLocaleString();
                } else {
                    element.textContent = target.toLocaleString();
                }
                clearInterval(timer);
                element.classList.add('animate');
            }
        }, 16);
    }

    // Initialize counters with Intersection Observer for better performance
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const numberElements = entry.target.querySelectorAll('.card-number');

                numberElements.forEach(element => {
                    const target = parseInt(element.getAttribute('data-target'));
                    animateCounter(element, target);
                });

                // Unobserve after animation starts
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Start observing the cards container
    const cardsContainer = document.querySelector('.top-cards-container');
    if (cardsContainer) {
        observer.observe(cardsContainer);
    }

    // Add hover effects
    const cards = document.querySelectorAll('.top-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.card-icon i');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
                icon.style.transition = 'transform 0.3s ease';
            }
        });

        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.card-icon i');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });

    // Add click effect
    cards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });

    // Real-time data simulation (optional)
    function simulateRealTimeUpdates() {
        const customerCard = document.querySelector('.customers-card .card-number');
        const paymentCard = document.querySelector('.payments-card .card-number');
        const orderCard = document.querySelector('.orders-card .card-number');

        setInterval(() => {
            // Simulate small random increases
            if (Math.random() > 0.7) { // 30% chance of update
                const customerIncrease = Math.floor(Math.random() * 3) + 1;
                const paymentIncrease = Math.floor(Math.random() * 500) + 100;
                const orderIncrease = Math.floor(Math.random() * 2) + 1;

                // Update data-target attributes
                const currentCustomers = parseInt(customerCard.getAttribute('data-target'));
                const currentPayments = parseInt(paymentCard.getAttribute('data-target'));
                const currentOrders = parseInt(orderCard.getAttribute('data-target'));

                customerCard.setAttribute('data-target', currentCustomers + customerIncrease);
                paymentCard.setAttribute('data-target', currentPayments + paymentIncrease);
                orderCard.setAttribute('data-target', currentOrders + orderIncrease);

                // Update display
                customerCard.textContent = (currentCustomers + customerIncrease).toLocaleString();
                paymentCard.textContent = '$' + (currentPayments + paymentIncrease).toLocaleString();
                orderCard.textContent = (currentOrders + orderIncrease).toLocaleString();

                // Add flash effect
                [customerCard, paymentCard, orderCard].forEach(card => {
                    card.style.color = '#4ade80';
                    setTimeout(() => {
                        card.style.color = '';
                    }, 1000);
                });
            }
        }, 10000); // Update every 10 seconds
    }

    // Uncomment the line below to enable real-time simulation
    // simulateRealTimeUpdates();
});
