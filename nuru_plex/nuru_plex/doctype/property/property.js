// Copyright (c) 2024, Nuru and contributors
// For license information, please see license.txt

frappe.ui.form.on("Property", {
    refresh(frm) {
      var currentUser = frappe.session.user;
      frappe.call({
        method: "frappe.client.get_list",
        args: {
          doctype: "Owner",
          filters: {
            user: currentUser
          },
          fields: ["name"]
        },
        callback: function(response) {
          if (response.message && response.message.length > 0) {
            var ownerName = response.message[0].name;
            console.log(ownerName, currentUser);
            frm.set_value("landlord", ownerName);
          }
        }
      });
    }
  });
  