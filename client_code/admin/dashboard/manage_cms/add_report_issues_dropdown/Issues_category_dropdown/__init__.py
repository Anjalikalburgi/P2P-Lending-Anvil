from ._anvil_designer import Issues_category_dropdownTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Issues_category_dropdown(Issues_category_dropdownTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_9_click(self, **event_args):
    self.refresh()
    self.column_panel_3.visible = True
   

  def button_1_click(self, **event_args):
    open_form('admin.dashboard.manage_cms.add_report_issues_dropdown')

  def refresh(self):
    self.repeating_panel_1.items = app_tables.fin_issue_category.search()

  def loan_category_click(self, **event_args):
    
    enter_data = self.text_box_2.text

    valid_statuses = ['Loan Issues', 'Technical Issues', 'Other']
    if enter_data not in valid_statuses:
      alert("Please enter a valid Loan Issue Category: 'Loan Issues', 'Technical Issue', 'Other'.")
      return
    app_tables.fin_issue_category.add_row(issue_category=enter_data)
    self.text_box_2.text = ' '
    self.refresh()

  