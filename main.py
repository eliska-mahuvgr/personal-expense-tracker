"""
Personal Expense Tracker
A beginner-friendly command-line app that stores expenses and budgets in JSON files.
Run: python main.py
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path("data")
EXPENSES_FILE = DATA_DIR / "expenses.json"
BUDGETS_FILE = DATA_DIR / "budgets.json"

CATEGORIES = [
    "Food", "Transport", "Shopping", "Education",
    "Bills", "Health", "Entertainment", "Other"
]


def load_json(file_path, default):
    """Read JSON data. Return a default value if the file does not exist."""
    if not file_path.exists():
        return default
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print(f"Warning: Could not read {file_path}. Starting with empty data.")
        return default


def save_json(file_path, data):
    """Save Python data as readable JSON."""
    DATA_DIR.mkdir(exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_expenses():
    return load_json(EXPENSES_FILE, [])


def save_expenses(expenses):
    save_json(EXPENSES_FILE, expenses)


def load_budgets():
    return load_json(BUDGETS_FILE, {})


def save_budgets(budgets):
    save_json(BUDGETS_FILE, budgets)


def ask_amount():
    """Keep asking until the user enters a positive number."""
    while True:
        try:
            amount = float(input("Amount (₹): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number, for example 250 or 99.50.")


def ask_date():
    """Accept YYYY-MM-DD or use today's date when left blank."""
    while True:
        value = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
        if not value:
            return datetime.today().strftime("%Y-%m-%d")
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use the format YYYY-MM-DD.")


def choose_category():
    print("\nCategories:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        choice = input("Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Please choose a valid category number.")


def add_expense(expenses):
    print("\n--- Add Expense ---")
    title = input("What did you spend on? ").strip()
    while not title:
        print("Description cannot be empty.")
        title = input("What did you spend on? ").strip()

    amount = ask_amount()
    category = choose_category()
    date = ask_date()

    expense = {
        "id": max([item.get("id", 0) for item in expenses], default=0) + 1,
        "title": title,
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense saved successfully!")


def list_expenses(expenses):
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'ID':<5}{'Date':<13}{'Description':<24}{'Category':<18}{'Amount (₹)':>12}")
    print("-" * 72)
    for item in sorted(expenses, key=lambda x: (x.get("date", ""), x.get("id", 0)), reverse=True):
        print(
            f"{item['id']:<5}{item['date']:<13}{item['title'][:22]:<24}"
            f"{item['category']:<18}{item['amount']:>12.2f}"
        )
    total = sum(item["amount"] for item in expenses)
    print("-" * 72)
    print(f"Total spent: ₹{total:.2f}")


def delete_expense(expenses):
    print("\n--- Delete Expense ---")
    if not expenses:
        print("There are no expenses to delete.")
        return

    list_expenses(expenses)
    value = input("\nEnter the ID to delete (or press Enter to cancel): ").strip()
    if not value:
        print("Delete cancelled.")
        return
    if not value.isdigit():
        print("Please enter a valid numeric ID.")
        return

    expense_id = int(value)
    for item in expenses:
        if item["id"] == expense_id:
            confirm = input(f"Delete '{item['title']}' for ₹{item['amount']:.2f}? (y/n): ").lower()
            if confirm == "y":
                expenses.remove(item)
                save_expenses(expenses)
                print("Expense deleted.")
            else:
                print("Delete cancelled.")
            return
    print("No expense found with that ID.")


def ask_month():
    while True:
        month = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
            return month
        except ValueError:
            print("Invalid month. Example: 2026-11")


def monthly_summary(expenses):
    print("\n--- Monthly Summary ---")
    month = ask_month()
    selected = [e for e in expenses if e["date"].startswith(month)]
    if not selected:
        print(f"No expenses found for {month}.")
        return

    total = sum(e["amount"] for e in selected)
    by_category = defaultdict(float)
    for item in selected:
        by_category[item["category"]] += item["amount"]

    print(f"\nSummary for {month}")
    print(f"Number of expenses: {len(selected)}")
    print(f"Total spent: ₹{total:.2f}")
    print("\nSpending by category:")
    for category, amount in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total) * 100 if total else 0
        print(f"- {category:<16} ₹{amount:>10.2f} ({percentage:.1f}%)")

    budgets = load_budgets()
    budget = budgets.get(month)
    if budget is not None:
        remaining = budget - total
        print(f"\nMonthly budget: ₹{budget:.2f}")
        print(f"Remaining: ₹{remaining:.2f}")
        if remaining < 0:
            print("Budget exceeded!")
        else:
            print("You are within your budget.")


def set_monthly_budget():
    print("\n--- Set Monthly Budget ---")
    month = ask_month()
    budget = ask_amount()
    budgets = load_budgets()
    budgets[month] = budget
    save_budgets(budgets)
    print(f"Budget for {month} saved: ₹{budget:.2f}")


def export_csv(expenses):
    print("\n--- Export Expenses to CSV ---")
    if not expenses:
        print("No expenses to export.")
        return

    export_path = Path("expenses_export.csv")
    with export_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "date", "title", "category", "amount"])
        writer.writeheader()
        for item in expenses:
            writer.writerow(item)

    print(f"Export complete: {export_path.resolve()}")


def show_menu():
    print("\n" + "=" * 38)
    print("       PERSONAL EXPENSE TRACKER")
    print("=" * 38)
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Delete an expense")
    print("4. Monthly summary")
    print("5. Set monthly budget")
    print("6. Export expenses to CSV")
    print("7. Exit")


def main():
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            monthly_summary(expenses)
        elif choice == "5":
            set_monthly_budget()
        elif choice == "6":
            export_csv(expenses)
        elif choice == "7":
            print("Thank you for using Personal Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
