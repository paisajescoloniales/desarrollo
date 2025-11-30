// Modal z-index management for multiple stacked modals (jQuery - to be converted to vanilla JS later)
$(document).on("click", "[data-toggle='modal']", function () {
  $(".modal-backdrop").eq(0).css({
    display: "none",
  });

  // if more than 1 modal openned.
  if ($(".modal-backdrop").length > 1) {
    // move backdrop up (in z)
    var ZindexBackdrop =
      parseInt($(".modal-backdrop").eq(0).css("z-index")) + 20;
    console.log("Backdrop z-index: " + ZindexBackdrop);
    $(".modal-backdrop").eq(1).css({
      "z-index": ZindexBackdrop,
    });

    // move modal up (in z)
    var ZindexModal = parseInt($(".modal").eq(0).css("z-index")) + 20;
    console.log("Modal z-index: " + ZindexModal);
    $(".modal").eq(1).css({
      "z-index": ZindexModal,
    });
  }
});
