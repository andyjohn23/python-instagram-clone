var img = document.forms["myform"]["image"];
var validFileEXtension = ["jpeg", "jpg", "png", "gif"];

function validation() {
  if (img.value != "") {
    var imageDot = img.value.lastIndexOf(".");
    var imageExtension = img.value.substring(imageDot);

    var result = validFileEXtension.includes(imageExtension);
    if (result == false) {
      alert("SELECTED FILE IS NOT AN IMAGE");
      return false;
    }
  } else {
    alert("NO IMAGE SELECTED");
    return false;
  }
}
