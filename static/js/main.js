$(document).on("click", ".toggle-password", function () {
  $(this).toggleClass("show hide");

  var input = $("#pass_log_id");
  input.attr("type") === "password"
    ? input.attr("type", "text")
    : input.attr("type", "password");
});
