from ._anvil_designer import star_1_borrower_registration_form_2_employment_business_2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class star_1_borrower_registration_form_2_employment_business_2(star_1_borrower_registration_form_2_employment_business_2Template):
  def __init__(self, user_id,**properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      #self.text_box_1.text=user_data['nearest_location']
      self.drop_down_1.selected_value=user_data['business_type']
      options_2 = app_tables.fin_borrower_no_of_employees.search()
      option_strings_2 = [str(option['borrower_no_of_employees']) for option in options_2]
      self.drop_down_2.items = option_strings_2
      self.drop_down_2.selected_value = user_data['employees_working']

      user_data.update()

        # Populate drop_down_1 with data from 'business_type' column
    options_1 = app_tables.fin_borrower_business_type.search()
    option_strings_1 = [str(option['borrower_business_type']) for option in options_1]
    self.drop_down_1.items = option_strings_1
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    #nearest_loc = self.text_box_1.text
    business_type = self.drop_down_1.selected_value
    empolyees_working = self.drop_down_2.selected_value
    year = self.date_picker_1.date
    #month = self.date_picker_1.date.year
    user_id = self.userId
    if   not business_type or not empolyees_working or not year:
      Notification("Please fill all the fields").show()
    else:
      today = datetime.today()
      months = today.year * 12 + today.month - year.year * 12 - year.month
      anvil.server.call('add_lendor_institutional_form_2',business_type,empolyees_working,year,months,user_id, )
      open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_3',user_id = user_id)
      """This method is called when the button is clicked"""

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_1',user_id=user_id)
    """This method is called when the button is clicked"""

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")
