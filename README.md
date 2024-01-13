

# Expense Tracker Application Documentation

## Overview

The Expense Tracker application is a simple GUI-based tool built using the Tkinter library in Python. It allows users to track their expenses and income, view records, apply date filters, generate an expense analysis report, export data to a CSV file, and set a monthly budget.

## Key Components

### 1. Data Management

The application uses a JSON file ('expense_data.json') to persistently store user data. If the file exists, it loads the data into a defaultdict. If not, it creates an empty defaultdict.

```python
try:
    with open('expense_data.json', 'r') as file:
        data = defaultdict(list, json.load(file))
except FileNotFoundError:
    data = defaultdict(list)
```

### 2. User Input and Submission

Users can input details such as amount, category, item name, and date. The 'Submit' button triggers the submission process, validating the input and updating the data accordingly. Invalid input prompts appropriate error messages.

```python
def submit():
    # Input validation
    # ...

    # Data update
    if category.lower() == 'income':
        data['Income'].append({'Amount': amount, 'Item Name': item_name, 'Date': date})
    else:
        data[category].append({'Amount': amount, 'Item Name': item_name, 'Date': date})

    save_data_to_file()
    # ...
```

### 3. Data Persistence

The application saves data to the JSON file after each update to ensure persistence across sessions.

```python
def save_data_to_file():
    with open('expense_data.json', 'w') as file:
        json.dump(data, file)
```

### 4. Balance and Monthly Summary Calculation

Functions `calculate_balance` and `calculate_monthly_summary` calculate and display the user's balance and monthly expenses, respectively.

```python
def calculate_balance():
    total_income = sum(float(expense['Amount']) for expense in data.get('Income', []))
    total_expenses = sum(float(expense['Amount']) for category, expenses in data.items() if category != 'Income' for expense in expenses)
    balance_var.set(f'Balance: Rs.{total_income - total_expenses:.2f}')

def calculate_monthly_summary():
    current_month = datetime.now().strftime('%B')
    monthly_expenses = sum(float(expense['Amount']) for category, expenses in data.items() if category != 'Income' for expense in expenses
                           if datetime.strptime(expense['Date'], '%d/%m/%Y').strftime('%B') == current_month)
    monthly_summary_var.set(f'Monthly Expenses ({current_month}): Rs.{monthly_expenses:.2f}')
```

### 5. Record Display

Records can be viewed in a new window, and a treeview displays them in a tabular format.

```python
def display_records(records):
    records_window = tk.Toplevel(root)
    # ...

    tree = ttk.Treeview(records_window)
    # ...

    for i, record in enumerate(records, 1):
        tree.insert('', i, text=str(i), values=(record['Category'], record['Amount'], record['Item Name'], record['Date']))

    tree.pack(expand=True, fill='both')
```

### 6. Chart Display

A Pie Chart is generated to visualize expense distribution across different categories.

```python
def display_chart():
    categories = []
    amounts = []

    for category, expenses in data.items():
        total_amount = sum(float(expense['Amount']) for expense in expenses)
        categories.append(category)
        amounts.append(total_amount)

    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    chart_window = tk.Toplevel(root)
    # ...
```

### 7. Exporting Data

The application allows users to export their data to a CSV file.

```python
def export_data():
    # ...

    export_file_path = 'expense_data_export.csv'
    with open(export_file_path, 'w', newline='') as csvfile:
        # ...

    success_message = f'Data exported successfully. CSV file saved at:\n{os.path.abspath(export_file_path)}'
    messagebox.showinfo('Success', success_message)
```

### 8. Expense Analysis Report

Users can generate an expense analysis report, which includes total expenses and average expenses per category.

