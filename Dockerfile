# Sets the lightweight Python 3.13 image as the starting base for our container.
FROM python:3.13-slim

# Creates and switches into a folder named /app where all our project files will live.
WORKDIR /app

# Copies only the requirements.txt file from your computer into the container's current directory.
COPY requirements.txt .

# Upgrades pip and installs your Python packages without saving temporary installer files to keep the image small.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copies the rest of your application's code files into the container's working directory.
COPY . .

# Informs Docker that the container will listen for incoming web network traffic on port 8000.
EXPOSE 8000

# Specifies the final command that starts the Uvicorn server to run your FastAPI app when the container boots up.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]