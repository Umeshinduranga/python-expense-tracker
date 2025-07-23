from expense_manager import *

def show_menu():
    print("\n== Personal Expense Tracker ==")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Expenses by Category")
    print("4. Delete Expense")
    print("5. Monthly Report")
    print("6. Exit")

while True:
    show_menu()
    choice = input("Enter your choice (1-6): ")
    
    if choice == '1':
        add_expense()
    elif choice == '2':
        view_expenses()
    elif choice == '3':
        view_by_category()
    elif choice == '4':
        delete_expense()
    elif choice == '5':
        monthly_report()
    elif choice == '6':
        print("Exiting...")
        break
    else:
        print("Invalid input, please choose between 1-6.")
