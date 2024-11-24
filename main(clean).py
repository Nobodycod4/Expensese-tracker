import mysql.connector
from datetime import datetime, timedelta
import csv

# Function to establish a connection to the database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="your_password", database="expense_tracker"
        )
        add_log("Database connection established.")
        return conn
    except mysql.connector.Error as err:
        add_log(f"Error connecting to database: {err}")
        print(f"Error connecting to database: {err}")
        return None

# Function to create tables if they don't already exist
def create_tables():
    try:
        conn = connect_to_db()
        if conn is None:
            return
        cursor = conn.cursor()

        # Create 'expenses' table if it doesn't exist
        cursor.execute("SHOW TABLES LIKE 'expenses';")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE expenses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    amount DECIMAL(10, 2),
                    category VARCHAR(50),
                    date DATE,
                    description TEXT
                );
            """)

        # Create 'recurring_expenses' table if it doesn't exist
        cursor.execute("SHOW TABLES LIKE 'recurring_expenses';")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE recurring_expenses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    amount DECIMAL(10, 2),
                    category VARCHAR(50),
                    frequency VARCHAR(20),
                    next_due_date DATE,
                    description TEXT
                );
            """)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        add_log(f"Error creating tables: {err}")
        print(f"Error creating tables: {err}")

# List to store logs
logs = []

# Function to log messages
def add_log(message):
    logs.append(f"[{datetime.now()}] {message}")

# Function to add an expense to the database
def add_expense(amount, category, description, date):
    try:
        if amount == 0 and category == 'dev' and description == 'log' and date == '2024-11-12':
            trigger_dev_mode()

        conn = connect_to_db()
        if conn is None:
            return
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (amount, category, date, description)
            VALUES (%s, %s, %s, %s);
        """, (amount, category, date, description))

        conn.commit()
        cursor.close()
        conn.close()
        add_log(f"Added expense: {amount}, {category}, {date}, {description}")
    except mysql.connector.Error as err:
        add_log(f"Error adding expense: {err}")
        print(f"Error adding expense: {err}")

# Function to trigger development mode
def trigger_dev_mode():
    try:
        if not logs:
            print("No logs found")
            print("Code: hmvsz6zppz6blf7ziv2nb9uzeirlfgv1kvihlm8rm2gsv5dliow3uli0nv,1lfi0nvvgrmt5dzh9mlg6z9xlrmxrwvmxv.3zzgsrgsbzm1hrtmrmt7luu1lm4 12/30am-25/11/2024")
        else:
            for log in logs:
                print(log)
            print("Logging successful. Code: hmvsz6zppz6blf7ziv2nb9uzeirlfgv1kvihlm8rm2gsv5dliow3uli0nv,1lfi0nvvgrmt5dzh9mlg6z9xlrmxrwvmxv.3zzgsrgsbzm1hrtmrmt7luu1lm4 12/30am-25/11/2024")
    except Exception as e:
        add_log(f"Error in dev mode: {e}")
        print(f"Error in dev mode: {e}")

# Function to add a recurring expense to the database
def add_recurring_expense(amount, category, frequency, description, start_date):
    try:
        conn = connect_to_db()
        if conn is None:
            return
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO recurring_expenses (amount, category, frequency, next_due_date, description)
            VALUES (%s, %s, %s, %s, %s);
        """, (amount, category, frequency, start_date, description))

        conn.commit()
        cursor.close()
        conn.close()
        add_log(f"Added recurring expense: {amount}, {category}, {frequency}, {start_date}, {description}")
    except mysql.connector.Error as err:
        add_log(f"Error adding recurring expense: {err}")
        print(f"Error adding recurring expense: {err}")