```python
def create_expense_analysis_report():
    total_expenses = sum(float(expense['Amount']) for category, expenses in data.items() if category != 'Income' for expense in expenses)
    average_expenses_per_category = {category: sum(float(expense['Amount']) for expense in expenses) / len(expenses) for category, expenses in data.items() if category != 'Income'}

    report = f"Expense Analysis Report\n\n"
    report += f"Total Expenses: Rs.{total_expenses:.2f}\n\n"
    report += "Average Expenses per Category:\n"
    for category, average_expense in average_expenses_per_category.items():
        report += f"{category}: Rs.{average_expense:.2f}\n"

    report_file_path = 'expense_analysis_report.txt'
    with open(report_file_path, 'w') as report_file:
        report_file.write(report)

    success_message = f"Expense analysis report generated successfully. Report saved at:\n{os.path.abspath(report_file_path)}"
    messagebox.showinfo('Success', success_message)
```

### 9. GUI Layout

The Tkinter GUI is designed with various input fields, buttons, and labels for a user-friendly interface.

```python
# ... GUI layout code ...
```

### 10. Monthly Budget

Users can set a monthly budget, and the application displays it.

```python
def show_budget_window():
    # ...



++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# Expense Tracker Project Guide

The Expense Tracker is a Python-based application that helps you manage your income and expenses. This guide will walk you through the features and provide step-by-step instructions on how to use the project.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Submitting Expenses](#submitting-expenses)
3. [Viewing Records](#viewing-records)
4. [Filtering Records by Date](#filtering-records-by-date)
5. [Generating Reports](#generating-reports)
6. [Exporting Data](#exporting-data)
7. [Setting Monthly Budget](#setting-monthly-budget)
8. [Deleting All Records](#deleting-all-records)

## 1. Getting Started<a name="getting-started"></a>

### Prerequisites:
- Python installed on your machine.
- Required libraries: `tkinter`, `matplotlib`. You can install them using `pip install tk matplotlib`.

### Running the Application:
1. Download the project files to your local machine.
2. Open a terminal or command prompt.
3. Navigate to the project directory.
4. Run the command: `python expense_tracker.py`

## 2. Submitting Expenses<a name="submitting-expenses"></a>

1. Launch the Expense Tracker application.
2. Enter the expense details in the provided fields:
    - **Amount:** The numerical value of the expense.
    - **Category:** Specify whether it's an income or an expense.
    - **Item Name:** A brief description of the expense.
    - **Date:** The date of the expense in DD/MM/YYYY format.
3. Click the "Submit" button to add the entry.

**Note:** All fields are required. Make sure to enter valid information.

## 3. Viewing Records<a name="viewing-records"></a>

1. After adding expenses, click the "View Records" button.
2. A new window will open, displaying a table with recorded expenses and income.
3. You can see the category, amount, item name, and date for each entry.

## 4. Filtering Records by Date<a name="filtering-records-by-date"></a>

1. Click the "Filter by Date" button on the main window.
2. In the new window, enter the start and end dates in DD/MM/YYYY format.
3. Click "Apply Filter" to display records within the specified date range.

## 5. Generating Reports<a name="generating-reports"></a>

1. Click the "Generate Expense Analysis Report" button.
2. The application will create a report with total expenses and average expenses per category.
3. The report will be saved as 'expense_analysis_report.txt' in the project directory.

## 6. Exporting Data<a name="exporting-data"></a>

1. Click the "Export Data" button to export your expenses to a CSV file.
2. The CSV file ('expense_data_export.csv') will be saved in the project directory.

## 7. Setting Monthly Budget<a name="setting-monthly-budget"></a>

1. Click the "Set Monthly Budget" button.
2. Enter the desired monthly budget in the popup window.
3. Click "Set Budget" to confirm. The monthly budget will be displayed on the main window.

## 8. Deleting All Records<a name="deleting-all-records"></a>

1. Click the "Delete All Records" button.
2. A confirmation prompt will appear; click "Yes" to delete all records.
3. A success message will be displayed, and the records will be cleared.

**Note:** Deleting records is irreversible. Be cautious before proceeding.

Now you're ready to efficiently manage your expenses using the Expense Tracker! Explore the various features and use them to gain insights into your financial activities.
def set_monthly_budget(budget_amount):
    # ...
```

## Conclusion

This Expense Tracker application provides a comprehensive solution for users to manage their finances efficiently. It combines data persistence, input validation, data visualization, and reporting features to deliver a robust expense tracking experience.
