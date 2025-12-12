# ===================================================================
# PROGRAM OVERVIEW
# This is a complete system to track your personal finances:
# - Record income and expenses
# - Calculate current balance
# - View summary by expense categories
# - Save and load data in JSON and CSV files
# - Fully validated with good structure (OOP)
# ===================================================================

import json
import csv
from typing import List, Dict


# ===================================================================
# CLASS 1: Transaction - Represents an individual income or expense
# ===================================================================
class Transaction:
    """
    Represents a financial transaction (income or expense).
    Examples: salary, rent, groceries, Netflix, etc.
    """

    def __init__(self, transaction_type: str, category: str, amount: float):
        # Validation: only allows "income" or "expense"
        if transaction_type not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'")
        # Validation: does not allow negative or zero amounts
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        self.transaction_type = transaction_type  # "income" or "expense"
        self.category = category  # E.g.: "salary", "food", "transportation"
        self.amount = amount     # Monetary value (e.g.: 2500.50)

    # Converts the object to a dictionary (needed for saving to JSON/CSV)
    def to_dict(self) -> Dict:
        """Converts the transaction to a dictionary (for JSON or CSV)."""
        return {
            "type": self.transaction_type, 
            "category": self.category, 
            "amount": self.amount
        }


# ===================================================================
# CLASS 2: ExpenseTracker - The brain of the system
# ===================================================================
class ExpenseTracker:
    """
    Main system for recording and analyzing financial transactions.
    It's like a small personal finance app.
    """

    def __init__(self):
        self.transactions: List[Transaction] = []  # List that stores all transactions

    # ==================== BASIC OPERATIONS ====================
    def add_transaction(self, transaction_type: str, category: str, amount: float) -> None:
        """Adds a new income or expense to the system."""
        transaction = Transaction(transaction_type, category, amount)  # Creates transaction with validations
        self.transactions.append(transaction)                         # Saves it to the list

    def calculate_balance(self) -> float:
        """Calculates how much money you have left: total income - total expenses."""
        income = sum(t.amount for t in self.transactions if t.transaction_type == "income")
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == "expense")
        return income - expenses

    def summary_by_category(self) -> Dict[str, float]:
        """Shows how much you spent in each category (food, transportation, etc.)."""
        summary: Dict[str, float] = {}
        for t in self.transactions:
            if t.transaction_type == "expense":
                # If category exists, adds. If not, creates with 0 and adds
                summary[t.category] = summary.get(t.category, 0) + t.amount
        return summary

    # ==================== SAVING TO FILES ====================
    def save_json(self, filename: str = "transactions.json") -> None:
        """Saves all transactions to a JSON file (universal format)."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.transactions], f, indent=4)
        print(f"Data saved to {filename}")

    def load_json(self, filename: str = "transactions.json") -> None:
        """Loads transactions from a JSON file."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.transactions = [Transaction(**item) for item in data]
            print(f"Data loaded from {filename}")
        except FileNotFoundError:
            print("JSON file not found. Starting with empty list.")
            self.transactions = []

    def save_csv(self, filename: str = "transactions.csv") -> None:
        """Saves transactions in CSV format (opens in Excel)."""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["type", "category", "amount"])
            writer.writeheader()
            for t in self.transactions:
                writer.writerow(t.to_dict())
        print(f"Data saved to {filename}")

    def load_csv(self, filename: str = "transactions.csv") -> None:
        """Loads transactions from a CSV file."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.transactions = [
                    Transaction(row["type"], row["category"], float(row["amount"])) 
                    for row in reader
                ]
            print(f"Data loaded from {filename}")
        except FileNotFoundError:
            print("CSV file not found. Starting with empty list.")
            self.transactions = []


# ===================================================================
# REAL USAGE EXAMPLE (system test)
# ===================================================================
if __name__ == "__main__":
    # Create a new expense tracking system
    system = ExpenseTracker()

    # Record some example transactions
    system.add_transaction("income", "salary", 2500)
    system.add_transaction("expense", "food", 300)
    system.add_transaction("expense", "transportation", 150)
    system.add_transaction("expense", "entertainment", 200)

    # Show current balance
    print(f"Current balance: ${system.calculate_balance():,.2f}")

    # Show how much was spent in each category
    print("\nExpense summary by category:")
    for category, total in system.summary_by_category().items():
        print(f" - {category}: ${total:,.2f}")

    # Save data to files
    system.save_json("transactions.json")
    system.save_csv("transactions.csv")
