FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory
COPY ./app ./app

# Install Whisper
RUN pip install git+https://github.com/openai/whisper.git 

ENV PORT=8000
EXPOSE ${PORT}

# Update the command to point to the correct module
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]