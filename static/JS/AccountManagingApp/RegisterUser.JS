document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".auth-form");

    form.addEventListener("submit", function (e) {
        let valid = true;

        // Reset all errors
        document.querySelectorAll(".error").forEach(el => el.style.display = "none");

        // Username
        const username = document.getElementById("username");
        if (username.value.trim().length < 3) {
            showError(username, "Username must be at least 3 characters.");
            valid = false;
        }

        // Email
        const email = document.getElementById("email");
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value)) {
            showError(email, "Enter a valid email address.");
            valid = false;
        }

        // Phone
        const phone = document.getElementById("phone");
        const phoneRegex = /^[0-9]{10}$/;
        if (!phoneRegex.test(phone.value)) {
            showError(phone, "Enter a valid 10-digit phone number.");
            valid = false;
        }

        // Password
        const password = document.getElementById("password");
        if (password.value.length < 6) {
            showError(password, "Password must be at least 6 characters.");
            valid = false;
        }

        // Confirm Password
        const cpassword = document.getElementById("cpassword");
        if (password.value !== cpassword.value) {
            showError(cpassword, "Passwords do not match.");
            valid = false;
        }

        if (!valid) e.preventDefault(); // stop form submission
    });

    function showError(input, message) {
        let error = input.nextElementSibling;
        if (!error || !error.classList.contains("error")) {
            error = document.createElement("div");
            error.className = "error";
            input.parentNode.appendChild(error);
        }
        error.textContent = message;
        error.style.display = "block";
    }
});


// Trigger file input when overlay is clicked
document.querySelector(".overlay-icon").addEventListener("click", function () {
    document.getElementById("fileInput").click();
});

document.getElementById("fileInput").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("imagePreview").src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
});


