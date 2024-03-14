# Copyright (c) 2024, Nuru and contributors
# For license information, please see license.txt

import frappe
import os
from frappe.model.document import Document

import cloudinary
import cloudinary.uploader
import cloudinary.api
from frappe.utils.file_manager import delete_file


class House(Document):
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
                    file_path, folder=f"house_images/{self.property}", use_filename=True
                )
                if upload_result.get("secure_url"):
                    image_row.link = upload_result["secure_url"]
                    delete_file(image_row.image)
                    image_row.image = upload_result["secure_url"]
                else:
                    frappe.throw("Failed to upload image to Cloudinary")
