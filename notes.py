from flask import Blueprint, request, redirect, url_for, flash
from db import get_db_connection
import mysql.connector

# Create a Blueprint for notes
notes_bp = Blueprint("notes", __name__)

# Add a new note
@notes_bp.route('/add_note/<int:domain_id>', methods=['POST'])
def add_note(domain_id):
    note_text = request.form.get("note_text").strip()

    if not note_text:
        flash("Note text cannot be empty!", "error")
        return redirect(url_for("domain.domain_details", domain_id=domain_id))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO notes (domain_id, text) VALUES (%s, %s)", (domain_id, note_text))
        conn.commit()
        flash("Note added successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("domain.domain_details", domain_id=domain_id))
