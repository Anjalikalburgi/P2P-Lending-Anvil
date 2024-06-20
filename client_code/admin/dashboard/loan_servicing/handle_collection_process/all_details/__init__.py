from ._anvil_designer import all_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class all_details(all_detailsTemplate):
  def __init__(self,selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.selected_row = selected_row


    self.borrower_id.text = f"{selected_row['borrower_customer_id']}"
    self.loan_id.text = f"{selected_row['loan_id']}"
    self.borrower_full_name.text = f"{selected_row['borrower_full_name']}"
    self.borrower_email.text = f"{selected_row['borrower_email_id']}"
    self.customer_address.text = f"{selected_row['street_adress_1']}"
    self.product_name.text = f"{selected_row['product_name']}"
    self.relative_name.text = f"{selected_row['guarantor_name']}"
    self.relative_relation.text = f"{selected_row['another_person']}"
    self.relative_number.text = f"{selected_row['guarantor_mobile_no']}"
    self.another_email.text = f"{selected_row['another_email']}"
    self.relative_address.text = f"{selected_row['guarantor_address']}"
    self.emi_number.text = f"{selected_row['emi_number']}"
    self.remaining_amount.text = f"{selected_row['total_remaining_amount']}"
    self.status.text = f"{selected_row['status']}"

    self.populate_field_engineer_dropdown()

  def populate_field_engineer_dropdown(self):
        street_address = self.selected_row['street_adress_1']
        # Call the server function to get field engineers
        field_engineers = anvil.server.call('find_nearby_field_engineers', street_address)
        self.field_engineer_dropdown.items = [(f"{fe['name']} ({fe['distance']:.2f} km)", fe) for fe in field_engineers]

  def field_engineer_dropdown_change(self, **event_args):
        """This method is called when a new item is selected in the dropdown"""
        selected_fe = self.field_engineer_dropdown.selected_value
        if selected_fe:
            # Display the map with selected field engineer and address
            self.show_map(self.selected_row['street_adress_1'], selected_fe['location'])

  def show_map(self, address, field_engineer_location):
        # Assuming you have a Map component in your form named `map_1`
        # You need to get the coordinates of the address and field engineer location
        address_coords = anvil.server.call('get_coordinates', address)
        fe_lat, fe_lng = map(float, field_engineer_location.split(", "))

        # Clear existing markers
        self.map_1.clear()

        # Add markers for the address and field engineer location
        self.map_1.add_marker(address_coords['lat'], address_coords['lng'], title="Customer Address")
        self.map_1.add_marker(fe_lat, fe_lng, title="Field Engineer Location")

        # Center the map between the two points
        self.map_1.fit_bounds([address_coords, {"lat": fe_lat, "lng": fe_lng}])

  
  # def populate_field_engineer_dropdown(self):
  #       street_address = self.selected_row['street_adress_1']
  #       # Call the server function to get field engineers
  #       field_engineers = anvil.server.call('find_nearby_field_engineers', street_address)
  #       self.field_engineer_dropdown.items = [(f"{fe['name']} ({fe['distance']:.2f} km)", fe) for fe in field_engineers]

  # def field_engineer_dropdown_change(self, **event_args):
  #       """This method is called when a new item is selected in the dropdown"""
  #       selected_fe = self.field_engineer_dropdown.selected_value
  #       if selected_fe:
  #           # Display the map with selected field engineer and address
  #           self.show_map(self.selected_row['street_adress_1'], selected_fe['location'])

  # def show_map(self, address, field_engineer_location):
  #       # Assuming you have a Map component in your form named `map_1`
  #       # You need to get the coordinates of the address and field engineer location
  #       address_coords = anvil.server.call('get_coordinates', address)
  #       fe_lat, fe_lng = map(float, field_engineer_location.split(", "))

  #       # Clear existing markers
  #       self.map_1.clear()

  #       # Add markers for the address and field engineer location
  #       self.map_1.add_marker(address_coords['lat'], address_coords['lng'], title="Customer Address")
  #       self.map_1.add_marker(fe_lat, fe_lng, title="Field Engineer Location")

  #       # Center the map between the two points
  #       self.map_1.fit_bounds([address_coords, {"lat": fe_lat, "lng": fe_lng}])

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.loan_servicing.handle_collection_process')
