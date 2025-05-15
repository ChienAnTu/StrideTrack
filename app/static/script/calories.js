// document.addEventListener("DOMContentLoaded", function () {
//   const activitySelect = document.getElementById("activity");
//   const distanceContainer = document.getElementById("distance-container");

//   function toggleDistanceField() {
//     const selected = activitySelect.value.toLowerCase();
//     if (selected === "yoga") {
//       distanceContainer.style.display = "none";
//     } else {
//       distanceContainer.style.display = "block";
//     }
//   }

//   if (activitySelect && distanceContainer) {
//     toggleDistanceField();
//     activitySelect.addEventListener("change", toggleDistanceField);
//   }
// });
// -------------------------------------
// document.addEventListener("DOMContentLoaded", function () {
//   // === Hide distance when yoga selected ===
//   const activitySelect = document.getElementById("activity");
//   const distanceContainer = document.getElementById("distance-container");

//   function toggleDistanceField() {
//     const selected = activitySelect.value.toLowerCase();
//     distanceContainer.style.display = selected === "yoga" ? "none" : "block";
//   }

//   if (activitySelect && distanceContainer) {
//     toggleDistanceField();
//     activitySelect.addEventListener("change", toggleDistanceField);
//   }

//   // === Drag-and-Drop CSV Upload ===
//   const dropZone = document.getElementById("drop-zone");
//   const fileInput = document.getElementById("file-input");
//   const form = document.getElementById("csv-upload-form");

//   if (dropZone && fileInput && form) {
//     dropZone.addEventListener("dragover", (e) => {
//       e.preventDefault();
//       dropZone.classList.add("bg-gray-100");
//     });

//     dropZone.addEventListener("dragleave", () => {
//       dropZone.classList.remove("bg-gray-100");
//     });

//     dropZone.addEventListener("drop", (e) => {
//       e.preventDefault();
//       dropZone.classList.remove("bg-gray-100");
//       const files = e.dataTransfer.files;
//       if (files.length) {
//         fileInput.files = files;
//         form.submit();
//       }
//     });

//     fileInput.addEventListener("change", () => {
//       if (fileInput.files.length) {
//         form.submit();
//       }
//     });
//   }
// });
document.addEventListener("DOMContentLoaded", function () {
  // === Hide distance field when 'yoga' selected ===
  const activitySelect = document.getElementById("activity");
  const distanceContainer = document.getElementById("distance-container");

  function toggleDistanceField() {
    const selected = activitySelect.value.toLowerCase();
    distanceContainer.style.display = selected === "yoga" ? "none" : "block";
  }

  if (activitySelect && distanceContainer) {
    toggleDistanceField();
    activitySelect.addEventListener("change", toggleDistanceField);
  }

  // === Drag and Drop CSV Upload with File List ===
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const form = document.getElementById("csv-upload-form");
  const fileList = document.getElementById("file-list");
  const submitBtn = document.getElementById("submit-btn");

  let fileBuffer = [];

  function renderFileList() {
    fileList.innerHTML = "";
    fileBuffer.forEach((file, index) => {
      const li = document.createElement("li");
      li.className = "flex justify-between items-center bg-white rounded border p-2 shadow-sm";

      const name = document.createElement("span");
      name.textContent = file.name;

      const del = document.createElement("button");
      del.textContent = "❌";
      del.className = "text-red-500 hover:text-red-700 text-sm font-bold";
      del.addEventListener("click", () => {
        fileBuffer.splice(index, 1);
        renderFileList();
      });

      li.appendChild(name);
      li.appendChild(del);
      fileList.appendChild(li);
    });

    // Enable or disable submit button
    submitBtn.disabled = fileBuffer.length === 0;
  }

  function handleFiles(files) {
    for (let i = 0; i < files.length; i++) {
      if (files[i].type === "text/csv") {
        fileBuffer.push(files[i]);
      }
    }
    renderFileList();
  }

  if (dropZone && fileInput && form && fileList && submitBtn) {
    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.classList.add("bg-blue-50", "border-blue-400");
    });

    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("bg-blue-50", "border-blue-400");
    });

    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("bg-blue-50", "border-blue-400");
      handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener("change", () => {
      handleFiles(fileInput.files);
    });

    form.addEventListener("submit", (e) => {
      if (fileBuffer.length === 0) {
        e.preventDefault();
        return;
      }

      const dataTransfer = new DataTransfer();
      fileBuffer.forEach(file => dataTransfer.items.add(file));
      fileInput.files = dataTransfer.files; // override input
    });
  }
});
