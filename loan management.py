# Online Loan Management System

"""
This system allows users to manage loans by adding new loans, viewing existing loans, and making payments.
It calculates monthly EMI, total interest, and total payment. It also checks for late payments and applies a 5% penalty if the due date is missed.
Loan details are stored persistently in a JSON file.
"""

import json
from datetime import datetime

def calculate_loan(amount, rate, tenure):
    monthly_rate = rate / (12 * 100)
    months = tenure * 12
    emi = (amount * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    total_payment = emi * months
    total_interest = total_payment - amount
    return emi, total_interest, total_payment

def apply_penalty(due_date, payment_date, amount_due):
    due_date = datetime.strptime(due_date, "%Y-%m-%d")
    payment_date = datetime.strptime(payment_date, "%Y-%m-%d")
    if payment_date > due_date:
        penalty = 0.05 * amount_due
        return penalty
    return 0

def save_loans(loans, filename="loans.json"):
    with open(filename, "w") as file:
        json.dump(loans, file, indent=4)

def load_loans(filename="loans.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def add_loan():
    loans = load_loans()
    user = input("Enter borrower name: ")
    amount = float(input("Enter loan amount: "))
    rate = float(input("Enter annual interest rate (in %): "))
    tenure = int(input("Enter loan tenure (in years): "))
    emi, total_interest, total_payment = calculate_loan(amount, rate, tenure)
    due_date = input("Enter due date for first payment (YYYY-MM-DD): ")
    
    loans[user] = {
        "amount": amount,
        "rate": rate,
        "tenure": tenure,
        "emi": emi,
        "total_interest": total_interest,
        "total_payment": total_payment,
        "due_date": due_date
    }
    
    save_loans(loans)
    print("Loan added successfully!")

def view_loans():
    loans = load_loans()
    if not loans:
        print("No loans found.")
        return
    for user, details in loans.items():
        print(f"\nBorrower: {user}")
        print(f"Loan Amount: {details['amount']}")
        print(f"Annual Interest Rate: {details['rate']}%")
        print(f"Loan Tenure: {details['tenure']} years")
        print(f"Monthly EMI: {details['emi']:.2f}")
        print(f"Total Interest: {details['total_interest']:.2f}")
        print(f"Total Payment: {details['total_payment']:.2f}")
        print(f"Due Date: {details['due_date']}")

def make_payment():
    loans = load_loans()
    user = input("Enter borrower name: ")
    if user not in loans:
        print("Loan not found.")
        return
    payment_date = input("Enter actual payment date (YYYY-MM-DD): ")
    penalty = apply_penalty(loans[user]['due_date'], payment_date, loans[user]['emi'])
    if penalty > 0:
        print(f"Late payment penalty applied: {penalty:.2f}")
    else:
        print("Payment made on time. No penalty.")

def main():
    while True:
        print("\nLoan Management System")
        print("1. Add Loan")
        print("2. View Loans")
        print("3. Make Payment")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_loan()
        elif choice == "2":
            view_loans()
        elif choice == "3":
            make_payment()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()