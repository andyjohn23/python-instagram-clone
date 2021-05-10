$(document).ready(function () {
  $(".like-form").submit(function (e) {
    e.preventDefault();

    const post_id = $(this).attr("id");
    const likeText = $(`like-btn${post_id}`).text();
    const trim = $.trim(likeText);

    const url = $(this).attr("action");

    let res;
    const likes = $(`.like-counts${post_id}`).text();
    const trimCount = parseInt(likes);

    $.ajax({
      type: "POST",
      url: url,
      data: {
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        post_id: post_id,
      },
      success: function (response) {
        if (trim === "unlike") {
          $(`like-btn${post_id}`).text("like");
          res = trimCount - 1;
        } else {
          $(`like-btn${post_id}`).text("unlike");
          res = trimCount + 1;
        }
        $(`.like-counts${post_id}`).text(res);
      },
      error: function (response) {
        console.log("error", response);
      },
    });
  });
});
