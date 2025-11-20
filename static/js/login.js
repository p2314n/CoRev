(function () {
  const form = document.getElementById('loginForm');
  const username = document.getElementById('username');
  const password = document.getElementById('password');
  const usernameNote = document.getElementById('usernameNote');
  const passwordNote = document.getElementById('passwordNote');
  const toggle = document.getElementById('togglePassword');

  // Validation on blur
  username.addEventListener('blur', () => {
    usernameNote.textContent = username.validity.valueMissing ? 'Username is required.' : '';
  });

  password.addEventListener('blur', () => {
    passwordNote.textContent = password.validity.valueMissing ? 'Password is required.' : '';
  });

  // Show/Hide password toggle
  toggle.addEventListener('click', () => {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    toggle.textContent = type === 'password' ? '👁️' : '🙈';
  });

  // Prevent invalid submission
  form.addEventListener('submit', (e) => {
    if (!form.checkValidity()) {
      e.preventDefault();
      usernameNote.textContent = username.validity.valueMissing ? 'Username is required.' : '';
      passwordNote.textContent = password.validity.valueMissing ? 'Password is required.' : '';
    }
  });
})();