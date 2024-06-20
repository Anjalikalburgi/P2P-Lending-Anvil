from ._anvil_designer import ItemTemplate113Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate113(ItemTemplate113Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    item_data = self.item
    open_form('admin.dashboard.manage_cms.loan_subcategory_dropdown.edit_technical_issue', selected_row=item_data)
    
