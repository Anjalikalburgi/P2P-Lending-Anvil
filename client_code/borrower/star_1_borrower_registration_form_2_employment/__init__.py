from ._anvil_designer import star_1_borrower_registration_form_2_employmentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class star_1_borrower_registration_form_2_employment(star_1_borrower_registration_form_2_employmentTemplate):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
     self.Profesion_borrower_registration_form_drop_down.selected_value=user_data['profession']
     user_data.update()

    options = app_tables.fin_borrower_profession.search()
    option_strings = [str(option['borrower_profession']) for option in options]
    self.Profesion_borrower_registration_form_drop_down.items = option_strings
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def home_borrower_registration_form_copy_1_click(self, **event_args):
    open_form('bank_users.user_form')

  def button_1_click(self, **event_args):
    open_form('borrower_registration_form.star_1_borrower_registration_form_1_education',user_id=self.userId)

  def button_1_next_click(self, **event_args):
    status_of_user = self.Profesion_borrower_registration_form_drop_down.selected_value
    user_id = self.userId
    if status_of_user not in ['Student', 'Employee', 'Self employment']:
      Notification("Please select a valid profession status").show()
    elif not user_id:
      Notification("User ID is missing").show()
    else:
     anvil.server.call('add_borrower_step2',status_of_user,user_id)
    if status_of_user == 'Student':
      open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_student',user_id=user_id)
    elif status_of_user == 'Employee':
      open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_1',user_id=user_id)
    elif status_of_user == 'Self employment':
      open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_self_employment',user_id=user_id) 
    # else:
    #   open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment',user_id=user_id)
    #   alert('Please select a valid Profesion')