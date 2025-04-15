# Cocktail Odyssey

Cocktail Odyssey is a web application for discovering, creating, and sharing cocktail recipes. Users can browse public cocktails, create their own recipes, and manage their personal collection.

## Project Structure

The project is divided into two main parts:

- **Frontend**: A responsive web interface built with HTML, CSS, and JavaScript
- **Backend**: A RESTful API built with Node.js, Express, and SQLite

## Features

- User authentication (register, login, logout)
- Browse public cocktails
- Search and filter cocktails
- Create, edit, and delete your own cocktails
- Mark cocktails as public or private
- Detailed view of cocktail recipes with ingredients

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Cocktail-Odyssey.git
cd Cocktail-Odyssey
```
2. Install backend dependencies:
```bash
cd backend
npm install
 ```

3. Install frontend dependencies:
```bash
cd ../frontend
npm install
 ```

### Configuration

1. Backend configuration:
   - Create a .env file in the backend directory with the following content:
   ```plaintext
   PORT=3000
   JWT_SECRET=your_secret_key
    ```
   
   - Replace your_secret_key with a secure random string

### Running the Application

1. Start the backend server:

```bash
cd backend
npm run dev
```
2. Open a new terminal and serve the frontend:
```bash
cd frontend
# If you have a simple HTTP server like 'serve' installed:
serve -s .
# Or you can open the index.html file directly in your browser
```

3. Access the application at http://localhost:3000 (or the port specified in your frontend server)

## API Endpoints

### Authentication

- POST /api/auth/register - Register a new user
- POST /api/auth/login - Login and get authentication token

### Cocktails

- GET /api/cocktails - Get all public cocktails
- GET /api/cocktails?mine=true - Get user's cocktails (requires authentication)
- GET /api/cocktails/:id - Get a specific cocktail
- POST /api/cocktails - Create a new cocktail (requires authentication)
- PUT /api/cocktails/:id - Update a cocktail (requires authentication)
- DELETE /api/cocktails/:id - Delete a cocktail (requires authentication)

## Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap Icons

### Backend

- Node.js
- Express.js
- SQLite (with sqlite3 and sqlite packages)
- JSON Web Tokens (JWT) for authentication
- bcryptjs for password hashing

## Project Structure

Cocktail-Odyssey/
├── backend/
│   ├── database/
│   ├── routes/
│   ├── .env
│   ├── package.json
│   └── server.js
└── frontend/
    ├── app.js
    ├── index.html
    ├── styles.css
    └── package.json


## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Cocktail recipes and images are for demonstration purposes only
- Icons provided by Bootstrap Icons

This README provides a comprehensive overview of your Cocktail Odyssey project, including setup instructions, features, API endpoints, and the technology stack. You can customize it further by adding screenshots, more detailed installation instructions, or any other project-specific information.
