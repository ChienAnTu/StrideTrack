document.addEventListener("DOMContentLoaded", function () {
  const activitySelect = document.getElementById("activity");
  const distanceContainer = document.getElementById("distance-container");

  function toggleDistanceField() {
    const selected = activitySelect.value.toLowerCase();
    if (selected === "yoga") {
      distanceContainer.style.display = "none";
    } else {
      distanceContainer.style.display = "block";
    }
  }

  if (activitySelect && distanceContainer) {
    toggleDistanceField();
    activitySelect.addEventListener("change", toggleDistanceField);
  }
});
