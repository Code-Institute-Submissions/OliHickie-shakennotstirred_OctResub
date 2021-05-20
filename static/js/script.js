// Clear flashes after 3sec
setTimeout(function() {
  $('#flashes').fadeOut('fast');
}, 3000);

// Add/remove icon to recipes side bar on hover
$(".spirit-list").hover(function(){
  $(this).children().removeClass("hide")
})

$(".spirit-list").mouseleave(function(){
  $(this).children().addClass("hide")
})


$(document).ready(function () {
  $('.sidenav').sidenav();
  $('.tabs').tabs();
  $('select').formSelect();
  M.textareaAutoResize($('#textarea1'));
});