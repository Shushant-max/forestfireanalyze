// Forest Fire Detection System - Frontend JavaScript

let selectedFile = null;
let map = null;
let markers = [];

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const predictBtn = document.getElementById('predictBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const previewImage = document.getElementById('previewImage');
const predictionBadge = document.getElementById('predictionBadge');
const confidenceValue = document.getElementById('confidenceValue');
const confidenceFill = document.getElementById('confidenceFill');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const locationSection = document.getElementById('locationSection');
const mapSection = document.getElementById('mapSection');
const view360Section = document.getElementById('view360Section');
const view360Image = document.getElementById('view360Image');
const view360Label = document.getElementById('view360Label');
const view360Description = document.getElementById('view360Description');
const latitudeInput = document.getElementById('latitude');
const longitudeInput = document.getElementById('longitude');

const firePanoramaImages = [
    'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1495427513695-ade6f5b9d887?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1501719539450-48b5b90d73e8?auto=format&fit=crop&w=1200&q=80'
];

const forestPanoramaImages = [
    'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1518837695005-2083093ee35b?auto=format&fit=crop&w=1200&q=80'
];

// Event Listeners
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

predictBtn.addEventListener('click', predictFire);

// Functions
function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file.');
        return;
    }

    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.style.display = 'flex';
    predictBtn.disabled = false;
    hideError();
    hideResults();
}

function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    predictBtn.disabled = true;
    hideResults();
    hideError();
    hideLocationAndMap();
    if (view360Section) {
        view360Section.style.display = 'none';
    }
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function hideResults() {
    resultsSection.style.display = 'none';
}

function hideLocationAndMap() {
    locationSection.style.display = 'none';
    mapSection.style.display = 'none';
}

function showLoading() {
    predictBtn.disabled = true;
    loadingSpinner.style.display = 'block';
    predictBtn.querySelector('.btn-text').textContent = 'Analyzing...';
}

function hideLoading() {
    predictBtn.disabled = false;
    loadingSpinner.style.display = 'none';
    predictBtn.querySelector('.btn-text').textContent = 'Detect Fire';
}

async function predictFire() {
    if (!selectedFile) {
        showError('Please select an image first.');
        return;
    }

    showLoading();
    hideError();

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('http://localhost:5000/api/predict', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            displayResults(result);
        } else {
            showError(result.error || 'An error occurred during prediction.');
        }
    } catch (error) {
        showError('Failed to connect to the server. Please make sure the backend is running.');
        console.error('Prediction error:', error);
    } finally {
        hideLoading();
    }
}

function displayResults(result) {
    // Display uploaded image
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
    };
    reader.readAsDataURL(selectedFile);

    // Display prediction
    const isFire = result.prediction === 'Fire Detected';
    const badgeClass = isFire ? 'fire' : 'safe';
    const badgeText = result.prediction;

    predictionBadge.innerHTML = `<div class="badge ${badgeClass}">${badgeText}</div>`;

    // Display confidence
    const confidencePercent = (result.confidence * 100).toFixed(1);
    confidenceValue.textContent = `${confidencePercent}%`;
    confidenceFill.style.width = `${confidencePercent}%`;

    // Show results section and visual preview controls
    resultsSection.style.display = 'block';
    mapSection.style.display = 'block';
    if (view360Section) {
        view360Section.style.display = 'block';
    }

    initializeMap();
    show360Preview(isFire);

    if (isFire) {
        locationSection.style.display = 'block';
        showRandomFireLocation(parseFloat(confidencePercent) / 100);
    } else {
        locationSection.style.display = 'none';
        showRandomForestLocation();
    }

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadUserProfile();
    requireLogin();

    // Check if backend is running
    fetch('http://localhost:5000/api/health')
        .then(response => response.json())
        .then(data => {
            console.log('Backend status:', data);
        })
        .catch(error => {
            console.warn('Backend not running:', error);
            showError('Warning: Backend server is not running. Please start the backend server first.');
        });
});

function requireLogin() {
    const user = getUserSession();
    if (!user) {
        window.location.href = 'login.html';
        return false;
    }
    updateUserStatus(user);
    return true;
}

function updateUserStatus(user) {
    const statusText = document.getElementById('userStatusText');
    const logoutHeaderBtn = document.getElementById('logoutHeaderBtn');
    if (statusText) {
        statusText.textContent = `Signed in as ${user.name}`;
    }
    if (logoutHeaderBtn) {
        logoutHeaderBtn.style.display = 'inline-flex';
    }
}

// Map Functions
function initializeMap() {
    if (map) {
        map.remove();
        markers = [];
    }

    // Show map section first so Leaflet can compute dimensions
    mapSection.style.display = 'block';

    // Default center for satellite view
    const defaultLat = 20.0;
    const defaultLng = 78.0;

    map = L.map('map', {
        center: [defaultLat, defaultLng],
        zoom: 3,
        zoomControl: true
    });

    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community',
        maxZoom: 19
    }).addTo(map);

    // Ensure the map resizes after being shown
    setTimeout(() => {
        map.invalidateSize();
    }, 200);
}

