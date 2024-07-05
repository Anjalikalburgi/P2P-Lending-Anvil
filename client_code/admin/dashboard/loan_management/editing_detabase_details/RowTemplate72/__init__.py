from ._anvil_designer import RowTemplate72Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate72(RowTemplate72Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_data_bindings()
    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    loan_details = self.item
    open_form('admin.dashboard.loan_management.editing_detabase_details.edit',loan_details = None,emi_details = None,extension_details = loan_details,foreclosure_details=None)
    # self.item['next_payment'] = self.date_picker_2.date
    # self.item['emi_number'] = int(self.text_box_3.text)
    # self.item['extension_request_date'] = self.date_picker_1.date
    # self.item['status'] = self.text_box_6.text
    # self.item['total_extension_months'] = int(self.text_box_7.text)
    # self.item.update()
    # self.refresh_data_bindings()
    # alert('data saved')