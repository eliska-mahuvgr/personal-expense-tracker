# Personal Expense Tracker (Python)

A beginner-friendly command-line project for recording everyday expenses, reviewing monthly spending, setting budgets, and exporting data.

## Features

- Add an expense with a description, amount, category, and date
- View all saved expenses and the total spent
- Delete an expense by its ID
- View a monthly summary with category-wise totals and percentages
- Set a monthly budget and see whether spending is within the budget
- Export expense records to a CSV file that can be opened in Excel or Google Sheets
- Automatically save expenses and budgets in local JSON files

## Requirements

- Python 3.8 or newer
- No third-party packages are required

## Run the project

1. Download or clone this repository.
2. Open the project folder in VS Code or a terminal.
3. Run:

   ```bash
   python main.py
   ```

   On some computers, use `python3 main.py`.

4. Follow the menu displayed in the terminal.

## Project structure

```text
personal-expense-tracker/
├── main.py
├── README.md
├── .gitignore
└── data/
    ├── expenses.json
    └── budgets.json
```

The `data` folder and JSON files are created automatically when you save your first expense or budget. They are intentionally excluded from Git so personal spending information is not accidentally published.

## Example workflow

1. Choose `1` to add an expense.
2. Enter a description such as `Lunch`, an amount such as `150`, a category, and a date.
3. Choose `2` to view saved expenses.
4. Choose `5` to set a budget for a month such as `2026-11`.
5. Choose `4` to see that month's spending summary.
6. Choose `6` to create `expenses_export.csv`.

## Concepts practised

Variables, data types, input/output, if/elif/else, loops, functions, lists, dictionaries, exception handling, file handling, JSON, CSV, and dates.

## Important note

This is an educational, local-only project. It is not connected to a bank account and does not process payments. Keep your personal expense data private. The JSON files are stored on your computer.

## Future improvements

- Search and filter expenses by date or category
- Edit an existing expense
- Add recurring expenses
- Create charts with Matplotlib
- Add a graphical interface with Tkinter
- Add a database with SQLite
- Add automated tests
