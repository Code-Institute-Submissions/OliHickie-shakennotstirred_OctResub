


$(document).ready(function () {
  $('.sidenav').sidenav();
  $('.tabs').tabs();
  $('.datepicker').datepicker({
    autoClose: true,
    format: "dd mmmm, yyyy",
    minDate: new Date('1900-01-01'), 
    maxDate: new Date(),
    yearRange: [1900, 2022]
  });
  $('.modal').modal();

  setTimeout(function() {
    $('#flashes').fadeOut('fast');
}, 3000);
});