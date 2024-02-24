import frappe
from frappe import auth


def generate_keys(user):
    user_doc = frappe.get_doc("User", user)
    api_secret = frappe.generate_hash(length=15)
    if not user_doc.api_key:
        api_key = frappe.generate_hash(length=15)
        user_doc.api_key = api_key

    user_doc.api_secret = api_secret
    user_doc.save()
    return api_secret


@frappe.whitelist(allow_guest=True)
def login(username, password):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=username, pwd=password)
        login_manager.post_login()

        secret = generate_keys(frappe.session.user)

        user = frappe.get_doc("User", frappe.session.user)
        frappe.response["message"] = {
            "success_key": 1,
            "sid": frappe.session.sid,
            "api_key": user.api_key,
            "api_secret": secret,
            "username": user.username,
            "email": user.email,
        }
    except Exception as e:
        return e
