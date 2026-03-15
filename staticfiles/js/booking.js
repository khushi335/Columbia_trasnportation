document.addEventListener("DOMContentLoaded", function () {
    // ===============================
    // --- Form Submission (AJAX) ---
    // ===============================
    const forms = document.querySelectorAll("#carouselId .carousel-item form");

    forms.forEach((form) => {
        const messagesDiv = document.createElement("div");
        messagesDiv.classList.add("form-messages", "mb-3");
        form.prepend(messagesDiv);

        form.addEventListener("submit", function (e) {
            e.preventDefault();
            messagesDiv.innerHTML = "";

            const formData = new FormData(form);

            fetch(window.location.href, {
                method: "POST",
                body: formData,
                headers: { "X-Requested-With": "XMLHttpRequest" },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        messagesDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
                        form.reset();
                        setTimeout(() => (messagesDiv.innerHTML = ""), 5000);
                    } else if (data.error) {
                        messagesDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                        setTimeout(() => (messagesDiv.innerHTML = ""), 5000);
                    }
                })
                .catch((err) => {
                    console.error(err);
                    messagesDiv.innerHTML = `<div class="alert alert-warning">An error occurred. Please try again later.</div>`;
                    setTimeout(() => (messagesDiv.innerHTML = ""), 5000);
                });
        });
    });

    // =========================================
    // --- Autocomplete Setup (Reusable) ---
    // =========================================
    function setupAutocomplete(inputId, suggestionsId, type) {
        const input = document.getElementById(inputId);
        const suggestionsBox = document.getElementById(suggestionsId);

        if (!input || !suggestionsBox) {
            console.warn(`Autocomplete skipped: missing ${inputId} / ${suggestionsId}`);
            return;
        }

        let selectedIndex = -1;

        // Input event → fetch suggestions
        input.addEventListener("input", function () {
            const query = input.value.trim();
            selectedIndex = -1;
            if (!query) {
                suggestionsBox.innerHTML = "";
                suggestionsBox.style.display = "none";
                return;
            }

            fetch(`/?q=${encodeURIComponent(query)}&type=${type}`)
                .then((res) => res.json())
                .then((data) => {
                    suggestionsBox.innerHTML = "";
                    if (data.locations && data.locations.length) {
                        data.locations.forEach((loc) => {
                            const div = document.createElement("div");
                            div.classList.add("suggestion-item");
                            div.textContent = loc.name;

                            div.addEventListener("click", () => {
                                input.value = loc.name;
                                suggestionsBox.innerHTML = "";
                                suggestionsBox.style.display = "none";
                            });

                            suggestionsBox.appendChild(div);
                        });
                        suggestionsBox.style.display = "block";
                    } else {
                        suggestionsBox.style.display = "none";
                    }
                })
                .catch((err) => console.error(err));
        });

        // Keyboard navigation
        input.addEventListener("keydown", function (e) {
            const items = suggestionsBox.querySelectorAll(".suggestion-item");
            if (!items.length) return;

            if (e.key === "ArrowDown") {
                e.preventDefault();
                selectedIndex = (selectedIndex + 1) % items.length;
                highlightItem(items);
            } else if (e.key === "ArrowUp") {
                e.preventDefault();
                selectedIndex = (selectedIndex - 1 + items.length) % items.length;
                highlightItem(items);
            } else if (e.key === "Enter") {
                e.preventDefault();
                if (selectedIndex > -1) {
                    input.value = items[selectedIndex].textContent;
                    suggestionsBox.innerHTML = "";
                    suggestionsBox.style.display = "none";
                    selectedIndex = -1;
                }
            }
        });

        function highlightItem(items) {
            items.forEach((item, i) => {
                item.classList.toggle("active-suggestion", i === selectedIndex);
            });
        }

        // Hide suggestions when clicking outside
        document.addEventListener("click", function (e) {
            if (!input.contains(e.target) && !suggestionsBox.contains(e.target)) {
                suggestionsBox.style.display = "none";
            }
        });
    }

    // =================================================
    // --- Auto attach autocomplete to all fields ---
    // =================================================
    for (let i = 1; i <= 4; i++) {
        setupAutocomplete(`pick-up-location-${i}`, `pick-up-suggestions-${i}`, "pick");
        setupAutocomplete(`drop-off-location-${i}`, `drop-off-suggestions-${i}`, "drop");
    }
});
