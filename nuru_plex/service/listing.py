# custom_app/custom_app/api/custom_api.py

import frappe

@frappe.whitelist(allow_guest=True)
def houses_list(start=0, limit=6, filters=None):
    # Parse filters if provided
    if filters:
        filters = frappe.parse_json(filters)
    else:
        filters = {}

    # Fetch total count of unique houses under the same constraints (without limit)
    total_houses_count = frappe.db.sql("""
        SELECT
            COUNT(DISTINCT h.name) as total_count
        FROM
            `tabHouse` h
        INNER JOIN
            `tabProperty` p ON h.property = p.name
        LEFT JOIN
            `tabHouse Images` i ON h.name = i.parent
        WHERE
            h.status = 'Vacant'
        GROUP BY
            h.property, h.type, h.rent_amount, h.status, p.description
    """, as_dict=True)
    
    total_houses_count = len(total_houses_count)

    # Fetch unique houses based on property, type, rent_amount, and status = Vacant
    unique_houses = frappe.db.sql("""
        SELECT
            h.name as house_id, h.property, h.type, h.rent_amount, h.status,
            p.description as property_description,
            COUNT(h.name) as units,
            GROUP_CONCAT(DISTINCT i.image) as house_images
        FROM
            `tabHouse` h
        INNER JOIN
            `tabProperty` p ON h.property = p.name
        LEFT JOIN
            `tabHouse Images` i ON h.name = i.parent
        WHERE
            h.status = 'Vacant'
        GROUP BY
            h.property, h.type, h.rent_amount, h.status, p.description
        ORDER BY
            h.rent_amount
        LIMIT %s, %s
    """, (int(start), int(limit)), as_dict=True)

    # Fetch total count of unique houses within limit
    total_houses = len(unique_houses)

    for house in unique_houses:
        if not house['house_images']:
            # If house images are empty, use property images
            property_images = frappe.get_all("House Images", filters={"parent": house['property']}, fields=["image"])
            house['house_images'] = [img['image'] for img in property_images]

        # Fetch amenities for the property
        amenities = frappe.get_all("House Ammenity", filters={"parent": house['property']}, fields=["ammenity"])
        house['amenities'] = [amenity['ammenity'] for amenity in amenities]

    return {
        "total_count": total_houses_count,
        "houses": unique_houses
    }




@frappe.whitelist(allow_guest=True)
def house_single(id):
    # Fetch details of the house with the provided name
    house = frappe.get_doc("House", id)

    if house:
        # Fetch property details associated with the house
        property_details = frappe.get_doc("Property", house.property)

        # Fetch property address
        property_address = frappe.get_doc("Property Address", property_details.address )

        # Fetch owner (landlord) details
        owner_details = frappe.get_doc("Owner", property_details.landlord)

        # Return house, property, property address, and owner details as dictionaries
        return {
            "house": house.as_dict(),
            "property": property_details.as_dict(),
            "property_address": property_address,
            "owner": owner_details.as_dict(),
            "featured_property": houses_list(start=0, limit=6)
        }
    else:
        return "House not found"




# @frappe.whitelist(allow_guest=True)
# def house_single(id):
    # Fetch details of the house with the provided name
    house = frappe.db.sql("""
        SELECT
            h.name as house_id, h.property, h.type, h.rent_amount, h.status,
            p.description as property_description,
            GROUP_CONCAT(DISTINCT i.image) as house_images
        FROM
            `tabHouse` h
        INNER JOIN
            `tabProperty` p ON h.property = p.name
        LEFT JOIN
            `tabHouse Images` i ON h.name = i.parent
        WHERE
            h.name = %s
    """, (id,), as_dict=True)

    if house:
        house = house[0]
        if not house['house_images']:
            # If house images are empty, use property images
            property_images = frappe.get_all("House Images", filters={"parent": house['property']}, fields=["image"])
            house['house_images'] = [img['image'] for img in property_images]

        # Fetch amenities for the property
        amenities = frappe.get_all("House Ammenity", filters={"parent": house['property']}, fields=["ammenity"])
        house['amenities'] = [amenity['ammenity'] for amenity in amenities]

        return house
    else:
        return "House not found"