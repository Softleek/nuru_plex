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


      const geoJSON = {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            properties: {},
            geometry: { type: "Point", coordinates: [36.930846133745185, -1.18069485] },
          },
        ],
      };
  
      const geoJSONString = JSON.stringify(geoJSON);
      if (!frm.doc.address) {
        frm.set_value("location", geoJSONString);
      }
    },


    location: async function (frm) {
      const geoJSON = JSON.parse(frm.doc.location);
  
      if (geoJSON && geoJSON.features && geoJSON.features.length > 0) {
        const lastFeature = geoJSON.features[geoJSON.features.length - 1];
        const coordinates = lastFeature.geometry.coordinates;
        const latitude = coordinates[1];
        const longitude = coordinates[0];
  
        try {
          const address = await getAddressFromCoordinates(latitude, longitude);
          if (address) {
            const flattenedAddress = {};
  
            for (const key in address) {
              if (
                typeof address[key] === "object" &&
                !Array.isArray(address[key])
              ) {
                for (const subKey in address[key]) {
                  flattenedAddress[subKey] = address[key][subKey];
                }
              } else {
                flattenedAddress[key] = address[key];
              }
            }
            console.log(flattenedAddress.city);
            frappe.call({
              method:
                "nuru_plex.nuru_plex.doctype.property.property.search_or_create_address",
              args: {
                address_data: JSON.stringify(flattenedAddress),
              },
              callback: function (r) {
                if (r.message) {
                  frm.set_value("address", r.message);
                }
              },
            });
          }
        } catch (error) {
          console.error("Error during reverse geocoding:", error);
        }
      }
    },
  });
  

//   async function getAddressFromCoordinates(latitude, longitude) {
//     const apiKey = 'AIzaSyB1m2K4hUES98q5yKk1wCsFge6VFFOXGEE'; // Replace 'YOUR_API_KEY' with your actual Google Maps API key
//     const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${apiKey}`;
//     console.log(latitude, longitude, url);
  
