-- Database Schema for Food Website
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    photo_url VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS menu_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT
);
CREATE TABLE IF NOT EXISTS recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category_id INT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    ingredients_text TEXT,
    image_url VARCHAR(255),
    video_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES menu_categories(id)
);
-- Example Initial Data
INSERT INTO menu_categories (name, slug, description)
VALUES ('Breakfast', 'breakfast', 'Start your day right'),
    ('Lunch', 'lunch', 'Midday meals'),
    ('Dinner', 'dinner', 'Evening feasts');
INSERT INTO users (name, photo_url)
VALUES ('Admin', 'https://via.placeholder.com/150');