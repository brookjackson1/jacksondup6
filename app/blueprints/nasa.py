from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

nasa = Blueprint('nasa', __name__)

NASA_API_KEY = os.getenv('NASA_API_KEY')
NASA_APOD_URL = 'https://api.nasa.gov/planetary/apod'

@nasa.route('/')
def show_nasa():
    """Main page showing current APOD and saved pictures"""
    connection = get_db()

    # Fetch today's APOD from NASA API
    current_apod = None
    error_message = None

    try:
        params = {
            'api_key': NASA_API_KEY,
            'thumbs': True
        }
        response = requests.get(NASA_APOD_URL, params=params, timeout=30)
        response.raise_for_status()
        current_apod = response.json()
    except requests.exceptions.Timeout:
        error_message = "NASA API request timed out. Please try again in a moment."
        flash(error_message, "warning")
    except requests.exceptions.ConnectionError:
        error_message = "Unable to connect to NASA API. Please check your internet connection."
        flash(error_message, "warning")
    except requests.exceptions.RequestException as e:
        error_message = f"Failed to fetch NASA APOD. The NASA API may be temporarily unavailable."
        flash(error_message, "warning")
    except Exception as e:
        error_message = f"Error processing NASA data: {str(e)}"
        flash(error_message, "error")

    # Fetch saved APODs from database
    saved_apods = []
    if connection is not None:
        try:
            query = "SELECT * FROM nasa_apod ORDER BY saved_at DESC"
            with connection.cursor() as cursor:
                cursor.execute(query)
                saved_apods = cursor.fetchall()
        except Exception as e:
            flash(f"Database error: {str(e)}", "error")
    else:
        flash("Database connection failed. Saved pictures unavailable.", "error")

    return render_template("nasa.html",
                         current_apod=current_apod,
                         saved_apods=saved_apods,
                         error_message=error_message)

@nasa.route('/save', methods=['POST'])
def save_apod():
    """Save current APOD to database"""
    connection = get_db()

    if connection is None:
        flash("Database connection failed. Cannot save picture.", "error")
        return redirect(url_for('nasa.show_nasa'))

    title = request.form.get('title')
    date = request.form.get('date')
    url = request.form.get('url')
    explanation = request.form.get('explanation')
    media_type = request.form.get('media_type', 'image')

    # Validate required fields
    if not all([title, date, url]):
        flash("Missing required fields. Cannot save picture.", "error")
        return redirect(url_for('nasa.show_nasa'))

    try:
        # Check if already saved
        check_query = "SELECT id FROM nasa_apod WHERE date = %s"
        with connection.cursor() as cursor:
            cursor.execute(check_query, (date,))
            existing = cursor.fetchone()

            if existing:
                flash("This picture is already saved!", "warning")
                return redirect(url_for('nasa.show_nasa'))

        # Insert new record
        query = """
        INSERT INTO nasa_apod (title, date, url, explanation, media_type, saved_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        with connection.cursor() as cursor:
            cursor.execute(query, (title, date, url, explanation, media_type))
        connection.commit()

        flash("Picture saved successfully!", "success")
    except Exception as e:
        flash(f"Error saving picture: {str(e)}", "error")

    return redirect(url_for('nasa.show_nasa'))

@nasa.route('/delete/<int:apod_id>', methods=['POST'])
def delete_apod(apod_id):
    """Delete a saved APOD from database"""
    connection = get_db()

    if connection is None:
        flash("Database connection failed. Cannot delete picture.", "error")
        return redirect(url_for('nasa.show_nasa'))

    try:
        query = "DELETE FROM nasa_apod WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (apod_id,))
        connection.commit()

        flash("Picture deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting picture: {str(e)}", "error")

    return redirect(url_for('nasa.show_nasa'))

@nasa.route('/search', methods=['GET'])
def search_apod():
    """Search for APOD by specific date"""
    search_date = request.args.get('date')

    if not search_date:
        flash("Please provide a date to search.", "warning")
        return redirect(url_for('nasa.show_nasa'))

    try:
        params = {
            'api_key': NASA_API_KEY,
            'date': search_date,
            'thumbs': True
        }
        response = requests.get(NASA_APOD_URL, params=params, timeout=30)
        response.raise_for_status()
        apod_data = response.json()

        return jsonify(apod_data)
    except requests.exceptions.Timeout:
        return jsonify({'error': 'NASA API request timed out. Please try again.'}), 408
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Unable to connect to NASA API. Please check your internet connection.'}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch APOD. The NASA API may be temporarily unavailable.'}), 503
    except Exception as e:
        return jsonify({'error': f"Error processing data: {str(e)}"}), 500

@nasa.route('/update/<int:apod_id>', methods=['POST'])
def update_apod(apod_id):
    """Update a saved APOD's title or explanation"""
    connection = get_db()

    if connection is None:
        flash("Database connection failed. Cannot update picture.", "error")
        return redirect(url_for('nasa.show_nasa'))

    title = request.form.get('title')
    explanation = request.form.get('explanation')

    if not title:
        flash("Title is required.", "error")
        return redirect(url_for('nasa.show_nasa'))

    try:
        query = """
        UPDATE nasa_apod
        SET title = %s, explanation = %s
        WHERE id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, (title, explanation, apod_id))
        connection.commit()

        flash("Picture updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating picture: {str(e)}", "error")

    return redirect(url_for('nasa.show_nasa'))
