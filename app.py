from flask import Flask
from dotenv import load_dotenv
import os
import mysql.connector

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

# Import and register the blueprint
from domain import domain_bp
app.register_blueprint(domain_bp)

if __name__ == '__main__':
    app.run(debug=True)