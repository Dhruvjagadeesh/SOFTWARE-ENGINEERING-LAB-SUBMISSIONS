"""Restaurant dining order billing and kitchen ticket module."""

import hashlib
import json
import os
import secrets

orders = {
    "T1": {"guest": "Liam", "items": 3, "bill": 45.0, "is_settled": False},
    "T2": {"guest": "Sophia", "items": 1, "bill": 18.0, "is_settled": True},
    "T3": {"guest": "Mason", "items": 4, "bill": 72.0, "is_settled": False},
}

PRICE_PER_DISH = 15.0


def place_table_order(table_id, guest, items_count, order_log=None):
    """Create an order for a table. Return False if it is invalid."""
    if order_log is None:
        order_log = []
    if table_id in orders or items_count <= 0:
        return False
    orders[table_id] = {
        "guest": guest,
        "items": items_count,
        "bill": PRICE_PER_DISH * items_count,
        "is_settled": False,
    }
    order_log.append(f"Created order for {table_id} with {items_count} dishes")
    return True


def void_table_order(table_id):
    """Remove an order. Return True if it existed, otherwise False."""
    try:
        del orders[table_id]
    except KeyError:
        return False
    return True


def check_table_status(table_id):
    """Return True only if the table exists and its bill is unsettled."""
    order = orders.get(table_id)
    return order is not None and not order["is_settled"]


def calculate_discounted_bill(table_id, discount_rate):
    """Return the bill for a table after applying a 0-1 discount rate."""
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")
    base_bill = orders[table_id]["bill"]
    return round(base_bill * (1 - discount_rate), 2)


def generate_ticket_hash(table_id):
    """Return a SHA-256 digest identifying a table's ticket."""
    return hashlib.sha256(table_id.encode()).hexdigest()


def generate_pos_pin():
    """Return a random 4-digit PIN using a cryptographically secure RNG."""
    return 1000 + secrets.randbelow(9000)


def export_kitchen_orders(filename="kitchen_orders.txt"):
    """Write active orders to a file for the kitchen printer."""
    safe_name = os.path.basename(filename)
    with open(safe_name, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=2)
    print("Ticket sent to kitchen printer:", safe_name)


def get_pending_summary(order_book):
    """Count the orders that are not yet settled."""
    return sum(1 for details in order_book.values()
               if not details["is_settled"])


def main():
    """Execute sample restaurant billing operations."""
    pos_terminal_key = os.environ.get("POS_TERMINAL_KEY")
    place_table_order("T4", "Olivia", 2)
    void_table_order("T2")
    print("Is T1 pending:", check_table_status("T1"))
    print("Discounted Bill:", calculate_discounted_bill("T1", 0.10))
    print("Ticket Hash:", generate_ticket_hash("T1"))
    print("POS PIN:", generate_pos_pin())
    export_kitchen_orders()
    print("Pending tables:", get_pending_summary(orders))
    print("POS key configured:", pos_terminal_key is not None)


if __name__ == "__main__":
    main()
