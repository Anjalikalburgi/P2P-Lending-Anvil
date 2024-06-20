from ._anvil_designer import edit_technical_issueTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class edit_technical_issue(edit_technical_issueTemplate):
  def __init__(self,selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.text_box_1.text = selected_row['subcategory_technical_issue']
        # Store the selected row for later use
    self.selected_row = selected_row

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    update = self.text_box_1.text.strip()
    if not update:
        alert("Please enter a valid data.")
        return
    self.selected_row['subcategory_technical_issue'] = update
    self.selected_row.update()
    alert("Changes saved successfully!")
    open_form('admin.dashboard.manage_cms.manage_issues_dropdown')

  def delete_button(self, **event_args):
    confirmation = alert(
            "Are you sure you want to delete this data?",
            title="Confirm Deletion",
            buttons=[("Cancel", False), ("Delete", True)],
        )
    if confirmation:
      # name = self.selected_row['borrower_subcategory_loan_issue']
      self.selected_row.delete()
      alert('Data Deleted Successfully!')
      open_form('admin.dashboard.manage_cms.manage_issues_dropdown')

  def button_2_click(self, **event_args):
    open_form('admin.dashboard.manage_cms.loan_subcategory_dropdown')

