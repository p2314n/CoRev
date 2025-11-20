document.addEventListener("DOMContentLoaded", () => {
  const stars = document.querySelectorAll(".star");
  const ratingInput = document.getElementById("ratingInput");
  let selectedRating = parseInt(ratingInput.value) || 0;

  highlightStars(selectedRating);

  stars.forEach((star, index) => {
    star.addEventListener("mouseover", () => highlightStars(index + 1));
    star.addEventListener("mouseout", () => highlightStars(selectedRating));

    star.addEventListener("click", () => {
      // If the user clicks the same star again, deselect all
      if (selectedRating === index + 1) {
        selectedRating = 0;
      } else {
        selectedRating = index + 1;
      }

      ratingInput.value = selectedRating || "";
      highlightStars(selectedRating);
    });
  });

  reviewText.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      if (e.shiftKey) {
        return;
      } else {
        e.preventDefault(); // Stop newline
        form.submit(); // Submit review
      }
    }
  });

  function highlightStars(count) {
    stars.forEach((star, i) => {
      star.classList.toggle("glow", i < count);
    });
  }
});