//     try {
//         const response = await fetch(url);
//         const data = await response.json();
//         console.log(data);
//         if (data.results && data.results.length > 0) {
//             return data.results[0].formatted_address;
//         } else {
//             return "Address not found";
//         }
//     } catch (error) {
//         console.error("Error during reverse geocoding:", error);
//         return "Error fetching address";
//     }
// }


  
  async function getAddressFromCoordinates(latitude, longitude) {
    const url = `https://geocode.maps.co/reverse?lat=${latitude}&lon=${longitude}`;
    console.log(latitude, longitude, url);
  
    return fetch(url)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.address) {
          return data;
        }
        return "Address not found";
      })
      .catch((error) => {
        console.error("Error during reverse geocoding:", error);
        return "Error fetching address";
      });
  }
  
  
  
  
  // frappe.ui.form.on("Building", {
  //   number_of_units: function (frm, cdt, cdn) {
  //     let item = locals[cdt][cdn];
  //     if (!item.address) {
  //         const geoJSON = {
  //       type: "FeatureCollection",
  //       features: [
  //         {
  //           type: "Feature",
  //           properties: {},
  //           geometry: { type: "Point", coordinates: [36.930846133745185, -1.18069485] },
  //         },
  //       ],
  //     };
  
  //     const geoJSONString = JSON.stringify(geoJSON);
  //     frappe.model.set_value(cdt, cdn, "location", geoJSONString);
  //     }
  // },
    
  //   location: async function (frm, cdt, cdn) {
  //     let item = locals[cdt][cdn];
  //     const geoJSON = JSON.parse(item.location);
  
  //     if (geoJSON && geoJSON.features && geoJSON.features.length > 0) {
  //       const lastFeature = geoJSON.features[geoJSON.features.length - 1];
  //       const coordinates = lastFeature.geometry.coordinates;
  //       const latitude = coordinates[1];
  //       const longitude = coordinates[0];
  
  //       try {
  //         const address = await getAddressFromCoordinates(latitude, longitude);
  //         if (address) {
  //           const flattenedAddress = {};
  
  //           for (const key in address) {
  //             if (
  //               typeof address[key] === "object" &&
  //               !Array.isArray(address[key])
  //             ) {
  //               for (const subKey in address[key]) {
  //                 flattenedAddress[subKey] = address[key][subKey];
  //               }
  //             } else {
  //               flattenedAddress[key] = address[key];
  //             }
  //           }
  //           console.log(flattenedAddress.city);
  //           frappe.call({
  //             method:
  //               "takataka_solutions.services.contact.search_or_create_address",
  //             args: {
  //               address_data: JSON.stringify(flattenedAddress),
  //             },
  //             callback: function (r) {
  //               if (r.message) {
  //                 // frm.set_value("address", r.message);
  //                 frappe.model.set_value(
  //                     cdt,
  //                     cdn,
  //                     "address",
  //                     r.message
  //                   );
  //               }
  //             },
  //           });
  //         }
  //       } catch (error) {
  //         console.error("Error during reverse geocoding:", error);
  //       }
  //     }
  //   },
  //   refresh: function (frm) {
  //       console.log(8989)
  //     const geoJSON = {
  //       type: "FeatureCollection",
  //       features: [
  //         {
  //           type: "Feature",
  //           properties: {},
  //           geometry: { type: "Point", coordinates: [36.930846133745185, -1.18069485] },
  //         },
  //       ],
  //     };
  
  //     const geoJSONString = JSON.stringify(geoJSON);
  //     if (!frm.doc.address) {
  //       frm.set_value("location", geoJSONString);
  //     }
  //   },
  // });
  
  
  
  // frappe.ui.form.on("Contact", "building_on_form_rendered", function (doc, cdt, cdn) {
  //     let child_table = locals[cdt][cdn].building;
  //     console.log(child_table);
  
  //     const gpsLocationContainer = $('div[data-fieldname="location"]', doc.wrapper);
  //     // gpsLocationContainer.html(`
  //     //     <div class="frappe-control" data-fieldtype="Geolocation" data-fieldname="geo_location">
  //     //         <div class="form-group">
  //     //             <div class="clearfix">
  //     //                 <label class="control-label" style="padding-right: 0px;">Location</label>
  //     //                 <span class="help"></span>
  //     //             </div>
  //     //             <div class="control-input-wrapper">
  //     //                 <div class="control-input hidden" style="display: block;"><input type="text" autocomplete="off" class="input-with-feedback form-control" data-fieldtype="Geolocation" data-fieldname="location" placeholder="" data-doctype="Testt"></div>
  //     //                 <div class="control-value" style="display: block;">
  //     //                     <div class="map-wrapper border">
  //     //                         <div id="unique-0" style="min-height: 400px; z-index: 1; max-width: 100%; position: relative;" class="leaflet-container leaflet-touch leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom" tabindex="0">
  //     //                             <div class="leaflet-pane leaflet-map-pane" style="transform: translate3d(-107px, 0px, 0px);">
  //     //                                 <div class="leaflet-pane leaflet-tile-pane">
  //     //                                     <div class="leaflet-layer" style="z-index: 1; opacity: 1;">
  //     //                                         <!-- Your missing <div> elements go here -->
  //     //                                         <div class="leaflet-tile-container leaflet-zoom-animated" style="z-index: 18; transform: translate3d(0px, 0px, 0px) scale(1);">
  //     //                                             <img alt="" role="presentation" src="https://tile.openstreetmap.org/13/5754/3653.png" class="leaflet-tile leaflet-tile-loaded" style="width: 256px; height: 256px; transform: translate3d(295px, 54px, 0px); opacity: 1;">
  //     //                                         </div>
  //     //                                         <!-- End of missing <div> elements -->
  //     //                                     </div>
  //     //                                 </div>
  //     //                             </div>
  //     //                             <!-- Rest of the HTML content -->
  //     //                         </div>
  //     //                     </div>
  //     //                     <p class="help-box small text-muted"></p>
  //     //                 </div>
  //     //             </div>
  //     //             <span class="tooltip-content">location</span>
  //     //         </div>
  //     //     </div>
  //     // `);
  
  //     // Loop through the rows in the child table
  //     $.each(child_table, function(index, row) {
  //         // Update the field in each row
  //         const geoJSON = {
  //             type: "FeatureCollection",
  //             features: [
  //                 {
  //                     type: "Feature",
  //                     properties: {},
  //                     geometry: { type: "Point", coordinates: [36.930846133745185, -1.18069485] },
  //                 },
  //             ],
  //         };
  
  //         const geoJSONString = JSON.stringify(geoJSON);
  //         frappe.model.set_value(row.doctype, row.name, 'number_of_units', 0);
  //         frappe.model.set_value(row.doctype, row.name, 'building_name', '');
  //     });
  // });
  
  
  
  // async function getAddressFromCoordinates(latitude, longitude) {
  //   const url = `https://geocode.maps.co/reverse?lat=${latitude}&lon=${longitude}`;
  
  //   return fetch(url)
  //     .then((response) => response.json())
  //     .then((data) => {
  //       console.log(data);
  //       if (data.address) {
  //         return data;
  //       }
  //       return "Address not found";
  //     })
  //     .catch((error) => {
  //       console.error("Error during reverse geocoding:", error);
  //       return "Error fetching address";
  //     });
  // }
  
  
  
  
  // frappe.ui.form.on('Contact', {
  // 	refresh(frm) {
  // 	    let contact_name = frm.doc.first_name
  // 	    if(contact_name){
  // 	        frappe.call({
  //                 method: "takataka_solutions.services.rest.get_building",
  //                 args: {
  //                   contact_name: contact_name,
  //                 },
  //                 callback: function (r) {
  //                   frm.fields_dict.contact_list.grid.update_docfield_property( "building", "options", r.message);
  //                 },
  //               });
  // 	    }
        
  //     	    var buiding_length = frm.doc.building.length;
  //     	    console.log(buiding_length)
  //     	    if(buiding_length>0 && frm.doc.first_name){
  //     	         var field2 = ['contact_list'];
  //                 	field2.forEach(function (fields2) {
  //                 		frm.set_df_property(fields2, 'hidden', 0);
  //                 	});
  //     	    }
  // 	     setTimeout(() => {
  //             frm.remove_custom_button('Invite as User');
  //         }, 1000);
          
  //          frm.add_custom_button(__('Contact List'), function(){
  //             frappe.set_route('form', "Customer")
  //         }).addClass('btn-primary');
      
  // 		frm.set_query("territory", function () {
  //             return {
  //                 "filters": {
  //                     "is_group": 0
  //                 }
  //             };
  //         });
  //         frm.set_query("contact_category", function () {
  //             return {
  //                 "filters": {
  //                     "is_group": 0
  //                 }
  //             };
  //         });
  //         frm.set_query("contact_sub_category", function () {
  //             return {
  //                 "filters": {
  //                     "parent": frm.doc.contact_category
  //                 }
  //             };
  //         });
          
  //         let contact_category = frm.doc.contact_category
  // 	    if(contact_category==="Residential"|| contact_category==="Commercial"){
  // 	            ContactSubGroup(frm)
  // 	    }else{
  // 	        HideContactSubGroup(frm)
  // 	    }
  // 	},
    
  // 	after_save: function(frm){
  // 	   frappe.call({
  //             method: "takataka_solutions.services.rest.create_customer",
  //             args: {
  //                 'name': frm.doc.name,
  //             },
  //             callback: function (r) {
      
  //             }
  //         });
  // 	},
    
  // 	contact_category: function(frm){
  // 	    let contact_category = frm.doc.contact_category
  // 	    if(contact_category==="Residential" || contact_category==="Commercial"){
  // 	            ContactSubGroup(frm)
  // 	    }else{
  // 	        HideContactSubGroup(frm)
  // 	    }
  // 	}
  // })
  
  // function ContactSubGroup(frm){
  //         var field = ['contact_sub_category'];
  //     	field.forEach(function(fields) {
  //     		frm.set_df_property(fields, 'hidden', 0);
  //     		frm.set_df_property(fields, 'reqd', 1);
  //     	}); 
  // }
  // function HideContactSubGroup(frm){
  //         var field = ['contact_sub_category'];
  //     	field.forEach(function(fields) {
  //     		frm.set_df_property(fields, 'hidden', 1);
  //     		frm.set_df_property(fields, 'reqd', 0);
  //     	}); 
  // }