import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
from datetime import datetime
import json
import csv
import os
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar

# Load existing data from the file
try:
    with open('expense_data.json', 'r') as file:
        data = defaultdict(list, json.load(file))
except FileNotFoundError:
    # If the file doesn't exist yet, create an empty data dictionary
    data = defaultdict(list)

def submit():
    amount = entry_amount.get()
    category = entry_category.get()
    item_name = entry_item_name.get()
    date = entry_date.get()

    if not amount or not category or not item_name or not date:
        messagebox.showerror('Error', 'All fields are required.')
        return

    # Validate amount input
    try:
        # Check if the amount contains only numbers and a decimal point
        float_amount = float(amount)
    except ValueError:
        messagebox.showerror('Error', 'Invalid amount. Please enter a valid number.')
        return

    # Validate date format
    try:
        datetime.strptime(date, '%d/%m/%Y')
    except ValueError:
        messagebox.showerror('Error', 'Incorrect date format. Please use DD/MM/YYYY.')
        return

    # Check if the category is provided
    if not category:
        messagebox.showerror('Error', 'Expense category is required.')
        return

    # Check if the entry is for income or expense
    if category.lower() == 'income':
        data['Income'].append({'Amount': amount, 'Item Name': item_name, 'Date': date})
    else:
        data[category].append({'Amount': amount, 'Item Name': item_name, 'Date': date})

    save_data_to_file()  # Save the data to the file
    entry_amount.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_item_name.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    messagebox.showinfo('Success', 'Entry added successfully.')
    calculate_balance()
    calculate_monthly_summary()  # Update monthly summary

def save_data_to_file():
    # Save the data to the file
    with open('expense_data.json', 'w') as file:
        json.dump(data, file)

def calculate_balance():
    # Calculate total income and expenses
    total_income = sum(float(expense['Amount']) for expense in data.get('Income', []))
    total_expenses = sum(float(expense['Amount']) for category, expenses in data.items() if category != 'Income' for expense in expenses)

    # Display the balance
    balance_var.set(f'Balance: Rs.{total_income - total_expenses:.2f}')

def calculate_monthly_summary():
    # Calculate total expenses for the current month
    current_month = datetime.now().strftime('%B')  # Get the full name of the current month
    monthly_expenses = sum(float(expense['Amount']) for category, expenses in data.items() if category != 'Income' for expense in expenses
                           if datetime.strptime(expense['Date'], '%d/%m/%Y').strftime('%B') == current_month)

    # Display the monthly summary
    monthly_summary_var.set(f'Monthly Expenses ({current_month}): Rs.{monthly_expenses:.2f}')

def filter_records_by_date(start_date, end_date):
    filtered_records = [record for record in get_all_records() if start_date <= record['Date'] <= end_date]
    display_records(filtered_records)

def show_date_filter():
    date_filter_window = tk.Toplevel(root)
    date_filter_window.title('Filter by Date')

    label_start_date = tk.Label(date_filter_window, text='Start Date (DD/MM/YYYY):')
    label_start_date.grid(row=0, column=0, padx=10, pady=10)
    entry_start_date = tk.Entry(date_filter_window)
    entry_start_date.grid(row=0, column=1, padx=10, pady=10)

    label_end_date = tk.Label(date_filter_window, text='End Date (DD/MM/YYYY):')
    label_end_date.grid(row=1, column=0, padx=10, pady=10)
    entry_end_date = tk.Entry(date_filter_window)
    entry_end_date.grid(row=1, column=1, padx=10, pady=10)

    apply_filter_button = tk.Button(date_filter_window, text='Apply Filter', command=lambda: filter_records_by_date(entry_start_date.get(), entry_end_date.get()))
    apply_filter_button.grid(row=2, column=0, columnspan=2, pady=10)

def view_records():
    records = get_all_records()
    display_records(records)
    display_chart()
    calculate_balance()

