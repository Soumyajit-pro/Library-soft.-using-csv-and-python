import csv
import os
from datetime import datetime
from uuid import uuid4

user_file = "user.csv"
book_details = "books.csv"
borrow_details = "borrow.csv"

# Initialize the CSV files
def initialization():
    for file_name, headers in [
        (user_file, ["User ID", "Name", "Contact"]),
        (book_details, ["ISBN", "Title", "Author", "Book Bio", "Available"]),
        (borrow_details, ["User ID", "ISBN", "Borrow Date", "Return Date"]),
    ]:
        try:
            if not os.path.exists(file_name):
                with open(file_name, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
        except Exception as e:
            print(f"Error initializing file {file_name}: {e}")

# Validate inputs
def validate_input(prompt, validation_fn, error_message):
    while True:
        value = input(prompt)
        if validation_fn(value):
            return value
        print(error_message)

# Add new users
def add_user():
    try:
        user_add_amnt = int(input("Enter the number of users to add: "))
        for _ in range(user_add_amnt):
            name = validate_input("Enter name: ", lambda x: x.isalpha(), "Name must contain only letters.")
            contact = validate_input(
                "Enter contact (10-digit number): ", lambda x: x.isdigit() and len(x) == 10, "Invalid contact number."
            )
            user_id = str(uuid4())[:8]  # Generate a unique ID
            with open(user_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([user_id, name, contact])
            print(f"User added successfully! User ID: {user_id}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Add new books
def add_book():
    try:
        book_add_amnt = int(input("Enter the number of books to add: "))
        for _ in range(book_add_amnt):
            isbn = validate_input("Enter ISBN: ", lambda x: x.strip() != "", "ISBN cannot be empty.")
            title = validate_input("Enter book title: ", lambda x: x.strip() != "", "Title cannot be empty.")
            author = validate_input("Enter book author: ", lambda x: x.strip() != "", "Author cannot be empty.")
            bio = input("Enter book bio: ")
            with open(book_details, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([isbn, title, author, bio, "Yes"])
            print(f"Book added successfully! ISBN: {isbn}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Check if user and book exist
def check_user_exists(user_id):
    with open(user_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return any(row[0] == user_id for row in reader)

def check_book_available(isbn):
    with open(book_details, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == isbn and row[4] == "Yes":
                return True
    return False

# Borrow a book
def borrow_book():
    user_id = validate_input("Enter User ID: ", check_user_exists, "User ID does not exist.")
    isbn = validate_input("Enter ISBN: ", check_book_available, "Book is not available or does not exist.")
    borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(borrow_details, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([user_id, isbn, borrow_date, "Not Returned"])
        # Mark book as unavailable
        update_book_availability(isbn, "No")
        print("Book borrowing record added successfully!")
    except Exception as e:
        print(f"Error borrowing book: {e}")

# Return a book
def return_book():
    user_id = input("Enter User ID: ")
    isbn = input("Enter ISBN: ")
    return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_rows = []
    found = False
    try:
        with open(borrow_details, "r", newline="") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row[0] == user_id and row[1] == isbn and row[3] == "Not Returned":
                    row[3] = return_date
                    found = True
                updated_rows.append(row)
        with open(borrow_details, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(updated_rows)
        if found:
            update_book_availability(isbn, "Yes")
            print("Book return record updated successfully!")
        else:
            print("No matching borrow record found.")
    except Exception as e:
        print(f"Error returning book: {e}")

# Update book availability
def update_book_availability(isbn, status):
    updated_rows = []
    with open(book_details, "r", newline="") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row[0] == isbn:
                row[4] = status
            updated_rows.append(row)
    with open(book_details, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(updated_rows)

# Show user history
def show_user_history():
    user_id = input("Enter User ID: ")
    print(f"Borrow history for User ID: {user_id}")
    print(f"{'ISBN':<15}{'Borrow Date':<25}{'Return Date'}")
    print("-" * 60)
    with open(borrow_details, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip headers
        for row in reader:
            if row[0] == user_id:
                print(f"{row[1]:<15}{row[2]:<25}{row[3]}")

# Show book history
def show_book_history():
    isbn = input("Enter Book ISBN: ")
    print(f"History for Book ISBN: {isbn}")
    print(f"{'User ID':<15}{'Borrow Date':<25}{'Return Date'}")
    print("-" * 60)
    with open(borrow_details, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip headers
        for row in reader:
            if row[1] == isbn:
                print(f"{row[0]:<15}{row[2]:<25}{row[3]}")

# Show channel log
def show_channel_log():
    print(
        """
        CSV and Python-based Library Management Software
        --->>> Soumyajit Biswas <<<---
        This project has improved error handling, data validation, and functionality.
        Future Scope:
        - Use Pandas for better data manipulation.
        - Migrate to SQLite for robust database management.
        - Add GUI with Tkinter or a web interface.
        Last edited: 08-12-2024
        """
    )

# Main function for menu
def main():
    initialization()
    print("""
██╗     ██╗██████╗ ██████╗  █████╗ ██████╗ ██╗   ██╗
██║     ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
██║     ██║██████╦╝██████╔╝███████║██████╔╝ ╚████╔╝
██║     ██║██╔══██╗██╔══██╗██╔══██║██╔══██╗  ╚██╔╝
███████╗██║██████╦╝██║  ██║██║  ██║██║  ██║   ██║
╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝

███╗   ███╗ █████╗ ███╗  ██╗ █████╗  ██████╗ ███████╗███╗   ███╗███████╗███╗  ██╗████████╗
████╗ ████║██╔══██╗████╗ ██║██╔══██╗██╔════╝ ██╔════╝████╗  ███║██╔════╝████╗ ██║╚══██╔══╝
██╔████╔██║███████║██╔██╗██║███████║██║  ██╗ █████╗  ██╔████╔██║█████╗  ██╔██╗██║   ██║
██║╚██╔╝██║██╔══██║██║╚████║██╔══██║██║  ╚██╗██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚████║   ██║
██║ ╚═╝ ██║██║  ██║██║ ╚███║██║  ██║╚██████╔╝███████╗██║ ╚═╝ ██║███████╗██║  ███║   ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚══╝   ╚═╝

██████╗ ██████╗  █████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
██████╔╝██████╔╝██║  ██║██║  ██╗ ██████╔╝███████║██╔████╔██║
██╔═══╝ ██╔══██╗██║  ██║██║  ╚██╗██╔══██╗██╔══██║██║╚██╔╝██║
██║     ██║  ██║╚█████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝ ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝""")
    
    while True:
        print("""
    Welcome to the Library Management System
    1. Add User
    2. Add Book
    3. Borrow Book
    4. Return Book
    5. Show User History
    6. Show Book History
    7. Show Channel Log
    8. Exit
    """)
        choice = input("Enter your choice: ")
        if choice == "1":
            add_user()
        elif choice == "2":
            add_book()
        elif choice == "3":
            borrow_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            show_user_history()
        elif choice == "6":
            show_book_history()
        elif choice == "7":
            show_channel_log()
        elif choice == "8":
            print("Exiting the program....")
            break

if __name__ == "__main__":
    main()



