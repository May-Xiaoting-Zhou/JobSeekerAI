# Backend Project with UV

This backend project uses [uv](https://github.com/astral-sh/uv) for Python package management. UV is a fast, reliable Python package installer and resolver, built in Rust.

## Setup

The project is configured with a virtual environment in the `.venv` directory. All dependencies are managed using uv.

## Using Just for Environment Management

The project now uses [Just](https://github.com/casey/just) as a command runner for managing both frontend and backend environments. The backend-specific commands are:

### Setup the Backend Environment

```bash
just setup-backend
```

This will create a virtual environment and install all dependencies.

### Run the Backend Server

```bash
just run-backend
```

### Add a New Dependency

```bash
just add-backend-dep <package_name>
```

This will install the package and add it to the requirements.txt file.

### Update Dependencies

```bash
just update-deps
```

This will update all dependencies for both backend and frontend.

## Manual UV Commands

If you prefer to use uv directly, here are some common commands:

### Create a Virtual Environment

```bash
uv venv .venv
```

### Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
uv sync
```

### Install a Specific Package

```bash
uv add <package_name>
```

### Update Dependencies

```bash
uv sync --upgrade
```

## Benefits of Using UV

- **Speed**: UV is significantly faster than pip for installing packages
- **Reliability**: Better dependency resolution to avoid conflicts
- **Caching**: Efficient caching for faster repeated installations
- **Compatibility**: Works with existing requirements.txt files
