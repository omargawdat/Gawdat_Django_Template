// Contact Messages JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {

    // View message function
    window.viewMessage = function(messageId) {
        // This would typically open a modal or navigate to a detailed view
        console.log('Viewing message:', messageId);

        // For demo purposes, show an alert
        // In a real implementation, you'd make an AJAX call or open a modal
        alert(`Viewing message #${messageId}\n\nIn a real implementation, this would open a detailed view of the message.`);
    };

    // Mark message as read function
    window.markAsRead = function(messageId) {
        const messageItem = document.querySelector(`[data-message-id="${messageId}"]`);

        // Simulate AJAX call to mark as read
        // In a real implementation, you'd make a POST request to your Django view
        console.log('Marking message as read:', messageId);

        // Visual feedback
        const button = event.target.closest('.mark-read-btn');
        if (button) {
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Marking...';
            button.disabled = true;

            // Simulate server response after 1 second
            setTimeout(() => {
                // Remove unread class and badge
                const messageElement = button.closest('.message-item');
                if (messageElement) {
                    messageElement.classList.remove('unread');

                    // Remove unread badge
                    const unreadBadge = messageElement.querySelector('.unread-badge');
                    if (unreadBadge) {
                        unreadBadge.remove();
                    }

                    // Remove the mark as read button
                    button.remove();

                    // Show success feedback
                    showNotification('Message marked as read!', 'success');
                }
            }, 1000);
        }
    };

    // Show notification function
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : '#3b82f6'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Add hover effects to message items
    const messageItems = document.querySelectorAll('.message-item');
    messageItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const avatar = this.querySelector('.customer-avatar');
            if (avatar) {
                avatar.style.transform = 'scale(1.1)';
                avatar.style.background = 'rgba(255, 255, 255, 0.3)';
            }
        });

        item.addEventListener('mouseleave', function() {
            const avatar = this.querySelector('.customer-avatar');
            if (avatar) {
                avatar.style.transform = 'scale(1)';
                avatar.style.background = 'rgba(255, 255, 255, 0.2)';
            }
        });
    });

    // View all messages button functionality
    const viewAllBtn = document.querySelector('.view-all-btn');
    if (viewAllBtn) {
        viewAllBtn.addEventListener('click', function() {
            // This would typically navigate to a full messages page
            console.log('Navigating to all messages page');

            // For demo purposes
            alert('This would navigate to a full messages management page.');
        });
    }

    // Auto-refresh messages every 30 seconds (optional)
    function autoRefreshMessages() {
        setInterval(() => {
            // In a real implementation, you'd make an AJAX call to check for new messages
            console.log('Checking for new messages...');

            // Simulate new message notification
            if (Math.random() > 0.95) { // 5% chance
                showNotification('New message received!', 'info');
            }
        }, 30000);
    }

    // Uncomment to enable auto-refresh
    // autoRefreshMessages();
});
