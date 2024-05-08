from ._anvil_designer import star_1_borrower_registration_form_2_employment_emp_detail_1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class star_1_borrower_registration_form_2_employment_emp_detail_1(star_1_borrower_registration_form_2_employment_emp_detail_1Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_1.text=user_data['company_name']
      self.drop_down_2.selected_value=user_data['organization_type']
      self.drop_down_1.selected_value=user_data['employment_type']
      self.drop_down_3.selected_value = user_data['occupation_type']
      
      
      user_data.update()

    options_1 = app_tables.fin_borrower_employee_type.search()
    option_strings_1 = [str(option['borrower_employee_type']) for option in options_1]
    self.drop_down_1.items = option_strings_1

        # Populate drop_down_2 with data from 'organization_type' column
    options_2 = app_tables.fin_borrower_organization_type.search()
    option_strings_2 = [str(option['borrower_organization_type']) for option in options_2]
    self.drop_down_2.items = option_strings_2

    options = app_tables.fin_occupation_type.search()
    option_strings = [str(option['occupation_type']) for option in options]
    self.drop_down_3.items = option_strings
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


  def button_2_click(self, **event_args):
    company_name = self.text_box_1.text    
    org_type = self.drop_down_2.selected_value
    emp_type = self.drop_down_1.selected_value
    occupation_type = self.drop_down_3.selected_value
    
    user_id = self.userId
    if not re.match(r'^[A-Za-z\s]+$', company_name):
      alert('Enter valid business name')
    elif not company_name or not org_type or not emp_type or not occupation_type:
      Notification("please fill the required fields ").show()
    else:
      anvil.server.call('add_lendor_individual_form_1', company_name,org_type,emp_type,occupation_type,user_id)
      open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_2',user_id=self.userId)




  # this is prev button
  def button_1_click(self, **event_args):
    open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment',user_id=self.userId)


  def button_3_click(self, **event_args):
    open_form("bank_users.user_form")
