const imageOverlay = document.getElementById('imageOverlay');
const imageInput = document.getElementById('imageInput');
const postImagePreview = document.getElementById('postImagePreview');

// Open file browser when overlay clicked
imageOverlay.addEventListener('click', () => {
    imageInput.click();
});

// Live preview when file selected
imageInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            postImagePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});
