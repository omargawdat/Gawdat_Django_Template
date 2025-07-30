// Line Chart JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {

    // Generate fake data for the last 30 days
    function generateFakeData() {
        const data = [];
        const labels = [];
        const today = new Date();

        for (let i = 29; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);

            // Format date as MM/DD
            const label = (date.getMonth() + 1).toString().padStart(2, '0') + '/' +
                         date.getDate().toString().padStart(2, '0');
            labels.push(label);

            // Generate realistic revenue data with some trend and randomness
            const baseValue = 2500;
            const trend = i * 50; // Upward trend
            const randomness = (Math.random() - 0.5) * 800;
            const value = Math.max(1000, baseValue + trend + randomness);

            data.push(Math.round(value));
        }

        return { labels, data };
    }

    // Initialize the line chart
    function initLineChart() {
        const canvas = document.getElementById('revenueLineChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const { labels, data } = generateFakeData();

        // Create gradient
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.4)');
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0.05)');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Revenue ($)',
                    data: data,
                    borderColor: '#ffffff',
                    backgroundColor: gradient,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: 'rgba(255, 255, 255, 0.8)',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    pointHoverBackgroundColor: '#ffffff',
                    pointHoverBorderColor: 'rgba(255, 255, 255, 0.9)',
                    pointHoverBorderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        titleColor: '#1f2937',
                        bodyColor: '#6b7280',
                        borderColor: 'rgba(255, 255, 255, 0.3)',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: false,
                        callbacks: {
                            title: function(context) {
                                return 'Date: ' + context[0].label;
                            },
                            label: function(context) {
                                return 'Revenue: $' + context.parsed.y.toLocaleString();
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.2)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.8)',
                            font: {
                                size: 12
                            },
                            maxTicksLimit: 8
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.2)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.8)',
                            font: {
                                size: 12
                            },
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                },
                elements: {
                    point: {
                        hoverRadius: 8
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    // Load Chart.js if not already loaded
    if (typeof Chart === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.min.js';
        script.onload = initLineChart;
        document.head.appendChild(script);
    } else {
        initLineChart();
    }
});
