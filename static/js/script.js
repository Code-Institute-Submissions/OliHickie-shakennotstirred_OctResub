// Clear flashes after 3sec
setTimeout(function() {
  $('#flashes').fadeOut('fast');
}, 3000);


$(document).ready(function () {
  $('.sidenav').sidenav();
  $('.tabs').tabs();
});