// API URL
const API_URL = 'http://localhost:3000/api';

// DOM Elements
const cocktailsContainer = document.getElementById('cocktails-container');
const cocktailDetailContent = document.getElementById('cocktail-detail-content');
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const filterBtns = document.querySelectorAll('.filter-btn');
const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');
const loginModal = document.getElementById('login-modal');
const registerModal = document.getElementById('register-modal');
const closeButtons = document.querySelectorAll('.close');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const logoutBtn = document.getElementById('logout-btn');
const userMenu = document.getElementById('user-menu');
const authButtons = document.querySelector('.auth-buttons');
const userName = document.getElementById('user-name');
const homeLink = document.getElementById('home-link');
const myCocktailsLink = document.getElementById('my-cocktails-link');
const createCocktailLink = document.getElementById('create-cocktail-link');
const backToListBtn = document.getElementById('back-to-list');
const cocktailCreateForm = document.getElementById('cocktail-create-form');
const addIngredientBtn = document.getElementById('add-ingredient');
const ingredientsList = document.getElementById('ingredients-list');
const cancelFormBtn = document.getElementById('cancel-form');

// Pages
const pages = document.querySelectorAll('.page');
const cocktailListPage = document.getElementById('cocktail-list');
const cocktailDetailPage = document.getElementById('cocktail-detail');
const cocktailFormPage = document.getElementById('cocktail-form');

// State
let currentFilter = 'all';
let searchQuery = '';
let currentCocktailId = null;
let isEditMode = false;

// Check Authentication
function checkAuth() {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user'));
    
    if (token && user) {
        userMenu.classList.remove('hidden');
        authButtons.querySelector('#login-btn').classList.add('hidden');
        authButtons.querySelector('#register-btn').classList.add('hidden');
        userName.textContent = user.name;
        return true;
    } else {
        userMenu.classList.add('hidden');
        authButtons.querySelector('#login-btn').classList.remove('hidden');
        authButtons.querySelector('#register-btn').classList.remove('hidden');
        return false;
    }
}

// API Functions
async function fetchCocktails(onlyMine = false) {
    try {
        const url = `${API_URL}/cocktails${onlyMine ? '?mine=true' : ''}`;
        const token = localStorage.getItem('token');
        
        const response = await fetch(url, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        
        if (!response.ok) {
            // If unauthorized and trying to get all cocktails, try again without token
            // This allows public cocktails to be viewed without authentication
            if (response.status === 401 && !onlyMine && token) {
                console.log('Unauthorized with token, trying to fetch public cocktails without authentication');
                const publicResponse = await fetch(url);
                if (publicResponse.ok) {
                    return await publicResponse.json();
                }
            }
            throw new Error('Failed to fetch cocktails');
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching cocktails:', error);
        return { cocktails: [] };
    }
}

async function fetchCocktail(id) {
    try {
        const url = `${API_URL}/cocktails/${id}`;
        const token = localStorage.getItem('token');
        
        const response = await fetch(url, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch cocktail');
        }
        
        const data = await response.json();
        return data.cocktail;
    } catch (error) {
        console.error('Error fetching cocktail:', error);
        return null;
    }
}

async function createCocktail(cocktailData) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Authentication required');
        }
        
        const response = await fetch(`${API_URL}/cocktails`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(cocktailData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create cocktail');
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error creating cocktail:', error);
        throw error;
    }
}

async function updateCocktail(id, cocktailData) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Authentication required');
        }
        
        const response = await fetch(`${API_URL}/cocktails/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(cocktailData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update cocktail');
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error updating cocktail:', error);
        throw error;
    }
}

async function deleteCocktail(id) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Authentication required');
        }
        
        const response = await fetch(`${API_URL}/cocktails/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete cocktail');
        }
        
        return true;
    } catch (error) {
        console.error('Error deleting cocktail:', error);
        throw error;
    }
}

async function login(credentials) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Login failed');
        }
        
        const data = await response.json();
        
        // Store the token exactly as received
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        return data;
    } catch (error) {
        console.error('Error logging in:', error);
        throw error;
    }
}

async function register(userData) {
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new Error('Registration failed');
        }
        
        const data = await response.json();
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        return data;
    } catch (error) {
        console.error('Error registering:', error);
        throw error;
    }
}

// UI Functions
function showPage(pageId) {
    pages.forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}

