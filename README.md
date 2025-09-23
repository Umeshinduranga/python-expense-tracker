# Personal Expense Tracker Pro 💰

A professional-grade command-line application built with Python for comprehensive personal expense management. Features a beautiful Rich-based UI with advanced tracking, budgeting, and reporting capabilities.

## ✨ Features

### 📊 Core Expense Management
*   **Add Expenses:** Record expenses with date, category, amount, and optional descriptions
*   **Edit Expenses:** Modify existing expense entries with full validation
*   **View All Expenses:** Beautiful table display of all recorded expenses
*   **Delete Expenses:** Remove incorrect or unwanted entries with confirmation
*   **Search & Filter:** Advanced filtering by keyword, category, date range, and amount range

### 📈 Reporting & Analytics
*   **Monthly Reports:** Comprehensive spending summaries with category breakdowns
*   **Budget Tracking:** Set monthly budgets per category with automatic monitoring
*   **Budget Alerts:** Real-time warnings when approaching or exceeding budget limits
*   **Category Analytics:** Detailed spending patterns by category

### 🎨 Enhanced User Experience
*   **Rich UI:** Beautiful command-line interface with colors, tables, and formatting
*   **Data Validation:** Input validation for dates, amounts, and categories
*   **Auto-backup:** Automatic data backup with configurable frequency
*   **Export Functions:** Export data to CSV format for external analysis

### ⚙️ Configuration & Management
*   **Custom Categories:** Add, edit, and manage expense categories
*   **Settings Management:** Configure currency, date formats, and preferences
*   **Data Organization:** Structured data storage with automatic directory creation
*   **Backup Management:** Automated backup system with restore capabilities

## 🚀 Getting Started

### Prerequisites

*   Python 3.7 or higher
*   **Optional:** `rich` library for enhanced UI (recommended)

### Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/umeshinduranga/python-expense-tracker.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd python-expense-tracker/expense_tracker
    ```

3.  **Install dependencies (recommended):**
    ```bash
    pip install rich
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

The application will automatically detect if Rich is installed and provide the enhanced UI experience.

## 🖥️ Interface

The application features an intuitive menu-driven interface:

```
💰 Personal Expense Tracker Pro
Professional expense management made simple

1. Add New Expense
2. View All Expenses  
3. Search & Filter Expenses
4. Edit Expense
5. Delete Expense
6. Monthly Report
7. Budget Management
8. Export Data
9. Settings
0. Exit
```

### Key Features in Action

**🔍 Advanced Search & Filtering:**
- Filter by keyword in descriptions
- Filter by category
- Date range filtering
- Amount range filtering
- Combined filter criteria

**📊 Budget Management:**
- Set monthly budgets per category
- Real-time budget tracking
- Visual budget status indicators
- Automatic alerts for budget limits

**📈 Enhanced Reporting:**
- Monthly spending summaries
- Category-wise breakdowns
- Budget vs actual comparisons
- Visual progress indicators

## 📁 Project Structure

```
python-expense-tracker/
├── expense_tracker/
│   ├── main.py                    # Application entry point
│   ├── expense_manager.py         # Core expense management logic
│   ├── enhanced_ui.py            # Rich-based user interface
│   └── data/                     # Data directory (auto-created)
│       ├── expenses.csv          # Main expense database
│       ├── config.json          # User preferences & settings
│       └── backups/             # Automatic backup storage
└── README.md
```

### File Descriptions

*   **`main.py`**: Application entry point with dependency checking and error handling
*   **`expense_manager.py`**: Core business logic for expense operations, budget management, and data persistence
*   **`enhanced_ui.py`**: Beautiful Rich-based user interface with tables, colors, and interactive prompts
*   **`data/expenses.csv`**: CSV database storing all expense records
*   **`data/config.json`**: Configuration file for user preferences, categories, and budgets
*   **`data/backups/`**: Automatic backup directory with timestamped data snapshots

## 💡 Examples

### Adding an Expense with Description
```
Enter your choice: 1
Enter date (YYYY-MM-DD) [2025-09-23]: 2025-09-20
Enter category: food
Enter amount: 25.50
Enter description (optional): Lunch at downtown cafe
✅ Expense added successfully!
⚠️  Budget warning: You've spent Rs.125.50 out of Rs.200.00 (62.8%) for food this month.
```

### Setting a Monthly Budget
```
Enter your choice: 7
Budget Management Menu:
1. View Current Budgets
2. Set New Budget
3. Edit Budget
4. Remove Budget

Enter your choice: 2
Enter month (YYYY-MM) [2025-09]: 2025-09
Enter category: food
Enter budget limit: 200.00
✅ Budget set successfully!
```

### Advanced Search Example
```
Enter your choice: 3
Search & Filter Options:
- Keyword: cafe
- Category: food
- Start date: 2025-09-01
- End date: 2025-09-30
- Min amount: 20.00
- Max amount: 50.00

Found 3 matching expenses totaling Rs.78.50
```

## 🔧 Configuration

The application supports various configuration options through the settings menu:

- **Currency Symbol**: Customize display currency (default: Rs.)
- **Date Format**: Configure date display format
- **Categories**: Add, edit, or remove expense categories
- **Auto-backup**: Enable/disable automatic data backups
- **Backup Frequency**: Set backup interval in days

## 📦 Dependencies

### Required
- Python 3.7+

### Optional (but recommended)
- `rich`: For enhanced UI with colors, tables, and beautiful formatting
  ```bash
  pip install rich
  ```

The application gracefully degrades to basic text output if Rich is not installed.

## 🔐 Data Security

- All data is stored locally on your machine
- No internet connection required
- Automatic backup system prevents data loss
- CSV format ensures data portability and longevity

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🚀 Version History

**v2.0.0 - Enhanced Professional Edition**
- Rich-based beautiful UI
- Advanced search and filtering
- Budget management system
- Export functionality
- Enhanced settings and configuration
- Automatic backup system

**v1.0.0 - Basic Edition**
- Simple CLI interface
- Basic expense tracking
- Monthly reports

## 📧 Support

For questions, suggestions, or support, please create an issue on GitHub.

---

**Happy expense tracking! 💰✨**
