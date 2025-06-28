# clociduck

A tool to fetch time entries from Clockify, process them for invoicing, and present them in a user-friendly UI built with Streamlit and DuckDB.

## Project Setup

Follow these steps to get the project running locally.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd clockiduck
```

### 2. Configure Environment Variables

The application requires a Clockify API Key and Workspace ID to function.

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Edit the newly created `.env` file and add your personal credentials.

### 3. Install Dependencies

This project's dependencies are listed in `pyproject.toml`. You can install them using `pip` or a modern package manager like `uv`.

```bash
# Using uv
uv pip sync pyproject.toml
```

## Usage

### Initial Data Sync

Before using the application, you must fetch your time entries from Clockify. Run the synchronization script from your terminal:

```bash
clociduck-sync
```

This command will:
- Create a `clockiduck.db` file in your project directory.
- Fetch all your time entries from Clockify and save them locally.
- On subsequent runs, it will only fetch entries created since the last sync.