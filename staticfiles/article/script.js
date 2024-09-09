document.addEventListener("DOMContentLoaded", function() {
    const editor = document.getElementById("editor");
    const toolbar = document.getElementById("tools");
    const imageInput = document.getElementById('article-image-input');
    const articleForm = document.getElementById('article-form');

    // Show toolbar when editor is focused
    editor.addEventListener("focus", function() {
        showToolbar();
    });

    // Hide toolbar when clicking outside editor or toolbar
    document.addEventListener("click", function(event) {
        if (!editor.contains(event.target) && !toolbar.contains(event.target)) {
            hideToolbar();
        }
    });

    // Initialize toolbar visibility
    hideToolbar();

    // Bind image input change to upload image function
    imageInput.addEventListener('change', uploadImage);

    // Bind form submission to validation and preparation function
    articleForm.addEventListener('submit', handleFormSubmission);

    // Shortcut keys for text formatting
    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey) {
            switch (event.key.toLowerCase()) {
                case 'b':
                    event.preventDefault();
                    formatText('bold');
                    break;
                case 'i':
                    event.preventDefault();
                    formatText('italic');
                    break;
                case 'l':
                    event.preventDefault();
                    formatText('justifyLeft');
                    break;
                case 'e':
                    event.preventDefault();
                    formatText('justifyCenter');
                    break;
                case 'r':
                    event.preventDefault();
                    formatText('justifyRight');
                    break;
                case 'h':
                    event.preventDefault();
                    toggleHighlight();
                    break;
                case 'k':
                    event.preventDefault();
                    createHyperlink();
                    break;
            }
        }
    });

    // Function to trigger file input when clicking the Image button
    window.triggerImageUpload = function() {
        imageInput.click();
    }

    // Function to upload image and display in editor
    function uploadImage(event) {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('image', file);
            formData.append('csrfmiddlewaretoken', '{{ csrf_token }}'); // Replace with actual CSRF token

            fetch('/article/upload_image/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const imgTag = `<img src="${data.url}" alt="Uploaded Image" style="width:80%; height: 80%;margin-left:10%; margin-right:10%">`;
                    insertHtmlAtCursor(imgTag);
                    document.getElementById('hiddenBody').value = document.getElementById('editor').innerHTML;
                } else {
                    console.error('Error uploading image:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }


   
    // Function to insert HTML content at the current cursor position in the editor
    function insertHtmlAtCursor(html) {
        const range = window.getSelection().getRangeAt(0);
        const frag = document.createRange().createContextualFragment(html);
        range.deleteContents(); // Clear existing content in the selection
        range.insertNode(frag);
        range.collapse(false);  // Move the cursor to the end of the inserted element
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    }

    window.createHyperlink = function() {
        const selection = window.getSelection();
        if (selection.rangeCount > 0 && !selection.isCollapsed) {
            const linkUrl = prompt('Enter the link URL:');
            
            if (linkUrl) {
                const range = selection.getRangeAt(0);
                const selectedText = range.toString();
                const linkHtml = `<a href="${linkUrl}" target="_blank">${selectedText}</a>`;
                const linkFragment = document.createRange().createContextualFragment(linkHtml);
                
                // Clear existing content in the selection
                range.deleteContents();
                
                // Insert new link content
                range.insertNode(linkFragment);
                
                // Move the cursor to the end of the inserted link
                range.collapse(false);
                const selectionObj = window.getSelection();
                selectionObj.removeAllRanges();
                selectionObj.addRange(range);
            } else {
                alert('Link URL is required.');
            }
        } else {
            alert('Please select some text first.');
        }
    }

    
    // Functions to increase or decrease font size
    window.increaseFontSize = function() {
        document.execCommand('fontSize', false, '4'); // Set to the largest size
    }

    window.decreaseFontSize = function() {
        document.execCommand('fontSize', false, '3'); // Set to a smaller size
    }

    // Function to toggle highlight
    window.toggleHighlight = function() {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const parentNode = range.startContainer.parentNode;
            if (parentNode.nodeType === 1 && parentNode.style.backgroundColor === 'yellow') {
                document.execCommand('hiliteColor', false, 'transparent');
            } else {
                document.execCommand('hiliteColor', false, 'yellow');
            }
        }
    }

    // Function to format text
    window.formatText = function(command) {
        document.execCommand(command, false, null);
    }

    // Function to prepare form submission
    function prepareFormSubmission() {
        var editorContent = document.getElementById('editor').innerHTML;
        document.getElementById('hiddenBody').value = editorContent;
    }

    // Show/hide toolbar functions
    function showToolbar() {
        toolbar.style.display = "block";
    }

    function hideToolbar() {
        toolbar.style.display = "none";
    }

    // Form validation
    function handleFormSubmission(event) {
        // Clear previous error messages and styles
        clearErrors();
        // Perform validation
        if (!validateForm()) {
            console.log('Validation failed.');
            // If validation fails, prevent form submission
            event.preventDefault();
            return false;
        }
        // If validation passes, prepare form submission (set editor content to hidden field)
        prepareFormSubmission();
    }

    function validateForm() {
        const title = document.getElementById('title').value;
        const summary = document.getElementById('summary').value;

        let isValid = true;

        // Validate title
        if (title.trim() === '') {
            showError('title', 'Please enter a title.');
            isValid = false;
        }

        // Validate summary
        if (summary.trim() === '' || summary.length > 100) {
            showError('summary', 'Summary should not be empty and should be less than 100 characters.');
            isValid = false;
        }

        const editorContent = document.getElementById('editor').innerHTML.trim();

        if (editorContent === '') {
            showError('editor', 'Content is required.', editor);
            document.getElementById('editor').classList.add('error-input');
            isValid = false;
        }

        return isValid; // Return true if all validations pass
    }

    function showError(fieldId, message) {
        const field = document.getElementById(fieldId);
        field.placeholder = message;
        field.classList.add('error-border');
    }

    function clearErrors() {
        const fields = ['title', 'summary'];
        fields.forEach(id => {
            const field = document.getElementById(id);
            field.placeholder = field.name.charAt(0).toUpperCase() + field.name.slice(1);
            field.classList.remove('error-border');
        });
    }
});
