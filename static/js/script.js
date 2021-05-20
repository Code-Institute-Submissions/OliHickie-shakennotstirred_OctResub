// Clear flashes after 3sec
setTimeout(function () {
  $('#flashes').fadeOut('fast');
}, 3000);

// Add/remove icon to recipes side bar on hover
$(".spirit-list").hover(function () {
  $(this).children().removeClass("hide")
})

$(".spirit-list").mouseleave(function () {
  $(this).children().addClass("hide")
})

// add/remove ingreients lines in recipe form
$("#add-ingredient").click(function () {
  $(".ingredients-list").append(
    `<div class="row">
      <div class="col s8">
        <i class="prefix fas fa-wine-bottle"></i>
        <input name="ingredients" type="text" required>
        <label for="ingredients">Add Ingredient</label>
      </div>
    </div>`
  );
})


$(document).ready(function () {
  $('.sidenav').sidenav();
  $('.tabs').tabs();
  $('select').formSelect();
  M.textareaAutoResize($('#textarea1'));
});