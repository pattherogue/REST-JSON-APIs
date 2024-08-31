# Rest JSON API

## Overview

This project is a Flask-based web application built with Python, offering an API for managing cupcakes. Using Python's Flask framework, the API facilitates creating, retrieving, updating, and deleting cupcake entries in a PostgreSQL database. Additionally, the application includes unit tests written in Python to ensure the functionality and reliability of the API endpoints.

## Project Structure

- **`app.py`**: The core application file, setting up the Flask app, defining routes, and integrating with the database.
- **`models.py`**: Defines the `Cupcake` model using SQLAlchemy, representing cupcakes in the database.
- **`requirements.txt`**: Lists the required Python packages to run the application.
- **`seed.py`**: Script for populating the database with initial cupcake data.
- **`tests.py`**: Contains unit tests for the API endpoints, ensuring that operations like creating, retrieving, and deleting cupcakes work correctly.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- PostgreSQL (or another supported database)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python seed.py
   ```

4. Set the environment variable for the database URI (optional, defaults to local PostgreSQL):
   ```bash
   export DATABASE_URL=postgresql:///cupcakes
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application in your web browser at `http://127.0.0.1:5000`.

### Running Tests

To run the tests, use the following command:
```bash
pytest tests.py
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
