from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from db import get_db_connection  # Updated import
import mysql.connector

# Create a Blueprint for domains
domain_bp = Blueprint("domain", __name__)

# Home route - Display all domains
@domain_bp.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM domains")
    domains = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('home.html', domains=domains)

# Add a new domain
@domain_bp.route('/add_domain', methods=['POST'])
def add_domain():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as domain_count FROM domains")
    domain_count = cursor.fetchone()["domain_count"]

    if domain_count >= 10:
        flash("Cannot add more than 10 domains!", "error")
        cursor.close()
        conn.close()
        return redirect(url_for("domain.home"))

    domain_name = request.form.get("domain_name").strip()
    description = request.form.get("description").strip()

    if not domain_name:
        flash("Domain name cannot be empty!", "error")
        cursor.close()
        conn.close()
        return redirect(url_for("domain.home"))

    cursor.execute("SELECT * FROM domains WHERE domain_name = %s", (domain_name,))
    existing_domain = cursor.fetchone()
    if existing_domain:
        flash("Domain name already exists!", "error")
        cursor.close()
        conn.close()
        return redirect(url_for("domain.home"))

    try:
        cursor.execute("INSERT INTO domains (domain_name, description) VALUES (%s, %s)", (domain_name, description))
        conn.commit()
        flash("Domain added successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("domain.home"))

# Domain details route
@domain_bp.route('/domain/<int:domain_id>')
def domain_details(domain_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM domains WHERE domain_id = %s", (domain_id,))
    domain = cursor.fetchone()
    cursor.execute("SELECT * FROM notes WHERE domain_id = %s", (domain_id,))
    notes = cursor.fetchall()
    cursor.execute("SELECT * FROM goals WHERE domain_id = %s", (domain_id,))
    goals = cursor.fetchall()
    cursor.close()
    conn.close()

    if not domain:
        flash("Domain not found!", "error")
        return redirect(url_for("domain.home"))

    return render_template('domain_details.html', domain=domain, notes=notes, goals=goals)

# Edit domain route
@domain_bp.route('/edit_domain/<int:domain_id>', methods=['POST'])
def edit_domain(domain_id):
    new_name = request.form.get("domain_name").strip()
    description = request.form.get("description").strip()

    if not new_name:
        flash("Domain name cannot be empty!", "error")
        return redirect(url_for("domain.home"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM domains WHERE domain_name = %s AND domain_id != %s", (new_name, domain_id))
    existing_domain = cursor.fetchone()
    if existing_domain:
        flash("Domain name already exists!", "error")
        cursor.close()
        conn.close()
        return redirect(url_for("domain.home"))

    try:
        cursor.execute("UPDATE domains SET domain_name = %s, description = %s WHERE domain_id = %s", (new_name, description, domain_id))
        conn.commit()
        flash("Domain updated successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("domain.domain_details", domain_id=domain_id))

# Update domain description
@domain_bp.route('/update_description/<int:domain_id>', methods=['POST'])
def update_description(domain_id):
    description = request.form.get("description").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE domains SET description = %s WHERE domain_id = %s", (description, domain_id))
        conn.commit()
        flash("Description updated successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("domain.domain_details", domain_id=domain_id))

# Delete a domain
@domain_bp.route('/delete_domain/<int:domain_id>', methods=['POST'])
def delete_domain(domain_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM domains WHERE domain_id = %s", (domain_id,))
        conn.commit()
        flash("Domain deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("domain.home"))

# Add a new note
@domain_bp.route('/add_note/<int:domain_id>', methods=['POST'])
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

# Add a new goal
@domain_bp.route('/add_goal/<int:domain_id>', methods=['POST'])
def add_goal(domain_id):
    goal_text = request.form.get("goal_text").strip()

    if not goal_text:
        flash("Goal text cannot be empty!", "error")
        return redirect(url_for("domain.domain_details", domain_id=domain_id))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO goals (domain_id, text) VALUES (%s, %s)", (domain_id, goal_text))
        conn.commit()
        flash("Goal added successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("domain.domain_details", domain_id=domain_id))

# Delete a note
@domain_bp.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM notes WHERE note_id = %s", (note_id,))
        conn.commit()
        flash("Note deleted successfully!", "success")
        return jsonify(success=True)
    except mysql.connector.Error as err:
        return jsonify(success=False, error=str(err))
    finally:
        cursor.close()
        conn.close()

# Delete a goal
@domain_bp.route('/delete_goal/<int:goal_id>', methods=['POST'])
def delete_goal(goal_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM goals WHERE goal_id = %s", (goal_id,))
        conn.commit()
        return jsonify(success=True)
    except mysql.connector.Error as err:
        return jsonify(success=False, error=str(err))
    finally:
        cursor.close()
        conn.close()