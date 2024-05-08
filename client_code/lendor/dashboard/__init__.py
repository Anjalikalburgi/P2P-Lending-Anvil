from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
from anvil.tables import app_tables
from anvil import open_form, server
from anvil import server
from ...bank_users.main_form import main_form_module


class dashboard(dashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.email = main_form_module.email
    email = self.email
    self.user_id=main_form_module.userId
    user_id = self.user_id
    

  
  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_opening_balance")

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_available_balance")

  def View_Loan_Requests_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_borrower_loan_request")
    # email = main_form_module.email
    # user_profile = app_tables.fin_user_profile.get(email_user=email)
    # if user_profile:
    #         user_id = user_profile['customer_id']
            
    #         wallet_row = app_tables.fin_wallet.get(customer_id=user_id)
            
    #         print(f"User ID: {user_id}")
            
    #         if wallet_row and wallet_row['wallet_id'] is not None:                
    #             open_form('lendor_registration_form.dashboard.view_borrower_loan_request')
    #         else:              
    #             alert("Wallet not found. Do some transaction", title="Alert")

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.loan_disbursement")

  def Todays_Due_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.today_dues")

  def View_Lost_Opportunities_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_lost_oppurtunities")

  def View_Loans_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.lender_view_loans")

  def View_Loan_Extension_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_loan_extension_requests")

  def View_Loan_Foreclosure_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_loan_foreclosure_Requests")

  def View_Edit_Profile_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.lender_profile")

  def View_Send_Notifications_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_or_send_notifications")

  def Change_Password_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.change_password")

  def historyView_Transaction_History_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.view_transaction_history")

  def login_signup_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    alert("Logged out sucessfully")
    anvil.users.logout()
    open_form('bank_users.main_form')

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard")

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.dasboard_about")

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.dasboard_contact")

  def button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_show(self, **event_args):
    """This method is called when the Button is shown on the screen"""
    pass

  def button_hide(self, **event_args):
    """This method is called when the Button is removed from the screen"""
    pass

  
  def toggleswitch_1_x_change(self, **event_args):
    
    if self.toggleswitch_1.checked:
      self.button_status.text = "ONLINE"
      self.button_status.background = '#0876e8'  # Green color
      self.button_status.foreground = '#FFFFFF'  # White text
      # Update 'make_visibility' column in the 'lender' table to True
      lender_row = app_tables.fin_lender.search() # Assuming you have a row with id=1 for the lender
      lender_row[0]['make_visibility'] = True
      lender_row[0].update()
    else:
      self.button_status.text = "OFFLINE"
      self.button_status.background = '#FFFFFF'  # White color
      self.button_status.foreground = '#FF0000'  # Red text
      lender_row = app_tables.fin_lender.search()# Assuming you have a row with id=1 for the lender
      lender_row[0]['make_visibility'] = False
      lender_row[0].update()

  def notification_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor_registration_form.dashboard.notification')


  def wallet_dashboard_link_click(self, **event_args):
    open_form('wallet.wallet')
