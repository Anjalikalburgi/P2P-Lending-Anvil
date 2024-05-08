from ._anvil_designer import check_outTemplate
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
from ...Module1 import transfer_money_1


class check_out(check_outTemplate):
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
        total_processing_fee_amount = selected_row['total_processing_fee_amount']
        processing_fee = total_processing_fee_amount/ tenure
        monthly_interest_rate = interest_rate / 12 / 100
        total_payments = tenure * 12
        total_repayment_amount = selected_row['total_repayment_amount']
  
        if emi_payment_type == 'One Time':
            emi = total_repayment_amount
            #total_emi += emi  # Add extension amount to 12-month EMI total
            total_emi = emi +  extension_amount + total_processing_fee_amount
        elif emi_payment_type == 'Monthly':
            # Calculate monthly EMI amount
            emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure)) / (((1 + monthly_interest_rate) ** tenure) - 1)
            total_emi = emi + extension_amount + processing_fee  # Add extension amount to monthly EMI
        elif emi_payment_type == 'Three Months':
            # Calculate EMI amount for 3 months
            processing_fee = processing_fee * 3
            emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure)) - 1)
            emi*=3
            total_emi = emi + extension_amount + processing_fee # Add extension amount to 3-month EMI
        elif emi_payment_type == 'Six Months':
            processing_fee = processing_fee * 6
            # Calculate EMI amount for 6 months
            emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure)) - 1)
            emi*=6
            total_emi = emi + extension_amount+ processing_fee  # Add extension amount to 6-month EMI
        else:
            # Default to monthly calculation
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
            total_emi = emi + extension_amount + processing_fee # Add extension amount to monthly EMI


        print(processing_fee)
        loan_state_status = app_tables.fin_loan_details.get(loan_id=loan_id)['loan_state_status']
      
        if loan_state_status == 'lapsed loan' and selected_row['days_left'] > 6:
            # Fetch the lapsed fee from product details table
            product_id = selected_row['product_id']
            lapsed_fee_1 = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
            total_lapsed_amount = lapsed_fee_1 * emi/100
            days_left = selected_row['days_left']
            days_difference = days_left - 6
            lapsed_fee = (days_difference * total_lapsed_amount)
            total_emi += lapsed_fee
            self.lapsed.text = "{:.2f}".format(lapsed_fee)
            self.lapsed.visible = True
            self.label_5.visible = True
            self.default.visible = False
            self.label_9.visible = False
          
        if loan_state_status == 'default loan' and selected_row['days_left'] > 16:
          product_id = selected_row['product_id']
    # Fetch default fee details from product details table
          product_details = app_tables.fin_product_details.get(product_id=product_id)
          
          # Check if default_fee or default_fee_amount should be used
          if product_details['default_fee'] != 0:
              # Calculate the number of days between today's date and the selected schedule payment date
              days_left = selected_row['days_left']
              days_difference = days_left - 16
      
              # Fetch default fee percentage and amount from product details table
              default_fee_percentage = product_details['default_fee']
              default_fee_decimal = default_fee_percentage * emi / 100
      
              # Calculate total default fee
              total_default_fee = days_difference * default_fee_decimal
      
          elif product_details['default_fee_amount'] != 0:
              # Fetch default fee amount from product details table
              default_fee_amount = product_details['default_fee_amount']
      
              # Calculate the number of days between today's date and the selected schedule payment date
              days_left = selected_row['days_left']
              days_difference = days_left - 16
      
              # Multiply default fee amount by days_difference
              total_default_fee = days_difference * default_fee_amount
      
          else:
              # Neither default_fee nor default_fee_amount is set, so default fee is zero
              total_default_fee = 0
      
          # Add default fee to total EMI
          total_emi += total_default_fee
          self.default.text = "{:.2f}".format(total_default_fee)
          self.default.visible = True
          self.label_9.visible = True
          self.lapsed.visible = False
          self.label_5.visible = False

        if loan_state_status == 'NPA' and selected_row['days_left'] > 106:
    # Fetch NPA fee details from product details table
          product_id = selected_row['product_id']
          product_details = app_tables.fin_product_details.get(product_id=product_id)
          
          # Check if npa or npa_amount should be used
          if product_details['npa'] != 0:
              # Calculate the number of days between today's date and the selected schedule payment date
              days_left = selected_row['days_left']
              days_difference = days_left - 106
      
              # Fetch NPA fee percentage and amount from product details table
              npa_percentage = product_details['npa']
              npa_decimal = npa_percentage * emi/ 100
      
              # Calculate total NPA fee
              total_npa_fee = days_difference * npa_decimal
      
          elif product_details['npa_amount'] != 0:
              # Fetch NPA fee amount from product details table
              npa_amount = product_details['npa_amount']
      
              # Calculate the number of days between today's date and the selected schedule payment date
              days_left = selected_row['days_left']
              days_difference = days_left - 106
      
              # Multiply NPA fee amount by days_difference
              total_npa_fee = days_difference * npa_amount
      
          else:
              # Neither npa nor npa_amount is set, so NPA fee is zero
              total_npa_fee = 0
      
          # Add NPA fee to total EMI
          total_emi += total_npa_fee
      
          # Update UI
          self.npa.text = "{:.2f}".format(total_npa_fee)
          self.npa.visible = True
          self.label_12.visible = True
          # Hide default and lapsed fee labels
          self.default.visible = False
          self.label_9.visible = False
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
        self.interest_label.text = "{:.2f}".format(total_interest_amount)
        self.tenure_label.text = str(tenure)
        self.account_no_label.text = str(selected_row['account_number'])
      
        # Display total EMI amount including extension amount
        self.update_total_emi_amount(total_emi)
      
        foreclosure_details = self.get_foreclosure_details(loan_id, selected_row['emi_number'])
        if foreclosure_details is not None :
            
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
            borrower_customer_id=self.selected_row['borrower_customer_id'],
            loan_id=loan_id,
            emi_number=q.less_than_or_equal_to(emi_number)
        )
        extension_months = 0
        if extension_row is not None and extension_row['status'] == 'approved':
            extension_months = extension_row['total_extension_months']
        return  extension_months

    def get_extension_details_1(self, loan_id, emi_number):
        extension_row = app_tables.fin_extends_loan.get(
            borrower_customer_id=self.selected_row['borrower_customer_id'],
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

    def get_first_payment_due_date(self, loan_id):
        loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
        if loan_row is not None:
            return loan_row['first_emi_payment_due_date']
        else:
            return None  # or handle the case where the loan ID is not found

    def pay_now_click(self, **event_args):
        try:
            lapsed_fee = float(self.lapsed.text)
        except ValueError:
            lapsed_fee = 0.0  # Default value if conversion fails
        
        try:
            default_fee = float(self.default.text)
        except ValueError:
            default_fee = 0.0

        try:
            extra_amount = float(self.extension_amount_label.text)
        except ValueError:
            extra_amount = 0.0

       # extra_amount = float(self.extension_amount_label.text)
        try:
            npa = float(self.npa.text)
        except ValueError:
            npa = 0.0

       # extra_amount = float(self.extension_amount_label.text)
        extra_fee = lapsed_fee + default_fee + extra_amount + npa
      
        total_emi_amount = float(self.total_emi_amount_label.text)  # Fetch total EMI amount including extra payment
        borrower_wallet = app_tables.fin_wallet.get(customer_id=self.user_id)
        print(self.selected_row['lender_customer_id'])
        print(self.selected_row['borrower_customer_id'])
        # transfer_money(lender_id = self.selected_row['lender_customer_id'], borrower_id=self.selected_row['borrower_customer_id'], transfer_amount=total_emi_amount) 

        if borrower_wallet is not None:
            wallet_balance = borrower_wallet['wallet_amount']

            if wallet_balance >= total_emi_amount:
                updated_balance = wallet_balance - total_emi_amount
                borrower_wallet['wallet_amount'] = updated_balance
                borrower_wallet.update()

                # Retrieve lender's wallet based on lender_customer_id
                lender_wallet = app_tables.fin_wallet.get(customer_id=self.selected_row['lender_customer_id'])
                transfer_money_1(lender_id = self.selected_row['lender_customer_id'], borrower_id=self.selected_row['borrower_customer_id'], transfer_amount=total_emi_amount) 

                if lender_wallet is not None:
                    lender_balance = lender_wallet['wallet_amount']

                    # If lender_balance is None, treat it as zero
                    if lender_balance is None:
                        lender_balance = 0

                    lender_balance += total_emi_amount  # Add deducted amount to lender's wallet
                    lender_wallet['wallet_amount'] = lender_balance
                    lender_wallet.update()

                    # self.update_payment_status()

                    loan_id = self.selected_row['loan_id']
                    current_emi_number = int(self.selected_row['emi_number'])
                    account_number = self.selected_row['account_number']
                    emi_payment_type = self.selected_row['emi_payment_type']
                    tenure = self.selected_row['tenure']
                    borrower_id = self.selected_row['borrower_customer_id']
                    lender_id = self.selected_row['lender_customer_id']
                    lender_email = self.selected_row['lender_email_id']
                    borrower_email = self.selected_row['borrower_email_id']

                    prev_scheduled_payment = self.selected_row['scheduled_payment']
                    prev_next_payment = self.selected_row['next_payment']

                  
                    # Calculate next scheduled payment based on emi_payment_type
                    if emi_payment_type in ['One Time', 'Monthly', 'Three Months', 'Six Months']:
                        
                        if emi_payment_type == 'Monthly':
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=30)
                            next_next_payment = prev_next_payment + timedelta(days=30)
                        elif emi_payment_type == 'Three Months':
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=90)
                            next_next_payment = prev_next_payment + timedelta(days=90)
                     
                        elif emi_payment_type == 'Six Months':
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=180)
                            next_next_payment = prev_next_payment + timedelta(days=180)
                        elif emi_payment_type == 'One Time':
                          if tenure:
                            next_scheduled_payment = prev_scheduled_payment + timedelta(days=30 * tenure)
                            next_next_payment = self.selected_row['next_payment'] + timedelta(days=30 * tenure)                
                    else:
                        # Default to monthly calculation
                        next_scheduled_payment = prev_scheduled_payment + timedelta(days=30)
                        next_next_payment = prev_next_payment + timedelta(days=30)

                    # Add a new row to fin_emi_table
                    new_emi_row = app_tables.fin_emi_table.add_row(
                        loan_id=loan_id,
                        emi_number=current_emi_number + 1,
                        account_number=account_number,
                        scheduled_payment_made=datetime.now(),
                        scheduled_payment=next_scheduled_payment,
                        next_payment=next_next_payment,
                        amount_paid= total_emi_amount,
                        extra_fee=extra_fee,
                        borrower_customer_id=borrower_id,
                        lender_customer_id=lender_id,
                        borrower_email=borrower_email,
                        lender_email=lender_email,
                        
                        
                    )

                    # Update the emi_number and next_payment in the selected_row
                    self.selected_row['emi_number'] = current_emi_number + 1
                    self.selected_row['next_payment'] = next_next_payment
                    self.selected_row.update()

                    if self.foreclosure_condition_satisfied(loan_id, current_emi_number):
                      self.update_loan_status(loan_id, 'close')

                    #self.status_label.text = "Payment successfully done..."
                    self.button_1_copy_3.visible = False
                    alert('Payment successfully done...')
                    open_form('borrower_registration_form.dashboard')
                else:
                    alert( "Lender's wallet not found.")
            else:
                alert("Insufficient funds in wallet. Please deposit more funds to continue.")
                open_form('wallet.wallet')
        else:
            self.status_label.text = "Wallet record not found."

    def button_1_copy_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard.today_dues')

    def update_loan_status(self, loan_id, new_status):
    # Update loan status in the loan details table for the given loan ID
      loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
      if loan_row is not None:
          loan_row['loan_updated_status'] = new_status
          loan_row.update()


    def foreclosure_condition_satisfied(self, loan_id, emi_number):
    # Check if foreclosure details are returned for the given loan and EMIs
      foreclosure_row = app_tables.fin_foreclosure.get(
          loan_id=loan_id,
          foreclosure_emi_num=emi_number
      )
      return foreclosure_row is not None

    # def update_payment_status(self):
    # # Update payment status in loan details table for the given loan ID, borrower ID, and condition
    #   loan_details = app_tables.fin_loan_details.search(
    #     loan_id=self.selected_row['loan_id'],
    #     borrower_customer_id=self.selected_row['borrower_customer_id'],
    #     first_emi_payment_due_date=q.less_than_or_equal_to(datetime.now().date())
    # )
    #   for loan_detail in loan_details:
    #     loan_detail['payment_status'] = True
    #     loan_detail.update()