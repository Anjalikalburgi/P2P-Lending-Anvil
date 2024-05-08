from ._anvil_designer import star_1_borrower_registration_form_2_employment_business_1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class star_1_borrower_registration_form_2_employment_business_1(star_1_borrower_registration_form_2_employment_business_1Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_1.text=user_data['business_name']
      self.text_box_3.text=user_data['business_add']
      self.drop_down_1.selected_value=user_data['business_type']
      options_2 = app_tables.fin_borrower_no_of_employees.search()
      option_strings_2 = [str(option['borrower_no_of_employees']) for option in options_2]
      self.drop_down_2.items = option_strings_2
      self.drop_down_2.selected_value = user_data['employees_working']
      
      user_data.update()
    # Set Form properties and Data Bindings.
    options_1 = app_tables.fin_borrower_business_type.search()
    option_strings_1 = [str(option['borrower_business_type']) for option in options_1]
    self.drop_down_1.items = option_strings_1
    
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    business_name = self.text_box_1.text
    business_add = self.text_box_3.text
    business_type = self.drop_down_1.selected_value
    empolyees_working = self.drop_down_2.selected_value
    user_id = self.userId
    if not re.match(r'^[A-Za-z\s]+$', business_name):
      alert('Enter valid business name')
    elif not business_name or not business_add or not business_type or not empolyees_working:
        Notification("Please fill all the fields").show()
    else:
      anvil.server.call('add_lendor_institutional_form_1',business_name,business_add,business_type,empolyees_working,user_id)
      open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_2',user_id=self.userId)


  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment',user_id=self.userId)
    

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")
