# Project description

The `clociduck` project is a tool designed to fetch time entries from Clockify, process them into an invoice-ready format, and provide a user-friendly interface for review and export. It uses DuckDB for local data storage and Streamlit for the UI.

## Core Workflow

### 1. Configuration

The application's behavior is controlled by a flexible configuration layer.

-   **Secrets**: `CLOCKIFY_API_KEY` and `CLOCKIFY_WORKSPACE_ID` are managed securely. The initial implementation uses a `.env` file, but the architecture allows for future methods like a `config.toml` or a database table.
-   **Parameters**: Key operational values are configurable with sensible defaults:
    -   `ROUNDING_MINUTES`: The interval to round durations up to (default: 15).
    -   `DAY_START_TIME`: The start time for the synthetic daily schedule (default: "08:00").

### 2. Data Ingestion & State Management

-   **Fetch**: A script connects to the Clockify API to pull time entries. To avoid redundant data fetching, it only retrieves entries created since the last successful sync.
-   **Storage**: Raw time entries are saved into a local `clockiduck.db` DuckDB database. This preserves the original data, including project and task details, for potential future analysis.
-   **State**: The timestamp of the last successful sync is stored in a dedicated `app_state` table within the same DuckDB database, ensuring robust state management.

### 3. Data Transformation Pipeline

For a user-selected date range, the raw data undergoes a multi-step transformation process:

1.  **Rounding**: Each individual time entry's duration is rounded **up** to the nearest configurable interval (e.g., 15 minutes). A 1-minute entry becomes 15 minutes; a 16-minute entry becomes 30 minutes.
2.  **Aggregation**: The rounded durations are then grouped by their `description` for a specific day, and their values are summed. This creates a consolidated list of tasks and their total billable time for the day.
3.  **Scheduling**: The aggregated tasks are arranged into a synthetic, contiguous workday schedule. The schedule begins at the configured `DAY_START_TIME` (e.g., 08:00), and each task is laid out sequentially based on its total duration. The order of tasks within the day is not critical, as long as there are no gaps.

### 4. User Interface (Streamlit)

A Streamlit application provides the primary user interface for interacting with the processed data.

-   **Display**: The final, scheduled data is presented in an editable table, showing columns like `Date`, `Description`, `Calculated Start Time`, `Calculated End Time`, and `Duration (hours)`.
-   **Editing**: Users can manually override values in the table (e.g., change a task's duration).
-   **Rescheduling**: A "Reschedule Day" button allows the user to re-run the scheduling logic after making manual edits, which will update the start and end times for all subsequent tasks on that day.

### 5. Export

-   The final, user-approved report can be exported to an Excel spreadsheet, ready for invoicing or internal reporting.

## Future Improvements

-   **Visual Timeline**: Add a Gantt chart (e.g., using Plotly) to visualize the generated daily schedule.
-   **Advanced Grouping**: Allow users to change the aggregation strategy in the UI (e.g., group by `Project` instead of `description`).
-   **Configurable Breaks**: Add a feature to automatically insert a lunch break into the schedule.
