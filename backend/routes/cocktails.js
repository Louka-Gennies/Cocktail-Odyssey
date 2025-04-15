const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const jwt = require('jsonwebtoken');

// Get all cocktails
router.get('/', async (req, res) => {
  try {
    const db = req.app.locals.db;
    let userId = null;
    let query = '';
    let params = [];
    
    // Check if user is authenticated
    if (req.headers.authorization) {
      try {
        const token = req.headers.authorization.split(' ')[1];
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        userId = decoded.id;
      } catch (error) {
        // Invalid token, just show public cocktails
        console.log('Invalid token, showing only public cocktails');
      }
    }
    
    // If mine=true parameter is provided and user is authenticated
    if (req.query.mine === 'true' && userId) {
      query = `
        SELECT c.*, u.name as user_name
        FROM cocktails c
        JOIN users u ON c.user_id = u.id
        WHERE c.user_id = ?
        ORDER BY c.created_at DESC
      `;
      params = [userId];
    } else {
      // Show public cocktails or all cocktails if user is authenticated
      query = `
        SELECT c.*, u.name as user_name
        FROM cocktails c
        JOIN users u ON c.user_id = u.id
        WHERE c.is_public = 1 ${userId ? 'OR c.user_id = ?' : ''}
        ORDER BY c.created_at DESC
      `;
      params = userId ? [userId] : [];
    }
    
    const cocktails = await db.all(query, params);
    
    // Get ingredients for each cocktail
    for (let cocktail of cocktails) {
      // Ensure dates are properly formatted
      if (cocktail.created_at) {
        // Convert string date to Date object if needed
        cocktail.created_at = new Date(cocktail.created_at).toISOString();
      }
      if (cocktail.updated_at) {
        cocktail.updated_at = new Date(cocktail.updated_at).toISOString();
      }
      
      const ingredients = await db.all(
        'SELECT * FROM ingredients WHERE cocktail_id = ?',
        [cocktail.id]
      );
      cocktail.ingredients = ingredients;
      
      // Add isOwner property
      cocktail.isOwner = userId ? cocktail.user_id === userId : false;
      
      // Format user object
      cocktail.user = {
        id: cocktail.user_id,
        name: cocktail.user_name
      };
      
      // Remove redundant properties
      delete cocktail.user_id;
      delete cocktail.user_name;
    }
    
    res.json({ cocktails });
  } catch (error) {
    console.error('Error fetching cocktails:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get cocktail by ID
router.get('/:id', async (req, res) => {
  try {
    const db = req.app.locals.db;
    const { id } = req.params;
    let userId = null;
    
    // Check if user is authenticated
    if (req.headers.authorization) {
      try {
        const token = req.headers.authorization.split(' ')[1];
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        userId = decoded.id;
      } catch (error) {
        // Invalid token, just show public cocktails
      }
    }
    
    // Get cocktail
    const cocktail = await db.get(
      `SELECT c.*, u.name as user_name
       FROM cocktails c
       JOIN users u ON c.user_id = u.id
       WHERE c.id = ?`,
      [id]
    );
    
    if (!cocktail) {
      return res.status(404).json({ message: 'Cocktail not found' });
    }
    
    // Check if user can access this cocktail
    if (!cocktail.is_public && (!userId || cocktail.user_id !== userId)) {
      return res.status(403).json({ message: 'Access denied' });
    }
    
    // Get ingredients
    const ingredients = await db.all(
      'SELECT * FROM ingredients WHERE cocktail_id = ?',
      [id]
    );
    
    cocktail.ingredients = ingredients;
    cocktail.isOwner = userId ? cocktail.user_id === userId : false;
    
    // Format user object
    cocktail.user = {
      id: cocktail.user_id,
      name: cocktail.user_name
    };
    
    // Remove redundant properties
    delete cocktail.user_id;
    delete cocktail.user_name;
    
    res.json({ cocktail });
  } catch (error) {
    console.error('Error fetching cocktail:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Create cocktail
router.post('/', auth, async (req, res) => {
  try {
    const db = req.app.locals.db;
    const { name, description, imageUrl, isPublic, ingredients } = req.body;
    
    // Insert cocktail
    const result = await db.run(
      `INSERT INTO cocktails (name, description, image_url, is_public, user_id)
       VALUES (?, ?, ?, ?, ?)`,
      [name, description, imageUrl, isPublic ? 1 : 0, req.user.id]
    );
    
    const cocktailId = result.lastID;
    
    // Insert ingredients
    if (ingredients && ingredients.length > 0) {
      for (const ingredient of ingredients) {
        await db.run(
          'INSERT INTO ingredients (cocktail_id, name, quantity) VALUES (?, ?, ?)',
          [cocktailId, ingredient.name, ingredient.quantity]
        );
      }
    }
    
    // Get the created cocktail with ingredients
    const cocktail = await db.get('SELECT * FROM cocktails WHERE id = ?', [cocktailId]);
    cocktail.ingredients = await db.all('SELECT * FROM ingredients WHERE cocktail_id = ?', [cocktailId]);
    
    res.status(201).json({ cocktail });
  } catch (error) {
    console.error('Error creating cocktail:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Update cocktail
router.put('/:id', auth, async (req, res) => {
  try {
    const db = req.app.locals.db;
    const { id } = req.params;
    const { name, description, imageUrl, isPublic, ingredients } = req.body;
    
    // Check if cocktail exists and belongs to user
    const cocktail = await db.get(
      'SELECT * FROM cocktails WHERE id = ?',
      [id]
    );
    
    if (!cocktail) {
      return res.status(404).json({ message: 'Cocktail not found' });
    }
    
    if (cocktail.user_id !== req.user.id) {
      return res.status(403).json({ message: 'Not authorized to update this cocktail' });
    }
    
    // Update cocktail
    await db.run(
      `UPDATE cocktails
       SET name = ?, description = ?, image_url = ?, is_public = ?, updated_at = CURRENT_TIMESTAMP
       WHERE id = ?`,
      [name, description, imageUrl, isPublic ? 1 : 0, id]
    );
    
    // Delete existing ingredients
    await db.run('DELETE FROM ingredients WHERE cocktail_id = ?', [id]);
    
    // Insert new ingredients
    if (ingredients && ingredients.length > 0) {
      for (const ingredient of ingredients) {
        await db.run(
          'INSERT INTO ingredients (cocktail_id, name, quantity) VALUES (?, ?, ?)',
          [id, ingredient.name, ingredient.quantity]
        );
      }
    }
    
    // Get updated cocktail
    const updatedCocktail = await db.get('SELECT * FROM cocktails WHERE id = ?', [id]);
    updatedCocktail.ingredients = await db.all('SELECT * FROM ingredients WHERE cocktail_id = ?', [id]);
    
    res.json({ cocktail: updatedCocktail });
  } catch (error) {
    console.error('Error updating cocktail:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Delete cocktail
router.delete('/:id', auth, async (req, res) => {
  try {
    const db = req.app.locals.db;
    const { id } = req.params;
    
    // Check if cocktail exists and belongs to user
    const cocktail = await db.get(
      'SELECT * FROM cocktails WHERE id = ?',
      [id]
    );
    
    if (!cocktail) {
      return res.status(404).json({ message: 'Cocktail not found' });
    }
    
    if (cocktail.user_id !== req.user.id) {
      return res.status(403).json({ message: 'Not authorized to delete this cocktail' });
    }
    
    // Delete ingredients (should cascade, but just to be safe)
    await db.run('DELETE FROM ingredients WHERE cocktail_id = ?', [id]);
    
    // Delete cocktail
    await db.run('DELETE FROM cocktails WHERE id = ?', [id]);
    
    res.json({ message: 'Cocktail deleted successfully' });
  } catch (error) {
    console.error('Error deleting cocktail:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router;