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