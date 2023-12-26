function previewImage(event) {
    let input = event.target;
    var file = input.files[0];
    let reader = new FileReader();
    if (file.size > 5 * 1024 * 1024) {
        alert("Please select an image file smaller than 5MB.");
        input.value = ''; // Reset the file input value
        return;
      }
    reader.onload = function() {
      let imgElement = document.getElementById("preview-image");
      imgElement.src = reader.result;
    };
  
    reader.readAsDataURL(input.files[0]);
  }