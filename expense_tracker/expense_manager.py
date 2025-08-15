"""
Enhanced Personal Expense Tracker
A professional-grade CLI expense management system with advanced features.
"""

import csv
import json
import shutil
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from decimal import Decimal, ROUND_HALF_UP

try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.progress import track
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Installing rich library for better UI experience...")
    print("Run: pip install rich")

# Constants
DATA_DIR = Path("data")
EXPENSES_FILE = DATA_DIR / "expenses.csv"
CONFIG_FILE = DATA_DIR / "config.json"
BACKUP_DIR = DATA_DIR / "backups"

DEFAULT_CATEGORIES = [
    "food", "transport", "bills", "entertainment", "shopping", 
    "healthcare", "education", "travel", "rent", "utilities", "other"
]

@dataclass
class Expense:
    """Represents a single expense entry."""
    date: str
    category: str
    amount: Decimal
    description: str = ""
    
    def to_dict(self) -> Dict:
        """Convert expense to dictionary for CSV writing."""
        return {
            'date': self.date,
            'category': self.category,
            'amount': str(self.amount),
            'description': self.description
        }

@dataclass
class Budget:
    """Represents a monthly budget."""
    month: str  # YYYY-MM format
    category: str
    limit: Decimal
    
class ExpenseManager:
    """Core expense management logic."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.expenses: List[Expense] = []
        self.config: Dict = {}
        self._initialize_data_structure()
        self.load_expenses()
        self.load_config()
    
    def _initialize_data_structure(self) -> None:
        """Create necessary directories and files."""
        DATA_DIR.mkdir(exist_ok=True)
        BACKUP_DIR.mkdir(exist_ok=True)
        
        if not EXPENSES_FILE.exists():
            self._create_expenses_file()
        
        if not CONFIG_FILE.exists():
            self._create_config_file()
    
    def _create_expenses_file(self) -> None:
        """Create the expenses CSV file with headers."""
        with open(EXPENSES_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
            writer.writeheader()
    
    def _create_config_file(self) -> None:
        """Create default configuration file."""
        default_config = {
            "currency": "Rs.",
            "date_format": "%Y-%m-%d",
            "categories": DEFAULT_CATEGORIES,
            "budgets": {},
            "auto_backup": True,
            "backup_frequency": 7  # days
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(default_config, file, indent=2)
    
    def load_config(self) -> None:
        """Load configuration from file."""
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                self.config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self._create_config_file()
            self.load_config()
    
    def save_config(self) -> None:
        """Save configuration to file."""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(self.config, file, indent=2)
    
    def load_expenses(self) -> None:
        """Load all expenses from CSV file."""
        self.expenses = []
        try:
            with open(EXPENSES_FILE, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expense = Expense(
                        date=row['date'],
                        category=row['category'],
                        amount=Decimal(row['amount']),
                        description=row.get('description', '')
                    )
                    self.expenses.append(expense)
        except FileNotFoundError:
            self._create_expenses_file()
    
    def save_expenses(self) -> None:
        """Save all expenses to CSV file."""
        with open(EXPENSES_FILE, 'w', newline='', encoding='utf-8') as file:
            if self.expenses:
                writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
                writer.writeheader()
                for expense in self.expenses:
                    writer.writerow(expense.to_dict())
            else:
                # Write just headers if no expenses
                writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
                writer.writeheader()
    
    def backup_data(self) -> None:
        """Create a backup of the expenses file."""
        if EXPENSES_FILE.exists():
            backup_name = f"expenses_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            backup_path = BACKUP_DIR / backup_name
            shutil.copy2(EXPENSES_FILE, backup_path)
            
            # Keep only last 10 backups
            backups = sorted(BACKUP_DIR.glob("expenses_backup_*.csv"))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
    
    def validate_date(self, date_str: str) -> bool:
        """Validate date format."""
        try:
            datetime.strptime(date_str, self.config['date_format'])
            return True
        except ValueError:
            return False
    
    def validate_amount(self, amount_str: str) -> bool:
        """Validate amount format and value."""
        try:
            amount = Decimal(amount_str)
            return amount > 0
        except (ValueError, TypeError):
            return False
    
    def add_expense(self, date_str: str, category: str, amount: Decimal, description: str = "") -> bool:
        """Add a new expense."""
        if not self.validate_date(date_str):
            return False
        
        if not self.validate_amount(str(amount)):
            return False
        
        expense = Expense(date_str, category.lower().strip(), amount, description.strip())
        self.expenses.append(expense)
        self.save_expenses()
        
        # Auto backup if enabled
        if self.config.get('auto_backup', True):
            self.backup_data()
        
        # Check budget warning
        self._check_budget_warning(expense)
        
        return True
    
    def edit_expense(self, index: int, date_str: str, category: str, amount: Decimal, description: str = "") -> bool:
        """Edit an existing expense."""
        if not (0 <= index < len(self.expenses)):
            return False
        
        if not self.validate_date(date_str) or not self.validate_amount(str(amount)):
            return False
        
        self.expenses[index] = Expense(date_str, category.lower().strip(), amount, description.strip())
        self.save_expenses()
        return True
    
    def delete_expense(self, index: int) -> bool:
        """Delete an expense by index."""
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            self.save_expenses()
            return True
        return False
    
    def search_expenses(self, keyword: str = "", category: str = "", start_date: str = "", end_date: str = "", min_amount: str = "", max_amount: str = "") -> List[Expense]:
        """Search expenses with multiple filters."""
        filtered_expenses = self.expenses.copy()
        
        if keyword:
            filtered_expenses = [e for e in filtered_expenses if keyword.lower() in e.description.lower() or keyword.lower() in e.category.lower()]
        
        if category:
            filtered_expenses = [e for e in filtered_expenses if e.category.lower() == category.lower()]
        
        if start_date:
            filtered_expenses = [e for e in filtered_expenses if e.date >= start_date]
        
        if end_date:
            filtered_expenses = [e for e in filtered_expenses if e.date <= end_date]
        
        if min_amount:
            min_amt = Decimal(min_amount)
            filtered_expenses = [e for e in filtered_expenses if e.amount >= min_amt]
        
        if max_amount:
            max_amt = Decimal(max_amount)
            filtered_expenses = [e for e in filtered_expenses if e.amount <= max_amt]
        
        return filtered_expenses
    
    def get_monthly_report(self, month: str) -> Dict:
        """Generate monthly expense report."""
        monthly_expenses = [e for e in self.expenses if e.date.startswith(month)]
        
        if not monthly_expenses:
            return {"total": Decimal("0"), "categories": {}, "expenses": []}
        
        total = sum(e.amount for e in monthly_expenses)
        categories = {}
        
        for expense in monthly_expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount
        
        return {
            "total": total,
            "categories": categories,
            "expenses": monthly_expenses,
            "budget_status": self._get_budget_status(month)
        }
    
    def set_budget(self, month: str, category: str, limit: Decimal) -> None:
        """Set budget for a category in a specific month."""
        if "budgets" not in self.config:
            self.config["budgets"] = {}
        
        if month not in self.config["budgets"]:
            self.config["budgets"][month] = {}
        
        self.config["budgets"][month][category] = str(limit)
        self.save_config()
    
    def _get_budget_status(self, month: str) -> Dict:
        """Get budget status for a month."""
        if "budgets" not in self.config or month not in self.config["budgets"]:
            return {}
        
        monthly_expenses = self.get_monthly_report(month)
        budget_status = {}
        
        for category, limit_str in self.config["budgets"][month].items():
            limit = Decimal(limit_str)
            spent = monthly_expenses["categories"].get(category, Decimal("0"))
            remaining = limit - spent
            percentage = (spent / limit * 100) if limit > 0 else 0
            
            budget_status[category] = {
                "limit": limit,
                "spent": spent,
                "remaining": remaining,
                "percentage": float(percentage)
            }
        
        return budget_status
    
    def _check_budget_warning(self, expense: Expense) -> None:
        """Check if expense exceeds budget and show warning."""
        month = expense.date[:7]  # YYYY-MM
        if "budgets" not in self.config or month not in self.config["budgets"]:
            return
        
        if expense.category in self.config["budgets"][month]:
            limit = Decimal(self.config["budgets"][month][expense.category])
            month_total = sum(e.amount for e in self.expenses if e.date.startswith(month) and e.category == expense.category)
            
            if month_total > limit:
                if RICH_AVAILABLE:
                    self.console.print(f"⚠️  Budget exceeded for {expense.category}! Spent: {self.config['currency']}{month_total}, Budget: {self.config['currency']}{limit}", style="bold red")
                else:
                    print(f"⚠️  Budget exceeded for {expense.category}! Spent: {self.config['currency']}{month_total}, Budget: {self.config['currency']}{limit}")
    
    def get_category_suggestions(self) -> List[str]:
        """Get category suggestions based on past entries and config."""
        used_categories = set(e.category for e in self.expenses)
        config_categories = set(self.config.get("categories", DEFAULT_CATEGORIES))
        return sorted(list(used_categories.union(config_categories)))
    
    def export_to_csv(self, filepath: str, expenses: List[Expense] = None) -> bool:
        """Export expenses to a CSV file."""
        if expenses is None:
            expenses = self.expenses
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
                writer.writeheader()
                for expense in expenses:
                    writer.writerow(expense.to_dict())
            return True
        except Exception:
            return False
