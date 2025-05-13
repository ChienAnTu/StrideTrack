function openSignIn() {
    document.getElementById('loginModal').classList.remove('hidden');
  }
  
  function closeSignIn() {
    document.getElementById('loginModal').classList.add('hidden');
  }

  // Open modal
function openSignUp() {
    document.getElementById('signupModal').classList.remove('hidden');
    document.body.classList.add('overflow-hidden'); // Prevent scrolling
  }
  
  // Close modal
  function closeSignup() {
    document.getElementById('signupModal').classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }
  
  // Close when clicking outside modal
  document.getElementById('signupModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('signupModal')) {
      closeSignup();
    }
  });

  // Define a trail as an array of LatLng points
var trailCoordinates = [
  [51.505, -0.09],
  [51.506, -0.092],
  [51.507, -0.093],
  [51.508, -0.095]
];

// Add the polyline to the map
var trailPath = L.polyline(trailCoordinates, {
  color: 'blue',
  weight: 5,
  opacity: 0.7,
  smoothFactor: 1
}).addTo(map);

// Zoom the map to fit the trail
map.fitBounds(trailPath.getBounds());
