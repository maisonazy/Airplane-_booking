import frappe


def get_context(context):
	context.no_cache = 1
	context.title = "Book Flight Ticket"

	flight_name = frappe.form_dict.get("flight")
	if not flight_name or not frappe.db.exists(
		"Airplane Flight", {"name": flight_name, "is_published": 1}
	):
		frappe.redirect("/flights")
