# ---- Stage 1: build the React app ----
# Uses a minimal, lightweight Node.js version 22 image as the base for building the frontend.
FROM node:22-slim AS frontend-build

# Creates and switches to a dedicated directory named "/frontend" inside the container.
WORKDIR /frontend

# Copies only the dependency files into the container to leverage Docker's caching mechanism.
COPY frontend/package.json frontend/package-lock.json ./

# Installs the exact dependencies specified in the lockfile quickly and cleanly.
RUN npm ci

# Copies the rest of the frontend source code into the container.
COPY frontend/ ./

# Runs the build script to compile the frontend application for production.
RUN npm run build

# ---- Stage 2: Python app that also serves the built React files ----
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

# Copies the compiled production assets from the "frontend-build" stage into the current image stage.
COPY --from=frontend-build /frontend/dist ./frontend/dist

# Informs Docker that the container will listen for incoming web network traffic on port 8000.
EXPOSE 8000

# Specifies the final command that starts the Uvicorn server to run your FastAPI app when the container boots up.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]