function getRandomFireLocation() {
    // Real fire-prone regions with location names
    const hotspots = [
        { name: 'Bolivian Andes', lat: -16.4897, lng: -68.1193, region: 'South America', season: 'Aug-Nov' },
        { name: 'Brazilian Cerrado', lat: -14.2350, lng: -51.9253, region: 'Brazil', season: 'Jul-Oct' },
        { name: 'Eastern Woodlands', lat: 38.9072, lng: -77.0369, region: 'USA East Coast', season: 'Jul-Sep' },
        { name: 'California Chaparral', lat: 37.7749, lng: -122.4194, region: 'California, USA', season: 'Jun-Nov' },
        { name: 'Canadian Boreal', lat: 45.4215, lng: -75.6972, region: 'Eastern Canada', season: 'Jun-Aug' },
        { name: 'European Forests', lat: 52.5200, lng: 13.4050, region: 'Central Europe', season: 'Jul-Sep' },
        { name: 'Mediterranean Scrub', lat: 36.5000, lng: 11.0000, region: 'Southern Europe', season: 'Jul-Oct' },
        { name: 'Asian Steppe', lat: 45.0000, lng: 110.0000, region: 'Mongolia', season: 'May-Oct' }
    ];
    const index = Math.floor(Math.random() * hotspots.length);
    return hotspots[index];
}

function showRandomFireLocation(confidence) {
    if (!map) {
        initializeMap();
    }

    const location = getRandomFireLocation();
    addEnhancedFireMarker(location.lat, location.lng, confidence, location.name, location.region, location.season);
}

function showRandomForestLocation() {
    if (!map) {
        initializeMap();
    }

    const forestLocations = [
        { name: 'Glacier National Park', lat: 48.7519, lng: -113.9020, region: 'Montana, USA', type: 'Alpine Forest' },
        { name: 'Schwarzwald Forest', lat: 48.5500, lng: 8.2500, region: 'Germany', type: 'Central European Forest' },
        { name: 'Mt. Fuji Forest Belt', lat: 35.3136, lng: 138.7278, region: 'Japan', type: 'Temperate Forest' },
        { name: 'Olympic National Forest', lat: 47.9790, lng: -122.4720, region: 'Washington, USA', type: 'Rainforest' },
        { name: 'Amazon Rainforest', lat: -5.5321, lng: -63.6132, region: 'Brazil', type: 'Tropical Rainforest' },
        { name: 'Taiga Forest', lat: 60.0000, lng: 95.0000, region: 'Siberia, Russia', type: 'Boreal Forest' },
        { name: 'Congo Basin Forest', lat: 2.5000, lng: 24.0000, region: 'Central Africa', type: 'Tropical Rainforest' },
        { name: 'Tongass National Forest', lat: 58.0000, lng: -133.0000, region: 'Alaska, USA', type: 'Temperate Rainforest' }
    ];
    const index = Math.floor(Math.random() * forestLocations.length);
    const forest = forestLocations[index];
    addForestMarker(forest.lat, forest.lng, forest.name, forest.region, forest.type);
}

function addForestMarker(lat, lng, name, region, type) {
    if (!map) return;

    const markerColor = '#22c55e';
    const markerIcon = L.divIcon({
        className: 'custom-marker',
        html: `<div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); width: 32px; height: 32px; border-radius: 50%; border: 4px solid white; box-shadow: 0 4px 12px rgba(34,197,94,0.45); display: flex; align-items: center; justify-content: center; font-size: 18px;">🌲</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    const marker = L.marker([lat, lng], { icon: markerIcon }).addTo(map);

    const popupContent = `
        <div style="text-align: center; font-family: 'Arial', sans-serif; padding: 8px;">
            <strong style="color: #16a34a; font-size: 1.1rem;">✅ Safe Forest Area</strong><br>
            <span style="color: #047857; font-weight: 600;">${name}</span><br>
            <span style="color: #059669; font-size: 0.9rem;">${region}</span><br>
            <span style="color: #10b981; font-size: 0.85rem;">${type}</span><br>
            <span style="color: #7c3aed; font-size: 0.85rem;">📍 ${lat.toFixed(4)}, ${lng.toFixed(4)}</span>
        </div>
    `;

    marker.bindPopup(popupContent).openPopup();
    markers.push(marker);
    map.setView([lat, lng], 9);
}

function addEnhancedFireMarker(lat, lng, confidence, name, region, season) {
    if (!map) return;

    const markerIcon = L.divIcon({
        className: 'custom-marker',
        html: `<div style="background: linear-gradient(135deg, #ff5f67 0%, #ff8a3f 100%); width: 40px; height: 40px; border-radius: 50%; border: 4px solid white; box-shadow: 0 6px 16px rgba(255,95,103,0.55); display: flex; align-items: center; justify-content: center; font-size: 20px; animation: pulse 2s infinite;\">🔥</div>`,
        iconSize: [40, 40],
        iconAnchor: [20, 20]
    });

    const marker = L.marker([lat, lng], { icon: markerIcon }).addTo(map);

    const popupContent = `
        <div style="text-align: center; font-family: 'Arial', sans-serif; padding: 10px; min-width: 220px;\">\n            <strong style=\"color: #d9534f; font-size: 1.15rem;\">🔥 Fire Alert Zone</strong><br>\n            <span style=\"color: #c1121f; font-weight: 600; font-size: 1.05rem;\">${name}</span><br>\n            <span style=\"color: #05668d; font-size: 0.9rem;\">📍 ${region}</span><br>\n            <span style=\"color: #ff6b35; font-size: 0.85rem;\">📅 Peak Season: ${season}</span><br>\n            <span style=\"color: #ff8c42; font-weight: 600;\">Confidence: ${(confidence * 100).toFixed(1)}%</span><br>\n            <span style=\"color: #7c3aed; font-size: 0.85rem;\">\uff0e ${lat.toFixed(4)}, ${lng.toFixed(4)}</span>\n        </div>\n    `;

    marker.bindPopup(popupContent).openPopup();
    markers.push(marker);
    map.setView([lat, lng], 11);
}

