from flask import Flask, jsonify
import mysql.connector

# --- CONFIGURE THIS TO MATCH YOUR MYSQL WORKBENCH SETTINGS ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # change if you use a different user
    "password": "",          # put your MySQL password here
    "database": "1st_sql_project",  # your schema name from Workbench screenshot
}


def get_db_connection():
    """Create a new connection to MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


app = Flask(__name__)


@app.route("/api/test-db")
def test_db():
    """
    Simple test endpoint: tries to connect to MySQL and
    returns rows from menu_categories.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, name, slug, description FROM menu_categories")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"status": "ok", "categories": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # Run the Flask dev server
    app.run(host="127.0.0.1", port=5000, debug=True)

