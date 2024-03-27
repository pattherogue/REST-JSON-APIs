# models.py

# Import SQLAlchemy module
from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy database instance
db = SQLAlchemy()

# Default image URL for cupcakes
DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"

# Cupcake model class
class Cupcake(db.Model):
    """Cupcake model."""

    # Table name for cupcakes in the database
    __tablename__ = "cupcakes"

    # Cupcake attributes as database columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)

    # Method to serialize cupcake object to a dictionary
    def to_dict(self):
        """Serialize cupcake to a dictionary of cupcake info."""
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }

# Function to connect the app to the database
def connect_db(app):
    """Connect to the database."""
    db.app = app
    db.init_app(app)
