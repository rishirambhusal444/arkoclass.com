function handleKeyDown(event, field) {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (field === 'title') {
                document.getElementById('editor').focus();
            } else if (field === 'summary') {
                hideToolbar();
                document.getElementById('submit').focus();
            }
        }
}
function uploadImage(event) {
  const file = event.target.files[0];
  if (file) {
    const formData = new FormData();
    formData.append('image', file);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}'); // Replace with actual CSRF token
    fetch('{% url "upload_image" %}', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const imgTag = `<img src="${data.url}" alt="Uploaded Image" style="max-width: 100%;">`;
        insertHtmlAtCursor(imgTag);
        document.getElementById('hiddenBody').value = document.getElementById('editor').innerHTML;
      } else {
        console.error('Error uploading image:', data.message);
      }
    })
    .catch(error => console.error('Error:', error));
  }
}

function insertHtmlAtCursor(html) {
  const range = window.getSelection().getRangeAt(0);
  const frag = document.createRange().createContextualFragment(html);
  range.insertNode(frag);
  range.collapse(false);  // Move the cursor to the end of the inserted element
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
}
document.getElementById('article-image-input').addEventListener('change', uploadImage);
function triggerImageUpload() {
  document.getElementById('article-image-input').click();
}
function increaseFontSize() {
    document.execCommand('fontSize', false, '4'); // Set to the largest size
  }

function decreaseFontSize() {
    document.execCommand('fontSize', false, '3'); // Set to a smaller size
  }
function toggleHighlight() 
{
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
function formatText(command) 
{
        document.execCommand(command, false, null);
}


function prepareFormSubmission() {
    var editorContent = document.getElementById('editor').innerHTML;
    document.getElementById('hiddenBody').value = editorContent;
  }

  document.getElementById('article-form').addEventListener('submit', prepareFormSubmission);



//this is for show /hide toolbar 
document.addEventListener("DOMContentLoaded", function() {
    const editor = document.getElementById("editor");
    const toolbar = document.getElementById("tools");
    
    function showToolbar() {
        toolbar.style.display = "block";
    }

    function hideToolbar() {
        toolbar.style.display = "none";
    }

    editor.addEventListener("focus", function() {
        showToolbar();
    });

    document.addEventListener("click", function(event) {
        if (!editor.contains(event.target) && !toolbar.contains(event.target)) {
            hideToolbar();
        }
    });

    hideToolbar();

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
            }
        }


    });



    // Bind handleKeyDown to specific fields if needed
    // Example:
    // document.getElementById('title').addEventListener('keydown', (event) => handleKeyDown(event, 'title'));
    // document.getElementById('summary').addEventListener('keydown', (event) => handleKeyDown(event, 'summary'));
});


  // this is for form Validity

  
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
      // Additional validation logic can be added here

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


  // Add event listener to form for handling submission
  document.getElementById('article-form').addEventListener('submit', handleFormSubmission);

function applyLink() {
  let url = document.getElementById('link-input').value.trim();
    // Check if the URL starts with 'http://' or 'https://'
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        // If not, prepend 'http://'
        url = 'http://' + url;
    }
    if (url) {
        document.execCommand('createLink', false, url);
        document.getElementById('link-input').value = '';  // Clear the input field after applying the link
        document.getElementById('link-input-container').style.display = 'none';  // Hide the input field after applying the link
    }
}
