document.addEventListener("DOMContentLoaded", function () {
  // Tab toggle
  const tabManual = document.getElementById("tab-manual");
  const tabTrail = document.getElementById("tab-trail");
  const manualCard = document.getElementById("manual-card");
  const trailCard = document.getElementById("trail-card");

  if (tabManual && tabTrail && manualCard && trailCard) {
    tabManual.addEventListener("click", () => {
      manualCard.classList.remove("hidden");
      trailCard.classList.add("hidden");
      tabManual.classList.replace("bg-gray-200", "bg-orange-600");
      tabManual.classList.replace("text-gray-700", "text-white");
      tabTrail.classList.replace("bg-orange-600", "bg-gray-200");
      tabTrail.classList.replace("text-white", "text-gray-700");
    });

    tabTrail.addEventListener("click", () => {
      trailCard.classList.remove("hidden");
      manualCard.classList.add("hidden");
      tabTrail.classList.replace("bg-gray-200", "bg-orange-600");
      tabTrail.classList.replace("text-gray-700", "text-white");
      tabManual.classList.replace("bg-orange-600", "bg-gray-200");
      tabManual.classList.replace("text-white", "text-gray-700");

      if (map) {
        setTimeout(() => {
          map.invalidateSize();
        }, 200);
      }
    });
  }


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

// ========== Trail GPX + Form Auto-fill ==========

// Define trail data
const trails = {
  kingsPark: {
    name: "Kings Park",
    gpx: "/static/trails/kingsPark.gpx",
    activity: "running",
    distance_km: 8.1,
    duration_min: 240,
    difficulty: "Hard",
    description: "Challenging ridge walk with steep sections and exposed areas."
  },
  hydePark: {
    name: "Hyde Park",
    gpx: "/static/trails/hydePark.gpx",
    activity: "walking",
    distance_km: 3.7,
    duration_min: 90,
    difficulty: "Easy",
    description: "Gentle loop through wildflower meadows, perfect for families."
  }
  // 👉 若有其他 trail 可繼續擴充
};

// Initialize map
const mapContainer = document.getElementById("trail-map");
let map, activeLayer;
if (mapContainer) {
  map = L.map("trail-map").setView([-31.95, 115.86], 13); // Default Perth area
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "Map data © OpenStreetMap contributors"
  }).addTo(map);
}

// Load trail and fill data
function loadTrail(trailId) {
  const trail = trails[trailId];
  if (!trail || !map) return;

  // Clear previous layer
  if (activeLayer) map.removeLayer(activeLayer);

  // Load GPX
  fetch(trail.gpx)
    .then((res) => res.text())
    .then((gpxData) => {
      activeLayer = new L.GPX(gpxData, {
        async: true,
        polyline_options: {
          color: "#10B981",
          weight: 4
        },
        marker_options: {
          startIconUrl: null,
          endIconUrl: null
        }
      }).on("loaded", function (e) {
        map.fitBounds(e.target.getBounds());
      }).addTo(map);
    });

  // Update trail info
  document.getElementById("trail-name").textContent = trail.name;
  document.getElementById("trail-distance").textContent = `${trail.distance_km} km`;
  document.getElementById("trail-duration").textContent = `${trail.duration_min} mins`;
  document.getElementById("trail-difficulty").textContent = trail.difficulty;
  document.getElementById("trail-description").textContent = trail.description;
  document.getElementById("trail-details").classList.remove("hidden");

  // === Auto-fill form fields ===
  const activityField = document.getElementById("trail_activity");
  const durationField = document.getElementById("trail_duration");
  const distanceField = document.getElementById("trail_distance_m");

  if (activityField) activityField.value = trail.activity;
  if (durationField) durationField.value = trail.duration_min;
  if (distanceField) distanceField.value = trail.distance_km * 1000;
}

// Handle activity filter
const filterSelect = document.getElementById("activity-select");
if (filterSelect) {
  filterSelect.addEventListener("change", () => {
    const selected = filterSelect.value;
    document.querySelectorAll(".trail-card").forEach((card) => {
      const activity = card.getAttribute("data-activity");
      const visible = selected === "all" || activity === selected;
      card.style.display = visible ? "block" : "none";
    });

    // Hide trail info
    document.getElementById("trail-details").classList.add("hidden");
  });
}

// Handle trail card click
document.querySelectorAll(".trail-card").forEach((card) => {
  card.addEventListener("click", () => {
    const trailId = card.dataset.trail;
    loadTrail(trailId);
  });
});

// Sync trail_weight input to main weight field
const trailWeightInput = document.getElementById("trail_weight");
if (trailWeightInput) {
  trailWeightInput.addEventListener("input", () => {
    const weightInput = document.getElementById("weight");
    if (weightInput) weightInput.value = trailWeightInput.value;
  });
}
