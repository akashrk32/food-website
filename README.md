# 🍔 Food Munch — Recipe Sharing & Food Ordering Web App

A full-stack food web application that lets users browse a menu, share their own recipes, manage a personal profile, and follow food creators in the community.

---

## 🚀 Features

- **Homepage** — Hero section, Why Choose Us, Explore Menu, Delivery & Payment info
- **Menu Details** — Browse food categories (Non-Veg Starters, Soups, Desserts, etc.)
- **Item Details** — View dish info, nutrition facts, ingredients, and customer reviews
- **Add Recipe** — Upload your own recipe with image, ingredients, category, and video URL
- **User Profile** — Edit name, bio, location, upload profile photo, view/delete your recipes
- **Community Page** — Follow food creators and view community stats
- **Login / Signup** — Client-side authentication stored in localStorage

---

## 🛠️ Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | HTML5, CSS3, Vanilla JS, Bootstrap 4 |
| Backend   | Python (Flask), Flask-CORS           |
| Database  | MySQL                               |
| Uploads   | Multipart form + local file storage |
| Deploy    | Gunicorn + Railway                  |

---

## 📁 Project Structure

```
food-website/
├── food.html           # Homepage
├── login.html          # Login / Signup page
├── profile.html        # User profile page
├── add-recipe.html     # Add a new recipe
├── menu-details.html   # Category-based menu view
├── item-details.html   # Individual item details
├── followers.html      # Community & follow creators
├── food.css            # Main stylesheet
├── add-recipe.css      # Add recipe page styles
├── profile.css         # Profile page styles
├── login.css           # Login page styles
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment config
├── .env.example        # Environment variable template
└── food_backend/
    └── main.py         # Flask API server
```

---

## ⚙️ Setup & Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/food-website.git
cd food-website
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Open .env and fill in your MySQL credentials
```

### 3. Set up the database

```bash
mysql -u root -p < schema.sql
```

### 4. Install Python dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 5. Start the backend server

```bash
cd food_backend
python main.py
```

### 6. Open in browser

Visit `http://localhost:5000` — the Flask server serves both the API and the frontend.

---

## 🌐 API Endpoints

| Method | Endpoint                            | Description              |
|--------|-------------------------------------|--------------------------|
| GET    | `/categories`                       | List all menu categories |
| GET    | `/recipes`                          | List all recipes         |
| POST   | `/recipes`                          | Create a new recipe      |
| DELETE | `/recipes/<id>`                     | Delete a recipe          |
| GET    | `/recipes/by-title/<title>`         | Get recipe by title      |
| GET    | `/categories/<name>/recipes`        | Recipes by category name |
| GET    | `/users/<id>/recipes`               | Recipes by user          |
| GET    | `/uploads/<filename>`               | Serve uploaded images    |

---

## 📦 Deployment

The project includes a `Procfile` for deployment on platforms like **Render** or **Heroku**:

```
web: gunicorn --bind 0.0.0.0:$PORT --chdir food_backend main:app
```

Set the environment variables (`MYSQLHOST`, `MYSQLUSER`, etc.) on your hosting platform's dashboard.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
