// Clear flashes after 3sec
setTimeout(function () {
  $('#flashes').fadeOut('fast');
}, 3000);


// Back button
function back() {
  window.history.back();
}


// Add ingredients line in recipe form
$("#add-ingredient").click(function () {
  $(".ingredients-list").append(
    `<div class="input-field additional-line">
        <input name="ingredients" type="text" required>
        <label for="ingredients" class="sr-only">Add Quantity/Ingredient</label>
    </div>`
  );
  $("#remove-ingredient").removeClass("hide");
})


// Remove add ingredients line in recipe form except first line
$("#remove-ingredient").click(function (){
  $(".ingredients-list").children(".additional-line").last().remove();
})


// Implement review ratings
function ratingStars(rating) {
  goldStars = "<i class='fas fa-star'></i>".repeat(rating)
  emptyStars = "<i class='far fa-star'></i>".repeat(5 - rating)

  return goldStars + emptyStars
}


// Implement difficulty ratings
function ratingCircles(difficulty) {
  fasIcon = "<i class='fas fa-circle'></i>".repeat(difficulty)
  farIcon = "<i class='far fa-circle'></i>".repeat(3 - difficulty)

  return fasIcon + farIcon
}


$(document).ready(function () {
  // Materialize Initialization
  $('.sidenav').sidenav();
  $('.tabs').tabs();
  $('select').formSelect();
  $('.modal').modal();
  $('.tooltipped').tooltip();


  // Set up carousel and interval
  $('.carousel').carousel();
  setInterval(function () {
    $('.carousel').carousel('next');
  }, 6000);


  // Change recipe difficulty to icons
  $(".difficulty-easy").append(
    ratingCircles(1)
  )
  $(".difficulty-medium").append(
    ratingCircles(2)
  )
  $(".difficulty-difficult").append(
    ratingCircles(3)
  )

  // change recipe review ratings to icons
  $(".rating-1").append(
    ratingStars(1)
  )
  $(".rating-2").append(
    ratingStars(2)
  )
  $(".rating-3").append(
    ratingStars(3)
  )
  $(".rating-4").append(
    ratingStars(4)
  )
  $(".rating-5").append(
    ratingStars(5)
  )
});