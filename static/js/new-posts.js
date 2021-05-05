var img = document.forms["myform"]["image"];
var captionText = document.forms["myform"]["caption"];
var validFileEXtension = ["jpeg", "jpg", "png", "gif"];

function validation() {
  if (img.value != "") {
    var imageExtension = img.value.substring(img.value.lastIndexOf(".") + 1);
    var result = validFileEXtension.includes(imageExtension);
    if (result == false) {
      swal("SELECTED FILE IS NOT AN IMAGE");
      return false;
    } else {
      if (parseFloat(img.files[0].size / (1024 * 1024)) >= 3) {
        swal("FILE SIZE IS GREATER THAN 3MB");
        return false;
      }
    }
  } else {
    swal("NO IMAGE SELECTED");
    return false;
  }
}
setTimeout(function () {
  if ($("#message").length > 0) {
    $("#message").fadeToggle();
  }
}, 3000);
