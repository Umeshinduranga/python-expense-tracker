# python-expense-tracker


A simple, lightweight command-line application built with Python for tracking personal expenses. It stores all data locally in an `expenses.csv` file, making it easy to manage, view, and back up your financial records.

## Features

*   **Add Expenses:** Record new expenses with a date, category, and amount.
*   **View All Expenses:** Get a complete list of all recorded expenses.
*   **Filter by Category:** View total spending for a specific category (e.g., food, travel, bills).
*   **Delete Expenses:** Remove incorrect or unwanted entries.
*   **Monthly Reports:** Generate a summary of total spending for any given month, with a category-wise breakdown.
*   **Data Persistence:** All expenses are saved to a `expenses.csv` file, so your data is never lost between sessions.

## Getting Started

### Prerequisites

*   Python 3.x

### Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/umeshinduranga/python-expense-tracker.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd python-expense-tracker/expense_tracker
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

This will launch the interactive command-line menu.

## How It Works

The application will present you with a menu of options:

```
== Personal Expense Tracker ==
1. Add Expense
2. View All Expenses
3. View Expenses by Category
4. Delete Expense
5. Monthly Report
6. Exit
Enter your choice (1-6):
```

Simply enter a number to perform the corresponding action. The application includes input validation for dates and amounts to ensure data integrity.

### File Structure

*   `main.py`: The entry point for the application. It displays the menu and handles user input.
*   `expense_manager.py`: Contains all the core logic for managing expenses, such as adding, viewing, deleting, and generating reports.
*   `expenses.csv`: The database file where all expense records are stored in CSV format. It is automatically created if it doesn't exist.

### Example: Adding an Expense

```
Enter your choice (1-6): 1
Enter date (YYYY-MM-DD): 2023-10-27
Enter category (food, travel, bills, etc.): food
Enter amount: 15.50
✅ Expense added successfully!