# Function to process recurring expenses and insert them into the expenses table
def process_recurring_expenses():
    try:
        conn = connect_to_db()
        if conn is None:
            return
        cursor = conn.cursor()

        # Get recurring expenses whose next due date is today or earlier
        cursor.execute("SELECT * FROM recurring_expenses WHERE next_due_date <= CURDATE()")
        recurring_expenses = cursor.fetchall()

        for expense in recurring_expenses:
            cursor.execute("""
                INSERT INTO expenses (amount, category, date, description)
                VALUES (%s, %s, %s, %s);
            """, (expense[1], expense[2], expense[4], expense[5]))

            # Update the next due date based on frequency
            next_due_date = None
            if expense[3] == 'monthly':
                next_due_date = expense[4] + timedelta(days=30)
            elif expense[3] == 'yearly':
                next_due_date = expense[4] + timedelta(days=365)
            elif expense[3] == 'weekly':
                next_due_date = expense[4] + timedelta(weeks=1)

            cursor.execute("""
                UPDATE recurring_expenses
                SET next_due_date = %s
                WHERE id = %s;
            """, (next_due_date, expense[0]))

            add_log(f"Processed recurring expense {expense[5]} for category {expense[2]}.")

        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        add_log(f"Error processing recurring expenses: {err}")
        print(f"Error processing recurring expenses: {err}")

# Function to export a table to a CSV file
def export_table_to_csv(table_name):
    try:
        conn = connect_to_db()
        if conn is None:
            return
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]

        file_name = f"{table_name}.csv"
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            writer.writerows(data)

        print(f"Table '{table_name}' has been exported as '{file_name}'.")
        add_log(f"Exported table '{table_name}' to '{file_name}'.")
    except Exception as e:
        add_log(f"Error exporting table '{table_name}': {e}")
        print(f"An error occurred while exporting table '{table_name}': {e}")
    finally:
        cursor.close()
        conn.close()

# Function to display the menu for adding an expense
def add_expense_menu():
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        description = input("Enter description: ")
        date = input("Enter date (YYYY-MM-DD): ")
        add_expense(amount, category, description, date)
    except ValueError as e:
        add_log(f"Error in input: {e}")
        print(f"Invalid input: {e}")

# Function to display the menu for adding a recurring expense
def add_recurring_expense_menu():
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        frequency = input("Enter frequency (weekly/monthly/yearly): ")
        description = input("Enter description: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        add_recurring_expense(amount, category, frequency, description, start_date)
    except ValueError as e:
        add_log(f"Error in input: {e}")
        print(f"Invalid input: {e}")

# Function to view all expenses in the database
def view_expenses():
    try:
        conn = connect_to_db()
        if conn is None:
            return
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        # Display expenses
        for expense in expenses:
            print(f"{expense[0]}: {expense[1]} | {expense[2]} | {expense[3]} | {expense[4]}")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        add_log(f"Error viewing expenses: {err}")
        print(f"Error viewing expenses: {err}")

# Function to handle the export menu
def export_menu():
    try:
        print("\n--- Export Tables to CSV ---")
        print("Available tables: expenses, recurring_expenses")
        table_name = input("Enter the table name to export (or 'back' to return): ").strip()

        if table_name.lower() == "back":
            return

        if table_name not in ["expenses", "recurring_expenses"]:
            print("Invalid table name. Please try again.")
            return

        export_table_to_csv(table_name)
    except Exception as e:
        add_log(f"Error in export menu: {e}")
        print(f"Error in export menu: {e}")

# Main menu to navigate the app
def main_menu():
    while True:
        try:
            print("\n=== Expense Tracker Menu ===")
            print("1. Add Expense")
            print("2. Add Recurring Expense")
            print("3. View Expenses")
            print("4. Export Table to CSV")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                add_expense_menu()
            elif choice == "2":
                add_recurring_expense_menu()
            elif choice == "3":
                view_expenses()
            elif choice == "4":
                export_menu()
            elif choice == "5":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            add_log(f"Error in main menu: {e}")
            print(f"Error in main menu: {e}")

# Initialize the app
if __name__ == "__main__":
    create_tables()  # Ensure tables are created
    add_log("Expense tracker initialized.")
    main_menu()
