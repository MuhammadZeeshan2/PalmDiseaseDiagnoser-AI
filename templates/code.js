// document.addEventListener('DOMContentLoaded', function() {
//     document.getElementById('loginForm').addEventListener('submit', function(event) {
//         event.preventDefault();

//         const username = document.getElementById('username').value.trim();
//         const password = document.getElementById('password').value.trim();

//         if (username === '') {
//             alert('Please enter your username.');
//             return;
//         }
//         if (password === '') {
//             alert('Please enter your password.');
//             return;
//         }


//         console.log('Username:', username);
//         console.log('Password:', password);

//     });

//     document.getElementById('signupButton').addEventListener('click', function() {
//         window.location.href = 'signup.html';
//     });
// });


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loginForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        console.log(username)
        console.log(password)
        if (username === '') {
            alert('Please enter your username.');
            return;
        }
        if (password === '') {
            alert('Please enter your password.');
            return;
        }

        // Send AJAX request to Flask server for authentication
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, password: password })
        })
            .then(response => {
                if (response.ok) {
                    // Authentication successful, redirect to homepage
                    window.location.href = '/';
                } else {
                    // Authentication failed, display error message
                    alert('Authentication failed. Please check your credentials.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing your request.');
            });
    });

    document.getElementById('signupButton').addEventListener('click', function () {
        window.location.href = 'signup.html';
    });
});
