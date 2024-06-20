from ._anvil_designer import manage_issues_dropdownTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class manage_issues_dropdown(manage_issues_dropdownTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def Manage_issues_click(self, **event_args):
    open_form('admin.dashboard.manage_cms.manage_issues')

  def button_21_copy_copy_click(self, **event_args):
    open_form('admin.dashboard.manage_cms.add_report_issues_dropdown')

  def button_1_click(self, **event_args):
    open_form('admin.dashboard.manage_cms')