function renderCocktails(cocktails) {
    cocktailsContainer.innerHTML = '';
    
    if (cocktails.length === 0) {
        cocktailsContainer.innerHTML = `
            <div class="no-results">
                <p>Aucun cocktail trouvé.</p>
            </div>
        `;
        return;
    }
    
    cocktails.forEach(cocktail => {
        const isOwner = cocktail.isOwner;
        const card = document.createElement('div');
        card.className = 'cocktail-card';
        card.innerHTML = `
            <div class="cocktail-image">
                ${cocktail.imageUrl 
                    ? `<img src="${cocktail.imageUrl}" alt="${cocktail.name}">`
                    : `<i class="bi bi-cup-straw"></i>`
                }
            </div>
            <div class="cocktail-info">
                <h3>${cocktail.name}</h3>
                <p>${cocktail.description || 'Aucune description disponible.'}</p>
                <div class="cocktail-meta">
                    <span class="badge ${cocktail.is_public ? 'badge-success' : 'badge-warning'}">
                        ${cocktail.is_public ? 'Public' : 'Privé'}
                    </span>
                    <small>${formatDate(cocktail.created_at)}</small>
                </div>
                <div class="cocktail-actions">
                    <button class="btn btn-primary view-cocktail" data-id="${cocktail.id}">Voir détails</button>
                    ${isOwner ? `
                        <div>
                            <button class="btn edit-cocktail" data-id="${cocktail.id}">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn delete-cocktail" data-id="${cocktail.id}">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
        
        cocktailsContainer.appendChild(card);
        
        // Add event listeners
        card.querySelector('.view-cocktail').addEventListener('click', () => {
            viewCocktailDetail(cocktail.id);
        });
        
        if (isOwner) {
            card.querySelector('.edit-cocktail').addEventListener('click', () => {
                editCocktail(cocktail.id);
            });
            
            card.querySelector('.delete-cocktail').addEventListener('click', () => {
                confirmDeleteCocktail(cocktail.id, cocktail.name);
            });
        }
    });
}

