from ._anvil_designer import star_1_borrower_registration_form_2_employment_farmerTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class star_1_borrower_registration_form_2_employment_farmer(star_1_borrower_registration_form_2_employment_farmerTemplate):
    def __init__(self, user_id, **properties):
        self.userId = user_id
        user_data = app_tables.fin_user_profile.get(customer_id=user_id)
        if user_data:
            self.drop_down_1.selected_value = user_data['land_type']
            self.text_box_1.text = str(user_data['total_acres'])  # Convert to string
            self.text_box_2.text = user_data['crop_name']
            self.text_box_3.text = user_data['farmer_earnings']

            options_2 = app_tables.fin_borrower_land_type.search()
            option_strings_2 = [str(option['land_type']) for option in options_2]
            self.drop_down_1.items = option_strings_2

            user_data.update()

        self.init_components(**properties)

    def button_2_click(self, **event_args):
        land_type = self.drop_down_1.selected_value
        total_acres = self.text_box_1.text
        crop_name = self.text_box_2.text
        farmer_earnings = self.text_box_3.text
        user_id = self.userId
        if not re.match(r'^[A-Za-z\s]+$', crop_name):
          alert('Enter valid crop name')
        elif not total_acres.isdigit():
          Notification("Acres of Land should be valid").show()
        elif not farmer_earnings.isdigit():
           Notification("Yearly Income should be valid").show()
        elif not land_type or not total_acres or not crop_name or not farmer_earnings:
            Notification("Please fill all the fields").show()
        else:
            anvil.server.call('add_borrower_farmer', land_type, total_acres, crop_name, farmer_earnings, user_id)
            open_form('borrower_registration_form.star_1_borrower_registration_form_3_marital', user_id=self.userId)

    def button_1_click(self, **event_args):
        user_id = self.userId
        open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment', user_id=self.userId)

    def button_3_click(self, **event_args):
        open_form("bank_users.user_form")
