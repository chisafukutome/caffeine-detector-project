const remainingCaffeineDisplay = document.getElementById(
  "remaining_caffeine_display"
);

if (
  remainingCaffeineDisplay.innerText == "You can still take 0 mg of caffeine!"
) {
  remainingCaffeineDisplay.innerHTML =
    "You have surpassed the recommended limit for your daily dose of caffeine.";
}
