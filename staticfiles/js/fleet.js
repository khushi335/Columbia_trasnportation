document.addEventListener('DOMContentLoaded', () => {
  // ===================== Filter by category =====================
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = btn.dataset.category;
      document.querySelectorAll('.fleet-card').forEach(card => {
        card.style.display = (!cat || card.dataset.category === cat) ? 'block' : 'none';
      });
    });
  });

  // ===================== LIGHTBOX =====================
  const lightbox = document.getElementById('lightboxModal');
  if (lightbox) {
    const lightboxImg = lightbox.querySelector('.lightbox-img');
    const closeLightbox = lightbox.querySelector('.close-lightbox');
    const prevBtn = lightbox.querySelector('.prev-lightbox');
    const nextBtn = lightbox.querySelector('.next-lightbox');
    let currentImages = [], currentIndex = 0;

    document.querySelectorAll('.fleet-card img').forEach(img => {
      img.addEventListener('click', () => {
        const gallery = img.dataset.gallery;
        currentImages = Array.from(document.querySelectorAll(`img[data-gallery="${gallery}"]`));
        currentIndex = currentImages.indexOf(img);
        if (lightboxImg) lightboxImg.src = currentImages[currentIndex].src;
        lightbox.classList.remove('hidden');
      });
    });

    function showLightbox() { 
      if (lightboxImg && currentImages.length) lightboxImg.src = currentImages[currentIndex].src; 
    }

    if (prevBtn) prevBtn.addEventListener('click', () => { 
      currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length; 
      showLightbox(); 
    });

    if (nextBtn) nextBtn.addEventListener('click', () => { 
      currentIndex = (currentIndex + 1) % currentImages.length; 
      showLightbox(); 
    });

    if (closeLightbox) closeLightbox.addEventListener('click', () => lightbox.classList.add('hidden'));
    window.addEventListener('click', e => { if(e.target === lightbox) lightbox.classList.add('hidden'); });
  }

  // ===================== BOOK NOW MODAL =====================
  const modal = document.getElementById('bookNowModal');
  if (modal) {
    const closeModal = modal.querySelector('.close-modal');
    const bookBtns = document.querySelectorAll('.book-now-btn');
    const vehicleIdInput = document.getElementById('modalVehicleId');

    bookBtns.forEach(btn => btn.addEventListener('click', () => {
      if (vehicleIdInput) vehicleIdInput.value = btn.dataset.vehicle;
      modal.classList.remove('hidden');
    }));

    if (closeModal) closeModal.addEventListener('click', () => modal.classList.add('hidden'));
    window.addEventListener('click', e => { if(e.target === modal) modal.classList.add('hidden'); });
  }
});
