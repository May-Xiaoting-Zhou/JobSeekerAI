# JobSeekerAI Project Management Justfile

# Default recipe to run when just is called without arguments
default:
    @just --list

# Project directories
backend_dir := "backend"
frontend_dir := "frontend"
backend_venv := ".venv"

# Setup the backend environment
setup-backend:
    #!/usr/bin/env bash
    echo "==== Setting up Backend Environment ===="
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        echo "Error: uv is not installed. Please install it first."
        echo "You can install uv with: pip install uv"
        exit 1
    fi
    
    # Get the absolute path to the project root
    PROJECT_ROOT="$(pwd)"
    
    # Create and activate virtual environment if it doesn't exist
    if [ ! -d "${PROJECT_ROOT}/{{backend_dir}}/{{backend_venv}}" ]; then
        echo "Creating virtual environment..."
        cd "${PROJECT_ROOT}/{{backend_dir}}" && uv venv "{{backend_venv}}"
        echo "Virtual environment created."
    else
        echo "Virtual environment already exists."
    fi
    
    # Install dependencies
    echo "Installing backend dependencies..."
    cd "${PROJECT_ROOT}/{{backend_dir}}" && source "{{backend_venv}}/bin/activate" && uv sync
    
    echo "Backend environment setup complete."

# Setup the frontend environment
setup-frontend:
    #!/usr/bin/env bash
    echo "==== Setting up Frontend Environment ===="
    
    # Check if npm is installed
    if ! command -v npm &> /dev/null; then
        echo "Error: npm is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Get the absolute path to the project root
    PROJECT_ROOT="$(pwd)"
    
    # Install dependencies
    echo "Installing frontend dependencies..."
    cd "${PROJECT_ROOT}/{{frontend_dir}}" && npm install
    
    echo "Frontend environment setup complete."

# Setup both environments
setup-all: setup-backend setup-frontend
    echo "All environments setup complete."

# Run the backend server
run-backend:
    #!/usr/bin/env bash
    echo "==== Starting Backend Server ===="
    PROJECT_ROOT="$(pwd)"
    cd "${PROJECT_ROOT}/{{backend_dir}}" && source "{{backend_venv}}/bin/activate" && uvicorn main:app --reload

# Run the frontend server
run-frontend:
    #!/usr/bin/env bash
    echo "==== Starting Frontend Server ===="
    PROJECT_ROOT="$(pwd)"
    cd "${PROJECT_ROOT}/{{frontend_dir}}" && npm run dev

# Run both servers concurrently (requires tmux)
run-all:
    #!/usr/bin/env bash
    echo "==== Starting Both Servers ===="
    
    # Get the absolute path to the project root
    PROJECT_ROOT="$(pwd)"
    
    # Check if tmux is installed
    if command -v tmux &> /dev/null; then
        echo "Using tmux to run both servers..."
        tmux new-session -d -s jobseeker-backend "cd ${PROJECT_ROOT}/{{backend_dir}} && source {{backend_venv}}/bin/activate && uvicorn main:app --reload"
        tmux new-session -d -s jobseeker-frontend "cd ${PROJECT_ROOT}/{{frontend_dir}} && npm run dev"
        echo "Both servers started in tmux sessions."
        echo "To attach to backend: tmux attach -t jobseeker-backend"
        echo "To attach to frontend: tmux attach -t jobseeker-frontend"
    else
        echo "Error: tmux is not installed. Please run the servers separately."
        echo "Run backend: just run-backend"
        echo "Run frontend: just run-frontend"
    fi

# Add a backend dependency
add-backend-dep package:
    #!/usr/bin/env bash
    echo "==== Adding Backend Dependency: {{package}} ===="
    PROJECT_ROOT="$(pwd)"
    cd "${PROJECT_ROOT}/{{backend_dir}}" && source "{{backend_venv}}/bin/activate" && uv add "{{package}}"
    echo "Backend dependency added."

# Add a frontend dependency
add-frontend-dep package:
    #!/usr/bin/env bash
    echo "==== Adding Frontend Dependency: {{package}} ===="
    PROJECT_ROOT="$(pwd)"
    cd "${PROJECT_ROOT}/{{frontend_dir}}" && npm install "{{package}}"
    echo "Frontend dependency added."

# Add a frontend dev dependency
add-frontend-dev-dep package:
    #!/usr/bin/env bash
    echo "==== Adding Frontend Dev Dependency: {{package}} ===="
    PROJECT_ROOT="$(pwd)"
    cd "${PROJECT_ROOT}/{{frontend_dir}}" && npm install --save-dev "{{package}}"
    echo "Frontend dev dependency added."

# Update all dependencies
update-deps:
    #!/usr/bin/env bash
    echo "==== Updating All Dependencies ===="
    
    # Get the absolute path to the project root
    PROJECT_ROOT="$(pwd)"
    
    # Update backend dependencies
    echo "Updating backend dependencies..."
    cd "${PROJECT_ROOT}/{{backend_dir}}" && source "{{backend_venv}}/bin/activate" && uv sync --upgrade
    echo "Backend dependencies updated."
    
    # Update frontend dependencies
    echo "Updating frontend dependencies..."
    cd "${PROJECT_ROOT}/{{frontend_dir}}" && npm update
    echo "Frontend dependencies updated."
    
    echo "All dependencies updated."

# Build the frontend for production
build-frontend:
    #!/usr/bin/env bash
    echo "==== Building Frontend ===="
    PROJECT_ROOT="$(pwd)"
    cd "${PROJECT_ROOT}/{{frontend_dir}}" && npm run build
    echo "Frontend built successfully."

# Clean up environments
clean:
    #!/usr/bin/env bash
    echo "==== Cleaning Environments ===="
    
    # Get the absolute path to the project root
    PROJECT_ROOT="$(pwd)"
    
    # Ask for confirmation
    read -p "This will remove node_modules and virtual environments. Are you sure? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Clean frontend
        echo "Cleaning frontend..."
        rm -rf "${PROJECT_ROOT}/{{frontend_dir}}/node_modules"
        rm -rf "${PROJECT_ROOT}/{{frontend_dir}}/build"
        
        # Clean backend
        echo "Cleaning backend..."
        rm -rf "${PROJECT_ROOT}/{{backend_dir}}/{{backend_venv}}"
        
        echo "Environments cleaned."
    else
        echo "Clean operation cancelled."
    fi
