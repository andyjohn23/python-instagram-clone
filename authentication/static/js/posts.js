$(document).ready(function () {
  $("#heart").click(function () {
    if ($("#heart").hasClass("liked")) {
      $("#heart").html('<i style="cursor:pointer;" class="material-icons">favorite_border</i>');
      $("#heart").removeClass("liked");
    } else {
      $("#heart").html('<i style="color:red; cursor:pointer;" class="material-icons">favorite</i>');
      $("#heart").addClass("liked");
    }
  });
});
