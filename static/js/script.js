// Clear flashes after 3sec
setTimeout(function () {
  $('#flashes').fadeOut('fast');
}, 3000);


// Add glass icon to recipes side bar on hover
// $(".spirit-list").hover(function () {
//   $(this).children().removeClass("hide")
// })
// $(".spirit-list").mouseleave(function () {
//   $(this).children().addClass("hide")
// })


// Add ingredients line in recipe form
$("#add-ingredient").click(function () {
  $(".ingredients-list").append(
    `<div class="input-field additional-line">
        <i class="prefix fas fa-wine-bottle"></i>
        <input name="ingredients" type="text" required>
        <label for="ingredients">Add Quantity/Ingredient</label>
    </div>`
  );
  $("#remove-ingredient").removeClass("hide");
})

// Remove add ingredients line in recipe form except first line
$("#remove-ingredient").click(function (){
  $(".ingredients-list").children(".additional-line").last().remove();
})

// User favourite a recipe
$(".fa-heart").click(function () {
  $(this).toggleClass("far fas favourite");
})


$(document).ready(function () {
  $('.sidenav').sidenav();
  $('.tabs').tabs();
  $('select').formSelect();
  $('.modal').modal();
  M.textareaAutoResize($('#textarea1'));


  // set up carousel and interval
  $('.carousel').carousel();
  setInterval(function () {
    $('.carousel').carousel('next');
  }, 6000);

  $('.slider').slider();



  // change recipe difficulty to icons
  $(".difficulty-easy").append(
    `<span><i class="fas fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i></span>`
  )
  $(".difficulty-medium").append(
    `<span><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="far fa-star"></i></span>`
  )
  $(".difficulty-difficult").append(
    `<span><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i></span>`
  )
});