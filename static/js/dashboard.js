// ----------------------
// 🔍 Search Functionality
// ----------------------
const search = document.getElementById("search");
const cards = document.querySelectorAll(".card-link");

if (search) {
  search.addEventListener("input", () => {
    const query = search.value.trim().toLowerCase();

    cards.forEach(card => {
      const text = card.innerText.toLowerCase();
      card.style.display = text.includes(query) ? "" : "none";
    });
  });
}

// ----------------------
// 👤 Dropdown Toggle for User Menu
// ----------------------
const userDropdown = document.querySelector(".user-dropdown");
const dropdownMenu = document.querySelector(".dropdown-menu");

if (userDropdown && dropdownMenu) {
  userDropdown.addEventListener("click", (e) => {
    e.stopPropagation(); // prevent closing immediately
    dropdownMenu.classList.toggle("show");
  });

  // Close when clicking outside
  document.addEventListener("click", (e) => {
    if (!userDropdown.contains(e.target)) {
      dropdownMenu.classList.remove("show");
    }
  });
}
