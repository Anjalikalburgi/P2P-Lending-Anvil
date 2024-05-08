from ._anvil_designer import star_1_borrower_registration_form_2_self_employmentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class star_1_borrower_registration_form_2_self_employment(star_1_borrower_registration_form_2_self_employmentTemplate):
  def __init__(self, user_id,**properties):
    # Set Form properties and Data Bindings.
    self.userId = user_id
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    user_data = app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.drop_down_1.selected_value = user_data['self_employment']
      user_data.update()
    options = app_tables.fin_self_employment.search()
    options_string = [str(option['self_employment']) for option in options]
    self.drop_down_1.items = options_string

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    status_of_user = self.drop_down_1.selected_value
    user_id = self.userId
    if status_of_user not in ['Business', 'Farmer']:
      Notification("Please select a valid profession status").show()
    elif not user_id:
      Notification("User ID is missing").show()
    else:
     anvil.server.call('add_borrwer_self_employment',status_of_user,user_id)
    if status_of_user == 'Business':
       open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_1',user_id=user_id)
    elif status_of_user == 'Farmer':
      open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_farmer',user_id=user_id)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment',user_id=self.userId)
