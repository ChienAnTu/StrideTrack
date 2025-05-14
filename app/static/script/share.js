document.addEventListener("DOMContentLoaded", function () {
  const selectAll = document.getElementById("select-all");
  const checkboxes = document.querySelectorAll(".row-checkbox");
  const shareForm = document.querySelector("form[action$='share']");
  const shareIdsInput = document.getElementById("share-ids");

  // Select All checkbox
  if (selectAll) {
    selectAll.addEventListener("change", () => {
      checkboxes.forEach(cb => cb.checked = selectAll.checked);
    });
  }

});

// Collect shared data id
function collectShareIds() {
  const checked = Array.from(document.querySelectorAll(".row-checkbox:checked"));
  const ids = checked.map(cb => cb.value);
  if (ids.length === 0) {
    alert("Please select at least one activity to share.");
    return false; // prevent submission
  }
  document.getElementById("share-ids").value = ids.join(",");
  return true;
}

// Delete button function
function setActionAndSubmit(action) {
  const form = document.getElementById("activity-form");
  const hidden = document.getElementById("form-action");
  hidden.value = action;
  form.submit();
}
