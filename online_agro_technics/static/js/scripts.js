function initMap() {
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: { lat: 55.7558, lng: 37.6173 }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('ordersChart')?.getContext('2d');
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
                datasets: [{
                    label: 'Завершённые заказы',
                    data: [10, 15, 20, 25, 30, 35],
                    backgroundColor: 'rgba(46, 125, 50, 0.8)',
                    borderColor: 'rgba(27, 94, 32, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: { y: { beginAtZero: true } },
                animation: { duration: 1000, easing: 'easeInOutQuad' }
            }
        });
    }

    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.add('animate-pulse');
            setTimeout(() => this.classList.remove('animate-pulse'), 600);
        });
        button.addEventListener('mouseover', function() {
            this.classList.add('hover:scale-105');
        });
        button.addEventListener('mouseout', function() {
            this.classList.remove('hover:scale-105');
        });
    });
});