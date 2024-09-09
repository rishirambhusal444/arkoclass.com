


document.addEventListener("DOMContentLoaded", function() {
    const becomeTeacherButton = document.getElementById("becomeTeacherButton");
   
    const teacherFormContainer = document.getElementById("teacherFormCard");
    const cancle_form = document.getElementById("cancle_form");

    // Toggle visibility of the form on button click
    becomeTeacherButton.addEventListener("click", function() {
        
        teacherFormContainer.style.display= 'block';
   
    });

    cancle_form.addEventListener("click",function(){
        teacherFormContainer.style.display="none";
        })

    // Image preview functionality
    function previewImage(input, imagePreviewId) {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgElement = document.getElementById(imagePreviewId);
                imgElement.src = e.target.result;
                imgElement.style.display = 'block'; // Show the image
            };
            reader.readAsDataURL(file);
        }
    }

    // Attach change event listeners for image inputs
    document.getElementById("profile_img").addEventListener("change", function() {
        previewImage(this, "profileImagePreview");
    });

    document.getElementById("cover_image").addEventListener("change", function() {
        previewImage(this, "coverImagePreview");
    });
});
document.addEventListener("DOMContentLoaded", function() {
    const EditTeacherButton = document.getElementById("EditTeacherButton");
   
    const EditTeacherFormContainer = document.getElementById("EditteacherFormCard");
    const cancle_form = document.getElementById("cancle_form");

    // Toggle visibility of the form on button click
    EditTeacherButton.addEventListener("click", function() {
        EditTeacherFormContainer.style.display = (EditTeacherFormContainer.style.display === "none" || EditTeacherFormContainer.style.display === "") ? "block" : "none";
        
    });
    
    cancle_form.addEventListener("click",function(){
        EditTeacherFormContainer.style.display="none";
        })

    // Image preview functionality
    function previewImage(input, imagePreviewId) {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgElement = document.getElementById(imagePreviewId);
                imgElement.src = e.target.result;
                imgElement.style.display = 'block'; // Show the image
            };
            reader.readAsDataURL(file);
        }
    }

    // Attach change event listeners for image inputs
    document.getElementById("profile_img").addEventListener("change", function() {
        previewImage(this, "profileImagePreview");
    });

    document.getElementById("cover_image").addEventListener("change", function() {
        previewImage(this, "coverImagePreview");
    });
});