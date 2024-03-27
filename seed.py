# Import the Flask app instance from the app module
from app import app

# Import the database instance and the Cupcake model from the models module
from models import db, Cupcake

# Drop all existing tables from the database and create new ones based on the models
db.drop_all()
db.create_all()

# Create instances of Cupcake model with specified attributes
c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

# Add the cupcake instances to the database session
db.session.add_all([c1, c2])

# Commit the changes to the database session
db.session.commit()
