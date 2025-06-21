Expense Tracker
Overview
This Expense Tracker is a Python application that helps users manage their personal finances by tracking expenses across different categories. It provides visual reports, spending analysis, and flexible filtering options to help users understand their spending habits.

Features
Total Spending Overview: Shows total expenses, highest expense, and lowest expense

Category Analysis: Breaks down spending by category with percentages

Visual Reports: Generates pie charts of expense distribution

Flexible Filtering: Filter expenses by date range or specific month

Expense Management: Add new expenses with flexible date formats

Data Export: Export category analysis to CSV

Case-Insensitive Categories: Smartly groups similar categories (e.g., "food" and "Food")


How to Run
Prerequisites
Python 3.6 or higher

Required libraries: pandas, numpy, matplotlib

Installation
Clone the repository:

bash
git clone https://github.com/incessant47/ExpenseTracker
cd expense-tracker
Install required packages:

bash
pip install pandas numpy matplotlib
Run the application:

bash
python expense_tracker.py
First Run Experience
When you first run the application:

It will scan for existing CSV files in the directory

You can select an existing file or use the default 'expenses.csv'

If no file exists, it will create a new one automatically

Usage Examples
Main Menu
text
Welcome to Expense Tracker! (Data file: expenses.csv)

===== EXPENSE TRACKER MENU =====
1. Spending Summary
2. Category Analysis
3. Spending Chart
4. Filter Expenses
5. Add Expense
6. Export Report
7. Exit
Choose an option (1-7): 
Adding an Expense
text
Enter date (DD-MM-YYYY): 15-06-2025
Enter category: Food
Enter amount: 25.50
Enter description: Lunch at Cafe
Expense added: 15-06-2025, Food, $25.50
Save to file now? (y/n): y
Expense securely saved!
Spending Summary
text
===== SPENDING SUMMARY =====
Total Expenses: $5400.00

Most Expensive Item:
  Date: 12-06-2025
  Category: Rent
  Amount: $5000.00
  Description: June Rent

Least Expensive Item:
  Date: 11-06-2025
  Category: Transport
  Amount: $50.00
  Description: Rickshaw fare
========================================
Category Analysis
text
===== CATEGORY ANALYSIS =====
           Total Amount  Transaction Count  Percentage (%)
Rent            5000.00                  1           92.59
Food             339.00                  2            6.28
Utilities        200.00                  1            3.70
Transport         50.00                  1            0.93
========================================
File Structure
text
ExpenseTracker/
├── expense_tracker.py      # Main application code
├── expenses.csv            # Sample expense data file
├── summary_report.csv      # Generated category analysis report
└── README.md               # This documentation file

Included Features
Input sanitization

Data size limits to prevent resource exhaustion

Secure file permissions

Case-insensitive category normalization

Customization
You can adjust these parameters in the code:

MAX_EXPENSE_AMOUNT: Maximum allowed expense amount (default: 1,000,000)

MAX_DESCRIPTION_LENGTH: Max characters for descriptions (default: 100)

MAX_EXPENSE_RECORDS: Max records to prevent memory issues (default: 10,000)

PIE_CHART_THRESHOLD: Minimum percentage to show separately in pie chart (default: 3%)

Troubleshooting
If you encounter date format errors, use DD-MM-YYYY format

Ensure you have write permissions in the application directory

For large datasets, consider increasing MAX_EXPENSE_RECORDS

Check logs for detailed error information
