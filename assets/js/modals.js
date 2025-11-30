// Modal z-index management for multiple stacked modals (vanilla JS)
document.addEventListener('click', function(event) {
  const trigger = event.target.closest('[data-toggle="modal"]');

  if (trigger) {
    const backdrops = document.querySelectorAll('.modal-backdrop');

    if (backdrops.length > 0) {
      backdrops[0].style.display = 'none';
    }

    // if more than 1 modal openned
    if (backdrops.length > 1) {
      // move backdrop up (in z)
      const zIndexBackdrop = parseInt(window.getComputedStyle(backdrops[0]).zIndex) + 20;
      console.log('Backdrop z-index: ' + zIndexBackdrop);
      backdrops[1].style.zIndex = zIndexBackdrop;

      // move modal up (in z)
      const modals = document.querySelectorAll('.modal');
      if (modals.length > 1) {
        const zIndexModal = parseInt(window.getComputedStyle(modals[0]).zIndex) + 20;
        console.log('Modal z-index: ' + zIndexModal);
        modals[1].style.zIndex = zIndexModal;
      }
    }
  }
});
