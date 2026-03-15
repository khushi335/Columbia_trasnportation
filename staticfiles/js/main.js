(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);

    // Initiate WOW.js
    new WOW().init();

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 200) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });

    // Car Categories Carousel
    $(".categories-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        dots: false,
        loop: true,
        margin: 25,
        nav: true,
        navText: [
            '<i class="fas fa-chevron-left"></i>',
            '<i class="fas fa-chevron-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0: { items: 1 },
            576: { items: 1 },
            768: { items: 1 },
            992: { items: 2 },
            1200: { items: 3 }
        }
    });

    // Testimonial Carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav: false,
        responsiveClass: true,
        responsive: {
            0: { items: 1 },
            576: { items: 1 },
            768: { items: 1 },
            992: { items: 2 },
            1200: { items: 2 }
        }
    });

    // Facts Counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 5,
        time: 2000
    });

    // Back to Top Button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });

    // ======================
    // AJAX Submission for Carousel Forms
    // ======================
    document.addEventListener("DOMContentLoaded", function () {
        const forms = document.querySelectorAll("#carouselId .carousel-item form");

        forms.forEach((form) => {
            // Create message container
            const messagesDiv = document.createElement("div");
            messagesDiv.classList.add("form-messages", "mb-3");
            form.prepend(messagesDiv);

            form.addEventListener("submit", function (e) {
                e.preventDefault();
                messagesDiv.innerHTML = ""; // Clear previous messages

                const formData = new FormData(form);

                fetch(window.location.href, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                })
                .then((response) => response.json())
                .then((data) => {
                    // Clear previous invalid styles
                    form.querySelectorAll(".is-invalid").forEach((el) => {
                        el.classList.remove("is-invalid");
                    });

                    if (data.success) {
                        messagesDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
                        form.reset();
                        setTimeout(() => { messagesDiv.innerHTML = ""; }, 5000);
                    } else if (data.error) {
                        messagesDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;

                        // Highlight fields with errors if provided
                        if (data.form_errors) {
                            const errors = JSON.parse(data.form_errors);
                            for (let field in errors) {
                                const input = form.querySelector(`[name="${field}"]`);
                                if (input) input.classList.add("is-invalid");
                            }
                        }

                        setTimeout(() => { messagesDiv.innerHTML = ""; }, 5000);
                    }
                })
                .catch((err) => {
                    console.error(err);
                    messagesDiv.innerHTML = `<div class="alert alert-warning">
                        An error occurred. Please try again later.
                    </div>`;
                    setTimeout(() => { messagesDiv.innerHTML = ""; }, 5000);
                });
            });
        });
    });

})(jQuery);
