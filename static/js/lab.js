document.addEventListener('DOMContentLoaded', () => {

    /* --- TOAST NOTIFICATIONS --- */
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        // Auto-dismiss after 4 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 500); // Remove from DOM after fade out
        }, 4000);
    });

    /* --- CUSTOM SELECT DROPDOWN --- */
    const selectWrapper = document.querySelector('.custom-select-wrapper');
    if (selectWrapper) {
        const select = selectWrapper.querySelector('.custom-select');
        const trigger = select.querySelector('.select-trigger');
        const options = select.querySelectorAll('.option');

        // Toggle dropdown
        trigger.addEventListener('click', () => {
            select.classList.toggle('open');
        });

        // Handle selection
        options.forEach(option => {
            option.addEventListener('click', function () {
                select.classList.remove('open');

                // Update trigger text
                const value = this.getAttribute('data-value');
                const text = this.textContent;
                trigger.querySelector('span').textContent = text;

                // Remove selected class from all and add to clicked
                options.forEach(opt => opt.classList.remove('selected'));
                this.classList.add('selected');

                // Optional: You could trigger a page reload or AJAX call here to filter the dashboard
                console.log(`Lab selected: ${value}`);

                // For now, redirect if it's not 'all' (Concept)
                // if (value !== 'all') window.location.href = `/dashboard?lab_id=${value}`;
            });
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!select.contains(e.target)) {
                select.classList.remove('open');
            }
        });
    }
});
