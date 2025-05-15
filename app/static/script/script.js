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

// Flash Messages.
document.addEventListener("DOMContentLoaded", () => {
  const messagesEl = document.getElementById("toast-data");
  if (!messagesEl) return;

  const messages = JSON.parse(messagesEl.textContent);
  const container = document.getElementById("toast-container");
  if (!container) return;

  messages.forEach(([category, text]) => {
    const toast = document.createElement("div");
    toast.className = `
      px-6 py-4 rounded shadow-lg text-base font-semibold flex items-center justify-between gap-3
      ${category === 'success' ? 'bg-green-100 text-green-800' :
        category === 'error' ? 'bg-red-100 text-red-800' :
        'bg-gray-100 text-gray-800'}
      animate-fadeIn
      `;

    toast.innerHTML = `
      <span>${text}</span>
      <button class="text-lg leading-none" onclick="this.parentElement.remove()">×</button>
    `;

    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  });
});

