# Backend Project with UV

This backend project uses [uv](https://github.com/astral-sh/uv) for Python package management. UV is a fast, reliable Python package installer and resolver, built in Rust.

## Setup

The project is configured with a virtual environment in the `.venv` directory. All dependencies are managed using uv.

## Using the Management Script

A management script `uv_manage.sh` is provided to simplify common tasks:

### Activate the Virtual Environment

```bash
./uv_manage.sh activate
```

### Install Dependencies

```bash
./uv_manage.sh install
```

### Update Dependencies

```bash
./uv_manage.sh update
```

### Add a New Dependency

```bash
./uv_manage.sh add <package_name>
```

This will install the package and add it to the requirements.txt file.

### Run the Backend Server

```bash
./uv_manage.sh run
```

### Get Help

```bash
./uv_manage.sh help
```

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
uv pip install -r ../requirements.txt
```

### Install a Specific Package

```bash
uv pip install <package_name>
```

### Update Dependencies

```bash
uv pip install --upgrade -r ../requirements.txt
```

## Benefits of Using UV

- **Speed**: UV is significantly faster than pip for installing packages
- **Reliability**: Better dependency resolution to avoid conflicts
- **Caching**: Efficient caching for faster repeated installations
- **Compatibility**: Works with existing requirements.txt files
