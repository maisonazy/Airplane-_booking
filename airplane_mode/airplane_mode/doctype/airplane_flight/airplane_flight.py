# Copyright (c) 2026, hilla and contributors
# For license information, please see license.txt
import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):

    def on_submit(self):
        self.status = "Completed"
	

def get_list_context(context=None):
    return {
        "title": "Available Flights",
        "filters": {"is_published": 1},
        "order_by": "date_of_departure asc",
        "hide_filters": True,
    }
