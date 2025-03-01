from flask import Blueprint, request, redirect, url_for, flash, jsonify
from db import get_db_connection
import mysql.connector

# Create a Blueprint for goals
goals_bp = Blueprint("goals", __name__)

# Add a new goal
@goals_bp.route('/add_goal/<int:domain_id>', methods=['POST'])
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

# Toggle goal completion status
@goals_bp.route('/toggle_goal_completion/<int:goal_id>', methods=['POST'])
def toggle_goal_completion(goal_id):
    data = request.get_json()
    completed = data.get("completed", False)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE goals SET completed = %s WHERE goal_id = %s", (completed, goal_id))
        conn.commit()
        return jsonify(success=True)
    except mysql.connector.Error as err:
        return jsonify(success=False, error=str(err))
    finally:
        cursor.close()
        conn.close()
