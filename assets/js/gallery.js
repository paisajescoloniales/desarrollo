// Gallery filtering (jQuery - to be converted to vanilla JS in Phase 4)
// Handles filter button clicks for the collection gallery
$(document).ready(function(){
  $(".facet").click(function(){
    var filterValue = $(this).attr('data-filter');
    $('.facet').removeClass('active');
    $(this).addClass('active');
    if(filterValue == 'all') {
      $('.all').show('slow');
    } else {
      $('.all').hide('slow');
      $(`.${filterValue}`).show('slow');
    }
  });
});
