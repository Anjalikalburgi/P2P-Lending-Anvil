from ._anvil_designer import manage_cmsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class manage_cms(manage_cmsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.dashboard')

  

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_cms.manage_dropdowns')

  def image_4_copy_5_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_cms.manage_dropdowns')

  def button_21_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_cms.manage_issues_dropdown')

  def image_10_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_cms.manage_issues')

  def button_2_click(self, **event_args):
    open_form('admin.dashboard')