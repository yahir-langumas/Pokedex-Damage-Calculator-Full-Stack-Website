# Builds the Pokédex Damage Calculator into a Docker image.
FROM python:3.13-slim

# Don't write .pyc files, and print logs right away.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

# Install the packages first, so Docker can reuse this step when only the code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the project.
COPY . .

# Gather the static files, set up the database and load the saved Pokémon data. DJANGO_DEBUG is only on for these build steps.
RUN DJANGO_DEBUG=True python manage.py collectstatic --noinput
RUN DJANGO_DEBUG=True python manage.py migrate
RUN DJANGO_DEBUG=True python manage.py loaddata pokedata

# Run the site as a regular user instead of root.
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Gunicorn runs the site on port 8000.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]