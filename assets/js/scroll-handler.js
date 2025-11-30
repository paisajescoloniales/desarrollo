// GSAP ScrollTrigger handler for panel pinning
// Handles card stacking effect in historia.html

document.addEventListener('DOMContentLoaded', function() {
  const panels = document.querySelectorAll('.panel');

  if (panels.length === 0) return; // No panels on this page

  // Create ScrollTrigger for each panel
  panels.forEach((panel, i) => {
    ScrollTrigger.create({
      trigger: panel,
      start: "top top",
      pin: true,
      pinSpacing: false,
      onEnter: () => (panel.style.pointerEvents = "auto"),
      onLeave: () => (panel.style.pointerEvents = "none"),
      onEnterBack: () => (panel.style.pointerEvents = "auto"),
      onLeaveBack: () => (panel.style.pointerEvents = "none")
    });
  });
});
