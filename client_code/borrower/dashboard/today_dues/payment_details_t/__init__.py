import anvil.google.auth
import anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.google.auth
import anvil.google.drive
from anvil.tables import app_tables
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
from anvil import DataGrid, alert, open_form
from datetime import datetime, timedelta
import anvil.server
from ._anvil_designer import payment_details_tTemplate
class payment_details_t(payment_details_tTemplate):
    def __init__(self, selected_row=None, entered_values=None, **properties):
        self.selected_row = selected_row
        self.init_components(**properties)

        if selected_row:
            self.load_payment_details(selected_row, entered_values)

    def load_payment_details(self, selected_row, entered_values):
      self.load_entered_values(entered_values)
      payment_details = []
  
      # Calculate number of payment details based on emi_payment_type
      num_payments = self.calculate_num_payments(selected_row)
  
      # Initialize beginning_balance to the loan amount
      beginning_balance = selected_row['total_repayment_amount']
      beginning_loan_amount_balance = selected_row['loan_amount']
      total_extra_payment = 0

      for month in range(1, num_payments + 1):
          payment_date = self.calculate_payment_date(selected_row, month)

          
          # Call the appropriate calculation method based on emi_payment_type
          if selected_row['emi_payment_type'] == 'Monthly':
              emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month, total_tenure = self.calculate_monthly_emi_and_balance(selected_row, month)
          elif selected_row['emi_payment_type'] == 'Three Months':
              emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month  ,total_tenure= self.calculate_three_month_emi_and_balance(selected_row, month)
          elif selected_row['emi_payment_type'] == 'Six Months':
              emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month ,total_tenure = self.calculate_six_month_emi_and_balance(selected_row, month)
          elif selected_row['emi_payment_type'] == 'One Time':
              emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month,total_tenure = self.calculate_one_time_emi_and_balance(selected_row, month)
          else:
              # Handle unsupported payment types
              emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month ,total_tenure = 0, 0, 0
  
          # Fetch extra payment from fin_extension_loan table
          # extension_row = app_tables.fin_extends_loan.get(
          #     loan_id=selected_row['loan_id'],
          #     emi_number=q.less_than_or_equal_to(month) 
          # )
          # # extra_payment = extension_row['extension_amount'] if extension_row else 0
          # new_emi_value = extension_row['new_emi'] if extension_row else None
          # if new_emi_value is not None:
          #   emi = new_emi_value
            
          # extension_row_1 = app_tables.fin_extends_loan.get(
          #     loan_id=selected_row['loan_id'],
          #     emi_number=month 
          # )   
          # extra_payment = extension_row_1['extension_amount'] if extension_row_1 else 0
            
          # # Add extension amount to beginning balance
          # total_extra_payment += extra_payment or 0
        
  
          # Fetch scheduled_payment_made and account_number from the emi_payments table
          emi_row = app_tables.fin_emi_table.get(
              borrower_customer_id=selected_row['borrower_customer_id'],
              loan_id=selected_row['loan_id'],
              emi_number=month
          )
          scheduled_payment_made = emi_row['scheduled_payment_made'] if emi_row else None
          account_number = emi_row['account_number'] if emi_row else None
          extra_payment = emi_row['extra_fee'] if emi_row else None
          
          # total_extra_payment += additional_fee or 0
          #emi_number = emi_row['emi_number']
  
          # Determine display values for EMIDate and AccountNumber
          scheduled_payment_made_display = f"{scheduled_payment_made:%Y-%m-%d}" if scheduled_payment_made else "N/A"
          emi_time_display = f"{scheduled_payment_made:%I:%M %p}" if scheduled_payment_made else "N/A"
          account_number_display = account_number if account_number else "N/A"
  
          # Format payment date
          formatted_payment_date = f"{payment_date:%Y-%m-%d}" if payment_date else "Awaiting Update"
          beginning_balance += extra_payment or 0

          foreclosure_row = app_tables.fin_foreclosure.get(
            loan_id=selected_row['loan_id'],
            foreclosure_emi_num=q.less_than(month)
        )
          if foreclosure_row is not None and foreclosure_row['status']=='approved':
            # If foreclosed, set beginning balance and ending balance to the total amount in the foreclosure table
            foreclosure_amount = foreclosure_row['foreclose_amount']
            beginning_balance = foreclosure_row['total_due_amount']
            # additional_fee = additional_fee or 0
            # foreclosure_amount += additional_fee
            ending_balance = 0
            extra_payment  = extra_payment or 0
            extra_payment += foreclosure_amount
            principal_amount = beginning_balance - interest_amount
            # Add the foreclosure details to payment details
            payment_details.append({
                'PaymentNumber': month ,
                'PaymentDate': formatted_payment_date if formatted_payment_date != "Awaiting Update" else "N/A", #foreclosure_row['requested_on'].strftime('%Y-%m-%d'),
                'EMIDate': "N/A",
                'EMITime': "N/A",
                'AccountNumber': "N/A",
                'ScheduledPayment': f"₹ {beginning_balance:.2f}",
                'Principal': f"₹ {principal_amount:.2f}",
                'Interest': f"₹ {interest_amount:.2f}",
                'BeginningBalance': f"₹ {beginning_balance+ extra_payment :.2f}",
                'ExtraPayment': f"₹ {extra_payment :.2f}",
                'TotalPayment': f"₹ {beginning_balance + extra_payment:.2f}",
                'EndingBalance': "₹ 0.00",
                'ProcessingFee': f"₹ {processing_fee_per_month:.2f}",
                'beginning_loan_amount_balance': f"₹ {beginning_loan_amount_balance:.2f}",
                'ending_loan_amount_balance': "₹ 0.00"
            })
            break
            
          # Add payment details to the list
          payment_details.append({
              'PaymentNumber': month,
              'PaymentDate': formatted_payment_date,
              'EMIDate': scheduled_payment_made_display,
              'EMITime': emi_time_display,
              'AccountNumber': account_number_display,
              'ScheduledPayment': f"₹ {emi:.2f}",
              'Principal': f"₹ {(emi - interest_amount):.2f}",
              'Interest': f"₹ {interest_amount:.2f}",
              'BeginningBalance': f"₹ {beginning_balance:.2f}",
              'ExtraPayment': f"₹ {extra_payment:.2f}" if extra_payment is not None else "₹ 0.00",
              'TotalPayment': f"₹ {emi + extra_payment if extra_payment is not None else emi:.2f}",
              'EndingBalance': f"₹ {ending_balance:.2f}",
              'ProcessingFee': f"₹ {processing_fee_per_month:.2f}",
              'beginning_loan_amount_balance': f"₹ {beginning_loan_amount_balance:.2f}",
              'ending_loan_amount_balance': f"₹ {ending_loan_amount_balance:.2f}"
          })
  
          # Update beginning balance for the next iteration
          beginning_balance = ending_balance
          beginning_loan_amount_balance = ending_loan_amount_balance
      # extra_payment += ex     
      #beginning_balance += total_extra_payment
      # If there are remaining months and the last payment type is 'Three Month' or 'Six Month'
      remaining_months = total_tenure % 3 if selected_row['emi_payment_type'] == 'Three Months' else total_tenure % 6
      beginning_balance = ending_balance  # Use the total repayment amount

    
