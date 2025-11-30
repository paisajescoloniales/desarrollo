// Gallery filtering (vanilla JS)
// Handles filter button clicks for the collection gallery
// Uses event delegation since buttons are created dynamically by jQuery
// Replicates jQuery .show('slow') and .hide('slow') fade behavior

function fadeIn(element, duration = 600) {
  element.style.opacity = 0;
  element.style.display = 'block';
  element.offsetHeight; // force reflow
  element.style.transition = `opacity ${duration}ms ease`;
  element.style.opacity = 1;

  setTimeout(() => {
    element.style.removeProperty('transition');
  }, duration);
}

function fadeOut(element, duration = 600) {
  element.style.transition = `opacity ${duration}ms ease`;
  element.style.opacity = 0;

  setTimeout(() => {
    element.style.display = 'none';
    element.style.removeProperty('transition');
    element.style.removeProperty('opacity');
  }, duration);
}

document.addEventListener('DOMContentLoaded', function() {
  const buttonContainer = document.getElementById('paisajes-facet-buttons');

  if (!buttonContainer) return;

  // Use event delegation - listen on parent container
  buttonContainer.addEventListener('click', function(event) {
    const button = event.target.closest('.facet');
    if (!button) return;

    const filterValue = button.getAttribute('data-filter');
    const allItems = document.querySelectorAll('.all');
    const allButtons = buttonContainer.querySelectorAll('.facet');

    // Remove active class from all buttons
    allButtons.forEach(btn => btn.classList.remove('active'));

    // Add active class to clicked button
    button.classList.add('active');

    // Show/hide gallery items with fade animation (matching jQuery's 'slow' = 600ms)
    if (filterValue === 'all') {
      // Show all items
      allItems.forEach(item => {
        if (item.style.display === 'none' || window.getComputedStyle(item).display === 'none') {
          fadeIn(item, 600);
        }
      });
    } else {
      // Hide non-matching items, show matching ones
      allItems.forEach(item => {
        const isVisible = item.style.display !== 'none' && window.getComputedStyle(item).display !== 'none';
        const shouldShow = item.classList.contains(filterValue);

        if (shouldShow && !isVisible) {
          fadeIn(item, 600);
        } else if (!shouldShow && isVisible) {
          fadeOut(item, 600);
        }
      });
    }
  });
});
