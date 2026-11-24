frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            frm.add_custom_button("Assign Seat", () => {

                let dialog = new frappe.ui.Dialog({
                    title: "Assign Seat",
                    fields: [
                        {
                            label: "Seat Number",
                            fieldname: "seat",
                            fieldtype: "Data",
                            reqd: 1,
                            default: frm.doc.seat
                        }
                    ],

                    primary_action_label: "Assign",

                    primary_action(values) {
                        frm.set_value("seat", values.seat);

                        dialog.hide();
                    }
                });

                dialog.show();
            });
        }
    }
});