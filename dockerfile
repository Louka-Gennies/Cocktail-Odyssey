FROM python:3.9

WORKDIR /app

# Créer le répertoire pour la base de données
RUN mkdir -p /app/data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Mettre à jour les permissions
RUN chmod -R 777 /app/data

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]