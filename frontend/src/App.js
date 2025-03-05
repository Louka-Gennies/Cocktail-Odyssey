import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [cocktails, setCocktails] = useState([]);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [newCocktail, setNewCocktail] = useState({
    name: '',
    description: '',
    ingredients: '',
    instructions: ''
  });

  useEffect(() => {
    fetchCocktails();
  }, []);

  const fetchCocktails = async () => {
    try {
      const response = await axios.get('http://localhost:8000/cocktails/');
      setCocktails(response.data);
    } catch (error) {
      console.error('Error fetching cocktails:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCocktail(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/cocktails/', newCocktail);
      fetchCocktails();
      setNewCocktail({
        name: '',
        description: '',
        ingredients: '',
        instructions: ''
      });
      setMessage({ text: 'Cocktail ajouté avec succès !', type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (error) {
      setMessage({ text: 'Erreur lors de la création du cocktail', type: 'error' });
      console.error('Error creating cocktail:', error);
    }
  };

  return (
    <div className="App">
      <h1>Cocktail Manager</h1>
      
      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
      
      <form className="cocktail-form" onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Cocktail Name"
          value={newCocktail.name}
          onChange={handleInputChange}
          required
        />
        <textarea
          name="description"
          placeholder="Description"
          value={newCocktail.description}
          onChange={handleInputChange}
          required
        />
        <textarea
          name="ingredients"
          placeholder="Ingredients"
          value={newCocktail.ingredients}
          onChange={handleInputChange}
          required
        />
        <textarea
          name="instructions"
          placeholder="Instructions"
          value={newCocktail.instructions}
          onChange={handleInputChange}
          required
        />
        <button type="submit">Add Cocktail</button>
      </form>

      <div className="cocktail-list">
        {cocktails.map(cocktail => (
          <div key={cocktail.id} className="cocktail-card">
            <h3>{cocktail.name}</h3>
            <p>{cocktail.description}</p>
            <p><strong>Ingredients:</strong> {cocktail.ingredients}</p>
            <p><strong>Instructions:</strong> {cocktail.instructions}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;