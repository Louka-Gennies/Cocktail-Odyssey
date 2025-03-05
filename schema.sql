-- Création des tables
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS cocktails (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    recipe TEXT,
    user_id VARCHAR(255) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS ingredients (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS cocktail_ingredients (
    id VARCHAR(255) PRIMARY KEY,
    cocktail_id VARCHAR(255) REFERENCES cocktails(id),
    ingredient_id VARCHAR(255) REFERENCES ingredients(id),
    quantity DECIMAL NOT NULL
);

CREATE TABLE IF NOT EXISTS favorites (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    cocktail_id VARCHAR(255) REFERENCES cocktails(id)
);

CREATE TABLE IF NOT EXISTS ratings (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    cocktail_id VARCHAR(255) REFERENCES cocktails(id),
    rating DECIMAL NOT NULL
);

CREATE TABLE IF NOT EXISTS user_ingredients (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    ingredient_id VARCHAR(255) REFERENCES ingredients(id)
); 