async function viewCocktailDetail(id) {
    cocktailDetailContent.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Chargement du cocktail...</p>
        </div>
    `;
    
    showPage('cocktail-detail');
    currentCocktailId = id;
    
    const cocktail = await fetchCocktail(id);
    
    if (!cocktail) {
        cocktailDetailContent.innerHTML = `
            <div class="alert alert-danger">
                Cocktail non trouvé.
            </div>
        `;
        return;
    }
    
    const isOwner = cocktail.isOwner;
    
    cocktailDetailContent.innerHTML = `
        <div class="cocktail-detail-container">
            <div class="cocktail-detail-image">
                ${cocktail.imageUrl 
                    ? `<img src="${cocktail.imageUrl}" alt="${cocktail.name}">`
                    : `<i class="bi bi-cup-straw"></i>`
                }
            </div>
            <div class="cocktail-detail-info">
                <div class="cocktail-detail-header">
                    <div>
                        <h2>${cocktail.name}</h2>
                        <span class="badge ${cocktail.is_public ? 'badge-success' : 'badge-warning'}">
                            ${cocktail.is_public ? 'Public' : 'Privé'}
                        </span>
                    </div>
                    ${isOwner ? `
                        <div class="cocktail-detail-actions">
                            <button class="btn edit-cocktail" data-id="${cocktail.id}">
                                <i class="bi bi-pencil"></i> Modifier
                            </button>
                            <button class="btn btn-danger delete-cocktail" data-id="${cocktail.id}">
                                <i class="bi bi-trash"></i> Supprimer
                            </button>
                        </div>
                    ` : ''}
                </div>
                
                <div class="cocktail-detail-meta">
                    <p>Créé par ${cocktail.user?.name || 'Utilisateur inconnu'} le ${formatDate(cocktail.created_at)}</p>
                </div>
                
                <div class="cocktail-detail-description">
                    <h3>Description</h3>
                    <p>${cocktail.description || 'Aucune description disponible.'}</p>
                </div>
                
                <div class="ingredients-list">
                    <h3>Ingrédients</h3>
                    ${cocktail.ingredients && cocktail.ingredients.length > 0 ? `
                        <ul>
                            ${cocktail.ingredients.map(ingredient => `
                                <li>
                                    <span>${ingredient.name}</span>
                                    <span>${ingredient.quantity}</span>
                                </li>
                            `).join('')}
                        </ul>
                    ` : '<p>Aucun ingrédient spécifié.</p>'}
                </div>
            </div>
        </div>
    `;
    
    // Add event listeners for edit and delete buttons
    if (isOwner) {
        cocktailDetailContent.querySelector('.edit-cocktail').addEventListener('click', () => {
            editCocktail(cocktail.id);
        });
        
        cocktailDetailContent.querySelector('.delete-cocktail').addEventListener('click', () => {
            confirmDeleteCocktail(cocktail.id, cocktail.name);
        });
    }
}

function editCocktail(id) {
    isEditMode = true;
    currentCocktailId = id;
    document.getElementById('form-title').textContent = 'Modifier le cocktail';
    
    // Fetch cocktail data and populate form
    fetchCocktail(id).then(cocktail => {
        if (!cocktail) {
            alert('Cocktail non trouvé.');
            return;
        }
        
        // Populate form fields
        document.getElementById('cocktail-name').value = cocktail.name || '';
        document.getElementById('cocktail-description').value = cocktail.description || '';
        document.getElementById('cocktail-image').value = cocktail.imageUrl || '';
        
        // Set visibility
        const visibilityRadios = document.getElementsByName('visibility');
        for (let radio of visibilityRadios) {
            if (radio.value === String(cocktail.is_public)) {
                radio.checked = true;
                break;
            }
        }
        
        // Clear existing ingredients
        ingredientsList.innerHTML = '';
        
        // Add ingredients
        if (cocktail.ingredients && cocktail.ingredients.length > 0) {
            cocktail.ingredients.forEach(ingredient => {
                addIngredientField(ingredient.name, ingredient.quantity);
            });
        } else {
            addIngredientField('', '');
        }
        
        showPage('cocktail-form');
    });
}

function confirmDeleteCocktail(id, name) {
    if (confirm(`Êtes-vous sûr de vouloir supprimer le cocktail "${name}" ?`)) {
        deleteCocktail(id).then(() => {
            // If we're on the detail page, go back to list
            if (cocktailDetailPage.classList.contains('active')) {
                showPage('cocktail-list');
            }
            
            // Refresh cocktails list
            loadCocktails();
        }).catch(error => {
            alert(`Erreur lors de la suppression: ${error.message}`);
        });
    }
}

function addIngredientField(name = '', quantity = '') {
    const ingredientItem = document.createElement('div');
    ingredientItem.className = 'ingredient-item';
    ingredientItem.innerHTML = `
        <input type="text" placeholder="Nom de l'ingrédient" class="ingredient-name" value="${name}" required>
        <input type="text" placeholder="Quantité" class="ingredient-quantity" value="${quantity}" required>
        <button type="button" class="remove-ingredient"><i class="bi bi-trash"></i></button>
    `;
    
    ingredientsList.appendChild(ingredientItem);
    
    // Add event listener to remove button
    ingredientItem.querySelector('.remove-ingredient').addEventListener('click', function() {
        ingredientsList.removeChild(ingredientItem);
    });
}

// Add this function or update your existing formatDate function
function formatDate(dateString) {
  if (!dateString) return 'Date inconnue';
  
  try {
    const date = new Date(dateString);
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
      return 'Date invalide';
    }
    
    return date.toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  } catch (error) {
    console.error('Error formatting date:', error);
    return 'Date invalide';
  }
}

function filterCocktails(cocktails) {
    // First apply search filter
    let filtered = cocktails;
    
    if (searchQuery) {
        const query = searchQuery.toLowerCase();
        filtered = filtered.filter(cocktail => 
            cocktail.name.toLowerCase().includes(query) || 
            (cocktail.description && cocktail.description.toLowerCase().includes(query))
        );
    }
    
    // Then apply visibility filter
    if (currentFilter === 'public') {
        filtered = filtered.filter(cocktail => cocktail.is_public);
    } else if (currentFilter === 'private') {
        filtered = filtered.filter(cocktail => !cocktail.is_public);
    }
    
    return filtered;
}

// Event Handlers
async function loadCocktails() {
    cocktailsContainer.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Chargement des cocktails...</p>
        </div>
    `;
    
    const onlyMine = myCocktailsLink.classList.contains('active');
    const data = await fetchCocktails(onlyMine);
    const cocktails = data.cocktails || [];
    
    renderCocktails(filterCocktails(cocktails));
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initial auth check
    checkAuth();
    
    // Load cocktails
    loadCocktails();
    
    // Navigation
    homeLink.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelectorAll('nav a').forEach(link => link.classList.remove('active'));
        homeLink.classList.add('active');
        showPage('cocktail-list');
        loadCocktails();
    });
    
    myCocktailsLink.addEventListener('click', (e) => {
        e.preventDefault();
        if (!checkAuth()) {
            alert('Veuillez vous connecter pour voir vos cocktails.');
            loginModal.style.display = 'block';
            return;
        }
        
        document.querySelectorAll('nav a').forEach(link => link.classList.remove('active'));
        myCocktailsLink.classList.add('active');
        showPage('cocktail-list');
        loadCocktails();
    });
    
    createCocktailLink.addEventListener('click', (e) => {
        e.preventDefault();
        if (!checkAuth()) {
            alert('Veuillez vous connecter pour créer un cocktail.');
            loginModal.style.display = 'block';
            return;
        }
        
        // Reset form
        isEditMode = false;
        currentCocktailId = null;
        document.getElementById('form-title').textContent = 'Créer un nouveau cocktail';
        document.getElementById('cocktail-create-form').reset();
        ingredientsList.innerHTML = '';
        addIngredientField();
        
        showPage('cocktail-form');
    });
    
    backToListBtn.addEventListener('click', () => {
        showPage('cocktail-list');
    });
    
    // Search
    searchBtn.addEventListener('click', () => {
        searchQuery = searchInput.value.trim();
        loadCocktails();
    });
    
    searchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            searchQuery = searchInput.value.trim();
            loadCocktails();
        }
    });
    
    // Filters
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            loadCocktails();
        });
    });
    
    // Auth
    loginBtn.addEventListener('click', () => {
        loginModal.style.display = 'block';
    });
    
    registerBtn.addEventListener('click', () => {
        registerModal.style.display = 'block';
    });
    
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === loginModal) {
            loginModal.style.display = 'none';
        }
        if (e.target === registerModal) {
            registerModal.style.display = 'none';
        }
    });
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const credentials = {
            email: document.getElementById('login-email').value,
            password: document.getElementById('login-password').value
        };
        
        try {
            await login(credentials);
            loginModal.style.display = 'none';
            checkAuth();
            loadCocktails();
        } catch (error) {
            alert('Erreur de connexion: ' + error.message);
        }
    });
    
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const userData = {
            name: document.getElementById('register-name').value,
            email: document.getElementById('register-email').value,
            password: document.getElementById('register-password').value
        };
        
        try {
            await register(userData);
            registerModal.style.display = 'none';
            checkAuth();
            loadCocktails();
        } catch (error) {
            alert('Erreur d\'inscription: ' + error.message);
        }
    });
    
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        checkAuth();
        
        // Go back to home page
        document.querySelectorAll('nav a').forEach(link => link.classList.remove('active'));
        homeLink.classList.add('active');
        showPage('cocktail-list');
        loadCocktails();
    });
    
    // Cocktail form
    addIngredientBtn.addEventListener('click', () => {
        addIngredientField();
    });
    
    cancelFormBtn.addEventListener('click', () => {
        showPage('cocktail-list');
    });
    
    cocktailCreateForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Get form data
        const name = document.getElementById('cocktail-name').value;
        const description = document.getElementById('cocktail-description').value;
        const imageUrl = document.getElementById('cocktail-image').value;
        const isPublic = document.querySelector('input[name="visibility"]:checked').value === 'true';
        
        // Get ingredients
        const ingredients = [];
        const ingredientItems = ingredientsList.querySelectorAll('.ingredient-item');
        
        ingredientItems.forEach(item => {
            const nameInput = item.querySelector('.ingredient-name');
            const quantityInput = item.querySelector('.ingredient-quantity');
            
            if (nameInput.value.trim() && quantityInput.value.trim()) {
                ingredients.push({
                    name: nameInput.value.trim(),
                    quantity: quantityInput.value.trim()
                });
            }
        });
        
        const cocktailData = {
            name,
            description,
            imageUrl,
            isPublic,
            ingredients
        };
        
        try {
            if (isEditMode) {
                await updateCocktail(currentCocktailId, cocktailData);
                alert('Cocktail mis à jour avec succès!');
            } else {
                await createCocktail(cocktailData);
                alert('Cocktail créé avec succès!');
            }
            
            showPage('cocktail-list');
            loadCocktails();
        } catch (error) {
            alert(`Erreur: ${error.message}`);
        }
    });
    
    // Add initial ingredient field
    if (ingredientsList.children.length === 0) {
        addIngredientField();
    }
});