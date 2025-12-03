# Use official Python base image
FROM python:3.10

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . /app/

# Expose Django port
EXPOSE 8000

# Run migrations automatically and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
