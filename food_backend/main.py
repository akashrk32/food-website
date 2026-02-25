from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import mysql.connector
import os
import uuid

load_dotenv()  # loads variables from .env into os.environ

app = Flask(__name__, static_folder='../', static_url_path='')
CORS(app)

# -------------------------
# Uploads Setup
# -------------------------
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


# -------------------------
# Database Connection
# -------------------------
def get_db():
    host = os.environ.get("MYSQLHOST", "localhost")
    use_ssl = host != "localhost"
    conn_args = dict(
        host=host,
        user=os.environ.get("MYSQLUSER", "root"),
        password=os.environ.get("MYSQLPASSWORD", ""),
        database=os.environ.get("MYSQLDATABASE", "1st_sql_project"),
        port=int(os.environ.get("MYSQLPORT", 3306)),
    )
    if use_ssl:
        conn_args["ssl_disabled"] = False
        conn_args["ssl_verify_cert"] = False
        conn_args["ssl_verify_identity"] = False
    return mysql.connector.connect(**conn_args)



# -------------------------
# Test Route
# -------------------------
@app.route("/api/test")
def test_api():
    return jsonify({"status": "ok", "message": "Backend is running!"})


# -------------------------
# Categories
# -------------------------
@app.route("/categories")
def get_categories():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, slug, description FROM menu_categories ORDER BY id")
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# -------------------------
# Recipes - All
# -------------------------
@app.route("/recipes", methods=["GET"])
def get_recipes():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM recipes ORDER BY created_at DESC")
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# -------------------------
# Recipes by Category ID
# -------------------------
@app.route("/recipes/category/<int:category_id>")
def get_recipes_by_category(category_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, u.name AS user_name, u.photo_url AS user_photo
            FROM recipes r
            JOIN users u ON r.user_id = u.id
            WHERE r.category_id = %s
            ORDER BY r.created_at DESC
        """, (category_id,))
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# -------------------------
# Recipes by Category Name
# -------------------------
@app.route("/categories/<name>/recipes")
def get_recipes_by_category_name(name):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, u.name AS user_name, u.photo_url AS user_photo
            FROM recipes r
            JOIN users u ON r.user_id = u.id
            JOIN menu_categories c ON r.category_id = c.id
            WHERE c.name = %s
            ORDER BY r.created_at DESC
        """, (name,))
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# -------------------------
# Create Recipe
# -------------------------
@app.route("/recipes", methods=["POST"])
def create_recipe():
    try:
        # Support both multipart/form-data (file upload) and JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            user_id = request.form.get('user_id')
            category_id = request.form.get('category_id')
            title = request.form.get('title')
            description = request.form.get('description')
            ingredients_text = request.form.get('ingredients_text')
            video_url = request.form.get('video_url') or None

            # Handle image file upload
            image_url = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_image(file.filename):
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"{uuid.uuid4().hex}.{ext}"
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    image_url = f'/uploads/{filename}'
        else:
            data = request.json
            user_id = data.get('user_id')
            category_id = data.get('category_id')
            title = data.get('title')
            description = data.get('description')
            ingredients_text = data.get('ingredients_text')
            image_url = data.get('image_url')
            video_url = data.get('video_url')

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO recipes 
            (user_id, category_id, title, description, ingredients_text, image_url, video_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            category_id,
            title,
            description,
            ingredients_text,
            image_url,
            video_url,
        ))
        db.commit()
        recipe_id = cursor.lastrowid
        cursor.close()
        db.close()
        return jsonify({"id": recipe_id, "message": "Recipe created successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# -------------------------
# Serve Uploaded Images
# -------------------------
@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# -------------------------
# Get Single Recipe by Title
# -------------------------
@app.route("/recipes/by-title/<path:title>")
def get_recipe_by_title(title):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, u.name AS user_name, c.name AS category_name
            FROM recipes r
            LEFT JOIN users u ON r.user_id = u.id
            LEFT JOIN menu_categories c ON r.category_id = c.id
            WHERE r.title = %s
            LIMIT 1
        """, (title,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            return jsonify(result)
        return jsonify({"error": "Recipe not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# -------------------------
# Get User Recipes
# -------------------------
@app.route("/users/<int:user_id>/recipes")
def get_user_recipes(user_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, c.name AS category_name
            FROM recipes r
            JOIN menu_categories c ON r.category_id = c.id
            WHERE r.user_id = %s
            ORDER BY r.created_at DESC
        """, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(result)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# -------------------------
# Delete Recipe
# -------------------------
@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
        db.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        db.close()

        if affected_rows > 0:
            return jsonify({"message": "Recipe deleted successfully"}), 200
        return jsonify({"error": "Recipe not found"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# -------------------------
# Serve Frontend
# -------------------------
@app.route("/")
def index():
    return send_from_directory("../", "food.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("../", filename)


# -------------------------
# Run App (Development Only)
# -------------------------
if __name__ == "__main__":
    app.run()
