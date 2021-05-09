# Set docker image
FROM python:latest

# Set our working directory
WORKDIR /usr/src/app

# Copy our source files and requirements
COPY main.py .
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Execute app
CMD ["python", "./main.py"]
