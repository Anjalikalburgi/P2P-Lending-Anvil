from ._anvil_designer import RowTemplate41Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate41(RowTemplate41Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

   
  def button_1_click_click(self, **event_args):
    selcted_row=self.item
    open_form('admin.dashboard.manage_cms.manage_issues.field_engineer', selected_row=selcted_row)

