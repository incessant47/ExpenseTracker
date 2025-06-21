import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import logging
from datetime import datetime
import re
from collections import defaultdict

class ExpenseTracker:
    # Define a safe directory for storing files
    SAFE_DIRECTORY = os.getcwd()

    def __init__(self, filename='expenses.csv'):
        # Initialize the tracker with a filename
        self.fasafe_file_path = self.make_safe_file_path(filename)
        self.setup_logging_system()
        self.logger.info(f"Using data file: {os.path.basename(self.fasafe_file_path)}")
        
        # Load expense data and setup category normalization
        self.expense_data = self.load_expense_data()
        self.category_name_mapping = self.build_category_name_mapping()
        self.normalize_all_categories()

    def setup_logging_system(self):
        # Configure logging for tracking events
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def make_safe_file_path(self, file_path):
        # Ensure filename is safe and has .csv extension
        clean_file_name = os.path.basename(file_path) or 'expenses.csv'
        if not clean_file_name.endswith('.csv'):
            clean_file_name += '.csv'
        return os.path.join(self.SAFE_DIRECTORY, clean_file_name)

    def load_expense_data(self):
        # Load data from CSV file with error handling
        try:
            if not os.path.exists(self.fasafe_file_path):
                self.logger.info("Creating new expense file")
                return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

            # Read CSV file
            expense_dataframe = pd.read_csv(self.fasafe_file_path)
            
            # Convert amounts to numbers
            expense_dataframe['Amount'] = pd.to_numeric(expense_dataframe['Amount'], errors='coerce')
            
            # Parse dates using our flexible parser
            expense_dataframe['Date'] = expense_dataframe['Date'].apply(self.parse_date_input)
            
            # Clean data: remove invalid entries
            expense_dataframe = expense_dataframe.dropna(subset=['Date', 'Amount'])
            expense_dataframe = expense_dataframe[expense_dataframe['Amount'] > 0]
            
            self.logger.info(f"Loaded {len(expense_dataframe)} expense records")
            return expense_dataframe
        except Exception as error:
            self.logger.error(f"Error loading file: {error}")
            return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

    def build_category_name_mapping(self):
        # Create mapping for consistent category naming
        name_mapping = {}
        if not self.expense_data.empty and 'Category' in self.expense_data.columns:
            # Count different name variations
            name_variations = defaultdict(lambda: defaultdict(int))
            for category_name in self.expense_data['Category']:
                if pd.isna(category_name):
                    continue
                    
                clean_name = str(category_name).strip().lower()
                original_name = str(category_name).strip()
                name_variations[clean_name][original_name] += 1
            
            # Use most common variation for each category
            for clean_name, variations in name_variations.items():
                most_common_name = max(variations.items(), key=lambda x: x[1])[0]
                name_mapping[clean_name] = most_common_name
                
        return name_mapping

    def normalize_all_categories(self):
        # Apply consistent naming to all categories
        if not self.expense_data.empty and 'Category' in self.expense_data.columns:
            self.expense_data['Category'] = self.expense_data['Category'].apply(
                lambda category: self.normalize_category_name(category)
            )
            self.logger.info("Standardized category names")

    def normalize_category_name(self, category_name):
        # Convert category name to standardized form
        if pd.isna(category_name):
            return category_name
            
        clean_name = str(category_name).strip()
        lowercase_name = clean_name.lower()
        return self.category_name_mapping.get(lowercase_name, clean_name)

    def save_expense_data(self):
        # Save data to CSV file
        try:
            # Prepare data for saving
            data_to_save = self.expense_data.copy()
            
            # Format dates as DD-MM-YYYY for storage
            data_to_save['Date'] = data_to_save['Date'].apply(
                lambda date: date.strftime('%d-%m-%Y') if isinstance(date, datetime) else date
            )
            
            # Save to CSV
            data_to_save.to_csv(self.fasafe_file_path, index=False)
            self.logger.info(f"Data saved to {os.path.basename(self.fasafe_file_path)}")
            return True
        except Exception as error:
            self.logger.error(f"Error saving file: {error}")
            return False

    def display_spending_summary(self):
        # Show overview of spending
        if self.expense_data.empty:
            self.logger.info("No expenses to display")
            print("\nNo expenses found")
            return

        total_spent = self.expense_data['Amount'].sum()
        highest_expense = self.expense_data.loc[self.expense_data['Amount'].idxmax()]
        lowest_expense = self.expense_data.loc[self.expense_data['Amount'].idxmin()]

        print("\n===== SPENDING SUMMARY =====")
        print(f"Total Expenses: ${total_spent:.2f}")
        
        print("\nMost Expensive Item:")
        print(f"  Date: {highest_expense['Date'].strftime('%d-%m-%Y')}")
        print(f"  Category: {highest_expense['Category']}")
        print(f"  Amount: ${highest_expense['Amount']:.2f}")
        print(f"  Description: {highest_expense['Description']}")
        
        print("\nLeast Expensive Item:")
        print(f"  Date: {lowest_expense['Date'].strftime('%d-%m-%Y')}")
        print(f"  Category: {lowest_expense['Category']}")
        print(f"  Amount: ${lowest_expense['Amount']:.2f}")
        print(f"  Description: {lowest_expense['Description']}")
        print("=" * 40)

    def analyze_categories(self):
        # Analyze spending by category
        if self.expense_data.empty:
            self.logger.info("No expenses to analyze")
            print("\nNo expenses to analyze")
            return pd.DataFrame()

        # Group expenses by category
        grouped_by_category = self.expense_data.groupby('Category')
        category_totals = grouped_by_category['Amount'].sum()
        transaction_counts = grouped_by_category.size()
        overall_spending = category_totals.sum()
        spending_percentages = (category_totals / overall_spending * 100).round(2)

        # Create summary report
        category_report = pd.DataFrame({
            'Total Amount': category_totals,
            'Transaction Count': transaction_counts,
            'Percentage (%)': spending_percentages
        }).sort_values('Total Amount', ascending=False)

        print("\n===== CATEGORY ANALYSIS =====")
        print(category_report.to_string(float_format='%.2f'))
        print("=" * 40)
        return category_report

    def create_category_pie_chart(self):
        # Visualize spending distribution
        if self.expense_data.empty:
            self.logger.info("No data for chart")
            return
            
        category_report = self.analyze_categories()
        if category_report.empty:
            return
            
        # Configure and display pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(category_report['Total Amount'], 
                labels=category_report.index, 
                autopct='%1.1f%%', 
                startangle=90)
        plt.title('Spending by Category')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def filter_expenses(self, start_date=None, end_date=None, target_month=None):
        # Filter expenses by date range or month
        expense_copy = self.expense_data.copy()
        
        if target_month:
            try:
                # Parse month input
                month_date = self.parse_date_input(target_month)
                if not month_date:
                    print("Invalid month format. Use formats like YYYY-MM or MM-YYYY")
                    return pd.DataFrame()
                    
                # Convert to monthly period
                month_period = month_date.to_period('M')
                return expense_copy[expense_copy['Date'].dt.to_period('M') == month_period]
            except Exception as error:
                self.logger.error(f"Month filter error: {error}")
                return pd.DataFrame()
                
        if start_date or end_date:
            # Parse date inputs
            parsed_start = self.parse_date_input(start_date) if start_date else None
            parsed_end = self.parse_date_input(end_date) if end_date else None
            
            # Validate dates
            if start_date and not parsed_start:
                print(f"Invalid start date: {start_date}")
                return pd.DataFrame()
            if end_date and not parsed_end:
                print(f"Invalid end date: {end_date}")
                return pd.DataFrame()
                
            try:
                # Apply date range filter
                if parsed_start:
                    expense_copy = expense_copy[expense_copy['Date'] >= parsed_start]
                if parsed_end:
                    expense_copy = expense_copy[expense_copy['Date'] <= parsed_end]
                return expense_copy
            except Exception as error:
                self.logger.error(f"Date range filter error: {error}")
                return pd.DataFrame()
                
        return expense_copy

    def parse_date_input(self, date_input):
        """Convert various date formats to datetime objects"""
        # Handle existing datetime objects or empty inputs
        if isinstance(date_input, datetime) or date_input is None:
            return date_input
            
        # Check for empty values
        if not date_input or str(date_input).strip() == "":
            return None
            
        # Handle missing/NaN values
        if pd.isna(date_input):
            return None
            
        # Clean input by removing non-date characters
        clean_input = re.sub(r'[^0-9/.-]', '', str(date_input))
        
        # Supported date formats
        date_formats = [
            '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',  # Day-Month-Year
            '%m-%d-%Y', '%m/%d/%Y', '%m.%d.%Y',  # Month-Day-Year
            '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d',  # Year-Month-Day
            '%m-%Y', '%m/%Y', '%m.%Y',           # Month-Year
            '%Y-%m', '%Y/%m', '%Y.%m'            # Year-Month
        ]
        
        # Try each format until successful
        for fmt in date_formats:
            try:
                date_object = datetime.strptime(clean_input, fmt)
                # Handle month-only formats
                if fmt in ['%m-%Y', '%m/%Y', '%m.%Y', '%Y-%m', '%Y/%m', '%Y.%m']:
                    return date_object.replace(day=1)
                return date_object
            except ValueError:
                continue
        
        self.logger.warning(f"Unrecognized date format: {date_input}")
        return None

    def add_new_expense(self):
        # Get expense details from user
        input_date = input("Enter date (DD-MM-YYYY, MM/DD/YYYY, or YYYY.MM.DD): ")
        input_category = input("Enter category: ").strip()
        input_amount = input("Enter amount: ")
        input_description = input("Enter description: ").strip()

        # Parse and validate date
        expense_date = self.parse_date_input(input_date)
        if not expense_date:
            print("Please use a valid date format like DD-MM-YYYY")
            return

        # Confirm future dates
        if expense_date > datetime.now():
            confirm = input("Future date detected. Continue? (y/n): ").lower()
            if confirm != 'y':
                return

        # Validate amount
        try:
            expense_amount = float(input_amount)
            if expense_amount <= 0:
                print("Amount must be positive")
                return
        except ValueError:
            print("Please enter a valid number")
            return

        # Normalize category name
        normalized_category = self.normalize_category_name(input_category)
        
        # Update mapping for new categories
        category_key = input_category.strip().lower()
        if category_key not in self.category_name_mapping:
            self.category_name_mapping[category_key] = normalized_category
        
        # Create new expense record
        new_record = pd.DataFrame({
            'Date': [expense_date],
            'Category': [normalized_category],
            'Amount': [expense_amount],
            'Description': [input_description]
        })
        
        # Add to expense data
        self.expense_data = pd.concat([self.expense_data, new_record], ignore_index=True)
        
        print(f"Added: {expense_date.strftime('%d-%m-%Y')}, {normalized_category}, ${expense_amount:.2f}")
        
        # Prompt to save
        save_choice = input("Save to file now? (y/n): ").strip().lower()
        if save_choice == 'y':
            if self.save_expense_data():
                print("Expense saved successfully!")
            else:
                print("Failed to save expense")
        else:
            print("Expense added locally. Save before exiting!")

    def export_analysis_report(self):
        # Export category analysis to CSV
        if self.expense_data.empty:
            print("No data to export")
            return
            
        category_report = self.analyze_categories()
        if category_report.empty:
            return
            
        report_path = os.path.join(self.SAFE_DIRECTORY, 'expense_summary.csv')
        category_report.to_csv(report_path)
        print(f"Report saved to {report_path}")

    def show_main_menu(self):
        # Display user options
        print("\n===== EXPENSE TRACKER MENU =====")
        print("1. Spending Summary")
        print("2. Category Analysis")
        print("3. Spending Chart")
        print("4. Filter Expenses")
        print("5. Add Expense")
        print("6. Export Report")
        print("7. Exit")

    def run_tracker(self):
        # Main application loop
        print(f"\nWelcome to Expense Tracker! (Data file: {os.path.basename(self.fasafe_file_path)})")
        while True:
            self.show_main_menu()
            user_choice = input("Choose an option (1-7): ").strip()
            
            if user_choice == '1':
                self.display_spending_summary()
            elif user_choice == '2':
                self.analyze_categories()
            elif user_choice == '3':
                self.create_category_pie_chart()
            elif user_choice == '4':
                self.show_filter_menu()
            elif user_choice == '5':
                self.add_new_expense()
            elif user_choice == '6':
                self.export_analysis_report()
            elif user_choice == '7':
                # Exit with save option
                if not self.expense_data.empty:
                    save_first = input("Save changes before exiting? (y/n): ").lower()
                    if save_first == 'y':
                        if self.save_expense_data():
                            print("Changes saved successfully!")
                        else:
                            print("Save failed")
                print("Thank you for using Expense Tracker!")
                break
            else:
                print("Invalid choice. Please enter 1-7")

    def show_filter_menu(self):
        # Submenu for filtering options
        print("\nFilter by:")
        print("1. Date Range")
        print("2. Month")
        filter_choice = input("Choose filter type (1-2): ").strip()
        
        if filter_choice == '1':
            start_input = input("Start date (e.g., DD-MM-YYYY): ")
            end_input = input("End date (e.g., DD-MM-YYYY): ")
            filtered_data = self.filter_expenses(start_date=start_input, end_date=end_input)
        elif filter_choice == '2':
            month_input = input("Month (e.g., YYYY-MM): ")
            filtered_data = self.filter_expenses(target_month=month_input)
        else:
            print("Invalid choice")
            return
            
        if filtered_data.empty:
            print("No matching records found")
        else:
            # Format dates for display
            display_data = filtered_data.copy()
            display_data['Date'] = display_data['Date'].dt.strftime('%d-%m-%Y')
            print(display_data.to_string(index=False))

# Application entry point
if __name__ == "__main__":
    # Find available CSV files
    csv_files = [f for f in os.listdir(os.getcwd()) if f.lower().endswith('.csv')]
    
    if csv_files:
        print("Available CSV files:")
        for i, file in enumerate(csv_files, 1):
            print(f"  {i}. {file}")
        print("Press Enter to use default 'expenses.csv'")
        file_choice = input("Select file number or press Enter: ").strip()
        
        if file_choice.isdigit() and 1 <= int(file_choice) <= len(csv_files):
            selected_file = csv_files[int(file_choice) - 1]
        else:
            selected_file = 'expenses.csv'
    else:
        selected_file = 'expenses.csv'
    # Start the tracker
    my_tracker = ExpenseTracker(selected_file)
    my_tracker.run_tracker()

#Project by Aditya Sinha
#Created on - 21-06-2025 10:30AM
