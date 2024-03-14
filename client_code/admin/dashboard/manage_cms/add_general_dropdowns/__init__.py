from ._anvil_designer import add_general_dropdownsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class add_general_dropdowns(add_general_dropdownsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()

    # Any code you write here will run before the form opens.
  def refresh(self):
        """Refresh repeating panels with the latest data"""
        self.repeating_panel_1.items = app_tables.fin_gender.search()
        self.repeating_panel_2.items = app_tables.fin_present_address.search()
        self.repeating_panel_3.items = app_tables.fin_duration_at_address.search()



  
  def gender_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_01.text
    new_row = app_tables.fin_gender.add_row(gender=entered_data)
    self.text_box_01.text = ' '
    self.refresh()

  def present_address_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_01_copy.text
    new_row = app_tables.fin_present_address.add_row(present_address=entered_data)
    self.text_box_01_copy.text = ' '
    self.refresh()

  def how_long_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_01_copy_2.text
    new_row = app_tables.fin_duration_at_address.add_row(duration_at_address=entered_data)
    self.text_box_01_copy_2.text = ' '
    self.refresh()

  def gender(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_01.visible = True
    self.column_panel_02.visible = False
    self.column_panel_03.visible = False

  def present(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_01.visible = False
    self.column_panel_02.visible = True
    self.column_panel_03.visible = False

  def duration(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_01.visible = False
    self.column_panel_02.visible = False
    self.column_panel_03.visible = True

