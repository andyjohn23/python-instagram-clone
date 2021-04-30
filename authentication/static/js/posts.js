$(document).on('click', '#like-button', function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '{% url "postlikes" %}',
    data:{
      postid:$('#like-button').val(),
      "csrfmiddlewaretoken" : "{{csrf_token}}",
      action: 'post'
    },
    success: function(json) {
      document.getElementById("like_count").innerHTML = json['result']
      console.log(json)
    },
    error: function(xhr, errmsg, err) {

    }
  })
})
