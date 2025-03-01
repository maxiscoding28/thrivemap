from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from app import get_db_connection

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
    domain_name = request.form.get("domain_name").strip()

    if not domain_name:
        flash("Domain name cannot be empty!", "error")
        return redirect(url_for("domain.home"))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO domains (domain_name) VALUES (%s)", (domain_name,))
        conn.commit()
        flash("Domain added successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("domain.home"))

# Edit domain route
@domain_bp.route('/edit_domain/<int:domain_id>', methods=['POST'])
def edit_domain(domain_id):
    new_name = request.form.get("domain_name").strip()

    if not new_name:
        flash("Domain name cannot be empty!", "error")
        return redirect(url_for("domain.home"))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE domains SET domain_name = %s WHERE domain_id = %s", (new_name, domain_id))
        conn.commit()
        flash("Domain updated successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("domain.home"))

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