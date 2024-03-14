# Copyright (c) 2024, Nuru and contributors
# For license information, please see license.txt

import frappe
import os
from frappe.model.document import Document

import cloudinary
import cloudinary.uploader
import cloudinary.api

class House(Document):
    def before_save(self):
        if self.image:
            # Configure Cloudinary
            cloudinary.config(
                cloud_name="dwlzooqso",
                api_key="857659825572139",
                api_secret="qeWb7SIa5AtWNGMHad3LriPp98Q"
            )

            localhost_url = frappe.utils.get_url()
            
            # Get the absolute file path
            file_path = f'{localhost_url}{self.image}'
            
            print(file_path, '\n\n\n', )
            
            # Upload image to Cloudinary
            upload_result = cloudinary.uploader.upload(file_path, folder="house_images", use_filename = True)

            # Check if upload was successful
            if upload_result.get("secure_url"):
                # Update the 'link' field with the Cloudinary URL
                self.link = upload_result["secure_url"]
            else:
                frappe.throw("Failed to upload image to Cloudinary")