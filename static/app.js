document.addEventListener("DOMContentLoaded", function() {
    fetchPlants(); // Fetch all plants on page load
});

// Function to fetch and display only plants with even IDs
function showEvenIdPlants() {
    fetch("/plants/even")  // Use the new endpoint
        .then(response => response.json())
        .then(data => {
            const plantList = document.getElementById("plant-list");
            plantList.innerHTML = "";  // Clear existing entries

            data.forEach(plant => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${plant.id}</td>
                    <td>${plant.name}</td>
                    <td>${plant.planted_date}</td>
                    <td>
                        <button class="action-btn" onclick="editPlant(${plant.id})">Edit</button>
                        <button class="action-btn delete-btn" onclick="deletePlant(${plant.id})">Delete</button>
                    </td>
                `;
                plantList.appendChild(row);
            });
        });
}


// Fetch all plants from the server
function fetchPlants() {
    fetch("/plants")
        .then(response => response.json())
        .then(data => {
            const plantList = document.getElementById("plant-list");
            plantList.innerHTML = "";  // Clear existing entries

            data.forEach(plant => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${plant.id}</td>
                    <td>${plant.name}</td>
                    <td>${plant.planted_date}</td>
                    <td>
                        <button class="action-btn" onclick="editPlant(${plant.id})">Edit</button>
                        <button class="action-btn delete-btn" onclick="deletePlant(${plant.id})">Delete</button>
                    </td>
                `;
                plantList.appendChild(row);
            });
        });
}

// Add a new plant
function addPlant() {
    const plantName = document.getElementById("plant-name").value;
    if (!plantName) {
        alert("Please enter a plant name");
        return;
    }

    fetch("/plants", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: plantName })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById("plant-name").value = "";  // Clear input
        fetchPlants();  // Refresh plant list
    });
}

// Delete a plant
function deletePlant(plantId) {
    fetch(`/plants/${plantId}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchPlants();  // Refresh plant list
    });
}

// Edit plant (To be implemented, could show a popup or inline editing)
function editPlant(plantId) {
    const newName = prompt("Enter new plant name:");
    if (newName) {
        fetch(`/plants/${plantId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name: newName })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchPlants();  // Refresh plant list
        });
    }
}
