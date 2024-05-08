from ._anvil_designer import RowTemplate6Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
from ... import main_form_module  # Adjusted import path

class RowTemplate6(RowTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user_id = main_form_module.userId
    user_data = app_tables.fin_user_profile.get(customer_id=self.user_id)
    if user_data:
            self.image_1.source = user_data['user_photo']


    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    selected_row = self.item
    open_form('borrower_registration_form.dashboard.foreclosure_request.borrower_foreclosure', selected_row=selected_row)

