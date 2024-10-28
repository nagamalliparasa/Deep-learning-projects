document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    var fileInput = document.getElementById('file-upload');
    var file = fileInput.files[0];
    
    if (file) {
        var reader = new FileReader();

        reader.onload = function(e) {
            var imageContainer = document.getElementById('image-container');
            var uploadedImage = document.getElementById('uploaded-image');
            var predictedOutput = document.getElementById('predicted-output');

            uploadedImage.src = e.target.result;
            imageContainer.style.display = 'block';

            // Hide the submit button
            document.querySelector('.form-button').style.display = 'none';

            // Display the predicted output (dummy text for now)
            predictedOutput.textContent = "Predicted Output: Sample Prediction";
        };

        reader.readAsDataURL(file);
    }
});
