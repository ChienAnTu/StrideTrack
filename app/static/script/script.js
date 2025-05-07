function openSignIn() {
    document.getElementById('loginModal').classList.remove('hidden');
  }
  
  function closeSignIn() {
    document.getElementById('loginModal').classList.add('hidden');
  }

  // Open modal
function openSignUp() {
    document.getElementById('signupModal').classList.remove('hidden');
    document.body.classList.add('overflow-hidden'); // Prevent scrolling
  }
  
  // Close modal
  function closeSignup() {
    document.getElementById('signupModal').classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }
  
  // Close when clicking outside modal
  document.getElementById('signupModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('signupModal')) {
      closeSignup();
    }
  });

// Fetch module
// Login modal
document.querySelector('#loginModal form').addEventListener('submit', function (e) {
  e.preventDefault();

  const email = document.querySelector('#loginModal input[name="email"]').value;
  const password = document.querySelector('#loginModal input[name="password"]').value;

  fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        window.location.href = data.redirect || '/dashboard';
      } else {
        alert(data.error || 'Login failed.');
      }
    });
});

// Register modal
document.querySelector('#signupModal form').addEventListener('submit', function (e) {
  e.preventDefault(); 

  const email = document.querySelector('#signupModal input[name="email"]').value;
  const password = document.querySelector('#signupModal input[name="password"]').value;
  const confirmPassword = document.querySelector('#signupModal input[name="confirm-password"]').value;
  const first_name = document.querySelector('#signupModal input[name="first-name"]').value;
  const last_name = document.querySelector('#signupModal input[name="last-name"]').value;

  fetch('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, confirm_password: confirmPassword, first_name, last_name })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("Registration successful!");
        closeSignup();
        openSignIn();  // Open login modal after successful registration
      } else {
        alert(data.error || 'Registration failed.');
      }
    });
});
