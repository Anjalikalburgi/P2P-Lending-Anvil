from ._anvil_designer import RowTemplate15Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class RowTemplate15(RowTemplate15Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def view_profile_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    selcted_row=self.item
    open_form('borrower_registration_form.dashboard.view_loans.view_profile',selected_row=selcted_row)