def get_all_records():
    all_records = []
    for category, expenses in data.items():
        for expense in expenses:
            record = {'Category': category, 'Amount': float(expense['Amount']), 'Item Name': expense['Item Name'], 'Date': expense['Date']}
            all_records.append(record)
    return all_records

def display_records(records):
    # Create a new window to display records
    records_window = tk.Toplevel(root)
    records_window.title('Records')

    # Create a treeview to display records in tabular format
    tree = ttk.Treeview(records_window)
    tree['columns'] = ('Category', 'Amount', 'Item Name', 'Date')
    tree.heading('#0', text='ID')
    tree.heading('Category', text='Category')
    tree.heading('Amount', text='Amount')
    tree.heading('Item Name', text='Item Name')
    tree.heading('Date', text='Date')

    for i, record in enumerate(records, 1):
        tree.insert('', i, text=str(i), values=(record['Category'], record['Amount'], record['Item Name'], record['Date']))

    tree.pack(expand=True, fill='both')

def display_chart():
    # Create a Pie Chart to visualize the distribution of expenses across different categories
    categories = []
    amounts = []

    for category, expenses in data.items():
        total_amount = sum(float(expense['Amount']) for expense in expenses)
        categories.append(category)
        amounts.append(total_amount)

    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.

    # Display the chart in the Tkinter window
    chart_window = tk.Toplevel(root)
    chart_window.title('Distribution Chart')
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

def delete_all_records():
    confirmed = messagebox.askyesno('Delete All Records', 'Are you sure you want to delete all records?')
    if confirmed:
        data.clear()
        save_data_to_file()
        messagebox.showinfo('Success', 'All records deleted successfully.')
        # You might want to update the UI or take any other relevant action after deletion.

