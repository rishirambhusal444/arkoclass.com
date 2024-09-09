    function toggleEditForm() {
        var form = document.getElementById("edit_form");
        if (form.style.display === "none") {
            form.style.display = "block";
        } else {
            form.style.display = "none";
        }

    }

    function toggleEditForm_subject() {
        var edit_form_subject = document.getElementById("edit_form_subject");

        if (edit_form_subject.style.display === "none") {
            edit_form_subject.style.display = "block";
        } else {
            edit_form_subject.style.display = "none";
        }
    }

    function toggleDeleteWarning() {
        var checkbox = document.getElementById("delete_video");
        var warning = document.getElementById("delete_warning");
        if (checkbox.checked) {
            warning.style.display = "block";
        } else {
            warning.style.display = "none";
        }
    }

// start for video_player.html

    document.addEventListener('DOMContentLoaded', function () {
    const thumbnil = document.getElementById("thumbnil");
    if (thumbnil) {
        thumbnil.addEventListener("change", function(event) {
            var file = event.target.files[0];
            var reader = new FileReader();

            reader.onload = function(e) {
                var img = document.getElementById("thumbnil_preview");
                if (img) {
                    img.src = e.target.result;
                    img.style.display = "block";
                }
            };

            reader.readAsDataURL(file);
        });
    }

    const videoContainer = document.getElementById('video-container');
    const video = document.getElementById('video-player');
    const controls = document.getElementById('controls');
    const playPauseButton = document.getElementById('play-pause');
    const forwardButton = document.getElementById('forward');
    const progressBar = document.getElementById('progress-bar');
    const progress = document.getElementById('progress');
    const fullScreenButton = document.getElementById('full-screen');
    const soundButton = document.getElementById('sound');
    const currentTimeDisplay = document.getElementById('current-time');
    const totalTimeDisplay = document.getElementById('total-time');
    const commentToggleButton = document.getElementById('comment-toggle');
    const commentList = document.getElementById('comment-list');
    let controlsTimeout;

    if (videoContainer && video && controls) {
        // Function to show controls
        function showControls() {
            controls.classList.add('show');
            clearTimeout(controlsTimeout);
            controlsTimeout = setTimeout(() => {
                controls.classList.remove('show');
            }, 3000); // Hide controls after 3 seconds of inactivity
        }

        // Toggle controls on click
        videoContainer.addEventListener('click', showControls);

        // Format time in minutes:seconds
        function formatTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
        }

        // Update total time once metadata is loaded
        video.addEventListener('loadedmetadata', () => {
            totalTimeDisplay.textContent = formatTime(video.duration);
        });

        // Update progress bar and current time
        video.addEventListener('timeupdate', () => {
            const currentTime = video.currentTime;
            const duration = video.duration;
            const progressPercentage = (currentTime / duration) * 100;
            progress.style.width = `${progressPercentage}%`;
            currentTimeDisplay.textContent = formatTime(currentTime);
        });

        // Toggle play/pause
        if (playPauseButton) {
            playPauseButton.addEventListener('click', () => {
                if (video.paused) {
                    video.play();
                    playPauseButton.innerHTML = '<i class="fas fa-pause"></i>';
                } else {
                    video.pause();
                    playPauseButton.innerHTML = '<i class="fas fa-play"></i>';
                }
            });
        }

        // Forward video by 10 seconds
        if (forwardButton) {
            forwardButton.addEventListener('click', () => {
                video.currentTime += 10;
            });
        }

        // Seek video on progress bar click
        if (progressBar) {
            progressBar.addEventListener('click', (e) => {
                const rect = progressBar.getBoundingClientRect();
                const offsetX = e.clientX - rect.left;
                const newTime = (offsetX / rect.width) * video.duration;
                video.currentTime = newTime;
            });
        }

        // Toggle fullscreen
        if (fullScreenButton) {
            fullScreenButton.addEventListener('click', () => {
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                } else {
                    videoContainer.requestFullscreen();
                }
            });
        }

        // Toggle sound on/off
        if (soundButton) {
            soundButton.addEventListener('click', () => {
                video.muted = !video.muted;
                soundButton.innerHTML = video.muted ? '<i class="fas fa-volume-mute"></i>' : '<i class="fas fa-volume-up"></i>';
            });
        }

        // Show/hide comments
        if (commentToggleButton && commentList) {
            commentToggleButton.addEventListener('click', () => {
                if (commentList.style.display === 'none') {
                    commentList.style.display = 'block';
                    commentToggleButton.textContent = 'Hide Comments';
                } else {
                    commentList.style.display = 'none';
                    commentToggleButton.textContent = 'Show Comments';
                }
            });
        }

        // Show controls when mouse moves over video container
        videoContainer.addEventListener('mousemove', showControls);
    }
});



