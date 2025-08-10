FROM python:3.11-slim

# Install system dependencies for GUI
RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-dev \
    xvfb \
    xauth \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x *.py

CMD ["bash"]
