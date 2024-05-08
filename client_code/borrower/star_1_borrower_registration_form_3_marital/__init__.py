from ._anvil_designer import star_1_borrower_registration_form_3_maritalTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class star_1_borrower_registration_form_3_marital(star_1_borrower_registration_form_3_maritalTemplate):
  def __init__(self,user_id, **properties):
    # Set Form properties and Data Bindings.
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.marital_status_borrower_registration_dropdown.selected_value=user_data['marital_status']
      user_data.update()

    options = app_tables.fin_borrower_marrital_status.search()
    options_string = [str(option['borrower_marrital_status']) for option in options]
    self.marital_status_borrower_registration_dropdown.items = options_string
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def home_borrower_registration_form_copy_1_click(self, **event_args):
    open_form('bank_users.user_form')

  def button_next_click(self, **event_args):
      marital_status = self.marital_status_borrower_registration_dropdown.selected_value
      user_id = self.userId
  
      if not marital_status or marital_status not in ['Not Married', 'Married', 'Other']:
          Notification("Please select a valid marital status").show()
      else:
          # Call the server function before opening the next form
          anvil.server.call('add_borrower_step3', marital_status, user_id)
  
          open_form('borrower_registration_form.star_1_borrower_registration_form_3_marital.star_1_borrower_registration_form_3_marital_married',
                    user_id=user_id, marital_status=marital_status)

      # else:
      #   open_form('borrower_registration_form.star_1_borrower_registration_form_3_marital',user_id = user_id)
      #   alert('Please select a valid marital status')

  
  def button_1_click(self, **event_args):
    open_form('borrower_registration_form.star_1_borrower_registration_form_2_employment',user_id=self.userId)


    
    
    
    
 