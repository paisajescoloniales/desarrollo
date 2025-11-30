// Vanilla JS scroll handler to replace GSAP ScrollTrigger
// Handles panel pinning and pointer events for historia pages

document.addEventListener('DOMContentLoaded', function() {
  const panels = document.querySelectorAll('.panel');

  if (panels.length === 0) return; // No panels on this page

  // Use IntersectionObserver to track when panels enter/leave viewport
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: [0, 0.1, 0.9, 1]
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const panel = entry.target;

      // Enable pointer events when panel is intersecting (visible)
      // Disable when not intersecting (scrolled past)
      if (entry.isIntersecting) {
        panel.style.pointerEvents = 'auto';
      } else {
        panel.style.pointerEvents = 'none';
      }
    });
  }, observerOptions);

  // Observe all panels
  panels.forEach(panel => {
    observer.observe(panel);
  });
});