# Check if there are remaining months
      if remaining_months and selected_row['emi_payment_type'] in ['Three Months', 'Six Months']:
          # Calculate EMI for the remaining month(s)
          remaining_emi = self.calculate_emi_1(beginning_balance, remaining_months,selected_row['interest_rate'])
          
          # Calculate interest amount for the remaining months
          interest_amount = self.calculate_interest(beginning_balance, selected_row['interest_rate'], remaining_months)
        
          extension_row = app_tables.fin_extends_loan.get(
            borrower_customer_id=selected_row['borrower_customer_id'],
          loan_id=selected_row['loan_id'],
          emi_number=num_payments + 1  # Assuming num_payments is the last paid EMIs count
             )
          extra_payment = extension_row['extension_amount'] if extension_row else 0

          if selected_row['total_processing_fee_amount'] is not None:
              # Ensure processing fee is considered monthly
              processing_fee = selected_row['total_processing_fee_amount'] / total_tenure
              # If remaining months are less than tenure, add processing fee for each remaining month
              if remaining_months < total_tenure:
                  processing_fee_per_month = processing_fee * remaining_months
              else:
                  processing_fee_per_month = selected_row['total_processing_fee_amount']
          else:
              processing_fee_per_month = 0
                    
          emi_row_remaining = app_tables.fin_emi_table.get(
               borrower_customer_id=selected_row['borrower_customer_id'],
              loan_id=selected_row['loan_id'],
              emi_number=q.greater_than(num_payments)
          )

          date = emi_row_remaining['scheduled_payment_made'] if emi_row_remaining else None
         # if date is not None:
          scheduled_payment_made_display = f"{date:%Y-%m-%d}" if date else "N/A"
          emi_time_display = f"{date:%I:%M %p}" if date else "N/A"

          extra_fee = emi_row_remaining['extra_fee'] if emi_row_remaining else 0
          extra_payment += extra_fee or 0

          account_number_display = emi_row_remaining['account_number']  if emi_row_remaining else   "N/A"
        
          loan_updated_status = selected_row['loan_updated_status'].lower() if selected_row['loan_updated_status'] else None
          # Checking if loan_updated_status is 'close' before proceeding with date manipulation
          if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
              formatted_payment_date_datetime = datetime.strptime(formatted_payment_date, '%Y-%m-%d')
          
              if selected_row['emi_payment_type'] == 'Three Months':
                  # For 'Three Month', add 90 days and update to the next boundary
                  payment_date = formatted_payment_date_datetime + timedelta(days=90)
              elif selected_row['emi_payment_type'] == 'Six Months':
                  # For 'Six Month', add 180 days
                  payment_date = formatted_payment_date_datetime + timedelta(days=180)
              else:
                  # Assuming payment date is None for other payment types
                  payment_date = None
          
              # Concatenate only the date component if payment_date is not None
              formatted_payment_date = payment_date.strftime('%Y-%m-%d') if payment_date else "Awaiting Update"  # Indicate that this is for the remaining month(s)
          else:
              formatted_payment_date = "Awaiting Update"
          beginning_balance = ending_balance  # Use the total repayment amount
          
          # Add the details for the remaining month(s)
          payment_details.append({
              'PaymentNumber': num_payments + 1,
              'PaymentDate': formatted_payment_date,
              'EMIDate': scheduled_payment_made_display,
              'EMITime': emi_time_display,
              'AccountNumber': account_number_display,
              'ScheduledPayment': f"₹ {remaining_emi:.2f}",
              'Principal': f"₹ {(remaining_emi - interest_amount):.2f}",
              'Interest': f"₹ {interest_amount:.2f}",
              'BeginningBalance': f"₹ {beginning_balance + extra_payment:.2f}",
              'ProcessingFee': f"₹ {processing_fee_per_month:.2f}",
              'ExtraPayment': f"₹ {extra_payment:.2f}" if extra_payment is not None else "N/A",
              'TotalPayment': f"₹ {remaining_emi + extra_payment:.2f}",
              'EndingBalance': f"₹ 0.00",  # Ending balance is assumed to be 0 for the final month(s)
              'beginning_loan_amount_balance': f"₹ {ending_loan_amount_balance}",  # Assuming the loan is fully paid off
              'ending_loan_amount_balance': f"₹ 0.00"  # Assuming the loan is fully paid off
          })
      
      # Set the Data Grid's items property to the list of payment details
      self.repeating_panel_1.items = payment_details

    def calculate_interest(self, beginning_balance, interest_rate, remaining_months):
    # Calculate the interest amount based on the remaining balance and the annual interest rate
        monthly_interest_rate = interest_rate / 12 / 100
        interest_amount = beginning_balance * monthly_interest_rate * remaining_months
        return interest_amount

    def calculate_emi_1(self, beginning_balance, remaining_months, interest_rate):
        monthly_interest_rate = interest_rate / 12 / 100
        emi = (beginning_balance * monthly_interest_rate * ((1 + monthly_interest_rate) ** remaining_months)) / (((1 + monthly_interest_rate) ** remaining_months) - 1)
        return emi
      
    def load_entered_values(self, entered_values):
        if entered_values:
            # Load previously entered values into the form fields
            self.entered_loan_amount = entered_values.get('loan_amount', None)
            self.entered_tenure = entered_values.get('tenure', None)
            self.entered_payment_type = entered_values.get('payment_type', None)

    def calculate_payment_date(self, selected_row, current_month):
        loan_updated_status = selected_row['loan_updated_status'].lower()
        print("Loan Updated Status:", loan_updated_status)

        if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
            try:
                loan_disbursed_timestamp = selected_row['loan_disbursed_timestamp']
                emi_payment_type = selected_row['emi_payment_type']

                if loan_disbursed_timestamp:
                    print("Loan Disbursed Timestamp:", loan_disbursed_timestamp)

                    if emi_payment_type == 'Monthly':
                        # Add months based on current month
                        payment_date = loan_disbursed_timestamp + timedelta(days=current_month * 30)
                    elif emi_payment_type == 'One Time':
                        # Payment date is set for the first month only
                        payment_date = loan_disbursed_timestamp + timedelta(days=30)  # Assuming 30 days per month
                    elif emi_payment_type == 'Three Months':
                        # Add 3 months to the loan disbursal date
                        payment_date = loan_disbursed_timestamp + timedelta(days=current_month * 90)
                    elif emi_payment_type == 'Six Months':
                        # Add 6 months to the loan disbursal date
                        payment_date = loan_disbursed_timestamp + timedelta(days=current_month * 180)
                    else:
                        payment_date = None

                    return payment_date
                else:
                    print("Loan Disbursed Timestamp is None")
                    return None
            except Exception as e:
                print(f"Error in calculate_payment_date: {e}")
                return None
        else:
            print("Loan Updated Status not in expected list")
            return None

    def calculate_monthly_emi_and_balance(self, selected_row, current_month):
      emi = self.calculate_emi(selected_row, current_month)
      
      beginning_balance = selected_row['total_repayment_amount']
  
      # Initialize Total Repayment Beginning Balance (TRBB) and Total Repayment Ending Balance (TREB)
      beginning_loan_amount_balance = selected_row['loan_amount']
      total_tenure = selected_row['tenure']
      
      # Check for extension months
      extension_rows = app_tables.fin_extends_loan.search(loan_id=selected_row['loan_id'],borrower_customer_id=selected_row['borrower_customer_id'])
      for extension_row in extension_rows:
          if current_month > extension_row['emi_number'] and extension_row['status'] == 'approved':
              total_tenure += extension_row['total_extension_months']
      
      processing_fee_per_month = selected_row['total_processing_fee_amount'] / total_tenure if selected_row['total_processing_fee_amount'] is not None else 0
  
      # For monthly payments, calculate ending balance
      for month in range(1, current_month + 1):
          interest_amount = beginning_loan_amount_balance * (selected_row['interest_rate'] / 100) / 12
          principal_amount = emi - interest_amount
          beginning_loan_amount_balance -= principal_amount  # Update TRBB for the next iteration
          ending_loan_amount_balance = beginning_loan_amount_balance
          beginning_balance -= emi + processing_fee_per_month  # Update beginning balance for the next iteration
          total_tenure = total_tenure
      ending_balance = beginning_balance
  
      return emi, interest_amount, ending_balance, ending_loan_amount_balance, processing_fee_per_month, total_tenure
    
    def calculate_three_month_emi_and_balance(self, selected_row, current_month):
      emi = self.calculate_emi(selected_row, current_month)
      emi *= 3  # Multiply the monthly EMI by 3 for three-month EMI
      
      beginning_balance = selected_row['total_repayment_amount']
    
      # Initialize Total Repayment Beginning Balance (TRBB) and Total Repayment Ending Balance (TREB)
      beginning_loan_amount_balance = selected_row['loan_amount']
      ending_loan_amount_balance = beginning_loan_amount_balance
    
      # Since processing fee is a one-time charge, apply it only at the beginning
      processing_fee = selected_row['total_processing_fee_amount'] if selected_row['total_processing_fee_amount'] is not None else 0
      
      # Adjust processing fee based on total tenure
      total_tenure = selected_row['tenure']
      extension_rows = app_tables.fin_extends_loan.search(loan_id=selected_row['loan_id'],borrower_customer_id=selected_row['borrower_customer_id'])
      for extension_row in extension_rows:
          if current_month > extension_row['emi_number'] and extension_row['status'] == 'approved':
              total_tenure += extension_row['total_extension_months']
      processing_fee_per_month = processing_fee / (total_tenure /3) if processing_fee != 0 else 0
    
      # Subtract processing fee from the total repayment amount at the beginning
      beginning_balance -= processing_fee
    
      # Calculate ending balance for the current month
      for period in range(1, current_month + 1):
          interest_amount = beginning_loan_amount_balance * (selected_row['interest_rate'] / 100) / (12 * 3)
          principal_amount = emi - interest_amount
          beginning_loan_amount_balance -= principal_amount  # Update TRBB for the next iteration
          ending_loan_amount_balance = beginning_loan_amount_balance
          beginning_balance -= emi  # Update beginning balance for the next iteration
          total_tenure = total_tenure
      ending_balance = beginning_balance
  
      return emi, interest_amount, ending_balance, ending_loan_amount_balance, processing_fee_per_month,total_tenure
    
    def calculate_six_month_emi_and_balance(self, selected_row, current_month):
    # Calculate total tenure including extensions
      total_tenure = selected_row['tenure']
      extension_rows = app_tables.fin_extends_loan.search(loan_id=selected_row['loan_id'],borrower_customer_id=selected_row['borrower_customer_id'])
      for extension_row in extension_rows:
          if current_month > extension_row['emi_number'] and extension_row['status'] == 'approved':
              total_tenure += extension_row['total_extension_months']
              break
  
      emi = self.calculate_emi(selected_row, current_month)
      emi *= 6  # Multiply the monthly EMI by 6 for six-month EMI
      
      beginning_balance = selected_row['total_repayment_amount']
    
      # Initialize Total Repayment Beginning Balance (TRBB) and Total Repayment Ending Balance (TREB)
      beginning_loan_amount_balance = selected_row['loan_amount']
      ending_loan_amount_balance = beginning_loan_amount_balance
    
      # Since processing fee is a one-time charge, apply it only at the beginning
      processing_fee = selected_row['total_processing_fee_amount'] if selected_row['total_processing_fee_amount'] is not None else 0
      
      # Divide processing fee equally among the six months
      processing_fee_per_month = processing_fee / (total_tenure/6) if processing_fee != 0 else 0
      
      # Subtract processing fee from the total repayment amount at the beginning
      beginning_balance -= processing_fee
    
      # Calculate ending balance for the current month
      for period in range(1, current_month + 1):
          interest_amount = beginning_loan_amount_balance * (selected_row['interest_rate'] / 100) / (12 * total_tenure)
          principal_amount = emi - interest_amount
          beginning_loan_amount_balance -= principal_amount  # Update TRBB for the next iteration
          ending_loan_amount_balance = beginning_loan_amount_balance
          beginning_balance -= emi  # Update beginning balance for the next iteration
          total_tenure = total_tenure
      ending_balance = beginning_balance
  
      return emi, interest_amount, ending_balance, ending_loan_amount_balance, processing_fee_per_month,total_tenure
    
  
    def calculate_one_time_emi_and_balance(self, selected_row, current_month):
        emi = self.calculate_emi(selected_row,current_month)
        beginning_balance = selected_row['total_repayment_amount']
    
        # Initialize Total Repayment Beginning Balance (TRBB) and Total Repayment Ending Balance (TREB)
        beginning_loan_amount_balance = selected_row['loan_amount']
        ending_loan_amount_balance = beginning_loan_amount_balance

        total_tenure = selected_row['tenure']
        extension_rows = app_tables.fin_extends_loan.search(loan_id=selected_row['loan_id'],borrower_customer_id=selected_row['borrower_customer_id'])
        for extension_row in extension_rows:
            if current_month > extension_row['emi_number'] and extension_row['status'] == 'approved':
                total_tenure += extension_row['total_extension_months']
    
        # For one-time payment, calculate ending balance for the single payment
        interest_amount = beginning_loan_amount_balance * (selected_row['interest_rate'] / 100) / 12
        principal_amount = emi - interest_amount
        beginning_loan_amount_balance -= principal_amount  # Update TRBB for the next iteration
        ending_loan_amount_balance = beginning_loan_amount_balance
        beginning_balance -= emi  # Update beginning balance for the next iteration
        processing_fee_per_month = selected_row['total_processing_fee_amount']
        ending_balance = beginning_balance
        return emi, interest_amount, ending_balance, ending_loan_amount_balance,processing_fee_per_month,total_tenure
        
    def calculate_num_payments(self, selected_row):
      tenure = selected_row['tenure']
      payment_type = selected_row['emi_payment_type']
  
      if payment_type == 'One Time':
          return 1
      elif payment_type == 'Monthly':
          return tenure + self.calculate_extension_months(selected_row)
      elif payment_type == 'Three Months':
          num_payments = tenure // 3
          return num_payments #+ self.calculate_extension_months(selected_row)
      elif payment_type == 'Six Months':
          num_payments = tenure // 6
          return num_payments #+ self.calculate_extension_months(selected_row)
      else:
          return 0

    # def calculate_emi(self, selected_row, tenure=None, repayment_amount=None):
    #     tenure = selected_row['tenure'] if tenure is None else tenure
    #     monthly_interest_rate = (selected_row['interest_rate'] / 100) / 12
    #     loan_amount = selected_row['loan_amount'] - repayment_amount if repayment_amount else selected_row['loan_amount']
    
    #     if selected_row['emi_payment_type'] == 'Monthly':
    #         emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure)) / (((1 + monthly_interest_rate) ** tenure) - 1)
    #     elif selected_row['emi_payment_type'] == 'One Time':
    #         emi = selected_row['total_repayment_amount']
    #     elif selected_row['emi_payment_type'] == 'Three Month':
    #         monthly_interest_rate = (selected_row['interest_rate'] / 100) / (12)  # Convert annual interest rate to monthly
    #         emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure)) - 1)
    #     elif selected_row['emi_payment_type'] == 'Six Month':
    #         monthly_interest_rate = (selected_row['interest_rate'] / 100) / (12 )  # Corrected calculation for 6 months
    #         emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure )) - 1)
    #     else:
    #         emi = 0  # Handle unsupported payment types
    
    #     return emi

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard')

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard.today_dues', selected_row=self.selected_row)


    def calculate_extension_months(self, selected_row):
      # Query the fin_extends_loan table to find extension months for the given loan_id
      extension_rows = app_tables.fin_extends_loan.search(loan_id=selected_row['loan_id'],borrower_customer_id=selected_row['borrower_customer_id'])
      total_extension_months = sum(row['total_extension_months'] for row in extension_rows)
      return total_extension_months


    def calculate_emi(self, selected_row, current_month, repayment_amount=None):
    # Get the total tenure including extension months
      total_tenure = selected_row['tenure']
      extension_rows = app_tables.fin_extends_loan.search(loan_id=selected_row['loan_id'],borrower_customer_id=selected_row['borrower_customer_id'])
      for extension_row in extension_rows:
          if current_month > extension_row['emi_number'] and extension_row['status'] == 'approved':
              total_tenure += extension_row['total_extension_months']
              break
  
      # Calculate EMI based on the adjusted total tenure
      monthly_interest_rate = (selected_row['interest_rate'] / 100) / 12
      loan_amount = selected_row['loan_amount'] - repayment_amount if repayment_amount else selected_row['loan_amount']
  
      # Calculate EMI based on the adjusted total tenure
      if selected_row['emi_payment_type'] == 'Monthly':
          emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** total_tenure)) / (((1 + monthly_interest_rate) ** total_tenure) - 1)
      elif selected_row['emi_payment_type'] == 'One Time':
          emi = selected_row['total_repayment_amount']
      elif selected_row['emi_payment_type'] == 'Three Months':
          monthly_interest_rate = (selected_row['interest_rate'] / 100) / (12)  # Convert annual interest rate to monthly
          emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (total_tenure ))) / (((1 + monthly_interest_rate) ** (total_tenure)) - 1)
      elif selected_row['emi_payment_type'] == 'Six Months':
          monthly_interest_rate = (selected_row['interest_rate'] / 100) / (12 )  # Corrected calculation for 6 months
          emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** total_tenure)) / (((1 + monthly_interest_rate) ** total_tenure) - 1)
      else:
          emi = 0  # Handle unsupported payment types
  
      return emi