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
    `
    <div class="col s10 m8 input-field">
        <i class="prefix fas fa-wine-bottle"></i>
        <input name="ingredients" type="text">
        <label for="ingredients">Add Quantity/Ingredient</label>
    </div>`
  );
})


// Carousel photos
function carousel() {
  var carouselImages = ["three-jugs.jpg", "friends.jpg", "large-cocktail.jpg", "serving-drinks.jpg"]

  for (i = 0; i < carouselImages.length; i++) {
    $("#home-carousel").append(
      `<a class="carousel-item" href="#"><img src="/static/images/${carouselImages[i]}"></a>`
      );
  }
}


// User favourite a recipe
$(".fa-heart").click(function(){
  $(this).toggleClass("far").toggleClass("fas");
})
$(".fa-heart").hover(function(){
  $(this).toggleClass("far").toggleClass("fas");
})

$(document).ready(function () {
  $('.sidenav').sidenav();
  $('.tabs').tabs();
  $('select').formSelect();
  M.textareaAutoResize($('#textarea1'));

  carousel()
  $('.carousel').carousel();
  setInterval(function() {
    $('.carousel').carousel('next');
  }, 5000);

  
});