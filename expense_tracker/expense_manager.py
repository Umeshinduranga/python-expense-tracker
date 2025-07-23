import csv
from datetime import datetime

FILENAME = "expenses.csv"

def initialize_csv():
    try:
        with open(FILENAME, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount'])
    except FileExistsError:
        pass

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False
        return True
    except ValueError:
        return False

def add_expense():
    initialize_csv()
    while True:
        date = input("Enter date (YYYY-MM-DD): ")
        if not validate_date(date):
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue
        
        category = input("Enter category (food, travel, bills, etc.): ").strip().lower()
        if not category:
            print("Category cannot be empty.")
            continue
            
        amount_str = input("Enter amount: ")
        if not validate_amount(amount_str):
            print("Invalid amount. Please enter a positive number.")
            continue
            
        amount = float(amount_str)
        with open(FILENAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount])
        
        print("✅ Expense added successfully!")
        break

def view_expenses():
    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header row
            expenses = list(reader)
            if not expenses:
                print("No expenses found.")
                return
                
            print("\nDate       | Category     | Amount")
            print("-" * 40)
            for row in expenses:
                print(f"{row[0]} | {row[1]:<12} | Rs. {float(row[2]):>6.2f}")
    except FileNotFoundError:
        print("No expenses found.")

def view_by_category():
    category = input("Enter category to view (food, travel, bills, etc.): ").strip().lower()
    try:
        total = 0
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header row
            print(f"\nExpenses for category: {category}")
            print("\nDate       | Amount")
            print("-" * 25)
            found = False
            for row in reader:
                if row[1].lower() == category:
                    found = True
                    total += float(row[2])
                    print(f"{row[0]} | Rs. {float(row[2]):>6.2f}")
            if not found:
                print(f"No expenses found for category: {category}")
            else:
                print(f"\nTotal for {category}: Rs. {total:.2f}")
    except FileNotFoundError:
        print("No expenses found.")

def delete_expense():
    view_expenses()
    target_date = input("Enter the date of the expense to delete (YYYY-MM-DD): ")
    if not validate_date(target_date):
        print("Invalid date format.")
        return
        
    target_category = input("Enter the category: ").strip().lower()
    if not target_category:
        print("Category cannot be empty.")
        return

    rows = []
    deleted = False
    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Keep header
            rows.append(header)
            for row in reader:
                if row[0] == target_date and row[1].lower() == target_category:
                    deleted = True
                    continue
                rows.append(row)

        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        if deleted:
            print("🗑️ Expense deleted successfully.")
        else:
            print("Expense not found.")
    except FileNotFoundError:
        print("No expenses found.")

def monthly_report():
    while True:
        month = input("Enter month (YYYY-MM): ")
        try:
            datetime.strptime(month, '%Y-%m')
            break
        except ValueError:
            print("Invalid month format. Please use YYYY-MM.")

    total = 0
    categories = {}
    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if row[0].startswith(month):
                    amount = float(row[2])
                    total += amount
                    cat = row[1]
                    categories[cat] = categories.get(cat, 0) + amount
    except FileNotFoundError:
        print("No data found for the specified month.")
        return

    if not categories:
        print(f"No expenses found for {month}.")
        return

    print(f"\n📆 Report for {month}")
    print(f"Total Spent: Rs. {total:.2f}")
    print("Category-wise breakdown:")
    for cat, amt in sorted(categories.items()):
        print(f"  {cat.capitalize():<12}: Rs. {amt:>6.2f}")
