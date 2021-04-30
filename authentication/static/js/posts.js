$(document).on("submit", "#like-form", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: '{% url "postlike" %}',
    data: {
      post_id: $("#likes").val(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      action: "post",
    },
    success: function (json) {
      document.getElementById("like_count").innerHTML = json["result"];
      console.log(json);
    },
    error: function (xhr, errmsg, err) {},
  });
});
href="{% url 'postdetails' post_item.id %}"
