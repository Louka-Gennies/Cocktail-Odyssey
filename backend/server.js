const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const sqlite3 = require('sqlite3').verbose();
const { open } = require('sqlite');
const path = require('path');
const fs = require('fs').promises; // Add this line to import fs module
const authRoutes = require('./routes/auth');
const cocktailRoutes = require('./routes/cocktails');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Database setup
let db;
async function setupDatabase() {
  // Create database directory if it doesn't exist
  const dbDir = path.join(__dirname, 'database');
  try {
    await fs.mkdir(dbDir, { recursive: true });
  } catch (err) {
    if (err.code !== 'EEXIST') {
      console.error('Error creating database directory:', err);
    }
  }

  // Open database connection
  db = await open({
    filename: path.join(__dirname, 'database', 'cocktail-odyssey.db'),
    driver: sqlite3.Database
  });
  
  // Create tables if they don't exist
  await db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS cocktails (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      description TEXT,
      image_url TEXT,
      is_public BOOLEAN DEFAULT 1,
      user_id INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users (id)
    );
    
    CREATE TABLE IF NOT EXISTS ingredients (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cocktail_id INTEGER NOT NULL,
      name TEXT NOT NULL,
      quantity TEXT NOT NULL,
      FOREIGN KEY (cocktail_id) REFERENCES cocktails (id) ON DELETE CASCADE
    );
  `);
  
  // Make database available globally
  app.locals.db = db;
  
  console.log('Database setup complete');
  return db;
}

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/cocktails', cocktailRoutes);

// Base route
app.get('/', (req, res) => {
  res.send('Cocktail Odyssey API is running');
});

// Start server
setupDatabase()
  .then(() => {
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  })
  .catch(err => {
    console.error('Database setup failed:', err);
  });