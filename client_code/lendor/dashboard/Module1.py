import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .lendor_registration_form.dashboard import Module1
#

# Define a client-side function to transfer money
def transfer_money(lender_id, borrower_id, transfer_amount):
    # Call the server-side function to handle the transfer
    success = anvil.server.call('transfer_money', lender_id, borrower_id, transfer_amount)
    
    if success:
        # Handle success case (e.g., show success message)
        print("Money transferred successfully!")
    else:
        # Handle failure case (e.g., show error message)
        print("Money transfer failed.")
