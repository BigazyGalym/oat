document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alerts
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.classList.add('opacity-0');
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);

    // Form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Button animations
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.add('animate-pulse');
            setTimeout(() => this.classList.remove('animate-pulse'), 600);
        });
        button.addEventListener('mouseover', function() {
            this.classList.add('transform', 'scale-105');
        });
        button.addEventListener('mouseout', function() {
            this.classList.remove('transform', 'scale-105');
        });
    });
});