from ._anvil_designer import dasboard_about_lendor_registration_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class dasboard_about_lendor_registration_form(dasboard_about_lendor_registration_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard")

  def login_signup_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    alert("Logged out sucessfully")
    anvil.users.logout()
    open_form('bank_users.main_form')

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.dasboard_contact")

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def notification_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor_registration_form.dashboard.notification')

  def wallet_dashboard_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wallet.wallet')

  def image_2_mouse_enter(self, x, y, **event_args):
    """This method is called when the mouse cursor enters this component"""
    self.label_9.visible=True

  def image_2_mouse_leave(self, x, y, **event_args):
    """This method is called when the mouse cursor leaves this component"""
    self.label_9.visible=False

  def image_2_copy_mouse_enter(self, x, y, **event_args):
    """This method is called when the mouse cursor enters this component"""
    self.label_10.visible=True

  def image_2_copy_mouse_leave(self, x, y, **event_args):
    """This method is called when the mouse cursor leaves this component"""
    self.label_10.visible=False

  def image_2_copy_copy_mouse_enter(self, x, y, **event_args):
    """This method is called when the mouse cursor enters this component"""
    self.label_11.visible=True

  def image_2_copy_copy_mouse_leave(self, x, y, **event_args):
    """This method is called when the mouse cursor leaves this component"""
    self.label_11.visible=False

  def image_2_copy_copy_copy_mouse_enter(self, x, y, **event_args):
    """This method is called when the mouse cursor enters this component"""
    self.label_12.visible=True

  def image_2_copy_copy_copy_mouse_leave(self, x, y, **event_args):
    """This method is called when the mouse cursor leaves this component"""
    self.label_12.visible=False
