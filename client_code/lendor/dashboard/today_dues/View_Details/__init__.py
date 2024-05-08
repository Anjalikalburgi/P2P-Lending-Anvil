from ._anvil_designer import View_DetailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
from .. import main_form_module as main_form_module
from datetime import date

class View_Details(View_DetailsTemplate):
    def __init__(self, selected_row, **properties):
        self.selected_row = selected_row
        self.user_id = main_form_module.userId
        self.init_components(**properties)
  
        loan_id = selected_row['loan_id']
        extension_months = self.get_extension_details(loan_id, selected_row['emi_number'])
        extension_amount = self.get_extension_details_1(loan_id,selected_row['emi_number'])
        loan_amount = selected_row['loan_amount']
        tenure = selected_row['tenure'] + extension_months
        interest_rate = selected_row['interest_rate']
        emi_payment_type = selected_row['emi_payment_type']
        total_interest_amount = selected_row['total_interest_amount']
  
        monthly_interest_rate = interest_rate / 12 / 100
        total_payments = tenure * 12
  
        if emi_payment_type == 'One Time':
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / ((1 + monthly_interest_rate) ** tenure - 1)
            total_emi = emi * tenure + extension_amount  # Add extension amount to 12-month EMI total
        elif emi_payment_type == 'Monthly':
            # Calculate monthly EMI amount
            emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure)) / (((1 + monthly_interest_rate) ** tenure) - 1)
            total_emi = emi + extension_amount  # Add extension amount to monthly EMI
        elif emi_payment_type == 'Three Months':
            # Calculate EMI amount for 3 months
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** 3) / ((1 + monthly_interest_rate) ** 3 - 1)
            total_emi = emi + extension_amount  # Add extension amount to 3-month EMI
        elif emi_payment_type == 'Six Months':
            # Calculate EMI amount for 6 months
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** 6) / ((1 + monthly_interest_rate) ** 6 - 1)
            total_emi = emi + extension_amount  # Add extension amount to 6-month EMI
        else:
            # Default to monthly calculation
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
            total_emi = emi + extension_amount  # Add extension amount to monthly EMI


        loan_state_status = app_tables.fin_loan_details.get(loan_id=loan_id)['loan_state_status']
        if loan_state_status == 'lapsed loan' and selected_row['days_left'] > 6:
            # Fetch the lapsed fee from product details table
            product_id = selected_row['product_id']
            lapsed_fee = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
            total_emi += lapsed_fee
            self.lapsed.text = "{:.2f}".format(lapsed_fee)
            self.lapsed.visible = True
            self.label_5.visible = True
            self.default.visible = False
            self.label_9.visible = False
        elif loan_state_status == 'default loan' and selected_row['days_left'] > 8:
            # Calculate the number of days between today's date and the selected schedule payment date
            days_left = selected_row['days_left']
            days_difference = days_left - 8 #(selected_payment_date - date.today()).days
            
            # Subtract 8 from the days difference and ensure it's not negative
            #remaining_days = max(days_difference - 8, 0)
            
            # Fetch the default fee from product details table
            product_id = selected_row['product_id']
            default_fee = app_tables.fin_product_details.get(product_id=product_id)['default_fee']
            total_default_fee = days_difference * default_fee
            # Multiply the remaining days with the default fee and add to the total EMI
            total_emi += total_default_fee
            self.default.text = "{:.2f}".format(total_default_fee)
            self.default.visible = True
            self.label_9.visible = True
            self.lapsed.visible = False
            self.label_5.visible = False


        # Display the calculated EMI amount in the EMI amount label
        self.emi_amount_label.text = "{:.2f}".format(emi)  # Show only the EMI amount without extension
        
        self.update_total_emi_amount(total_emi)
        self.total_emi_amount_label.visible = True

        # Update labels based on the presence of extension amount
        if extension_amount > 0:
            self.total_emi_amount_label.text = "{:.2f}".format(total_emi)
            self.extension_amount_label.text = "{:.2f}".format(extension_amount)
            self.total_emi_amount_label.visible = True
            self.extension_amount_label.visible = True
            self.label_6.visible = True
            self.label_3.visible = True
        else:
            self.total_emi_amount_label.visible = True
            self.extension_amount_label.visible = False
            self.label_6.visible = False
            self.label_3.visible = True
  
        # Update other labels
        self.loan_id_label.text = str(selected_row['loan_id'])
        self.loan_amount_label.text = str(loan_amount)
        self.interest_label.text = str(total_interest_amount)
        self.tenure_label.text = str(tenure)
        self.account_no_label.text = str(selected_row['account_number'])
      
        # Display total EMI amount including extension amount
        self.update_total_emi_amount(total_emi)
      
        foreclosure_details = self.get_foreclosure_details(loan_id, selected_row['emi_number'])
        if foreclosure_details is not None:
            total_due_amount = foreclosure_details['total_due_amount']
            foreclosure_amount = foreclosure_details['foreclose_amount']
        
            # Check if lapsed fee or default fee is applicable
            loan_state_status = app_tables.fin_loan_details.get(loan_id=loan_id)['loan_state_status']
            if loan_state_status == 'lapsed loan' and selected_row['days_left'] > 6:
                # Fetch the lapsed fee from product details table
                product_id = selected_row['product_id']
                lapsed_fee = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                total_due_amount += lapsed_fee
        
            elif loan_state_status == 'default loan' and selected_row['days_left'] > 8:
                # Calculate the number of days between today's date and the selected schedule payment date
                days_left = selected_row['days_left']
                days_difference = days_left - 8
        
                # Fetch the default fee from product details table
                product_id = selected_row['product_id']
                default_fee = app_tables.fin_product_details.get(product_id=product_id)['default_fee']
                total_default_fee = days_difference * default_fee
                total_due_amount += total_default_fee
            # Update labels with foreclosure details
            self.emi_amount_label.text = "{:.2f}".format(total_due_amount)
            self.extension_amount_label.text = "{:.2f}".format(foreclosure_amount)
            self.total_emi_amount_label.text = "{:.2f}".format(total_due_amount + foreclosure_amount)
            self.total_emi_amount_label.visible = True
            self.label_3.visible = True

    def get_extension_details(self, loan_id, emi_number):
        extension_row = app_tables.fin_extends_loan.get(
            loan_id=loan_id,
            emi_number=q.less_than_or_equal_to(emi_number)
        )
        extension_months = 0
        if extension_row is not None and extension_row['status'] == 'approved':
            extension_months = extension_row['total_extension_months']
        return  extension_months

    def get_extension_details_1(self, loan_id, emi_number):
        extension_row = app_tables.fin_extends_loan.get(
            loan_id=loan_id,
            emi_number=emi_number
        )
        extension_amount = 0
        if extension_row is not None and extension_row['status'] == 'approved':
            extension_amount = extension_row['extension_amount']
        return extension_amount

    def get_foreclosure_details(self, loan_id, emi_number):
      foreclosure_row = app_tables.fin_foreclosure.get(
          loan_id=loan_id,
          foreclosure_emi_num=emi_number,
      )
      
      if foreclosure_row is not None and foreclosure_row['status'] == 'approved':
          return foreclosure_row
      else:
          return None
  
    def update_total_emi_amount(self, total_emi):
        self.total_emi_amount_label.text = "{:.2f}".format(total_emi)

    def button_1_copy_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor_registration_form.dashboard.today_dues')
