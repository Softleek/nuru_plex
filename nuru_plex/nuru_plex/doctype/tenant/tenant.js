// Copyright (c) 2024, Nuru and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tenant", {
  validate: function (frm) {
    if (!frm.doc.__islocal) {
      return;
    }

    var full_name = frm.doc.full_name;
    var phone = frm.doc.phone;
    var email = frm.doc.email;

    frappe.call({
      method: "nuru_plex.service.rest.create_tenant_user",
      args: {
        full_name: full_name,
        phone: phone,
        email: email,
      },
      callback: function (response) {
        if (response.message) {
          frm.set_value("user", response.message.name);
          frm.set_value("mobile_no", phone);
        }
      },
    });
  },
});
