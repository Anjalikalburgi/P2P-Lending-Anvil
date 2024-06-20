from ._anvil_designer import field_engineerTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class field_engineer(field_engineerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    open_form('admin.dashboard.manage_cms.manage_issues')

  def Manage_issues_click(self, **event_args):
    self.column_panel_1.visible = True
    self.repeating_panel_1.items = app_tables.fin_field_engineers.search()

