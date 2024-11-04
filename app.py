"""
Plant Manager REST API using Flask and SQLite
"""

from flask import Flask, jsonify, request, abort, render_template
from plant import Plant
from plant_dao import PlantDao
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize DAO
dao = PlantDao("garden.db")

# Serve the index.html (Web UI)
@app.route("/")
def index():
    return render_template("index.html")

# POST /plants - Add a new plant
@app.route("/plants", methods=["POST"])
def add_plant():
    data = request.json
    if not data or "name" not in data:
        abort(400, description="Bad Request: Plant name is required.")

    planted_date = datetime.now().strftime("%Y-%m-%d")
    new_plant = Plant(None, data["name"], planted_date)
    dao.add_plant(new_plant)
    return jsonify({"id": new_plant.plant_id, "message": "Plant added successfully"}), 201

# GET /plants - List all plants
@app.route("/plants", methods=["GET"])
def get_all_plants():
    plants = dao.get_all_plants()
    return jsonify(
        [{"id": plant.plant_id, "name": plant.name, "planted_date": plant.planted_date} for plant in plants]), 200

# New Endpoint - GET /plants/even - List plants with even IDs only
@app.route("/plants/even", methods=["GET"])
def get_even_id_plants():
    plants = dao.get_all_plants()
    even_plants = [plant for plant in plants if plant.plant_id % 2 == 0]
    return jsonify(
        [{"id": plant.plant_id, "name": plant.name, "planted_date": plant.planted_date} for plant in even_plants]), 200

# PUT /plants/<int:plant_id> - Update an existing plant
@app.route("/plants/<int:plant_id>", methods=["PUT"])
def update_plant(plant_id):
    plant = dao.get_plant(plant_id)
    if not plant:
        abort(404, description="Plant not found")

    data = request.json
    if not data or "name" not in data:
        abort(400, description="Bad Request: Plant name is required.")

    plant.name = data["name"]
    plant.planted_date = data.get("planted_date", plant.planted_date)
    if dao.update_plant(plant):
        return jsonify({"message": "Plant updated successfully"}), 200
    else:
        abort(400, description="Failed to update plant")

# DELETE /plants/<int:plant_id> - Delete a plant
@app.route("/plants/<int:plant_id>", methods=["DELETE"])
def delete_plant(plant_id):
    if dao.delete_plant(plant_id):
        return jsonify({"message": "Plant deleted successfully"}), 200
    else:
        abort(400, description="Failed to delete plant")

# Start the app
if __name__ == "__main__":
    app.run(debug=True)
