from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

news = Blueprint('news', __name__)

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'
NEWS_SEARCH_URL = 'https://newsapi.org/v2/everything'

@news.route('/')
def show_news():
    """Main page showing top headlines and saved articles"""
    connection = get_db()

    # Fetch top headlines from News API
    top_headlines = []
    error_message = None

    try:
        params = {
            'apiKey': NEWS_API_KEY,
            'country': 'us',
            'pageSize': 10
        }
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('status') == 'ok':
            top_headlines = data.get('articles', [])
        else:
            error_message = data.get('message', 'Failed to fetch news')
            flash(error_message, "warning")
    except requests.exceptions.Timeout:
        error_message = "News API request timed out. Please try again in a moment."
        flash(error_message, "warning")
    except requests.exceptions.ConnectionError:
        error_message = "Unable to connect to News API. Please check your internet connection."
        flash(error_message, "warning")
    except requests.exceptions.RequestException as e:
        error_message = "Failed to fetch news. The News API may be temporarily unavailable."
        flash(error_message, "warning")
    except Exception as e:
        error_message = f"Error processing news data: {str(e)}"
        flash(error_message, "error")

    # Fetch saved articles from database
    saved_articles = []
    if connection is not None:
        try:
            query = "SELECT * FROM news_articles ORDER BY saved_at DESC"
            with connection.cursor() as cursor:
                cursor.execute(query)
                saved_articles = cursor.fetchall()
        except Exception as e:
            flash(f"Database error: {str(e)}", "error")
    else:
        flash("Database connection failed. Saved articles unavailable.", "error")

    return render_template("news.html",
                         top_headlines=top_headlines,
                         saved_articles=saved_articles,
                         error_message=error_message)

@news.route('/save', methods=['POST'])
def save_article():
    """Save article to database"""
    connection = get_db()

    if connection is None:
        flash("Database connection failed. Cannot save article.", "error")
        return redirect(url_for('news.show_news'))

    title = request.form.get('title')
    author = request.form.get('author', 'Unknown')
    description = request.form.get('description')
    url = request.form.get('url')
    url_to_image = request.form.get('url_to_image')
    published_at = request.form.get('published_at')
    source_name = request.form.get('source_name')

    # Validate required fields
    if not all([title, url]):
        flash("Missing required fields. Cannot save article.", "error")
        return redirect(url_for('news.show_news'))

    try:
        # Check if already saved
        check_query = "SELECT id FROM news_articles WHERE url = %s"
        with connection.cursor() as cursor:
            cursor.execute(check_query, (url,))
            existing = cursor.fetchone()

            if existing:
                flash("This article is already saved!", "warning")
                return redirect(url_for('news.show_news'))

        # Insert new record
        query = """
        INSERT INTO news_articles (title, author, description, url, url_to_image, published_at, source_name, saved_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        with connection.cursor() as cursor:
            cursor.execute(query, (title, author, description, url, url_to_image, published_at, source_name))
        connection.commit()

        flash("Article saved successfully!", "success")
    except Exception as e:
        flash(f"Error saving article: {str(e)}", "error")

    return redirect(url_for('news.show_news'))

@news.route('/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    """Delete a saved article from database"""
    connection = get_db()

    if connection is None:
        flash("Database connection failed. Cannot delete article.", "error")
        return redirect(url_for('news.show_news'))

    try:
        query = "DELETE FROM news_articles WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (article_id,))
        connection.commit()

        flash("Article deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting article: {str(e)}", "error")

    return redirect(url_for('news.show_news'))

@news.route('/search', methods=['GET'])
def search_news():
    """Search for news by keyword or category"""
    search_query = request.args.get('q')
    category = request.args.get('category')

    if not search_query and not category:
        return jsonify({'error': 'Please provide a search query or category'}), 400

    try:
        if category:
            # Search by category using top-headlines
            params = {
                'apiKey': NEWS_API_KEY,
                'category': category,
                'country': 'us',
                'pageSize': 20
            }
            response = requests.get(NEWS_API_URL, params=params, timeout=10)
        else:
            # Search by keyword using everything endpoint
            params = {
                'apiKey': NEWS_API_KEY,
                'q': search_query,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 20
            }
            response = requests.get(NEWS_SEARCH_URL, params=params, timeout=10)

        response.raise_for_status()
        data = response.json()

        if data.get('status') == 'ok':
            return jsonify(data)
        else:
            return jsonify({'error': data.get('message', 'Search failed')}), 400

    except requests.exceptions.Timeout:
        return jsonify({'error': 'News API request timed out. Please try again.'}), 408
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Unable to connect to News API. Please check your internet connection.'}), 503
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Failed to search news. The News API may be temporarily unavailable.'}), 503
    except Exception as e:
        return jsonify({'error': f"Error processing data: {str(e)}"}), 500

@news.route('/update/<int:article_id>', methods=['POST'])
def update_article(article_id):
    """Update a saved article's title or description"""
    connection = get_db()

    if connection is None:
        flash("Database connection failed. Cannot update article.", "error")
        return redirect(url_for('news.show_news'))

    title = request.form.get('title')
    description = request.form.get('description')

    if not title:
        flash("Title is required.", "error")
        return redirect(url_for('news.show_news'))

    try:
        query = """
        UPDATE news_articles
        SET title = %s, description = %s
        WHERE id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, (title, description, article_id))
        connection.commit()

        flash("Article updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating article: {str(e)}", "error")

    return redirect(url_for('news.show_news'))
