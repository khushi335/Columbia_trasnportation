document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('reservationForm');
    const serviceType = document.getElementById('serviceType');
    const vehicleClass = document.getElementById('vehicleClass');
    const passengers = document.getElementById('passengers');
    const luggage = document.getElementById('luggage');
    const paymentMethod = document.getElementById('paymentMethod');
    const submitBtn = document.getElementById('submitBtn');
    const totalPriceEl = document.getElementById('totalPrice');
    const addStopBtn = document.getElementById('addStopBtn');
    const stopsList = document.getElementById('stopsList');
    const paypalContainer = document.getElementById('paypal-button-container');
    const customPaypalBtn = document.getElementById('custom-paypal-btn');

    if (!form) return; // exit if form not present

    let paypalRendered = false;
    let currentPrice = 0;

    // ================= Extra stops =================
    addStopBtn?.addEventListener('click', () => {
        if (!stopsList) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'stop-item';
        wrapper.innerHTML = `
            <input type="text" name="stops" placeholder="Extra stop address" />
            <button type="button" class="remove-stop">✕</button>
        `;

        wrapper.querySelector('.remove-stop').addEventListener('click', () => {
            wrapper.remove();
            calculatePrice();
        });

        stopsList.appendChild(wrapper);
        calculatePrice();
    });

    // ================= Price calculation =================
    function animatePrice(newPrice) {
        if (!totalPriceEl) return;
        const start = currentPrice;
        const end = newPrice;
        const duration = 300;
        const startTime = performance.now();

        function updatePrice(time) {
            const elapsed = time - startTime;
            const progress = Math.min(elapsed / duration, 1);
            currentPrice = start + (end - start) * progress;
            totalPriceEl.textContent = currentPrice.toFixed(2);
            if (progress < 1) requestAnimationFrame(updatePrice);
        }

        requestAnimationFrame(updatePrice);
    }

    function calculatePrice() {
        if (!vehicleClass || !serviceType) return 0;

        let price = 0;

        const vehicleRates = {
            sedan: 50,
            suv: 70,
            van: 90,
            luxury: 150
        };

        const serviceMultiplier = {
            point_to_point: 1,
            round_trip: 1.8,
            hourly: 2
        };

        const vClass = vehicleClass.value;
        const sType = serviceType.value;
        const pCount = parseInt(passengers?.value) || 0;
        const lCount = parseInt(luggage?.value) || 0;
        const stops = stopsList ? stopsList.querySelectorAll('input[name="stops"]').length : 0;

        if (vClass && sType) {
            price = vehicleRates[vClass] * serviceMultiplier[sType];
            price += lCount * 5;
            price += stops * 10;
            if (pCount > 4) price += (pCount - 4) * 10;
        }

        animatePrice(price);
        return price;
    }

    [vehicleClass, serviceType, passengers, luggage].forEach(el => {
        el?.addEventListener('input', calculatePrice);
    });

    stopsList?.addEventListener('input', calculatePrice);

    // ================= PayPal Smart Button =================
    function renderPayPalButton() {
        if (!window.paypal || paypalRendered || !paypalContainer) return;

        paypalRendered = true;

        paypal.Buttons({
            createOrder: (data, actions) => {
                const price = calculatePrice();
                return actions.order.create({
                    purchase_units: [{
                        amount: { value: price.toFixed(2) }
                    }]
                });
            },
            onApprove: (data, actions) => {
                return actions.order.capture().then(details => {
                    alert('Payment completed by ' + details.payer.name.given_name);

                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'paypal_payment_id';
                    input.value = details.id;
                    form.appendChild(input);

                    form.submit();
                });
            }
        }).render('#paypal-button-container');
    }

    // ================= Toggle Payment =================
    function togglePayment() {
        if (!paymentMethod) return;

        if (paymentMethod.value === 'paypal') {
            submitBtn?.style.setProperty('display', 'none', 'important');
            paypalContainer?.style.setProperty('display', 'block', 'important');
            customPaypalBtn?.style.setProperty('display', 'block', 'important');
            renderPayPalButton();
        } else {
            submitBtn?.style.setProperty('display', 'inline-block', 'important');
            paypalContainer?.style.setProperty('display', 'none', 'important');
            customPaypalBtn?.style.setProperty('display', 'none', 'important');
        }
    }

    paymentMethod?.addEventListener('change', togglePayment);
    togglePayment(); // initial check
});
