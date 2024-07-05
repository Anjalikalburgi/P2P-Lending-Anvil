from ._anvil_designer import RowTemplate66Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime


class RowTemplate66(RowTemplate66Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.refresh_data_bindings()


  def save_button_click(self, **event_args):
    """This method is called when the save button is clicked"""
    loan_details = self.item
    open_form('admin.dashboard.loan_management.editing_detabase_details.edit',loan_details = loan_details,emi_details = None,extension_details = None,foreclosure_details=None)
    # self.item['first_emi_payment_due_date'] = self.date_picker_1.date
    # self.item['loan_disbursed_timestamp'] = self.date_picker_2.date
    # self.item.update()
    # alert('data saved')
    # self.refresh_data_bindings()

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    

