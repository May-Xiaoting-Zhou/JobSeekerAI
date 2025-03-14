# Frontend Project

This is the frontend part of the JobSeekerAI project, built with React and TypeScript.

## Setup

The project uses [Just](https://github.com/casey/just) as a command runner for managing both frontend and backend environments.

## Using Just for Environment Management

### Setup the Frontend Environment

```bash
just setup-frontend
```

This will install all dependencies using npm.

### Run the Frontend Server

```bash
just run-frontend
```

This will start the development server using Vite.

### Add a New Dependency

```bash
just add-frontend-dep <package_name>
```

This will install the package and add it to package.json.

### Add a New Dev Dependency

```bash
just add-frontend-dev-dep <package_name>
```

This will install the package as a dev dependency and add it to package.json.

### Update Dependencies

```bash
just update-deps
```

This will update all dependencies for both frontend and backend.

### Build for Production

```bash
just build-frontend
```

This will build the frontend for production.

## Project Structure

- `public/`: Static assets that will be served directly
- `src/`: Source code
  - `App.tsx`: Main application component
  - `index.tsx`: Entry point
  - `types.ts`: TypeScript type definitions

## Available Scripts in package.json

- `npm start`: Start the React development server (using react-scripts)
- `npm run build`: Build the app for production
- `npm test`: Run tests
- `npm run eject`: Eject from react-scripts
- `npm run dev`: Start the Vite development server
- `npm run serve`: Preview the production build locally
