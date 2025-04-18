# JobSeekerAI: Your Personalized Job Hunt Partner

## Overview
JOBSEEKERAI is an AI-powered job search assistant that combines conversational AI with intelligent job matching capabilities. The system uses Llama2 for natural language understanding and multiple job search APIs to help users find relevant job opportunities through a chat interface. By leveraging advanced natural language processing and machine learning algorithms, JobSeekerAI provides personalized job recommendations, optimizes user resumes, and ensures that users have access to the latest job listings.

## Features
- **Latest Published Positions**: Aggregates the most up-to-date job listings from various sources.
- **Job Description Matching**: Analyzes user resumes and matches job descriptions that are over 70% aligned with their skills and experience.
- **Experience Optimization**: Identifies and highlights key words in the user's working experience to ensure their resume stands out.
- **Chronological Sorting**: Organizes matched job listings by their publication date, prioritizing the most recent opportunities.
- **Location Filtering**: Filters job listings to match the user's top 5 preferred cities.

## Technical Architecture
### Backend (FastAPI/Python)
- FastAPI Framework: RESTful API server with WebSocket support

- Ollama Integration: Local Llama2 model for conversational AI

- Job Search APIs:
  - JSearch API (RapidAPI) for comprehensive job search
  - Remotive API for remote tech jobs
      
- Job Matching System: Intelligent parameter extraction from conversations

### Frontend (React/TypeScript)
- React-based chat interface
- Real-time message updates
- TypeScript for type safety
- Responsive design for multiple devices

## Key Features
1. Conversational AI
-  Natural language processing using Llama2
- Context-aware responses
- Job-focused conversation guidance
  
2. Intelligent Job Matching`
- Extracts job preferences from conversation:
- Position/Title
- Location
- Salary requirements
- Experience level
- Job type (remote, hybrid, etc.)
- Maintains conversation history for context
  
3. Multi-Source Job Search
- Aggregates results from multiple job boards
- Standardized job listing format
- Real-time job data fetching
  
4. Smart Response System
- Combines AI responses with job listings
- Provides formatted job details
- Supports search refinement

## Data Flow
- User sends message
- Ollama LLM processes message
- Job intent detection
- Parameter extraction
- Job API searches
- Response combination
- Formatted reply

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
