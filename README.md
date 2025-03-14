# JobSeekerAI: Your Personalized Job Hunt Partner

## Overview
JobSeekerAI is an intelligent AI agent designed to streamline and enhance the job search process for job seekers. By leveraging advanced natural language processing and machine learning algorithms, JobSeekerAI provides personalized job recommendations, optimizes user resumes, and ensures that users have access to the latest job listings.

## Features
- **Latest Published Positions**: Aggregates the most up-to-date job listings from various sources.
- **Job Description Matching**: Analyzes user resumes and matches job descriptions that are over 70% aligned with their skills and experience.
- **Experience Optimization**: Identifies and highlights key words in the user's working experience to ensure their resume stands out.
- **Chronological Sorting**: Organizes matched job listings by their publication date, prioritizing the most recent opportunities.
- **Location Filtering**: Filters job listings to match the user's top 5 preferred cities.

## Project Structure
The project consists of the following components:
- `job_scraper.py`: Script for scraping or using APIs to gather job listings.
- `job_matcher.py`: Script for matching job descriptions to user resumes and highlighting key words.
- `main.py`: Main script that integrates all components and provides the user interface.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/JobSeekerAI.git
   ```

2. Python dependencies are defined in `backend/requirements.txt` and are installed automatically when setting up the backend environment.

3. The project uses [Just](https://github.com/casey/just) as a command runner for managing both frontend and backend environments. Make sure you have Just installed:
   ```sh
   # On macOS with Homebrew
   brew install just
   
   # On Linux with apt
   apt install just
   
   # On Windows with Scoop
   scoop install just
   ```

3. Setup the project environments:
   ```sh
   # Setup both frontend and backend environments
   just setup-all
   
   # Or setup them separately
   just setup-backend
   just setup-frontend
   ```

## Usage

The project uses Just commands to manage both frontend and backend environments:

### Environment Management
```sh
# Setup both environments
just setup-all

# Setup only backend
just setup-backend

# Setup only frontend
just setup-frontend

# Clean up environments (removes node_modules and virtual environments)
just clean
```

### Running Servers
```sh
# Run both frontend and backend servers (requires tmux)
just run-all

# Run only backend server
just run-backend

# Run only frontend server
just run-frontend
```

### Dependency Management
```sh
# Add a backend dependency
just add-backend-dep <package>

# Add a frontend dependency
just add-frontend-dep <package>

# Add a frontend dev dependency
just add-frontend-dev-dep <package>

# Update all dependencies
just update-deps
```

### Build Operations
```sh
# Build the frontend for production
just build-frontend
```
