from expense_manager import *

def show_menu():
    print("\n== Personal Expense Tracker ==")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Monthly Report")
    print("5. Exit")

while True:
    show_menu()
    choice = input("Enter your choice (1-5): ")
    
    if choice == '1':
        add_expense()
    elif choice == '2':
        view_expenses()
    elif choice == '3':
        delete_expense()
    elif choice == '4':
        monthly_report()
    elif choice == '5':
        print("Exiting...")
        break
    else:
        print("Invalid input, try again.")

