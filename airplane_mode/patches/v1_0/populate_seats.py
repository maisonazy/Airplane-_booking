import random
import frappe


def generate_seat():
    number = random.randint(1, 99)
    letter = random.choice("ABCDE")

    return f"{number}{letter}"


def execute():

    tickets = frappe.get_all(
        "Airplane Ticket",
        fields=["name"],
        filters={
            "seat": ["in", ["", None]]
        }
    )

    for ticket in tickets:

        seat = generate_seat()

        frappe.db.set_value(
            "Airplane Ticket",
            ticket.name,
            "seat",
            seat
        )

    frappe.db.commit()