function show360Preview(isFire) {
    const imageUrl = getRandom360Image(isFire);
    const title = isFire ? 'Fire Panorama' : 'Forest Panorama';
    const description = isFire
        ? 'Simulated 360° fire hotspot preview in satellite view.'
        : 'A calm forest 360° preview showing no fire activity.';

    set360Viewer(imageUrl, title, description);
}

function getRandom360Image(isFire) {
    const pool = isFire ? firePanoramaImages : forestPanoramaImages;
    return pool[Math.floor(Math.random() * pool.length)];
}

function set360Viewer(url, title, description) {
    if (!view360Section || !view360Image || !view360Label || !view360Description) {
        return;
    }
    view360Image.src = url;
    view360Label.textContent = title;
    view360Description.textContent = description;
}

function randomizeView() {
    const isFire = predictionBadge.querySelector('.badge.fire') !== null;
    show360Preview(isFire);
}

function addFireMarker(lat, lng, confidence) {
    if (!map) return;

    const isFire = confidence > 0.5;
    const markerColor = isFire ? '#ff3d3d' : '#28a745';
    const markerEmoji = isFire ? '🔥' : '✅';
    const markerIcon = L.divIcon({
        className: 'custom-marker',
        html: `<div style="background: linear-gradient(135deg, ${isFire ? '#ff5f67' : '#22c55e'} 0%, ${isFire ? '#ff8a3f' : '#16a34a'} 100%); width: 32px; height: 32px; border-radius: 50%; border: 4px solid white; box-shadow: 0 4px 12px ${isFire ? 'rgba(255,95,103,0.45)' : 'rgba(34,197,94,0.45)'}; display: flex; align-items: center; justify-content: center; font-size: 18px;">${markerEmoji}</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    const marker = L.marker([lat, lng], { icon: markerIcon }).addTo(map);

    const statusText = isFire ? '🔥 Fire Detected Area' : '✅ Safe Forest Area';
    const popupContent = `
        <div style="text-align: center; font-family: 'Arial', sans-serif; padding: 8px;">
            <strong style="color: ${isFire ? '#d9534f' : '#047857'}; font-size: 1.1rem;">\${statusText}</strong><br>
            Confidence: ${(confidence * 100).toFixed(1)}%<br>
            <span style="color: #7c3aed; font-size: 0.85rem;">📍 ${lat.toFixed(4)}, ${lng.toFixed(4)}</span>
        </div>
    `;

    marker.bindPopup(popupContent).openPopup();
    markers.push(marker);
    map.setView([lat, lng], isFire ? 12 : 9);
}
function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;

                latitudeInput.value = lat;
                longitudeInput.value = lng;

                // Update map view
                if (map) {
                    map.setView([lat, lng], 12);
                }
            },
            (error) => {
                console.error('Error getting location:', error);
                showError('Unable to get your current location. Please enter coordinates manually.');
            }
        );
    } else {
        showError('Geolocation is not supported by this browser.');
    }
}

function addLocationToMap() {
    const lat = parseFloat(latitudeInput.value);
    const lng = parseFloat(longitudeInput.value);

    if (isNaN(lat) || isNaN(lng)) {
        showError('Please enter valid latitude and longitude coordinates.');
        return;
    }

    if (lat < -90 || lat > 90 || lng < -180 || lng > 180) {
        showError('Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180.');
        return;
    }

    // Add marker with current prediction confidence
    const confidence = parseFloat(confidenceValue.textContent) / 100;
    addFireMarker(lat, lng, confidence);

    // Clear inputs
    latitudeInput.value = '';
    longitudeInput.value = '';
}

// Make functions globally available
window.getCurrentLocation = getCurrentLocation;
window.addLocationToMap = addLocationToMap;
