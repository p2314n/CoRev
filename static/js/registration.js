(function () {
  const form = document.getElementById('regForm');
  const first = document.getElementById('firstName');
  const last = document.getElementById('lastName');
  const firstNote = document.getElementById('firstNameNote');
  const lastNote = document.getElementById('lastNameNote');
  const select = document.getElementById('designation');
  const otherWrap = document.getElementById('otherWrapper');
  const otherText = document.getElementById('otherText');
  const username = document.getElementById('username');
  const password = document.getElementById('password');
  const usernameNote = document.getElementById('usernameNote');
  const passwordNote = document.getElementById('passwordNote');

  username.addEventListener('blur', () => {
    usernameNote.textContent = username.validity.valueMissing ? 'Username is required.' : '';
  });

  password.addEventListener('blur', () => {
    passwordNote.textContent = password.validity.valueMissing ? 'Password is required.' : '';
  });

  // ✅ Password strength check (at least 6 chars, 1 number, 1 special character)
  const passwordPattern = /^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{6,}$/;

  password.addEventListener('input', () => {
    const pass = password.value;
    if (pass.length === 0) {
      passwordNote.textContent = '';
      passwordNote.style.color = '';
      return;
    }

    if (!passwordPattern.test(pass)) {
      passwordNote.textContent = '❌ Must be at least 6 characters, include a number, a special character(eg. @,#), one Uppercase and one Lowercase character';
      passwordNote.style.color = 'red';
    } else {
      passwordNote.textContent = '✅ Strong password!';
      passwordNote.style.color = 'green';
    }
  });

  function toggleOther() {
    const isOther = select.value === 'other';
    otherWrap.style.display = isOther ? 'block' : 'none';
    otherText.required = isOther;
    if (!isOther) otherText.value = '';
  }
  select.addEventListener('change', toggleOther);
  toggleOther();

  function showHint(input, hintEl, field) {
    if (input.validity.valueMissing) {
      hintEl.textContent = field + ' is required.';
    } else {
      hintEl.textContent = '';
    }
  }

  first.addEventListener('blur', () => showHint(first, firstNote, 'First name'));
  last.addEventListener('blur', () => showHint(last, lastNote, 'Last name'));

  form.addEventListener('submit', (e) => {
    if (!form.checkValidity()) {
      e.preventDefault();
      showHint(first, firstNote, 'First name');
      showHint(last, lastNote, 'Last name');
      if (!select.value) select.reportValidity();
      return;
    }

    // ✅ Prevent submission if password is weak
    if (!passwordPattern.test(password.value)) {
      e.preventDefault();
      alert('Must be at least 6 characters, include a number, a special character(eg. @,#), one Uppercase and one Lowercase character');
      password.focus();
      return;
    }
  });
})();

// 👁️ Show/Hide Password Toggle
document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");

  if (toggleBtn && passwordInput) {
    toggleBtn.addEventListener("click", () => {
      const isPassword = passwordInput.getAttribute("type") === "password";
      passwordInput.setAttribute("type", isPassword ? "text" : "password");
      toggleBtn.textContent = isPassword ? "🙈" : "👁️";
      toggleBtn.setAttribute("aria-label", isPassword ? "Hide password" : "Show password");
    });
  }
});