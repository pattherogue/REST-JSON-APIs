# Import necessary modules and classes from unittest, app, and models modules
from unittest import TestCase
from app import app
from models import db, Cupcake

# Use a test database and suppress SQL output during tests
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Set Flask to testing mode to raise exceptions instead of HTML error pages
app.config['TESTING'] = True

# Drop and recreate all tables in the test database
db.drop_all()
db.create_all()

# Define data for testing cupcake creation and retrieval
CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

# Define a test case class for testing cupcake views
class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    # Set up test data before each test
    def setUp(self):
        """Make demo data."""
        # Delete all existing cupcakes from the test database
        Cupcake.query.delete()
        # Create a cupcake instance using the first set of data and add it to the database
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()
        # Save the cupcake instance for later use in tests
        self.cupcake = cupcake

    # Clean up any changes made during tests
    def tearDown(self):
        """Clean up fouled transactions."""
        # Rollback any changes made to the database during the test
        db.session.rollback()

    # Test retrieving a list of cupcakes
    def test_list_cupcakes(self):
        with app.test_client() as client:
            # Send a GET request to the endpoint for listing cupcakes
            resp = client.get("/api/cupcakes")

            # Assert that the response status code is 200 (OK)
            self.assertEqual(resp.status_code, 200)

            # Extract JSON data from the response
            data = resp.json
            # Assert that the JSON data matches the expected format and content
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    # Test retrieving a specific cupcake
    def test_get_cupcake(self):
        with app.test_client() as client:
            # Send a GET request to the endpoint for retrieving a specific cupcake
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            # Assert that the response status code is 200 (OK)
            self.assertEqual(resp.status_code, 200)
            # Extract JSON data from the response
            data = resp.json
            # Assert that the JSON data matches the expected format and content
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    # Test creating a new cupcake
    def test_create_cupcake(self):
        with app.test_client() as client:
            # Send a POST request to the endpoint for creating cupcakes with new cupcake data
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            # Assert that the response status code is 201 (Created)
            self.assertEqual(resp.status_code, 201)

            # Extract JSON data from the response
            data = resp.json

            # Ensure the ID is an integer and remove it for comparison
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            # Assert that the JSON data matches the expected format and content
            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            # Assert that there are now two cupcakes in the database
            self.assertEqual(Cupcake.query.count(), 2)
