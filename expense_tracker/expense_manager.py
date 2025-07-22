import csv
from datetime import datetime

FILENAME = "expenses.csv"

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (food, travel, bills, etc.): ")
    amount = float(input("Enter amount: "))

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])
    
    print("✅ Expense added!")

def view_expenses():
    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            print("\nDate\t\tCategory\tAmount")
            print("-" * 40)
            for row in reader:
                print(f"{row[0]}\t{row[1]}\t\t{row[2]}")
    except FileNotFoundError:
        print("No expenses found.")

def delete_expense():
    view_expenses()
    target_date = input("Enter the date of the expense to delete: ")
    target_category = input("Enter the category: ")

    rows = []
    deleted = False
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == target_date and row[1] == target_category:
                deleted = True
                continue
            rows.append(row)

    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    if deleted:
        print("🗑️ Expense deleted.")
    else:
        print("Expense not found.")

def monthly_report():
    month = input("Enter month (YYYY-MM): ")
    total = 0
    categories = {}

    try:
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].startswith(month):
                    amount = float(row[2])
                    total += amount
                    cat = row[1]
                    categories[cat] = categories.get(cat, 0) + amount
    except FileNotFoundError:
        print("No data found.")
        return

    print(f"\n📆 Report for {month}")
    print(f"Total Spent: Rs. {total:.2f}")
    print("Category-wise breakdown:")
    for cat, amt in categories.items():
        print(f"  {cat}: Rs. {amt:.2f}")

