# Cocktail Manager Application

## Overview
Full-stack application for managing cocktail recipes using:
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Frontend: React
- Containerization: Docker

## Prerequisites
- Docker
- Docker Compose

## Setup and Running

1. Clone the repository
```bash
git clone https://your-repo-url.git
cd cocktail-app
```

2. Build and start the application
```bash
docker-compose up --build
```

3. Access the application
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000

## Development

### Backend
- Add new dependencies in `backend/requirements.txt`
- Modify API routes in `backend/app/main.py`

### Frontend
- Add new dependencies in `frontend/package.json`
- Modify React components in `frontend/src`

### Database
- Database is persisted in `postgres_data` volume
- Modify connection settings in `docker-compose.yml`

## Deployment Notes
- Use environment variables for sensitive information
- Configure CORS and security settings as needed