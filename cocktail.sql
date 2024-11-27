CREATE TABLE "cocktails" (
  "id" uuid PRIMARY KEY,
  "name" varchar,
  "description" text,
  "image" varchar,
  "recipe" text,
  "user_id" uuid
);

CREATE TABLE "ingredients" (
  "id" uuid PRIMARY KEY,
  "name" varchar,
  "unit" varchar
);

CREATE TABLE "cocktail_ingredients" (
  "id" uuid PRIMARY KEY,
  "cocktail_id" uuid,
  "ingredient_id" uuid,
  "quantity" decimal
);

CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "email" varchar,
  "password" varchar,
  "name" varchar
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

ALTER TABLE "cocktail_ingredients" ADD FOREIGN KEY ("cocktail_id") REFERENCES "cocktails" ("id");

ALTER TABLE "cocktail_ingredients" ADD FOREIGN KEY ("ingredient_id") REFERENCES "ingredients" ("id");

ALTER TABLE "favorites" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "favorites" ADD FOREIGN KEY ("cocktail_id") REFERENCES "cocktails" ("id");

ALTER TABLE "user_ingredients" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_ingredients" ADD FOREIGN KEY ("ingredient_id") REFERENCES "ingredients" ("id");

ALTER TABLE "ratings" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "ratings" ADD FOREIGN KEY ("cocktail_id") REFERENCES "cocktails" ("id");
