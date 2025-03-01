from flask import Flask
from dotenv import load_dotenv
import os
import mysql.connector
from domain import domain_bp
from notes import notes_bp  # Import notes blueprint
from goals import goals_bp  # Import goals blueprint

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "thrivemap_secret"  # Required for flashing messages

# Establish MySQL connection function
def get_db_connection():
    db_config = {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "database": os.getenv("MYSQL_DB"),
    }
    return mysql.connector.connect(**db_config)

# Import and register the blueprints
app.register_blueprint(domain_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(goals_bp)

if __name__ == '__main__':
    app.run(debug=True)