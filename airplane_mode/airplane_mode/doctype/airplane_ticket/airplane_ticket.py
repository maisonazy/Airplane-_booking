# Copyright (c) 2026, hilla and contributors
# For license information, please see license.txt

import random

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class AirplaneTicket(Document):
	def before_validate(self):
		self.populate_flight_details()

	def before_insert(self):
		if not self.flight:
			return

		self.populate_flight_details()
		self.seat = f"{random.randint(1, 99)}{random.choice('ABCDE')}"

	def populate_flight_details(self):
		if not self.flight:
			return

		flight = frappe.get_doc("Airplane Flight", self.flight)
		self.source_airport = flight.source_airport
		self.destination_airport = flight.destination_airport
		self.source_airport_code = flight.source_airport_code
		self.destination_airport_code = flight.destination_airport_code
		self.departure_date = flight.date_of_departure
		self.departure_time = flight.time_of_departure
		self.duration_of_flight = flight.duration

	def validate(self):
		self.remove_duplicate_addons()
		self.calculate_total_amount()

	def remove_duplicate_addons(self):
		seen = set()
		unique_addons = []

		for addon in self.add_ons or []:
			if addon.item not in seen:
				seen.add(addon.item)
				unique_addons.append(addon)

		self.add_ons = unique_addons

	def calculate_total_amount(self):
		addon_total = sum(flt(addon.amount) for addon in self.add_ons or [])
		self.total_amount = flt(self.flight_price) + addon_total

	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("You can only submit a ticket when the passenger has boarded.")

		self.validate_flight_capacity()

	def validate_flight_capacity(self):
		if not self.flight:
			frappe.throw("Please select an Airplane Flight.")

		flight = frappe.get_doc("Airplane Flight", self.flight)
		airplane = frappe.get_doc("Airplane", flight.airplane)
		capacity = airplane.capacity

		booked_tickets = frappe.db.count(
			"Airplane Ticket",
			filters={"flight": self.flight, "docstatus": 1},
		)

		if booked_tickets >= capacity:
			frappe.throw(
				f"Booking failed! The airplane capacity is {capacity}. "
				"All seats for this flight have been booked."
			)
