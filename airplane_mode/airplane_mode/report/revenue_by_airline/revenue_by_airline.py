# Copyright (c) 2026, hilla and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
			"width": 220,
		},
		{
			"label": _("Revenue"),
			"fieldname": "revenue",
			"fieldtype": "Currency",
			"width": 160,
		},
	]

	data = frappe.db.sql(
		"""
		SELECT
			airline.name AS airline,
			COALESCE(SUM(ticket.total_amount), 0) AS revenue
		FROM `tabAirline` airline
		LEFT JOIN `tabAirplane` airplane ON airplane.airline = airline.name
		LEFT JOIN `tabAirplane Flight` flight ON flight.airplane = airplane.name
		LEFT JOIN `tabAirplane Ticket` ticket
			ON ticket.flight = flight.name AND ticket.docstatus = 1
		GROUP BY airline.name
		ORDER BY revenue DESC, airline.name
		""",
		as_dict=True,
	)

	total_revenue = sum(row.revenue or 0 for row in data)
	data.append({"airline": _("Total"), "revenue": total_revenue})

	chart = {
		"data": {
			"labels": [row.airline for row in data if row.airline != _("Total")],
			"datasets": [
				{
					"name": _("Revenue"),
					"values": [row.revenue for row in data if row.airline != _("Total")],
				}
			],
		},
		"type": "donut",
	}
	report_summary = [
		{
			"label": _("Total Revenue"),
			"value": total_revenue,
			"indicator": "Green",
			"datatype": "Currency",
		}
	]

	return columns, data, None, chart, report_summary
