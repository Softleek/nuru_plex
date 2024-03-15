# custom_app/custom_app/api/custom_api.py

import frappe

@frappe.whitelist(allow_guest=True)
def houses_list(start=0, limit=4):
    # Fetch unique houses based on property, type, rent_amount, and status = Vacant
    total_houses = frappe.db.sql("""
        SELECT
            COUNT(DISTINCT h.name) as total_count
        FROM
            `tabHouse` h
        INNER JOIN
            `tabProperty` p ON h.property = p.name
        WHERE
            h.status = 'Vacant'
    """, as_dict=True)[0]['total_count']

    # Fetch subset of houses based on start and limit
    houses = frappe.db.sql("""
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
            h.status = 'Vacant'
        GROUP BY
            h.name, h.property, h.type, h.rent_amount, h.status, p.description
        LIMIT %s, %s
    """, (int(start), int(limit)), as_dict=True)

    for house in houses:
        if not house['house_images']:
            # If house images are empty, use property images
            property_images = frappe.get_all("House Images", filters={"parent": house['property']}, fields=["image"])
            house['house_images'] = [img['image_link'] for img in property_images]

        # Fetch amenities for the property
        amenities = frappe.get_all("House Ammenity", filters={"parent": house['property']}, fields=["ammenity"])
        house['amenities'] = [amenity['ammenity'] for amenity in amenities]

    return {
        "total_count": total_houses,
        "houses": houses
    }


@frappe.whitelist(allow_guest=True)
def house_single(id):
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
            house['house_images'] = [img['image_link'] for img in property_images]

        # Fetch amenities for the property
        amenities = frappe.get_all("House Ammenity", filters={"parent": house['property']}, fields=["ammenity"])
        house['amenities'] = [amenity['ammenity'] for amenity in amenities]

        return house
    else:
        return "House not found"