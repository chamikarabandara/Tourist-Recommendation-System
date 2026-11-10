document.addEventListener("DOMContentLoaded", () => {

    // Mobile navigation
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", () => {
            const isOpen = navLinks.classList.toggle("open");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
        });

        navLinks.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => {
                navLinks.classList.remove("open");
                menuToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    // Recommendation form loading state
    const form = document.getElementById("recommendationForm");
    const searchButton = document.getElementById("searchButton");

    if (form && searchButton) {
        form.addEventListener("submit", () => {
            searchButton.disabled = true;
            searchButton.querySelector("span:first-child").textContent =
                "Finding destinations...";
        });
    }

    // Smooth appearance for destination cards
    const cards = document.querySelectorAll(".destination-card");

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        cards.forEach(card => observer.observe(card));
    }

});