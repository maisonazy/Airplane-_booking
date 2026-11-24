frappe.ui.form.on("Airline", {
    refresh(frm) {
        if (frm.doc.website) {
            frm.add_custom_button("Visit Website", () => {
                window.open(frm.doc.website, "_blank", "noopener");
            });
        }
    }
});

