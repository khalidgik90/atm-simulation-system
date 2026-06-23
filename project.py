"""
========================================================
  ATM Simulation System (Advanced Version)
  OOP + NumPy + Pandas + Matplotlib
========================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ==============================================
#  CLASS 1: Account
# ==============================================

class Account:
    def __init__(self, pin: int, balance: float = 0.0):
        self.__pin = pin
        self.__balance = balance

    def get_pin(self):
        return self.__pin

    def get_balance(self):
        return self.__balance

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def withdraw(self, amount: float):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False


# ==============================================
#  CLASS 2: Bank (Uses Pandas + NumPy)
# ==============================================

class Bank:
    DATA_FILE = "balances.csv"

    def __init__(self):
        self.__accounts = {}
        self.__load()

    # ---------- Load from CSV using Pandas ----------
    def __load(self):
        if not os.path.exists(Bank.DATA_FILE):
            return

        df = pd.read_csv(Bank.DATA_FILE)

        for _, row in df.iterrows():
            pin = int(row["PIN"])
            balance = float(row["Balance"])
            self.__accounts[pin] = Account(pin, balance)

    # ---------- Save to CSV using Pandas ----------
    def save(self):
        data = {
            "PIN": [],
            "Balance": []
        }

        for acc in self.__accounts.values():
            data["PIN"].append(acc.get_pin())
            data["Balance"].append(acc.get_balance())

        df = pd.DataFrame(data)
        df.to_csv(Bank.DATA_FILE, index=False)

    # ---------- Account Management ----------
    def register(self, account: Account):
        if account.get_pin() in self.__accounts:
            return False
        self.__accounts[account.get_pin()] = account
        self.save()
        return True

    def find(self, pin: int):
        return self.__accounts.get(pin)

    def has_accounts(self):
        return len(self.__accounts) > 0

    # ---------- NumPy Statistics ----------
    def show_statistics(self):
        if not self.__accounts:
            print("No accounts available.")
            return

        balances = np.array(
            [acc.get_balance() for acc in self.__accounts.values()]
        )

        print("\n===== BANK ANALYTICS =====")
        print(f"Total Accounts     : {len(balances)}")
        print(f"Total Bank Balance : Rs. {np.sum(balances):.2f}")
        print(f"Average Balance    : Rs. {np.mean(balances):.2f}")
        print(f"Highest Balance    : Rs. {np.max(balances):.2f}")
        print(f"Lowest Balance     : Rs. {np.min(balances):.2f}")
        print("===========================\n")

    # ---------- Matplotlib Graph ----------
    def plot_balances(self):
        if not self.__accounts:
            print("No accounts to display.")
            return

        pins = [acc.get_pin() for acc in self.__accounts.values()]
        balances = [acc.get_balance() for acc in self.__accounts.values()]

        plt.figure()
        plt.bar(pins, balances)
        plt.xlabel("Account PIN")
        plt.ylabel("Balance (Rs.)")
        plt.title("Account Balance Distribution")
        plt.show()


# ==============================================
#  CLASS 3: ATM
# ==============================================

class ATM:
    def __init__(self):
        self.__bank = Bank()

    @staticmethod
    def __is_valid_pin(pin_str):
        return pin_str.isdigit() and len(pin_str) == 4

    @staticmethod
    def __get_float(prompt):
        try:
            return float(input(prompt))
        except ValueError:
            return None

    # ---------- Banking Menu ----------
    def __banking_menu(self, account: Account):
        while True:
            print("\n1. Withdraw")
            print("2. Deposit")
            print("3. Check Balance")
            print("4. Exit")

            choice = input("Select option: ")

            if choice == "1":
                amount = self.__get_float("Enter amount: ")
                if amount and account.withdraw(amount):
                    self.__bank.save()
                    print("Withdrawal successful.")
                else:
                    print("Transaction failed.")

            elif choice == "2":
                amount = self.__get_float("Enter amount: ")
                if amount and account.deposit(amount):
                    self.__bank.save()
                    print("Deposit successful.")
                else:
                    print("Transaction failed.")

            elif choice == "3":
                print(f"Balance: Rs. {account.get_balance():.2f}")

            elif choice == "4":
                break

            else:
                print("Invalid option.")

    # ---------- Create Account ----------
    def __create_account(self):
        while True:
            pin_str = input("Choose 4-digit PIN: ")
            if not self.__is_valid_pin(pin_str):
                print("Invalid PIN format.")
                continue

            pin = int(pin_str)

            if self.__bank.find(pin):
                print("PIN already exists.")
                continue

            break

        amount = self.__get_float("Initial Deposit: ")
        if amount is None or amount < 0:
            print("Invalid deposit.")
            return

        new_account = Account(pin, amount)
        self.__bank.register(new_account)
        print("Account created successfully.")

    # ---------- Admin Panel ----------
    def __admin_panel(self):
        self.__bank.show_statistics()
        self.__bank.plot_balances()

    # ---------- Main Run ----------
    def run(self):
        while True:
            print("\n===== ATM MENU =====")
            print("1. Enter PIN")
            print("2. Create Account")
            print("3. Admin Analytics")
            print("4. Exit")

            choice = input("Choice: ")

            if choice == "1":
                pin_str = input("Enter PIN: ")

                if not self.__is_valid_pin(pin_str):
                    print("Invalid PIN format.")
                    continue

                account = self.__bank.find(int(pin_str))

                if account:
                    self.__banking_menu(account)
                else:
                    print("Invalid PIN.")

            elif choice == "2":
                self.__create_account()

            elif choice == "3":
                self.__admin_panel()

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("Invalid choice.")


# ==============================================
#  ENTRY POINT
# ==============================================

if __name__ == "__main__":
    atm = ATM()
    atm.run()
