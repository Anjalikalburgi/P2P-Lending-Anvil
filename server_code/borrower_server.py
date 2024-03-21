import anvil.secrets
import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from . import bessem as bessemfunctions
from . import wallet


@anvil.server.callable
def add_borrower_step1(qualification,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['qualification'] = qualification
    row[0]['form_count']=1
    
@anvil.server.callable
def add_borrower_step2(status_of_user,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['profession'] = status_of_user
    row[0]['form_count']=2

@anvil.server.callable
def add_borrwer_self_employment(status_of_user,user_id):
  row=app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['self_employment']=status_of_user
    
    

@anvil.server.callable
def add_borrower_step3(marital_status,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['marital_status']=marital_status
    row[0]['form_count']=3

@anvil.server.callable
def add_borrower_student(college_name,college_id,college_proof,college_address,user_id):
  row=app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['college_name']=college_name
    row[0]['college_id']=college_id
    row[0]['college_address']=college_address
    row[0]['college_proof']=college_proof

@anvil.server.callable
def add_borrower_step4(home_loan,other_loan,user_id,credit_card,wheeler):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['home_loan'] = home_loan
    row[0]['other_loan']=other_loan
    row[0]['credit_card_loans']=credit_card
    row[0]['vehicle_loan']=wheeler
    row[0]['form_count']=4
    
@anvil.server.callable
def add_borrower_step5(account_name, account_type,account_number,bank_name, user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['account_name'] = account_name
    row[0]['account_type'] = account_type
    row[0]['account_number'] = account_number
    row[0]['bank_name'] = bank_name  
    row[0]['form_count']=5

@anvil.server.callable
def add_borrower_step6(bank_id, bank_branch, user_id):
    row = app_tables.fin_user_profile.search(customer_id=user_id)
    
    if row:
        # Update fin_user_profile table
        row[0]['bank_id'] = bank_id
        row[0]['account_bank_branch'] = bank_branch
        row[0]['form_count'] = 6
        row[0]['usertype'] = 'borrower'
        row[0]['last_confirm'] = True
        bessem_value = final_points_update_bessem_table(user_id)
        row[0]['bessem_value'] = float(bessem_value)
        wallet.find_user_update_type(user_id,row[0]['full_name'],"borrower")
        

        # Search for an existing row with the same email_id in fin_borrower table
        existing_borrower_row = app_tables.fin_borrower.get(email_id=row[0]['email_user'])
        
        if existing_borrower_row:
            # If a row exists, update the existing row
            existing_borrower_row['user_name'] = row[0]['full_name']
            existing_borrower_row['bank_acc_details'] = row[0]['account_number']
            existing_borrower_row['beseem_score'] = row[0]['bessem_value']
            existing_borrower_row['credit_limit'] = 1000000

            if row[0]['last_confirm']:
                existing_borrower_row['borrower_since'] = datetime.now().date()

            existing_borrower_row.update()
        else:
            # If no row exists, create a new row in fin_borrower table
            fin_borrower_row = app_tables.fin_borrower.add_row(
                customer_id=row[0]['customer_id'],
                email_id=row[0]['email_user'],
                user_name=row[0]['full_name'],
                bank_acc_details=row[0]['account_number'],
                beseem_score=row[0]['bessem_value'],
                credit_limit=1000000
            )

            if row[0]['last_confirm']:
                fin_borrower_row['borrower_since'] = datetime.now().date()

            fin_borrower_row.update()
    else:
        # If user not found in fin_user_profile table
        raise ValueError("User not found in fin_user_profile table")
      
@anvil.server.callable
def update_loan_details(loan_id, emi, total_repayment_amount, interest_rate):
    rows = app_tables.fin_loan_details.search(loan_id=loan_id)

    if rows:
        row = rows[0]
        row['emi'] = emi
        row['total_repayment_amount'] = total_repayment_amount
        row['interest_rate'] = interest_rate
        row.update()
    else:
        raise ValueError(f"Row not found for loan_id {loan_id}")

@anvil.server.callable
def add_loan_details(loan_amount, tenure,user_id,interest_rate, total_repayment_amount,product_id,membership_type,credit_limit,product_name,emi_payment_type,processing_fee_amount,total_interest,product_description,emi):
                                    
    
    # Generate a unique loan ID and get the updated counter
    loan_id = generate_loan_id()
    loan_created_timestamp = datetime.now().date()

    # Search for the user profile
    user_profiles = app_tables.fin_user_profile.search(customer_id=user_id)
    
    if user_profiles and len(user_profiles) > 0:
        # If there is a user profile, get the first one
        user_profile = user_profiles[0]

        # Extract the full name from the user profile
        borrower_full_name = user_profile['full_name']
        borrower_email_id = user_profile['email_user']

 
        app_tables.fin_loan_details.add_row(
          loan_amount=loan_amount,
          tenure=tenure,
          borrower_customer_id=user_id,
          interest_rate = interest_rate,
          total_repayment_amount = total_repayment_amount,
          loan_id = loan_id,
          membership_type = membership_type,
          credit_limit=int(credit_limit),
          borrower_full_name = borrower_full_name,
          borrower_email_id = borrower_email_id,
          loan_updated_status = "under process",
          borrower_loan_created_timestamp=loan_created_timestamp,
          product_id = product_id,
          product_name = product_name,
          emi_payment_type = emi_payment_type,
          total_processing_fee_amount = processing_fee_amount,
          total_interest_amount = total_interest,
          product_description = product_description,
          monthly_emi = emi
          # beseem_score= find_beseem_points_based_on_id(user_id)
         )

        # Return the generated loan ID to the client
        return loan_id
    else:
        # Handle the case where no user profile is found
        return "User profile not found"


def generate_loan_id():
    # Query the latest loan ID from the data table
    latest_loan = app_tables.fin_loan_details.search(tables.order_by("loan_id", ascending=False))

    if latest_loan and len(latest_loan) > 0:
        # If there are existing loans, increment the last loan ID
        last_loan_id = latest_loan[0]['loan_id']
        counter = int(last_loan_id[2:]) + 1
    else:
        # If there are no existing loans, start the counter at 100001
        counter = 1000001

    # Return the new loan ID
    return f"LA{counter}"


@anvil.server.callable
def add_fin_emi_details(borrower_customer_id, borrower_email, scheduled_payment,
                     payment_number, payment_date, loan_id, emi_status):
    # Generate a unique loan ID and get the updated counter
    emi_id = generate_emi_id()
    loan_details = app_tables.fin_loan_details.search(borrower_customer_id = borrower_customer_i)
                       
    if loan_details and len(loan_details) > 0:
        loan_details = loan_details[0]
        loan_id = loan_details['loan_id']
    
        # Add details to fin_emi_table
        app_tables.fin_emi_table.add_row(
            emi_id=emi_id,
            borrower_customer_id=borrower_customer_id,  # Fix: use borrower_customer_id instead of user_id
            borrower_email=borrower_email,
            scheduled_payment=scheduled_payment,
            payment_number=payment_number,
            payment_date=payment_date,
            loan_id=loan_id,
            emi_status=emi_status
        )
        return emi_id
    else:
      return 'loan details not found'
      

def generate_emi_id():
    # Query the latest EMI ID from the data table
    latest_emi = app_tables.fin_emi_table.search(tables.order_by("emi_id", ascending=False))

    if latest_emi and len(latest_emi) > 0:
        # If there are existing EMIs, increment the last EMI ID
        last_emi_id = latest_emi[0]['emi_id']
        counter = int(last_emi_id[3:]) + 1
    else:
        # If there are no existing EMIs, start the counter at 1000
        counter = 1000

    # Return the new EMI ID
    return f"EMI{counter}"

# def find_user_and_add_bessem_value(user_id):
#   users = app_tables.fin_beseem_score.search(borrower_customer_id=user_id)
#   if users:
#     users[0]['total_point']=bessemfunctions.final_points_update_bessem_table(user_id)
#     users[0]['user_type'] = 'borrower'

# def find_beseem_points_based_on_id(user_id):
#   users = app_tables.fin_beseem_score.search(borrower_customer_id=user_id)
#   if users:
#     total_points = users[0]['total_point']
#     return total_points

# bessem code

def final_points_update_bessem_table(user_id):
    user_points = get_user_points(user_id)
    group_points = get_group_points()

    print(f"Debug: user_points={user_points}, group_points={group_points}")

    if user_points is not None and group_points is not None and group_points != 0:
        points = (user_points / group_points) * 100

        final_points = '{:.2f}'.format(points)

        return final_points
    return None

def get_user_points(id):
    users = app_tables.fin_user_profile.search(customer_id=id)
    if users:
        user = users[0]
        gender = user['gender'].lower() 
        qualification = user['qualification'].lower()  
        marital_status = user['marital_status'].lower()  
        profession = user['profession'].lower()
        user_age = user['user_age']
        organization_type = user['organization_type'].lower()
        present_address = user['present_address'].lower()
        duration_at_address = str(user['duration_at_address']).lower()
        self_employment = user['self_employment'].lower()
        age_of_business = user['business_age']
        salary_type = user['salary_type'].lower()
        # home_loan = user['home_loan'].lower()
        # other_loan = user['other_loan'].lower()
        # credit_card_loan = user['credit_card_loans'].lower()
        # vehicle_loan = user['vehicle_loan'].lower()
        
        loan_columns = ['home_loan', 'other_loan', 'credit_card_loans', 'vehicle_loan']
        
        # Initialize user points
        user_points = 0

        # Find the age range for the user_age
        user_age_range = None
        if 18 <= user_age <= 24:
          user_age_range = '18-24'
        elif 25 <= user_age <= 30:
          user_age_range = '25-30'
        elif 31 <= user_age <= 36:
          user_age_range = '31-36'
        elif 37 <= user_age <= 40:
          user_age_range = '37-40'
        elif 41 <= user_age <= 50:
          user_age_range = '41-50'
        else:
          user_age_range = '51'

        
      
        gender_search = app_tables.fin_admin_beseem_categories.search(group_name='gender', sub_category=gender)
        if gender_search:
            gender_points = gender_search[0]['min_points']
            print("Gender Points:", gender_points)
            user_points += gender_points

        present_address_search = app_tables.fin_admin_beseem_categories.search(group_name='present_address', sub_category=present_address.lower())
        if present_address_search:
            present_address_points = present_address_search[0]['min_points']
            print("Present address Points:", present_address_points)
            user_points += present_address_points

        duration_at_address_search = app_tables.fin_admin_beseem_categories.search(group_name='duration_at_address', sub_category=duration_at_address.lower())
        if duration_at_address_search:
           duration_at_address_points = duration_at_address_search[0]['min_points']
           print("Duration at address Points:", duration_at_address_points)
           user_points += duration_at_address_points

        qualification_search = app_tables.fin_admin_beseem_categories.search(group_name='qualification', sub_category=qualification.lower())
        if qualification_search:
            qualification_points = qualification_search[0]['min_points']
            print("Qualification Points:", qualification_points)
            user_points += qualification_points

        profession_search = app_tables.fin_admin_beseem_categories.search(group_name='profession', sub_category=profession.lower())
        if profession_search:
            profession_points = profession_search[0]['min_points']
            print("Profession Points:", profession_points)
            user_points += profession_points

            if profession == 'self employment':
              self_employment_search = app_tables.fin_admin_beseem_categories.search(group_name='profession', sub_category= self_employment.lower())
              if self_employment_search:
                self_employment_points = self_employment_search[0]['min_points']
                print("self employment Points:", self_employment_points)
                user_points += self_employment_points
                
            elif profession == 'employee':
                organization_type_search = app_tables.fin_admin_beseem_categories.search(group_name='organization_type', sub_category=organization_type.lower())
                if organization_type_search:
                    organization_type_points = organization_type_search[0]['min_points']
                    print("Organization type Points:", organization_type_points)
                    user_points += organization_type_points
                salary_type_search = app_tables.fin_admin_beseem_categories.search(group_name='salary_type',sub_category=salary_type.lower())
                if salary_type_search:
                  salary_type_points = salary_type_search[0]['min_points']
                  print("Salary type Points:", salary_type_points)

            elif profession == 'business':
                business_age_search = app_tables.fin_admin_beseem_categories.search(group_name='age_of_business', sub_category=age_of_business.lower())
                if business_age_search:
                    business_age_points = business_age_search
                    print("Business Age Points:", business_age_points)
                    user_points += business_age_points
                  
        marital_status_search = app_tables.fin_admin_beseem_categories.search(group_name='marital_status', sub_category=marital_status.lower(), age=user_age_range)
        if marital_status_search:
           marital_status_points = marital_status_search[0]['min_points']
           print("Marital status Points:", marital_status_points)
           user_points += marital_status_points
    
           data = app_tables.fin_guarantor_details.search(customer_id=id)
           if data:
              for item in data:
               another_person = item['another_person'].lower()
               spouse_profession = item['guarantor_profession'].lower()

               if marital_status == 'married' and another_person == 'spouse':
                 spouse_profession_search = app_tables.fin_admin_beseem_categories.search(group_name='spouse_profession', sub_category=spouse_profession.lower())
                 if spouse_profession_search:
                    spouse_profession_points = spouse_profession_search[0]['min_points']
                    print("Spouse profession:", spouse_profession_points)
                    user_points += spouse_profession_points

        loan_points_total = 0
        for loan_column in loan_columns:
            loan_value = user[loan_column].lower()
            if loan_value in ['yes', 'no']: 
                loan_search = app_tables.fin_admin_beseem_categories.search(
                    (app_tables.fin_admin_beseem_categories.group_name == 'all_loans') &
                    (app_tables.fin_admin_beseem_categories.sub_category == loan_column.lower()) &
                    (app_tables.fin_admin_beseem_categories.is_liveloan == loan_value.lower())
                )
                if loan_search:
                    loan_points_total += loan_search[0]['min_points']

        user_points += loan_points_total

        # if home_loan:
        #     home_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='all_loans', sub_category=home_loan.lower())
        #     if home_loan_search and home_loan_search[0]['is_liveloan']:
        #         home_loan_points = home_loan_search[0]['min_points']
        #         user_points += home_loan_points

        # if other_loan:
        #     other_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='all_loans', sub_category=other_loan.lower())
        #     if other_loan_search and other_loan_search[0]['is_liveloan']:
        #         other_loan_points = other_loan_search[0]['min_points']
        #         user_points += other_loan_points

        # if credit_card_loan:
        #     credit_card_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='all_loans', sub_category=credit_card_loan.lower())
        #     if credit_card_loan_search and credit_card_loan_search[0]['is_liveloan']:
        #         credit_card_loan_points = credit_card_loan_search[0]['min_points']
        #         user_points += credit_card_loan_points

        # if vehicle_loan:
        #     vehicle_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='all_loans', sub_category=vehicle_loan.lower())
        #     if vehicle_loan_search and vehicle_loan_search[0]['is_liveloan']:
        #         vehicle_loan_points = vehicle_loan_search[0]['min_points']
        #         user_points += vehicle_loan_points

        # home_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='all_loans', sub_category=home_loan.lower())
        # if home_loan_search:
        #     home_loan_points = home_loan_search[0]['min_points']
        #     print("Home loan Points:", home_loan_points)
        #     user_points += home_loan_points

        # other_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='all_loans', sub_category=other_loan.lower())
        # if other_loan_search:
        #     other_loan_points = other_loan_search[0]['min_points']
        #     print("Other loan Points:", other_loan_points)
        #     user_points += other_loan_points

        # live_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='all_loans', sub_category=live_loan.lower())
        # if live_loan_search:
        #     live_loan_points = live_loan_search[0]['min_points']
        #     print("Live loan Points:", live_loan_points)
        #     user_points += live_loan_points

        # credit_card_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='all_loans', sub_category=credit_card_loan.lower())
        # if credit_card_loan_search:
        #     credit_card_loan_points = credit_card_loan_search[0]['min_points']
        #     print("Credit card loan Points:", credit_card_loan_points)
        #     user_points += credit_card_loan_points

        # vehicle_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='all_loans', sub_category=vehicle_loan.lower())
        # if vehicle_loan_search:
        #     vehicle_loan_points = vehicle_loan_search[0]['min_points']
        #     print("Vehicle Points:", vehicle_loan_points)
        #     user_points += vehicle_loan_points       

        return user_points
    else:
        return None

def get_group_points():
    groups = app_tables.fin_admin_beseem_groups.search()

    if groups:
        group_points = 0

        for group_row in groups:
            group_points += group_row['max_points']

        return group_points
    return None

      
# def get_user_points(id):
#     users = app_tables.fin_user_profile.search(customer_id=id)

#     if users:
#         user = users[0]
#         gender = user['gender'].lower()
#         qualification = user['qualification'].lower()
#         marrital_status = user['marital_status'].lower()
#         profession = user['profficen'].lower()
#         user_age = user['user_age']
        
#         print(f"Debug: gender={gender}, qualification={qualification}, marrital_status={marrital_status}, profession={profession}, age={age}")

#         def is_age_within_range(row):
#             if age is not None and row['age'] is not None:
#                 age_range = map(int, row['age'].split('-'))
#                 return age_range[0] <= int(age) <= age_range[1]
#             return True

#         def search_category(group_name, sub_category, age=None):
#             group_name = group_name.lower()
#             sub_category = sub_category.lower()
#             return [row for row in app_tables.fin_admin_beseem_categories.search(
#                 group_name=group_name, sub_category=sub_category, age=str(age).lower())
#                 if is_age_within_range(row)]

#         # Initialize user_points to 0
#         user_points = 0

#         gender_category_rows = search_category('gender', gender)
#         print(f"Debug: gender_category_rows={gender_category_rows}")
#         if gender_category_rows:
#             user_points += gender_category_rows[0]['min_points']

#         qualification_category_rows = search_category('qualification', qualification)
#         print(f"Debug: qualification_category_rows={qualification_category_rows}")
#         if qualification_category_rows:
#             user_points += qualification_category_rows[0]['min_points']

#         marital_status_category_rows = search_category('marrital_status', marrital_status, age)
#         print(f"Debug: marital_status_category_rows={marital_status_category_rows}")
#         for row in marital_status_category_rows:
#             user_points += row['min_points']

#         profession_category_rows = search_category('profession', profession)
#         print(f"Debug: profession_category_rows={profession_category_rows}")
#         if profession_category_rows:
#             user_points += profession_category_rows[0]['min_points']

#         # Return the total user_points
#         print(f"Debug: user_points={user_points}")
#         return user_points
#     return None

