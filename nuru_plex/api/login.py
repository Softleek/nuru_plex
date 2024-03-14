import frappe
from frappe import auth
import random
import string


def generate_random_password(length=5):
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(random.choice(letters_and_digits) for i in range(length))


@frappe.whitelist(allow_guest=True)
def social_login(email, first_name):
    login_manager = frappe.auth.LoginManager()
    login_manager.authenticate(user="Administrator", pwd="1")
    login_manager.post_login()
    try:
        
        existing_user = frappe.get_all(
            "User", filters={"email": email}, fields=["name"]
        )

        print(frappe.session.user)
        if existing_user:
            user = frappe.get_doc("User", existing_user[0].name)
            secret = generate_keys(user)
        else:
            random_password = generate_random_password()
            user = frappe.get_doc(
                {
                    "doctype": "User",
                    "email": email,
                    "first_name": first_name,
                    "send_welcome_email": 0,
                    "new_password": random_password,
                }
            )
            user.insert()
            secret = generate_keys(user)


        frappe.response["message"] = {
            "success_key": 1,
            "sid": frappe.session.sid,
            "api_key": user.api_key,
            "api_secret": secret,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
        }
    except Exception as e:
        return str(e)


def generate_keys(user):
    login_manager = frappe.auth.LoginManager()
    login_manager.authenticate(user="Administrator", pwd="1")
    login_manager.post_login()
    api_secret = frappe.generate_hash(length=15)
    if not user.api_key or len(user.api_key) < 15:
        api_key = frappe.generate_hash(length=15)
        user.api_key = api_key

    user.api_secret = api_secret
    user.save()
    return api_secret


@frappe.whitelist(allow_guest=True)
def login(username, password):
    try:
        login_manager = frappe.auth.LoginManager()
        print(username)
        login_manager.authenticate(user=username, pwd=password)
        login_manager.post_login()

        user = frappe.get_doc("User", frappe.session.user)
        if user:
            print(user)
            secret = generate_keys(user)
            frappe.response["message"] = {
                "success_key": 1,
                "sid": frappe.session.sid,
                "api_key": user.api_key,
                "api_secret": secret,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
            }
        else:
            frappe.response["message"] = {
                "error": "Wrong credentials"
            }
    except Exception as e:
        return e