document.addEventListener('DOMContentLoaded', function() {

    const facultySelect = document.getElementById('facultySelect');
    const levelSelect = document.getElementById('levelSelect');
    const subjectSelect = document.getElementById('subjectSelect');
    
    const new_faculty_create = document.getElementById('new-faculty-create');
    const new_level_create = document.getElementById('new-level-create');
    const new_subject_create = document.getElementById('new-subject-create');
    
    const level_plus_btn = document.getElementById("level_plus_btn");
    const new_level_form = document.getElementById("new_level_form");
    const new_level_name_input = document.getElementById("new_level_input_text");
    const create_level_button = document.getElementById("create-level-button");
    const level_error = document.getElementById("level-error");
    const levelSelect_container = document.getElementById("levelSelect_container");
    
    const newFaculty = document.getElementById('newFaculty');
    const newLevel = document.getElementById('newLevel');
    const newSubject = document.getElementById('newSubject');
    
    const selectedFacultyName = document.getElementById('selectedFacultyName');
    const Create_class_Button = document.getElementById('create-class');
    
    const subject_plus_btn = document.getElementById('subject_plus_btn');
    const new_subject_form = document.getElementById("new-subject-form");
    const new_subject_name_input = document.getElementById("new_subject_input_text");
    const create_subject_button = document.getElementById("create-subject-button");
    const subjectSelect_container = document.getElementById("subjectSelect_container");
    
    const select_FLS_btn = document.getElementById("select_FLS_btn");
    const create_FLS_btn = document.getElementById("create_FLS_btn");
    
    const create_FLS_form = document.getElementById("create_FLS_form");
    const select_FLS_form = document.getElementById("select_FLS_form");
    
    const thumbnilUpload = document.getElementById('thumbnil-upload')
    const videoUpload = document.getElementById('video-upload')
    
    thumbnilUpload.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const Upload_thumbnil_btn = document.getElementById('upload-thumbnil')
        const thumbnilPreview = document.getElementById('thumbnil-preview');
        const thumbnilPreview_close = document.getElementById('close-button-thumbnil');
        if (file) {
            const fileURL = URL.createObjectURL(file);
            thumbnilPreview.style.display = "block";
            thumbnilPreview.innerHTML = `<img src="${fileURL}" alt="Thumbnail">`;
            thumbnilPreview_close.style.display="block"
            Upload_thumbnil_btn.style.display = "none";
    
            
        } else {
            thumbnilPreview.innerHTML = '';
        }
    
        
        thumbnilPreview_close.addEventListener('click',function(event){
            thumbnilPreview.innerHTML = '';
            thumbnilUpload.value  = '';
            Upload_thumbnil_btn.style.display = "block";  
            thumbnilPreview_close.style.display = "none";
    
        })
    });
    
    videoUpload.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const videoPreview = document.getElementById('video-preview');
        const Upload_video_btn = document.getElementById('upload-video');
        const videoPreview_close = document.getElementById('close-button-video');
    
    
       if (file) {
            const fileURL = URL.createObjectURL(file);
            videoPreview.style.display = "block";
            videoPreview_close.style.display = "block";
            Upload_video_btn.style.display = "none";
            videoPreview.innerHTML = `<video controls src="${fileURL}" width="150px" alt="Thumbnail"></video>`;
        
        } else {
            videoPreview.innerHTML = '';
        }
    
        videoPreview_close.addEventListener('click',function(event){
            videoPreview.innerHTML = '';
            videoUpload.value = '';
            Upload_video_btn.style.display = "block";  
            videoPreview_close.style.display = "none";
    
        })
    });
    
    
    
    select_FLS_btn.addEventListener("click", function() {
            select_FLS_btn.style.display = 'none';
            create_FLS_btn.style.display = 'block';
            select_FLS_form.style.display = 'flex';
            create_FLS_form.style.display = 'none';
            newFaculty.value = '';
            newLevel.value = "";
            newSubject.value = "";
            new_faculty_create.value = "";
            new_level_create.value = "";
            new_subject_create.value = "";
        });
    
    create_FLS_btn.addEventListener("click", function() {
            select_FLS_btn.style.display = 'block';
            create_FLS_btn.style.display = 'none';
            create_FLS_form.style.display = 'flex';
            select_FLS_form.style.display = 'none';
             newFaculty.value = '';
            newLevel.value = "";
            newSubject.value = "";
            facultySelect.value ="";
            levelSelect.value ="";
            subjectSelect.value ="";
    });
    
    
    document.getElementById("submit-button").addEventListener("click", function(event) {
    
    const isCreateFLSFormVisible = create_FLS_form.style.display !== 'none';
    
    const videoUploadButton= document.getElementById('video_border');
    const thumbnilUploadButton = document.getElementById('thumbnil_border'); 
    
    const videoUploadInput = document.getElementById('video-upload');
    const thumbnilInput = document.getElementById('thumbnil-upload');
    
    
    const isVideoValid = valid_video(videoUploadInput,videoUploadButton,'Video');
    const isThumbnilValid = valid_video(thumbnilInput,thumbnilUploadButton, 'Thumbnail');
    
    
    let isValid = true;
    
    if (isCreateFLSFormVisible) {
        
        // Use the validation for the create_FLS_form fields
        const isFacultyValid = validateField(new_faculty_create,new_faculty_create,'faculty name');
        const isLevelValid = validateField(new_level_create,new_level_create, 'level name');
        const isSubjectValid = validateField(new_subject_create,new_subject_create, 'subject name');
    
    
        isValid = isFacultyValid && isLevelValid && isSubjectValid ;
    
    } else {
    
        // Use the hidden field validation
        const isNewFacultyValid = validateField_hidden(newFaculty, facultySelect, 'faculty name');
        const isNewLevelValid = validateField_hidden(newLevel, levelSelect, 'level name');
        const isNewSubjectValid = validateField_hidden(newSubject, subjectSelect, 'subject name');
    
        isValid = isNewFacultyValid && isNewLevelValid && isNewSubjectValid ;
    }
    
    
    if (!isValid || !isVideoValid || !isThumbnilValid) {
        event.preventDefault(); // Prevent form submission if any field is invalid
    
    
    } else {
        // Hide the error button if no error exists
        document.getElementById('form-error-button').style.display = 'none';
    }
    
    
    function valid_video(field, bordor, fieldName) {
        if (field.files && field.files.length > 0) {
            bordor.style.borderColor = 'green';
    
            return true;
        } else {
            bordor.style.borderColor = 'red';
            field.value= "";
    
            // Show error message in the button
            const errorButton = document.getElementById('form-error-button');
            errorButton.textContent = `Invalid ${fieldName}: Please upload a file.`;
            errorButton.style.display = 'inline-block'; // Make the button visible
    
            return false;
        }
    }
    
    function validateField(field, border, fieldName) {
    
    const value = field.value.trim();
    const regex = /^[a-zA-Z]{4,16}$/;
    
    if (regex.test(value)) {
    field.style.borderColor = 'green';
    return true;
    } else {
    field.style.borderColor = 'red';
    field.value = "";
    const errorButton = document.getElementById('form-error-button');
    errorButton.textContent = `Invalid ${fieldName}: Should be 4-16 characters, contain only letters, and no special characters.`;
    errorButton.style.display = 'inline-block';
    
    return false;
    }
    }
    
    function validateField_hidden(field, select_field, fieldName) {
    const value = field.value.trim();
    
    if (value.length > 0) {
    select_field.style.borderColor = 'green';
    return true;
    } else {
    select_field.style.borderColor = 'red';
    field.value = "";
    const errorButton = document.getElementById('form-error-button');
    errorButton.textContent = `Invalid ${fieldName}: Please fill out this field.`;
    errorButton.style.display = 'inline-block';
    
    return false;
    }
    }
    
    });
    
    // Validation functions
    new_faculty_create.addEventListener('input',function(){
        newFaculty.value=this.value;
    });
    new_level_create.addEventListener('input',function(){
        newLevel.value=this.value;
    });
    new_subject_create.addEventListener('input',function(){
        newSubject.value=this.value;
    });
    
    
    facultySelect.addEventListener('change', function(event) {
        const selectedFacultyId = event.target.value;
        newFaculty.value=selectedFacultyId;
        fetchLevels(selectedFacultyId);
    });
    
    subjectSelect.addEventListener('change', function(event) {
        const selectedSubjectId = subjectSelect.options[subjectSelect.selectedIndex].dataset.id;
        newSubject.value=selectedSubjectId
    });
    
    
    subjectSelect.addEventListener('change', function(event) {
        const selectedSubjectId = subjectSelect.options[subjectSelect.selectedIndex].dataset.id;
        newSubject.value=selectedSubjectId
    });
    
    levelSelect.addEventListener('change', function(event) {
        const selectedLevelId = levelSelect.options[levelSelect.selectedIndex].dataset.id;     
        fetchSubjects(selectedLevelId);
        newLevel.value=selectedLevelId
    });
    
    
    
    
    
    async function fetchLevels(facultyId) {
        try {
            const response = await fetch(`/videos/get_levels/?facultyId=${facultyId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch levels');
            }
            const data = await response.json();
    
            // Clear existing options
            levelSelect.innerHTML = '';
            
            // Add default option
            levelSelect.appendChild(new Option('Select Level/Semester/Class', ''));
            
            // Populate levels
            data.levels.forEach(level => {
                const option = new Option(level.level_name, level.id);
                option.dataset.id = level.id; // Store the id in a data attribute
                levelSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching levels:', error.message);
        }
    }
    
    async function fetchSubjects(levelId) {
        try {
            const response = await fetch(`/videos/get_subjects/?levelId=${levelId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch subjects');
    
            }
            const data = await response.json();
    
            // Clear existing options
            subjectSelect.innerHTML = '';
            
            // Add default option
            subjectSelect.appendChild(new Option('Select Subject', ''));
            
            // Populate subjects
            data.subjects.forEach(subject => {
                const option = new Option(subject.subject_name, subject.id);
                option.dataset.id = subject.id; // Store the id in a data attribute
                subjectSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching subjects:', error.message);
        }
         // Show the select button when a subject is selected
            subjectSelect.addEventListener('change', function() {
                if (subjectSelect.value) {
                    selected_FLS.style.display = 'block';
                    Create_class_Button.style.display = 'none';
                    // this is for redering the selected subject :
    
        const selectedFacultyName = facultySelect.options[facultySelect.selectedIndex].text;
        const selectedLevelName = levelSelect.options[levelSelect.selectedIndex].text;
        const selectedSubjectName = subjectSelect.options[subjectSelect.selectedIndex].text;
        selected_FLS.textContent = `Select: ${selectedFacultyName} / ${selectedLevelName} / ${selectedSubjectName}`;
    
    
                } else {
                    selected_FLS.style.display = 'none';
                }
            });
    
            // Hide the select button when the "Add New Subject" button is clicked
                 subject_plus_btn.addEventListener('click', function() {
                selected_FLS.style.display = 'none';
                Create_class_Button.style.display = 'block';
    
                
                // toggleNewForm('', 'new-subject-form')
    
            });
            
    }
    
    
    level_plus_btn.addEventListener("click", function() {
        level_plus_btn.style.display = 'none';
        levelSelect_container.style.display = 'none';
        subjectSelect_container.style.display = 'none';
    
        new_level_form.style.display = 'block';
        new_subject_form.style.display = 'block';
    
        newLevel.value ='';
        newSubject.value ='';
        selected_FLS.style.display = 'none';
        Create_class_Button.style.display = 'flex';
    });
    
    subject_plus_btn.addEventListener("click", function() {
            subject_plus_btn.style.display = 'none';
            new_subject_form.style.display = 'flex';
            subjectSelect_container.style.display = 'none';
    
    
    
     });         
    
    
    create_level_button.addEventListener("click", function() {
        const new_level_name = new_level_name_input.value.trim();
        const regex = /^[a-zA-Z]{4,16}$/;
    
    
        if (!isNaN(new_level_name) || !regex.test(new_level_name)) {
            level_error.textContent = "Level name should be a non-empty string/ not allow of special charector.";
            level_error.style.display = 'block';
            new_level_name_input.value = '';
            return false;
        } else if (new_level_name) {
            const level_dropdown = document.getElementById("levelSelect");
            const option = document.createElement("option");
            option.value = new_level_name;
            option.text = new_level_name;
            level_dropdown.add(option);
            level_dropdown.value = new_level_name;
            newLevel.value=new_level_name  // this is sending newly created value or level to input fild
            new_level_name_input.value = '';
    
            new_level_form.style.display = 'none';
            level_plus_btn.style.display = 'inline-block';
            level_error.style.display = 'none';
            levelSelect_container.style.display = 'flex';
    
    
        }
        selected_FLS.style.display = 'none';
        Create_class_Button.style.display = 'flex';
    });
      
            // Event listener for creating new faculty
            create_subject_button.addEventListener("click", function() {
                const new_subject_name = new_subject_name_input.value.trim();
                const regex = /^[a-zA-Z]{4,16}$/;
    
        if (!isNaN(new_subject_name) || !regex.test(new_subject_name)) {
            subject_error.textContent = "Level name should be a non-empty string/ not allow of special charector.";
                    subject_error.style.display = 'block'; // Show the error message
                    new_subject_name.value = '';
    
                    return false;
                    }
                else if (new_subject_name) {
    
                    // Handle creating new faculty without using an API
                    const subject_dropdown = document.getElementById("subjectSelect");
                    const option = document.createElement("option");
                    option.value = new_subject_name; // This should be the ID from the database in a real scenario
                    option.text = new_subject_name;
                    subject_dropdown.add(option);
                    subject_dropdown.value = new_subject_name;
    
                    // Clear the new faculty form
                    newSubject.value=new_subject_name;
                    new_subject_name_input.value = '';
                    new_subject_form.style.display = 'none';
                    subject_plus_btn.style.display = 'flex';
                    subjectSelect_container.style.display = 'flex';
    
                }
    
            });
    });
    
// this is forupload js for view

// this is end of js for video upload 
