// Open login modal
function openSignIn() {
  const loginModal = document.getElementById('loginModal');
  if (loginModal) {
    loginModal.classList.remove('hidden');
  }
}

// Close login modal
function closeSignIn() {
  const loginModal = document.getElementById('loginModal');
  if (loginModal) {
    loginModal.classList.add('hidden');
  }
}

// Open signup modal
function openSignUp() {
  const signupModal = document.getElementById('signupModal');
  if (signupModal) {
    signupModal.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }
}

// Close signup modal
function closeSignup() {
  const signupModal = document.getElementById('signupModal');
  if (signupModal) {
    signupModal.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }
}

// Close when clicking outside modal
const signupModal = document.getElementById('signupModal');
if (signupModal) {
  signupModal.addEventListener('click', (e) => {
    if (e.target === signupModal) {
      closeSignup();
    }
  });
}
