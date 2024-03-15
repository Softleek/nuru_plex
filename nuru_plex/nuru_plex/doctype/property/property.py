# Copyright (c) 2024, Nuru and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import cloudinary
import cloudinary.uploader
import cloudinary.api
from frappe.utils.file_manager import delete_file

class Property(Document):
    def before_save(self):
        for image_row in self.get("images"):
            if not image_row.link:
                cloudinary.config(
                    cloud_name="dwlzooqso",
                    api_key="857659825572139",
                    api_secret="qeWb7SIa5AtWNGMHad3LriPp98Q",
                )
                localhost_url = frappe.utils.get_url()
                file_path = f"{localhost_url}{image_row.image}"
                upload_result = cloudinary.uploader.upload(
                    file_path, folder=f"house_images/{self.name}", use_filename=True, public_id=image_row.label
                )
                if upload_result.get("secure_url"):
                    image_row.link = upload_result["secure_url"]
                    delete_file(image_row.image)
                    image_row.image = upload_result["secure_url"]
                else:
                    frappe.throw("Failed to upload image to Cloudinary")


@frappe.whitelist()
def search_or_create_address(address_data):
    address_dict = frappe.parse_json(address_data)
    existing_address = frappe.get_all(
        "Property Address",
        filters={
            "address_title": address_dict.get("display_name"),
        },
        fields=["name"],
        limit=1,
    )

    if existing_address:
        address_doc = frappe.get_doc("Property Address", existing_address[0].name)
    else:
        address_doc = frappe.new_doc("Property Address")

    address_fields = {
        "address_title": address_dict.get("display_name", ""),
        "address_line1": address_dict.get("road", "display_name"),
        "address_line2": address_dict.get("suburb", ""),
        "ammenity": address_dict.get(
            "amenity", address_dict.get("display_name", "").split(",")[0]
        ),
        "city_district": address_dict.get("city_district", ""),
        "suburb": address_dict.get("suburb", ""),
        "town": address_dict.get("county", ""),
        "state": address_dict.get("region", ""),
        "country": address_dict.get("country", ""),
        "pincode": address_dict.get("postcode", ""),
        "longitude": address_dict.get("lon", ""),
        "lattitude": address_dict.get("lat", ""),
    }

    city = address_dict.get("city", "")
    town = address_dict.get("town", "")

    if city:
        address_fields["city"] = city
    elif town:
        address_fields["city"] = town
    else:
        address_fields["city"] = "N/A"

    address_doc.update(address_fields)
    address_doc.save()

    return address_doc.name
