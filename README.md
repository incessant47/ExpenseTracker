# Expense Tracker Application

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![Pandas](https://img.shields.io/badge/pandas-1.0%2B-orange)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.0%2B-green)

## Overview
A Python application that helps you track and analyze your personal expenses. Features include spending analysis, visual reports, and flexible filtering options to help you understand your spending habits.

## Features
- 📊 **Spending Summary**: Total expenses, highest/lowest expenses
- 🗂️ **Category Analysis**: Breakdown by category with percentages
- 📈 **Visual Reports**: Pie charts of expense distribution
- 🔍 **Flexible Filtering**: By date range or specific month
- ➕ **Expense Management**: Add new expenses with multiple date formats
- 💾 **Data Export**: Save category analysis to CSV
- 🔄 **Smart Categories**: Groups similar categories (e.g., "food" and "Food")

## Installation

1. Clone the repository:
```bash
git clone https://github.com/incessant47/ExpenseTracker.git
cd expense-tracker
```
2. Install required packages:
```bash
pip install pandas numpy matplotlib
```
3. Run the application:
```bash
python expense_tracker.py
```
## Usage
### First Run
1. The program will scan for existing CSV files
2. Select an existing file or press Enter to use default 'expenses.csv'
3. New file will be created automatically if none exists

## Main Menu
```text
===== EXPENSE TRACKER MENU =====
1. Spending Summary
2. Category Analysis
3. Spending Chart
4. Filter Expenses
5. Add Expense
6. Export Report
7. Exit
```
## Adding an Expense
```text
Enter date (DD-MM-YYYY): 15-06-2025
Enter category: Food
Enter amount: 25.50
Enter description: Lunch at Cafe
Expense added: 15-06-2025, Food, $25.50
Save to file now? (y/n): y
Expense securely saved!
```
## Sample Outputs
### Spending Summary:
```text
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
```
### Category Analysis:
```text
===== CATEGORY ANALYSIS =====
           Total Amount  Transaction Count  Percentage (%)
Rent            5000.00                  1           92.59
Food             339.00                  2            6.28
Utilities        200.00                  1            3.70
Transport         50.00                  1            0.93
========================================
```
## File Structure
```text
ExpenseTracker/
├── expense_tracker.py      # Main application
├── expenses.csv            # Sample expense data
├── summary_report.csv      # Generated analysis report
└── README.md               # This documentation
```
## Security Features
```text
🔐 Input sanitization

🛡️ Path validation

⚖️ Data size limits

🔑 Secure file permissions
```
## Customization
Adjust these parameters in the code:
```text
MAX_EXPENSE_AMOUNT = 1000000    # Max expense amount ($1,000,000)
MAX_DESCRIPTION_LENGTH = 100    # Max description characters
MAX_EXPENSE_RECORDS = 10000     # Max records to store
PIE_CHART_THRESHOLD = 3.0       # Min % to show separately in pie chart
```
