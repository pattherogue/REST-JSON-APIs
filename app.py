# Import necessary modules and classes from Flask and the custom models module
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
from flask_cors import CORS

# Create Flask app instance
app = Flask(__name__)
CORS(app)

# Configure app to connect to the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

# Connect the app to the database
connect_db(app)

# Define route for the homepage
@app.route("/")
def root():
    """Render homepage."""
    return render_template("index.html")

# Define route to get all cupcakes in the system
@app.route("/api/cupcakes")
def list_cupcakes():
    """Return all cupcakes in system.

    Returns JSON like:
        {cupcakes: [{id, flavor, rating, size, image}, ...]}
    """
    # Query all cupcakes from the database and convert them to dictionary format
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    # Return the cupcakes data as JSON
    return jsonify(cupcakes=cupcakes)

# Define route to create a new cupcake
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add cupcake, and return data about new cupcake.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """
    # Get the JSON data from the request
    data = request.json
    # Create a new cupcake instance with data from the request
    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)
    # Add the new cupcake to the database session and commit changes
    db.session.add(cupcake)
    db.session.commit()
    # Return the newly created cupcake data as JSON with status code 201 (created)
    return (jsonify(cupcake=cupcake.to_dict()), 201)

# Define route to get data on a specific cupcake
@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return data on specific cupcake.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """
    # Query the specific cupcake from the database by its ID, return 404 if not found
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    # Return the cupcake data as JSON
    return jsonify(cupcake=cupcake.to_dict())

# Define route to update a cupcake
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake from data in request. Return updated data.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """
    # Get the JSON data from the request
    data = request.json
    # Query the cupcake to update from the database
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    # Update cupcake attributes with data from the request
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']
    # Add the updated cupcake to the database session and commit changes
    db.session.add(cupcake)
    db.session.commit()
    # Return the updated cupcake data as JSON
    return jsonify(cupcake=cupcake.to_dict())

# Define route to delete a cupcake
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake and return confirmation message.

    Returns JSON of {message: "Deleted"}
    """
    # Query the cupcake to delete from the database
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    # Delete the cupcake from the database session and commit changes
    db.session.delete(cupcake)
    db.session.commit()
    # Return a confirmation message as JSON
    return jsonify(message="Deleted")
