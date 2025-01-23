-- cocktail_data.sql

-- Insérer des utilisateurs
INSERT INTO users (id, email, password, name) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'user1@example.com', 'password1', 'User One'),
('550e8400-e29b-41d4-a716-446655440001', 'user2@example.com', 'password2', 'User Two');

-- Insérer des ingrédients
INSERT INTO ingredients (id, name, unit) VALUES
('550e8400-e29b-41d4-a716-446655440002', 'Vodka', 'ml'),
('550e8400-e29b-41d4-a716-446655440003', 'Orange Juice', 'ml'),
('550e8400-e29b-41d4-a716-446655440004', 'Grenadine', 'ml');

-- Insérer des cocktails
INSERT INTO cocktails (id, name, description, image, recipe, user_id) VALUES
('550e8400-e29b-41d4-a716-446655440005', 'Screwdriver', 'A refreshing cocktail made with vodka and orange juice.', 'screwdriver.jpg', 'Mix vodka and orange juice.', '550e8400-e29b-41d4-a716-446655440000'),
('550e8400-e29b-41d4-a716-446655440006', 'Tequila Sunrise', 'A cocktail made with tequila, orange juice, and grenadine.', 'tequila_sunrise.jpg', 'Pour tequila and orange juice, then add grenadine.', '550e8400-e29b-41d4-a716-446655440001');

-- Insérer des ingrédients de cocktails
INSERT INTO cocktail_ingredients (id, cocktail_id, ingredient_id, quantity) VALUES
('550e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440002', 50),
('550e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440003', 150),
('550e8400-e29b-41d4-a716-446655440009', '550e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440003', 100),
('550e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440004', 20);

-- Insérer des favoris
INSERT INTO favorites (id, user_id, cocktail_id) VALUES
('550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440005'),
('550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440006');

-- Insérer des ingrédients d'utilisateur
INSERT INTO user_ingredients (id, user_id, ingredient_id) VALUES
('550e8400-e29b-41d4-a716-446655440013', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440002'),
('550e8400-e29b-41d4-a716-446655440014', '550e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440003');

-- Insérer des évaluations
INSERT INTO ratings (id, user_id, cocktail_id, rating) VALUES
('550e8400-e29b-41d4-a716-446655440015', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440005', 4.5),
('550e8400-e29b-41d4-a716-446655440016', '550e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440006', 5.0);