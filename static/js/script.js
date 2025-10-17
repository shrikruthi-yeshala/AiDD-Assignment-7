document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                }
            });
        });
    }

    const projectForm = document.getElementById('projectForm');
    if (projectForm) {
        const titleInput = projectForm.querySelector('input[name="title"]');
        const descriptionInput = projectForm.querySelector('textarea[name="description"]');
        const imageInput = projectForm.querySelector('input[name="image_file_name"]');
        const errorBanner = document.getElementById('formStatus');

        projectForm.addEventListener('submit', event => {
            const errors = [];

            if (titleInput && !titleInput.value.trim()) {
                errors.push('A project title is required.');
            }

            if (descriptionInput && !descriptionInput.value.trim()) {
                errors.push('Please include a short description.');
            }

            if (imageInput && !imageInput.value.trim()) {
                errors.push('Add the image file name stored in static/images.');
            }

            if (errors.length && errorBanner) {
                event.preventDefault();
                errorBanner.textContent = errors.join(' ');
                errorBanner.classList.remove('success', 'info');
                errorBanner.classList.add('error');
                errorBanner.style.display = 'block';
            }
        });
    }

    const animatedCards = document.querySelectorAll('.highlight-card, .project-card, .interest-card');
    if (animatedCards.length) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        animatedCards.forEach(card => observer.observe(card));
    }
});
