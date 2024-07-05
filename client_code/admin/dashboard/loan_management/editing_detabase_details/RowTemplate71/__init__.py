from ._anvil_designer import RowTemplate71Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate71(RowTemplate71Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.refresh_data_bindings()
    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    loan_details = self.item
    open_form('admin.dashboard.loan_management.editing_detabase_details.edit',loan_details = None,emi_details = loan_details,extension_details = None,foreclosure_details=None)
    # self.item['next_payment'] = self.date_picker_2.date
    # self.item['scheduled_payment'] = self.date_picker_1.date
    # self.item.update()
    # self.refresh_data_bindings()
    # alert('data saved')

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.item.delete()
    
    alert('data deleted')
