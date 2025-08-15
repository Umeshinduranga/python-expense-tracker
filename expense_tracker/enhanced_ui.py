"""
Enhanced UI Module for Personal Expense Tracker
Provides a beautiful command-line interface with rich formatting.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
import sys

try:
    from rich.console import Console
    from rich.table import Table
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.panel import Panel
    from rich.progress import track
    from rich.text import Text
    from rich import print as rprint
    from rich.layout import Layout
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from expense_manager import ExpenseManager, Expense

class ExpenseUI:
    """Enhanced user interface for the expense tracker."""
    
    def __init__(self):
        self.manager = ExpenseManager()
        self.console = Console() if RICH_AVAILABLE else None
    
    def print_header(self):
        """Print application header."""
        if RICH_AVAILABLE:
            header = Panel.fit(
                "[bold blue]💰 Personal Expense Tracker Pro[/bold blue]\n"
                "[dim]Professional expense management made simple[/dim]",
                style="bright_blue"
            )
            self.console.print(header)
        else:
            print("\n" + "="*50)
            print("💰 Personal Expense Tracker Pro")
            print("Professional expense management made simple")
            print("="*50)
    
    def show_menu(self):
        """Display the main menu."""
        if RICH_AVAILABLE:
            menu = Table(show_header=False, box=None, padding=(0, 2))
            menu.add_column(justify="left")
            menu.add_column(justify="left")
            
            menu.add_row("[bold cyan]1.[/bold cyan]", "Add New Expense")
            menu.add_row("[bold cyan]2.[/bold cyan]", "View All Expenses")
            menu.add_row("[bold cyan]3.[/bold cyan]", "Search & Filter Expenses")
            menu.add_row("[bold cyan]4.[/bold cyan]", "Edit Expense")
            menu.add_row("[bold cyan]5.[/bold cyan]", "Delete Expense")
            menu.add_row("[bold cyan]6.[/bold cyan]", "Monthly Report")
            menu.add_row("[bold cyan]7.[/bold cyan]", "Budget Management")
            menu.add_row("[bold cyan]8.[/bold cyan]", "Export Data")
            menu.add_row("[bold cyan]9.[/bold cyan]", "Settings")
            menu.add_row("[bold red]0.[/bold red]", "Exit")
            
            self.console.print("\n")
            self.console.print(Align.center(menu))
        else:
            print("\n--- Main Menu ---")
            print("1. Add New Expense")
            print("2. View All Expenses")
            print("3. Search & Filter Expenses")
            print("4. Edit Expense")
            print("5. Delete Expense")
            print("6. Monthly Report")
            print("7. Budget Management")
            print("8. Export Data")
            print("9. Settings")
            print("0. Exit")
    
    def get_input(self, prompt: str, default: str = "", choices: List[str] = None) -> str:
        """Get user input with rich formatting if available."""
        if RICH_AVAILABLE:
            if choices:
                return Prompt.ask(prompt, choices=choices, default=default)
            return Prompt.ask(prompt, default=default)
        else:
            if choices:
                prompt += f" ({'/'.join(choices)})"
            if default:
                prompt += f" [default: {default}]"
            return input(f"{prompt}: ").strip() or default
    
    def get_confirmation(self, message: str) -> bool:
        """Get yes/no confirmation from user."""
        if RICH_AVAILABLE:
            return Confirm.ask(message)
        else:
            while True:
                response = input(f"{message} (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    return True
                elif response in ['n', 'no']:
                    return False
                print("Please enter 'y' or 'n'")
    
    def print_success(self, message: str):
        """Print success message."""
        if RICH_AVAILABLE:
            self.console.print(f"✅ {message}", style="bold green")
        else:
            print(f"✅ {message}")
    
    def print_error(self, message: str):
        """Print error message."""
        if RICH_AVAILABLE:
            self.console.print(f"❌ {message}", style="bold red")
        else:
            print(f"❌ {message}")
    
    def print_warning(self, message: str):
        """Print warning message."""
        if RICH_AVAILABLE:
            self.console.print(f"⚠️  {message}", style="bold yellow")
        else:
            print(f"⚠️  {message}")
    
    def display_expenses_table(self, expenses: List[Expense], title: str = "Expenses"):
        """Display expenses in a formatted table."""
        if not expenses:
            self.print_warning("No expenses found.")
            return
        
        if RICH_AVAILABLE:
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("#", style="dim", width=4)
            table.add_column("Date", style="cyan", width=12)
            table.add_column("Category", style="green", width=12)
            table.add_column("Amount", style="yellow", justify="right", width=10)
            table.add_column("Description", style="white", width=30)
            
            currency = self.manager.config.get('currency', 'Rs.')
            
            for i, expense in enumerate(expenses, 1):
                table.add_row(
                    str(i),
                    expense.date,
                    expense.category.title(),
                    f"{currency} {expense.amount:,.2f}",
                    expense.description[:27] + "..." if len(expense.description) > 30 else expense.description
                )
            
            self.console.print(table)
            
            total = sum(expense.amount for expense in expenses)
            self.console.print(f"\n[bold]Total: {currency} {total:,.2f}[/bold]")
        else:
            print(f"\n{title}")
            print("-" * 80)
            print(f"{'#':<4} {'Date':<12} {'Category':<12} {'Amount':<12} {'Description'}")
            print("-" * 80)
            
            currency = self.manager.config.get('currency', 'Rs.')
            total = Decimal("0")
            
            for i, expense in enumerate(expenses, 1):
                total += expense.amount
                desc = expense.description[:25] + "..." if len(expense.description) > 25 else expense.description
                print(f"{i:<4} {expense.date:<12} {expense.category.title():<12} {currency} {expense.amount:>8.2f} {desc}")
            
            print("-" * 80)
            print(f"Total: {currency} {total:,.2f}")
    
    def add_expense(self):
        """Handle adding a new expense."""
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]Add New Expense[/bold blue]")
        else:
            print("\n--- Add New Expense ---")
        
        # Get date
        today = date.today().strftime(self.manager.config['date_format'])
        date_input = self.get_input("Enter date", default=today)
        
        if not self.manager.validate_date(date_input):
            self.print_error("Invalid date format. Please use YYYY-MM-DD.")
            return
        
        # Get category with suggestions
        categories = self.manager.get_category_suggestions()
        if RICH_AVAILABLE:
            self.console.print(f"Available categories: {', '.join(categories)}", style="dim")
        else:
            print(f"Available categories: {', '.join(categories)}")
        
        category = self.get_input("Enter category").lower().strip()
        if not category:
            self.print_error("Category cannot be empty.")
            return
        
        # Get amount
        amount_str = self.get_input("Enter amount")
        if not self.manager.validate_amount(amount_str):
            self.print_error("Invalid amount. Please enter a positive number.")
            return
        
        amount = Decimal(amount_str).quantize(Decimal('0.01'))
        
        # Get description (optional)
        description = self.get_input("Enter description (optional)")
        
        # Add expense
        if self.manager.add_expense(date_input, category, amount, description):
            self.print_success("Expense added successfully!")
        else:
            self.print_error("Failed to add expense.")
    
    def edit_expense(self):
        """Handle editing an existing expense."""
        if not self.manager.expenses:
            self.print_warning("No expenses found to edit.")
            return
        
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]Edit Expense[/bold blue]")
        else:
            print("\n--- Edit Expense ---")
        
        # Show current expenses
        self.display_expenses_table(self.manager.expenses, "Current Expenses")
        
        try:
            if RICH_AVAILABLE:
                index = IntPrompt.ask("Enter expense number to edit", default=1) - 1
            else:
                index = int(input("Enter expense number to edit: ")) - 1
            
            if not (0 <= index < len(self.manager.expenses)):
                self.print_error("Invalid expense number.")
                return
            
            current_expense = self.manager.expenses[index]
            
            # Get new values
            date_input = self.get_input("Enter new date", default=current_expense.date)
            category = self.get_input("Enter new category", default=current_expense.category)
            amount_str = self.get_input("Enter new amount", default=str(current_expense.amount))
            description = self.get_input("Enter new description", default=current_expense.description)
            
            if not self.manager.validate_date(date_input) or not self.manager.validate_amount(amount_str):
                self.print_error("Invalid date or amount format.")
                return
            
            amount = Decimal(amount_str).quantize(Decimal('0.01'))
            
            if self.manager.edit_expense(index, date_input, category, amount, description):
                self.print_success("Expense updated successfully!")
            else:
                self.print_error("Failed to update expense.")
                
        except (ValueError, KeyboardInterrupt):
            self.print_error("Invalid input.")
    
    def search_expenses(self):
        """Handle searching and filtering expenses."""
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]Search & Filter Expenses[/bold blue]")
        else:
            print("\n--- Search & Filter Expenses ---")
        
        # Get search criteria
        keyword = self.get_input("Search keyword (description/category, optional)")
        category = self.get_input("Filter by category (optional)")
        start_date = self.get_input("Start date (YYYY-MM-DD, optional)")
        end_date = self.get_input("End date (YYYY-MM-DD, optional)")
        min_amount = self.get_input("Minimum amount (optional)")
        max_amount = self.get_input("Maximum amount (optional)")
        
        # Perform search
        results = self.manager.search_expenses(keyword, category, start_date, end_date, min_amount, max_amount)
        
        if results:
            self.display_expenses_table(results, f"Search Results ({len(results)} found)")
        else:
            self.print_warning("No expenses found matching your criteria.")
    
    def monthly_report(self):
        """Display monthly report."""
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]Monthly Report[/bold blue]")
        else:
            print("\n--- Monthly Report ---")
        
        current_month = date.today().strftime("%Y-%m")
        month = self.get_input("Enter month (YYYY-MM)", default=current_month)
        
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            self.print_error("Invalid month format. Please use YYYY-MM.")
            return
        
        report = self.manager.get_monthly_report(month)
        
        if not report["expenses"]:
            self.print_warning(f"No expenses found for {month}.")
            return
        
        currency = self.manager.config.get('currency', 'Rs.')
        
        if RICH_AVAILABLE:
            # Summary panel
            summary = f"[bold]Month:[/bold] {month}\n"
            summary += f"[bold]Total Spent:[/bold] {currency} {report['total']:,.2f}\n"
            summary += f"[bold]Number of Expenses:[/bold] {len(report['expenses'])}"
            
            self.console.print(Panel(summary, title="📊 Monthly Summary", style="green"))
            
            # Category breakdown
            if report['categories']:
                table = Table(title="Category Breakdown", show_header=True, header_style="bold cyan")
                table.add_column("Category", style="green")
                table.add_column("Amount", style="yellow", justify="right")
                table.add_column("Percentage", style="blue", justify="right")
                
                for category, amount in sorted(report['categories'].items(), key=lambda x: x[1], reverse=True):
                    percentage = (amount / report['total'] * 100) if report['total'] > 0 else 0
                    table.add_row(
                        category.title(),
                        f"{currency} {amount:,.2f}",
                        f"{percentage:.1f}%"
                    )
                
                self.console.print(table)
            
            # Budget status
            if report['budget_status']:
                budget_table = Table(title="Budget Status", show_header=True, header_style="bold magenta")
                budget_table.add_column("Category", style="green")
                budget_table.add_column("Spent", style="yellow", justify="right")
                budget_table.add_column("Budget", style="blue", justify="right")
                budget_table.add_column("Remaining", style="cyan", justify="right")
                budget_table.add_column("Status", justify="center")
                
                for category, status in report['budget_status'].items():
                    remaining_style = "red" if status['remaining'] < 0 else "green"
                    status_icon = "🔴" if status['remaining'] < 0 else ("🟡" if status['percentage'] > 80 else "🟢")
                    
                    budget_table.add_row(
                        category.title(),
                        f"{currency} {status['spent']:,.2f}",
                        f"{currency} {status['limit']:,.2f}",
                        f"[{remaining_style}]{currency} {status['remaining']:,.2f}[/{remaining_style}]",
                        status_icon
                    )
                
                self.console.print(budget_table)
        else:
            print(f"\n📊 Monthly Report for {month}")
            print(f"Total Spent: {currency} {report['total']:,.2f}")
            print(f"Number of Expenses: {len(report['expenses'])}")
            
            print("\nCategory Breakdown:")
            print("-" * 40)
            for category, amount in sorted(report['categories'].items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / report['total'] * 100) if report['total'] > 0 else 0
                print(f"{category.title():<15}: {currency} {amount:>8.2f} ({percentage:.1f}%)")
    
    def manage_budgets(self):
        """Handle budget management."""
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]Budget Management[/bold blue]")
        else:
            print("\n--- Budget Management ---")
        
        action = self.get_input("Action", choices=["set", "view", "delete"])
        
        if action == "set":
            current_month = date.today().strftime("%Y-%m")
            month = self.get_input("Enter month (YYYY-MM)", default=current_month)
            
            try:
                datetime.strptime(month, "%Y-%m")
            except ValueError:
                self.print_error("Invalid month format.")
                return
            
            categories = self.manager.get_category_suggestions()
            if RICH_AVAILABLE:
                self.console.print(f"Available categories: {', '.join(categories)}", style="dim")
            
            category = self.get_input("Enter category").lower().strip()
            limit_str = self.get_input("Enter budget limit")
            
            try:
                limit = Decimal(limit_str)
                self.manager.set_budget(month, category, limit)
                self.print_success(f"Budget set for {category} in {month}: {self.manager.config['currency']} {limit}")
            except ValueError:
                self.print_error("Invalid budget amount.")
        
        elif action == "view":
            month = self.get_input("Enter month (YYYY-MM)", default=date.today().strftime("%Y-%m"))
            
            try:
                datetime.strptime(month, "%Y-%m")
            except ValueError:
                self.print_error("Invalid month format.")
                return
            
            report = self.manager.get_monthly_report(month)
            if report['budget_status']:
                if RICH_AVAILABLE:
                    self.console.print(f"\n[bold]Budget Status for {month}[/bold]")
                    
                    table = Table(show_header=True, header_style="bold cyan")
                    table.add_column("Category", style="green")
                    table.add_column("Budget", style="blue", justify="right")
                    table.add_column("Spent", style="yellow", justify="right")
                    table.add_column("Remaining", justify="right")
                    table.add_column("Status", justify="center")
                    
                    currency = self.manager.config.get('currency', 'Rs.')
                    
                    for category, status in report['budget_status'].items():
                        remaining_style = "red" if status['remaining'] < 0 else "green"
                        status_icon = "🔴" if status['remaining'] < 0 else ("🟡" if status['percentage'] > 80 else "🟢")
                        
                        table.add_row(
                            category.title(),
                            f"{currency} {status['limit']:,.2f}",
                            f"{currency} {status['spent']:,.2f}",
                            f"[{remaining_style}]{currency} {status['remaining']:,.2f}[/{remaining_style}]",
                            f"{status_icon} {status['percentage']:.0f}%"
                        )
                    
                    self.console.print(table)
                else:
                    print(f"\nBudget Status for {month}")
                    print("-" * 60)
                    currency = self.manager.config.get('currency', 'Rs.')
                    
                    for category, status in report['budget_status'].items():
                        status_text = "OVER" if status['remaining'] < 0 else ("WARNING" if status['percentage'] > 80 else "OK")
                        print(f"{category.title():<12}: Budget {currency}{status['limit']:>8.2f} | Spent {currency}{status['spent']:>8.2f} | {status_text}")
            else:
                self.print_warning(f"No budgets set for {month}.")
        
        elif action == "delete":
            month = self.get_input("Enter month (YYYY-MM)")
            category = self.get_input("Enter category to delete budget").lower().strip()
            
            if ("budgets" in self.manager.config and 
                month in self.manager.config["budgets"] and 
                category in self.manager.config["budgets"][month]):
                
                del self.manager.config["budgets"][month][category]
                if not self.manager.config["budgets"][month]:
                    del self.manager.config["budgets"][month]
                
                self.manager.save_config()
                self.print_success(f"Budget deleted for {category} in {month}")
            else:
                self.print_error("Budget not found.")
    
    def export_data(self):
        """Handle data export."""
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]Export Data[/bold blue]")
        else:
            print("\n--- Export Data ---")
        
        if not self.manager.expenses:
            self.print_warning("No expenses to export.")
            return
        
        export_type = self.get_input("Export type", choices=["all", "filtered", "monthly"])
        filename = self.get_input("Enter filename (without extension)", default=f"expenses_{datetime.now().strftime('%Y%m%d')}")
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        expenses_to_export = []
        
        if export_type == "all":
            expenses_to_export = self.manager.expenses
        elif export_type == "filtered":
            if RICH_AVAILABLE:
                self.console.print("[dim]Enter filter criteria (leave blank to skip):[/dim]")
            else:
                print("Enter filter criteria (leave blank to skip):")
            
            keyword = self.get_input("Keyword")
            category = self.get_input("Category")
            start_date = self.get_input("Start date (YYYY-MM-DD)")
            end_date = self.get_input("End date (YYYY-MM-DD)")
            
            expenses_to_export = self.manager.search_expenses(keyword, category, start_date, end_date)
        elif export_type == "monthly":
            month = self.get_input("Enter month (YYYY-MM)", default=date.today().strftime("%Y-%m"))
            report = self.manager.get_monthly_report(month)
            expenses_to_export = report["expenses"]
        
        if not expenses_to_export:
            self.print_warning("No expenses match the criteria.")
            return
        
        if self.manager.export_to_csv(filename, expenses_to_export):
            self.print_success(f"Data exported to {filename} ({len(expenses_to_export)} expenses)")
        else:
            self.print_error("Failed to export data.")
    
    def settings_menu(self):
        """Handle settings management."""
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]Settings[/bold blue]")
        else:
            print("\n--- Settings ---")
        
        while True:
            if RICH_AVAILABLE:
                self.console.print("\n[dim]Current Settings:[/dim]")
                settings_table = Table(show_header=False, box=None)
                settings_table.add_column("Setting", style="cyan")
                settings_table.add_column("Value", style="yellow")
                
                settings_table.add_row("Currency", self.manager.config.get('currency', 'Rs.'))
                settings_table.add_row("Auto Backup", str(self.manager.config.get('auto_backup', True)))
                settings_table.add_row("Categories", str(len(self.manager.config.get('categories', []))))
                
                self.console.print(settings_table)
                
                menu = Table(show_header=False, box=None)
                menu.add_column(justify="left")
                menu.add_column(justify="left")
                
                menu.add_row("[bold cyan]1.[/bold cyan]", "Change Currency")
                menu.add_row("[bold cyan]2.[/bold cyan]", "Toggle Auto Backup")
                menu.add_row("[bold cyan]3.[/bold cyan]", "Manage Categories")
                menu.add_row("[bold cyan]4.[/bold cyan]", "Create Backup")
                menu.add_row("[bold red]0.[/bold red]", "Back to Main Menu")
                
                self.console.print(menu)
            else:
                print(f"\nCurrent Settings:")
                print(f"Currency: {self.manager.config.get('currency', 'Rs.')}")
                print(f"Auto Backup: {self.manager.config.get('auto_backup', True)}")
                print(f"Categories: {len(self.manager.config.get('categories', []))}")
                print("\n1. Change Currency")
                print("2. Toggle Auto Backup")
                print("3. Manage Categories")
                print("4. Create Backup")
                print("0. Back to Main Menu")
            
            choice = self.get_input("Choose option", choices=["1", "2", "3", "4", "0"])
            
            if choice == "1":
                new_currency = self.get_input("Enter new currency symbol", default=self.manager.config.get('currency', 'Rs.'))
                self.manager.config['currency'] = new_currency
                self.manager.save_config()
                self.print_success(f"Currency changed to {new_currency}")
            
            elif choice == "2":
                current = self.manager.config.get('auto_backup', True)
                self.manager.config['auto_backup'] = not current
                self.manager.save_config()
                status = "enabled" if not current else "disabled"
                self.print_success(f"Auto backup {status}")
            
            elif choice == "3":
                self.manage_categories()
            
            elif choice == "4":
                self.manager.backup_data()
                self.print_success("Manual backup created successfully!")
            
            elif choice == "0":
                break
    
    def manage_categories(self):
        """Handle category management."""
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]Manage Categories[/bold blue]")
        else:
            print("\n--- Manage Categories ---")
        
        current_categories = self.manager.config.get('categories', [])
        
        if RICH_AVAILABLE:
            self.console.print(f"[dim]Current categories: {', '.join(current_categories)}[/dim]")
        else:
            print(f"Current categories: {', '.join(current_categories)}")
        
        action = self.get_input("Action", choices=["add", "remove", "reset"])
        
        if action == "add":
            new_category = self.get_input("Enter new category name").lower().strip()
            if new_category and new_category not in current_categories:
                current_categories.append(new_category)
                self.manager.config['categories'] = sorted(current_categories)
                self.manager.save_config()
                self.print_success(f"Category '{new_category}' added")
            else:
                self.print_error("Category already exists or is empty")
        
        elif action == "remove":
            if not current_categories:
                self.print_warning("No categories to remove")
                return
            
            category = self.get_input(f"Enter category to remove", choices=current_categories)
            if category in current_categories:
                current_categories.remove(category)
                self.manager.config['categories'] = current_categories
                self.manager.save_config()
                self.print_success(f"Category '{category}' removed")
        
        elif action == "reset":
            if self.get_confirmation("Reset categories to default?"):
                from expense_manager import DEFAULT_CATEGORIES
                self.manager.config['categories'] = DEFAULT_CATEGORIES.copy()
                self.manager.save_config()
                self.print_success("Categories reset to default")
    
    def delete_expense(self):
        """Handle deleting an expense."""
        if not self.manager.expenses:
            self.print_warning("No expenses found to delete.")
            return
        
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]Delete Expense[/bold blue]")
        else:
            print("\n--- Delete Expense ---")
        
        self.display_expenses_table(self.manager.expenses, "Current Expenses")
        
        try:
            if RICH_AVAILABLE:
                index = IntPrompt.ask("Enter expense number to delete") - 1
            else:
                index = int(input("Enter expense number to delete: ")) - 1
            
            if not (0 <= index < len(self.manager.expenses)):
                self.print_error("Invalid expense number.")
                return
            
            expense = self.manager.expenses[index]
            currency = self.manager.config.get('currency', 'Rs.')
            
            if self.get_confirmation(f"Delete expense: {expense.date} - {expense.category} - {currency}{expense.amount}?"):
                if self.manager.delete_expense(index):
                    self.print_success("Expense deleted successfully!")
                else:
                    self.print_error("Failed to delete expense.")
        
        except (ValueError, KeyboardInterrupt):
            self.print_error("Invalid input.")
    
    def run(self):
        """Main application loop."""
        if not RICH_AVAILABLE:
            print("Note: Install 'rich' library for enhanced UI experience: pip install rich")
        
        while True:
            try:
                self.print_header()
                self.show_menu()
                
                choice = self.get_input("\nChoose an option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
                
                if choice == "1":
                    self.add_expense()
                elif choice == "2":
                    self.display_expenses_table(self.manager.expenses, "All Expenses")
                elif choice == "3":
                    self.search_expenses()
                elif choice == "4":
                    self.edit_expense()
                elif choice == "5":
                    self.delete_expense()
                elif choice == "6":
                    self.monthly_report()
                elif choice == "7":
                    self.manage_budgets()
                elif choice == "8":
                    self.export_data()
                elif choice == "9":
                    self.settings_menu()
                elif choice == "0":
                    if self.get_confirmation("Are you sure you want to exit?"):
                        if RICH_AVAILABLE:
                            self.console.print("\n[bold green]Thank you for using Personal Expense Tracker Pro![/bold green]")
                        else:
                            print("\nThank you for using Personal Expense Tracker Pro!")
                        break
                
                # Pause before showing menu again
                if RICH_AVAILABLE:
                    Prompt.ask("\nPress Enter to continue", default="")
                else:
                    input("\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                if self.get_confirmation("\nAre you sure you want to exit?"):
                    break
            except Exception as e:
                self.print_error(f"An unexpected error occurred: {str(e)}")
                if RICH_AVAILABLE:
                    Prompt.ask("Press Enter to continue", default="")
                else:
                    input("Press Enter to continue...")

if __name__ == "__main__":
    app = ExpenseUI()
    app.run()
