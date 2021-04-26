var img = document.forms["myform"]["image"];

function validation() {
  if (img.value != "") {
  } else {
    alert("NO IMAGE SELECTED!!!");
    return false;
  }
}
