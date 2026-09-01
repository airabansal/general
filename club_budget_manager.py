from datetime import datetime
import json


class FinancialTransaction:

    def __init__(
        self, trans_type, description, amount, category, logged_by, event=None
    ):
        """Represents a single income or expense transaction.

        :param trans_type: str ("INCOME" or "EXPENSE")
        :param description: str (e.g., "Car Wash Ticket Sales", "Robot Chassis")
        :param amount: float (Positive dollar amount)
        :param category: str (e.g., "Dues", "Fundraiser", "Supplies", "Travel")
        :param logged_by: str (Name of student officer)
        :param event: str (Optional tag like "Fall Bake Sale")
        """
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.trans_type = trans_type.upper()
        self.description = description
        self.amount = float(amount)
        self.category = category
        self.logged_by = logged_by
        self.event = event or "General Club Fund"

    def to_dict(self):
        return self.__dict__


class ClubFinancialTracker:

    def __init__(self, club_name, starting_balance=0.0):
        self.club_name = club_name
        self.starting_balance = float(starting_balance)
        self.transactions = []
        self.fundraisers = {}  # Format: {"Event Name": Target Goal Amount}

    def set_fundraiser_goal(self, event_name, goal_amount):
        """Sets a target fundraising goal for a specific event."""
        self.fundraisers[event_name] = float(goal_amount)
        print(
            f"🎯 Fundraiser Goal Set: '{event_name}' ➔ Goal: ${goal_amount:,.2f}"
        )

    def log_income(
        self, description, amount, category="Fundraiser", logged_by="Treasurer", event=None
    ):
        """Logs incoming revenue."""
        tx = FinancialTransaction(
            "INCOME", description, amount, category, logged_by, event
        )
        self.transactions.append(tx)
        print(f"💵 Registered Income: +${amount:,.2f} ({description})")

    def log_expense(
        self, description, amount, category="Supplies", logged_by="Treasurer", event=None
    ):
        """Logs outgoing expenditure."""
        tx = FinancialTransaction(
            "EXPENSE", description, amount, category, logged_by, event
        )
        self.transactions.append(tx)
        print(f"💸 Registered Expense: -${amount:,.2f} ({description})")

    def calculate_current_balance(self):
        """Calculates total net balance (Starting + Income - Expenses)."""
        income = sum(
            tx.amount for tx in self.transactions if tx.trans_type == "INCOME"
        )
        expenses = sum(
            tx.amount for tx in self.transactions if tx.trans_type == "EXPENSE"
        )
        return self.starting_balance + income - expenses

    def print_financial_dashboard(self):
        """Generates a complete financial status report for officers and school advisors."""
        total_income = sum(
            tx.amount for tx in self.transactions if tx.trans_type == "INCOME"
        )
        total_expense = sum(
            tx.amount for tx in self.transactions if tx.trans_type == "EXPENSE"
        )
        net_balance = self.calculate_current_balance()

        print("\n" + "=" * 70)
        print(
            f"       FINANCIAL & FUNDRAISER DASHBOARD: {self.club_name.upper()}"
        )
        print("=" * 70)

        # 1. Executive Summary
        print(f"📊 ACCOUNT OVERVIEW")
        print(f"   • Starting Treasury : ${self.starting_balance:>10,.2f}")
        print(f"   • Total Revenue (+) : ${total_income:>10,.2f}")
        print(f"   • Total Spending (-) : ${total_expense:>10,.2f}")
        print(f"   ─────────────────────────────────────────")
        print(f"   💰 NET BALANCE      : ${net_balance:>10,.2f}")

        # 2. Fundraiser Progress Tracker
        if self.fundraisers:
            print("\n🎯 FUNDRAISER CAMPAIGN PROGRESS")
            print("-" * 70)
            for event_name, goal in self.fundraisers.items():
                raised = sum(
                    tx.amount
                    for tx in self.transactions
                    if tx.event == event_name and tx.trans_type == "INCOME"
                )
                pct = (raised / goal * 100) if goal > 0 else 0
                status_icon = "🎉 GOAL MET!" if raised >= goal else "📈 IN PROGRESS"
                print(
                    f"   • {event_name:<25} | Raised: ${raised:>8,.2f} / ${goal:>8,.2f} "
                    f"({pct:>5.1f}%) [{status_icon}]"
                )

        # 3. Transaction History
        print("\n🧾 RECENT TRANSACTION LEDGER")
        print("-" * 70)
        if not self.transactions:
            print("   No transactions recorded.")
        else:
            print(
                f"   {'Type':<8} | {'Date':<16} | {'Description':<22} | {'Category':<10} | {'Amount':<9}"
            )
            print("   " + "-" * 66)
            for tx in self.transactions:
                sign = "+" if tx.trans_type == "INCOME" else "-"
                print(
                    f"   {tx.trans_type:<8} | {tx.date:<16} | {tx.description:<22} | "
                    f"{tx.category:<10} | {sign}${tx.amount:>7.2f}"
                )

        print("=" * 70 + "\n")


# --- Example Execution ---
if __name__ == "__main__":
    # Create tracker for Model UN Club with $300 starting cash
    mun_club = ClubFinancialTracker(
        club_name="Model UN Club", starting_balance=300.00
    )

    # Set up fundraising campaigns
    mun_club.set_fundraiser_goal("Fall Car Wash", 500.00)
    mun_club.set_fundraiser_goal("Krispy Kreme Donut Sale", 300.00)

    # Log incoming revenue
    mun_club.log_income(
        "Member Annual Dues (15 members)",
        amount=225.00,
        category="Dues",
        logged_by="Sarah (Treasurer)",
    )
    mun_club.log_income(
        "Car Wash Presale Tickets",
        amount=340.00,
        category="Fundraiser",
        logged_by="Sarah (Treasurer)",
        event="Fall Car Wash",
    )
    mun_club.log_income(
        "Car Wash Day-of Cash",
        amount=210.00,
        category="Fundraiser",
        logged_by="Alex (President)",
        event="Fall Car Wash",
    )
    mun_club.log_income(
        "Donut Box Orders",
        amount=180.00,
        category="Fundraiser",
        logged_by="Sarah (Treasurer)",
        event="Krispy Kreme Donut Sale",
    )

    # Log expenses
    mun_club.log_expense(
        "Soap & Sponges for Car Wash",
        amount=42.50,
        category="Supplies",
        logged_by="Alex (President)",
        event="Fall Car Wash",
    )
    mun_club.log_expense(
        "State Conference Registration Fee",
        amount=450.00,
        category="Travel",
        logged_by="Sarah (Treasurer)",
    )

    # Display Financial Dashboard
    mun_club.print_financial_dashboard()
