#!/bin/bash

# uv_manage.sh - Script to manage the backend project using uv

# Set the virtual environment path
VENV_PATH=".venv"

# Function to activate the virtual environment
activate_venv() {
    echo "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
    echo "Virtual environment activated. Python: $(which python)"
}

# Function to install dependencies
install_deps() {
    echo "Installing dependencies using uv..."
    uv pip install -r ../requirements.txt
    echo "Dependencies installed successfully."
}

# Function to update dependencies
update_deps() {
    echo "Updating dependencies using uv..."
    uv pip install --upgrade -r ../requirements.txt
    echo "Dependencies updated successfully."
}

# Function to add a new dependency
add_dep() {
    if [ -z "$1" ]; then
        echo "Error: Please specify a package to install."
        echo "Usage: ./uv_manage.sh add <package_name>"
        return 1
    fi
    
    echo "Installing $1 using uv..."
    uv pip install "$1"
    
    # Add the package to requirements.txt if it's not already there
    if ! grep -q "^$1" ../requirements.txt; then
        echo "$1" >> ../requirements.txt
        echo "Added $1 to requirements.txt"
    fi
}

# Function to run the backend server
run_server() {
    echo "Starting backend server..."
    uvicorn main:app --reload
}

# Function to show help
show_help() {
    echo "uv_manage.sh - Script to manage the backend project using uv"
    echo ""
    echo "Usage: ./uv_manage.sh [command]"
    echo ""
    echo "Commands:"
    echo "  activate    - Activate the virtual environment"
    echo "  install     - Install dependencies from requirements.txt"
    echo "  update      - Update dependencies to latest versions"
    echo "  add <pkg>   - Install a new package and add it to requirements.txt"
    echo "  run         - Run the backend server"
    echo "  help        - Show this help message"
}

# Main script logic
case "$1" in
    activate)
        activate_venv
        ;;
    install)
        activate_venv
        install_deps
        ;;
    update)
        activate_venv
        update_deps
        ;;
    add)
        activate_venv
        add_dep "$2"
        ;;
    run)
        activate_venv
        run_server
        ;;
    help|*)
        show_help
        ;;
esac
