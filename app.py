"""
Plant Manager REST API using Flask and SQLite
to run code enter "flask run --host=0.0.0.0 --port=8000" in to terminal
to stop code enter "ctrl + c" in terminal
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

# Closure-based Filter Maker
def make_filter(condition):
    """Creates a filter function based on the provided condition."""
    def filter_func(plant):
        return condition(plant)
    return filter_func

# General Filter Function for Plants
def get_filtered_plants(filter_func):
    plants = dao.get_all_plants()
    return [plant for plant in plants if filter_func(plant)]

# Endpoint to get plants with a custom filter using make_filter
@app.route("/plants/filter", methods=["GET"])
def filter_plants():
    filter_type = request.args.get("filter_type", "even")

    # Define filters using closures
    if filter_type == "even":
        even_id_filter = make_filter(lambda plant: plant.plant_id % 2 == 0)
        filtered_plants = get_filtered_plants(even_id_filter)
    elif filter_type == "odd":
        odd_id_filter = make_filter(lambda plant: plant.plant_id % 2 != 0)
        filtered_plants = get_filtered_plants(odd_id_filter)
    else:
        abort(400, description="Unknown filter type provided.")

    return jsonify(
        [{"id": plant.plant_id, "name": plant.name, "planted_date": plant.planted_date} for plant in filtered_plants]
    ), 200

# Additional filter with multiple arguments
@app.route("/plants/specific", methods=["GET"])
def get_specific_plant():
    plant_id = request.args.get("id", type=int)
    plant_name = request.args.get("name", type=str)

    if plant_id is None or plant_name is None:
        abort(400, description="Both 'id' and 'name' are required parameters.")

    # Lambda function that checks for both plant_id and plant_name
    specific_filter = lambda plant, id, name: plant.plant_id == id and plant.name == name

    # Use the lambda with the specific values for id and name
    plants = dao.get_all_plants()
    filtered_plants = [plant for plant in plants if specific_filter(plant, plant_id, plant_name)]

    return jsonify(
        [{"id": plant.plant_id, "name": plant.name, "planted_date": plant.planted_date} for plant in filtered_plants]
    ), 200

# Endpoint to sort plants based on user-defined criteria using lambdas
@app.route("/plants/sorted", methods=["GET"])
def get_sorted_plants():
    sort_by = request.args.get("sort_by", "name")  # Default sorting is by name

    plants = dao.get_all_plants()

    # Lambda for sorting by different criteria
    if sort_by == "name":
        sorted_plants = sorted(plants, key=lambda plant: plant.name.lower())
    elif sort_by == "planted_date":
        sorted_plants = sorted(plants, key=lambda plant: plant.planted_date)
    else:
        abort(400, description="Invalid sort criteria provided.")

    return jsonify(
        [{"id": plant.plant_id, "name": plant.name, "planted_date": plant.planted_date} for plant in sorted_plants]
    ), 200

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
