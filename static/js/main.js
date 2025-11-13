// Set up OSM map. This will be used for defining the bounding box.
const map = L.map("map").setView([51.5, -0.12], 13);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors" // Attribution required. Include elsewhere if necessary.
}).addTo(map);

// Add draw controls
const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);
const drawControl = new L.Control.Draw({
    draw: {
        polygon: false,
        polyline: false,
        circle: false,
        marker: false,
        circlemarker: false,
        rectangle: true
    },
    edit: { featureGroup: drawnItems }
});
// It's ideal to keep all of the draw functions false, considering it'll just make a rectange anyway.
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function (e) {
    drawnItems.clearLayers(); // only one box at a time
    const layer = e.layer;
    drawnItems.addLayer(layer);

    const b = layer.getBounds();
    const sw = b.getSouthWest();
    const ne = b.getNorthEast();
    const bbox = [sw.lng, sw.lat, ne.lng, ne.lat];

    // Check area in degrees (must not exceed 0.01 square degrees)
    const width = ne.lng - sw.lng;
    const height = ne.lat - sw.lat;
    const area = width * height;
    if (area > 0.01) {
        document.getElementById("status").textContent =
            "Warning: BBox area is " + area.toFixed(4) + " deg², larger than 0.01.";
    } else {
        document.getElementById("status").textContent =
            "BBox set: " + bbox.map(v => v.toFixed(6)).join(", ");
    }

    // Send to backend
    fetch("/set_bbox", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bbox })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Server bbox updated:", data);
    });
});

async function loadRandom() {
    const btn = document.getElementById("next-btn");
    const img = document.getElementById("static-img");
    const status = document.getElementById("status");

    btn.disabled = true;
    status.textContent = "Loading...";
    try {
        const res = await fetch("/random.json");
        const meta = await res.json();

        if (meta.error) {
            status.textContent = meta.error;
            btn.disabled = false;
            return;
        }

        img.onload = () => {
            btn.disabled = false;
            status.textContent = "Loaded.";
        };
        img.onerror = () => {
            btn.disabled = false;
            status.textContent = "Failed to load image.";
        };
        img.src = meta.thumb_url;
    } catch (err) {
        console.error(err);
        btn.disabled = false;
        status.textContent = "Request failed.";
    }
}