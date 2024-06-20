from ._anvil_designer import edit_categoryTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class edit_category(edit_categoryTemplate):
  def __init__(self,selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components( **properties)
    self.selected_row = selected_row 

    self.text_box_1.text = selected_row['issue_category']
        # Store the selected row for later use
    

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    update = self.text_box_1.text.strip()
    if not update:
        alert("Please enter a valid data.")
        return

        # Update the 'borrower_gender' field in the database
    self.selected_row['issue_category'] = update
    self.selected_row.update()
        # Close the form
    alert("Changes saved successfully!")
    open_form('admin.dashboard.manage_cms.add_report_issues_dropdown.Issues_category_dropdown')

  def delete_button_click(self, **event_args):
     confirmation = alert(
            "Are you sure you want to delete this data?",
            title="Confirm Deletion",
            buttons=[("Cancel", False), ("Delete", True)],
        )
     if confirmation:
            # Get the name of the group to be deleted
            # name = self.selected_row['issue_category']
            # Delete the rows from the product_group table
            # self.name.delete()
            self.selected_row.delete()
            alert('Data Deleted Successfully!')
            open_form('admin.dashboard.manage_cms.add_report_issues_dropdown.Issues_category_dropdown')
