import frappe
from frappe.utils import get_url, random_string
import time

def create_user(full_name, phone, email, is_owner=False):
    password = random_string(5)
    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "mobile_no": phone,
        "first_name": full_name,
        "send_welcome_email": 0,
        "new_password": password
    })
    user.insert()
    send_welcome_email(email, password, full_name)
    if is_owner:
        user.add_roles("Landlord")
    user.save()
    time.sleep(5)
    return user

def send_welcome_email(email, password, full_name):
    subject = "Welcome to Nyumba Plex - Your Housing Management System!"
    message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; font-size: 14px;">
            <p>Hello {full_name},</p>
            <p>Welcome to Nyumba Plex, your comprehensive Housing Management System!</p>
            <p>We are thrilled to have you on board.</p>
            <p>Your login details for Nyumba Plex are as follows:</p>
            <ul>
                <li><strong>Email:</strong> {email}</li>
                <li><strong>Password:</strong> {password}</li>
            </ul>
            <p>Please log in at your convenience using the link below:</p>
            <p><a href="{get_url()}">Login here</a></p>
            <p>Once logged in, you'll have access to various features to manage your housing needs efficiently.</p>
            <p>Thank you for choosing us!</p>
            <p>Best regards,<br/>The Nyumba Plex Team</p>
        </body>
    </html>
    """
    frappe.sendmail(
        recipients=email,
        sender=None,
        subject=subject,
        message=message
    )
    return "Email sent successfully"

@frappe.whitelist()
def create_owner_user(full_name, phone, email):
    return create_user(full_name, phone, email, is_owner=True)

@frappe.whitelist()
def create_tenant_user(full_name, phone, email):
    return create_user(full_name, phone, email)
