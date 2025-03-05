CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "email" varchar,
  "password" varchar,
  "name" varchar
);

CREATE TABLE "ingredients" (
  "id" uuid PRIMARY KEY,
  "name" varchar,
  "unit" varchar
);

CREATE TABLE "cocktails" (
  "id" uuid PRIMARY KEY,
  "name" varchar,
  "description" text,
  "image" varchar,
  "recipe" text,
  "user_id" uuid
);

CREATE TABLE "cocktail_ingredients" (
  "id" uuid PRIMARY KEY,
  "cocktail_id" uuid,
  "ingredient_id" uuid,
  "quantity" decimal
);

CREATE TABLE "favorites" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "cocktail_id" uuid
);

CREATE TABLE "user_ingredients" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "ingredient_id" uuid
);

CREATE TABLE "ratings" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "cocktail_id" uuid,
  "rating" decimal
);

-- Ajout des clés étrangères
ALTER TABLE "cocktails" 
ADD CONSTRAINT fk_user FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "cocktail_ingredients" 
ADD CONSTRAINT fk_cocktail FOREIGN KEY ("cocktail_id") REFERENCES "cocktails" ("id"),
ADD CONSTRAINT fk_ingredient FOREIGN KEY ("ingredient_id") REFERENCES "ingredients" ("id");

ALTER TABLE "favorites" 
ADD CONSTRAINT fk_favorite_user FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
ADD CONSTRAINT fk_favorite_cocktail FOREIGN KEY ("cocktail_id") REFERENCES "cocktails" ("id");

ALTER TABLE "user_ingredients" 
ADD CONSTRAINT fk_user_ingredient_user FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
ADD CONSTRAINT fk_user_ingredient FOREIGN KEY ("ingredient_id") REFERENCES "ingredients" ("id");

ALTER TABLE "ratings" 
ADD CONSTRAINT fk_rating_user FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
ADD CONSTRAINT fk_rating_cocktail FOREIGN KEY ("cocktail_id") REFERENCES "cocktails" ("id");