def export_data():
    try:
        export_file_path = 'expense_data_export.csv'
        with open(export_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Category', 'Amount', 'Item Name', 'Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for category, expenses in data.items():
                for expense in expenses:
                    writer.writerow({
                        'Category': category,
                        'Amount': expense['Amount'],
                        'Item Name': expense['Item Name'],
                        'Date': expense['Date']
                    })

        success_message = f'Data exported successfully. CSV file saved at:\n{os.path.abspath(export_file_path)}'
        messagebox.showinfo('Success', success_message)
    except Exception as e:
        messagebox.showerror('Error', f'Error during export: {str(e)}')

def create_expense_analysis_report():
    total_expenses = sum(float(expense['Amount']) for category, expenses in data.items() if category != 'Income' for expense in expenses)
    average_expenses_per_category = {category: sum(float(expense['Amount']) for expense in expenses) / len(expenses) for category, expenses in data.items() if category != 'Income'}

    # Create a report
    report = f"Expense Analysis Report\n\n"
    report += f"Total Expenses: Rs.{total_expenses:.2f}\n\n"
    report += "Average Expenses per Category:\n"
    for category, average_expense in average_expenses_per_category.items():
        report += f"{category}: Rs.{average_expense:.2f}\n"
        
    # Save the report to a file
    report_file_path = 'expense_analysis_report.txt'
    with open(report_file_path, 'w') as report_file:
        report_file.write(report)

    # Show success message
    success_message = f"Expense analysis report generated successfully. Report saved at:\n{os.path.abspath(report_file_path)}"
    messagebox.showinfo('Success', success_message)

# Create the main window and its widgets
root = tk.Tk()
root.title('Expense Tracker')

# Create labels and entry widgets for user input
label_amount = tk.Label(root, text='Amount:')
label_amount.grid(row=0, column=0, sticky='W', padx=10, pady=10)
entry_amount = tk.Entry(root)
entry_amount.grid(row=0, column=1, padx=10, pady=10)

label_category = tk.Label(root, text='Category:')
label_category.grid(row=1, column=0, sticky='W', padx=10, pady=10)
entry_category = tk.Entry(root)
entry_category.grid(row=1, column=1, padx=10, pady=10)

label_item_name = tk.Label(root, text='Item Name:')
label_item_name.grid(row=2, column=0, sticky='W', padx=10, pady=10)
entry_item_name = tk.Entry(root)
entry_item_name.grid(row=2, column=1, padx=10, pady=10)

label_date = tk.Label(root, text='Date (DD/MM/YYYY):')
label_date.grid(row=3, column=0, sticky='W', padx=10, pady=10)
entry_date = tk.Entry(root)
entry_date.grid(row=3, column=1, padx=10, pady=10)

# Create the submit button
button_submit = tk.Button(root, text='Submit', command=submit, bg='orange', activebackground='greenyellow')
button_submit.grid(row=4, column=1, padx=10, pady=10)

# Create the button to view records
button_view_records = tk.Button(root, text='View Records', command=view_records, bg='orange', activebackground='greenyellow')
button_view_records.grid(row=5, column=0, padx=10, pady=10)

# Create the button to trigger date filter
button_date_filter = tk.Button(root, text='Filter by Date', command=show_date_filter, bg='orange', activebackground='greenyellow')
button_date_filter.grid(row=5, column=1, padx=10, pady=10)

# Create the button to generate an expense analysis report
button_expense_analysis = tk.Button(root, text='Generate Expense Analysis Report', command=create_expense_analysis_report, bg='orange', activebackground='greenyellow')
button_expense_analysis.grid(row=6, column=0, columnspan=2, pady=10)

# Create the button to export data
button_export_data = tk.Button(root, text='Export Data', command=export_data, bg='orange', activebackground='greenyellow')
button_export_data.grid(row=7, column=0, columnspan=2, pady=10)

# Display balance label
balance_var = tk.StringVar()
label_balance = tk.Label(root, textvariable=balance_var, font=('Helvetica', 12, 'bold'))
label_balance.grid(row=8, column=0, columnspan=2, pady=10)

# Create the button to delete all records
button_delete_all_records = tk.Button(root, text='Delete All Records', command=delete_all_records, bg='red', activebackground='darkred', fg='white')
button_delete_all_records.grid(row=9, column=0, columnspan=2, pady=10)

# Create a StringVar to store and update the monthly summary label
monthly_summary_var = tk.StringVar()

# Create the label for monthly summary
label_monthly_summary = tk.Label(root, textvariable=monthly_summary_var, font=('Helvetica', 12, 'bold'))
label_monthly_summary.grid(row=10, column=0, columnspan=2, pady=10)

def show_budget_window():
    budget_window = tk.Toplevel(root)
    budget_window.title('Set Monthly Budget')

    label_budget = tk.Label(budget_window, text='Set Monthly Budget:')
    label_budget.grid(row=0, column=0, padx=10, pady=10)
    entry_budget = tk.Entry(budget_window)
    entry_budget.grid(row=0, column=1, padx=10, pady=10)

    set_budget_button = tk.Button(budget_window, text='Set Budget', command=lambda: set_monthly_budget(entry_budget.get()))
    set_budget_button.grid(row=1, column=0, columnspan=2, pady=10)

def set_monthly_budget(budget_amount):
    try:
        monthly_budget = float(budget_amount)
        monthly_budget_var.set(f'Monthly Budget: Rs.{monthly_budget:.2f}')
    except ValueError:
        messagebox.showerror('Error', 'Invalid budget amount. Please enter a valid number.')

# Create a StringVar to store and update the monthly budget label
monthly_budget_var = tk.StringVar()

# Create the label for monthly budget
label_monthly_budget = tk.Label(root, textvariable=monthly_budget_var, font=('Helvetica', 12, 'bold'))
label_monthly_budget.grid(row=11, column=0, columnspan=2, pady=10)

# Create the button to set monthly budget
button_set_budget = tk.Button(root, text='Set Monthly Budget', command=show_budget_window, bg='blue', activebackground='darkblue', fg='white')
button_set_budget.grid(row=12, column=0, columnspan=2, pady=10)

# Start the main loop
root.mainloop()
