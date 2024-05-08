from ._anvil_designer import lender_registration_form_3_marital_marriedTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re
from datetime import datetime, timedelta

class lender_registration_form_3_marital_married(lender_registration_form_3_marital_marriedTemplate):
    selected_radio_button = None
    def __init__(self, user_id,marital_status, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.userId = user_id

        self.marital_status = marital_status

        # Set the visibility of the spouse controls based on the marital status
        if marital_status == 'Married':
            self.show_spouse_controls()
            self.button_1.visible = True
        else:
            self.hide_spouse_controls()
            self.button_1_3.visible = False
            self.button_1.visible = True

        options = app_tables.fin_lender_spouse_profession.search()
        option_strings = [str(option['spouse_profession']) for option in options]
        self.drop_down_1.items = option_strings

        user_data=app_tables.fin_guarantor_details.get(customer_id=user_id)
        if user_data:
           self.selected_radio_button = user_data['another_person']
           self.father_name_text.text=user_data['guarantor_name']
           self.date_picker_1.date =user_data['guarantor_date_of_birth']
           self.father_mbl_no_text.text=user_data['guarantor_mobile_no']
           self.father_profession_text.text = user_data['guarantor_profession']
           self.father_address_text.text = user_data['guarantor_address']

           self.selected_radio_button = user_data['another_person']
           self.mother_name_text_copy.text=user_data['guarantor_name']
           self.date_picker_2.date =user_data['guarantor_date_of_birth']
           self.mother_mbl_no_text.text=user_data['guarantor_mobile_no']
           self.mother_profession_text.text = user_data['guarantor_profession']
           self.mother_address_text.text = user_data['guarantor_address']

           self.selected_radio_button = user_data['another_person']
           self.spouse_name_text.text=user_data['guarantor_name']
           self.date_picker_3.date =user_data['guarantor_marriage_date']
           self.spouse_mbl_no_text.text=user_data['guarantor_mobile_no']
           self.drop_down_1.selected_value = user_data['guarantor_profession']
           self.spouse_companyname_text.text = user_data['guarantor_company_name']
           self.annual_earning_text.text = user_data['guarantor_annual_earning']

           self.selected_radio_button = user_data['another_person']
           self.related_person_text.text = user_data['guarantor_person_relation']
           self.name_text_copy.text=user_data['guarantor_name']
           self.date_picker_3_copy.date =user_data['guarantor_date_of_birth']
           self.mbl_no_text_copy.text=user_data['guarantor_mobile_no']
           self.profession_text_copy.text = user_data['guarantor_profession']
 
        
    def show_spouse_controls(self):
        # Show the spouse radio button and related panels
        self.grid_panel_1.visible = False
        self.grid_panel_2.visible = False
        self.grid_panel_3.visible = False
        self.grid_panel_4.visible = False
        self.button_submit.visible = False
        self.button_submit_copy.visible = False
        self.button_submit_copy_2.visible = False
        self.button_submit_copy_3.visible = False
        self.prev_1.visible = False
        self.prev_2.visible = False
        self.prev_3.visible = False
        self.prev_4.visible = False
        self.button_1.visible = False

    def hide_spouse_controls(self):
        # Hide the spouse radio button and related panels
        self.grid_panel_1.visible = False
        self.grid_panel_2.visible = False
        self.grid_panel_3.visible = False
        self.grid_panel_4.visible = False
        self.button_submit.visible = False
        self.button_submit_copy.visible = False
        self.button_submit_copy_2.visible = False
        self.button_submit_copy_3.visible = False
        self.prev_1.visible = False
        self.prev_2.visible = False
        self.prev_3.visible = False
        self.prev_4.visible = False
        self.button_1.visible = False
    def is_married(self):
        # Check the marital status in the user profile table
        user_profile = app_tables.fin_user_profile.get(customer_id=self.userId)
        return user_profile['marital_status'] == 'Married'

    def button_1_click(self, **event_args):
        open_form('lendor_registration_form.lender_registration_form_3_marital_details',user_id=self.userId)

    def button_1_1_click(self, **event_args):
        """This method is called when this radio button is selected"""
        self.button_1_1.background = '#0a2346'
        self.button_1_2.background = '#939191'
        self.button_1_3.background = '#939191'
        self.button_1_4.background = '#939191'
        self.grid_panel_1.visible = True
        self.grid_panel_2.visible = False
        self.grid_panel_3.visible = False
        self.grid_panel_4.visible = False
        self.button_submit.visible = True
        self.button_submit_copy.visible = False
        self.button_submit_copy_2.visible = False
        self.button_submit_copy_3.visible = False
        self.selected_radio_button = "father"
        self.prev_1.visible = True
        self.prev_2.visible = False
        self.prev_3.visible = False
        self.prev_4.visible = False
        self.button_1.visible = False

    def button_1_2_click(self, **event_args):
        """This method is called when this radio button is selected"""
        self.button_1_1.background = '#939191'
        self.button_1_2.background = '#0a2346'
        self.button_1_3.background = '#939191'
        self.button_1_4.background = '#939191'
        self.grid_panel_1.visible = False
        self.grid_panel_2.visible = True
        self.grid_panel_3.visible = False
        self.grid_panel_4.visible = False
        self.button_submit.visible = False
        self.button_submit_copy.visible = True
        self.button_submit_copy_2.visible = False
        self.button_submit_copy_3.visible = False
        self.selected_radio_button = "mother"
        self.prev_1.visible = False
        self.prev_2.visible = True
        self.prev_3.visible = False
        self.prev_4.visible = False
        self.button_1.visible = False

    def button_1_3_click(self, **event_args):
        self.button_1_1.background = '#939191'
        self.button_1_2.background = '#939191'
        self.button_1_3.background = '#0a2346'
        self.button_1_4.background = '#939191'
        self.grid_panel_1.visible = False
        self.grid_panel_2.visible = False
        self.grid_panel_3.visible = True
        self.grid_panel_4.visible = False
        self.button_submit.visible = False
        self.button_submit_copy.visible = False
        self.button_submit_copy_2.visible = True
        self.button_submit_copy_3.visible = False
        self.selected_radio_button = "spouse"
        self.prev_1.visible = False
        self.prev_2.visible = False
        self.prev_3.visible = True
        self.prev_4.visible = False
        self.button_1.visible = False

    def button_1_4_click(self, **event_args):
        """This method is called when this radio button is selected"""
        self.button_1_1.background = '#939191'
        self.button_1_2.background = '#939191'
        self.button_1_3.background = '#939191'
        self.button_1_4.background = '#0a2346'
        self.grid_panel_1.visible = False
        self.grid_panel_2.visible = False
        self.grid_panel_3.visible = False
        self.grid_panel_4.visible = True
        self.button_submit.visible = False
        self.button_submit_copy.visible = False
        self.button_submit_copy_2.visible = False
        self.button_submit_copy_3.visible = True
        self.selected_radio_button = "others"
        self.prev_1.visible = False
        self.prev_2.visible = False
        self.prev_3.visible = False
        self.prev_4.visible = True
        self.button_1.visible = False
        

    def collect_details(self):
        # Collect details from the form
        father_name = self.father_name_text.text
        father_dob = self.date_picker_1.date
        father_mbl_no_text = self.father_mbl_no_text.text
        father_mbl_no = int(father_mbl_no_text) if father_mbl_no_text.strip().isdigit() else None
        father_profession = self.father_profession_text.text
        father_address = self.father_address_text.text

        # Mother details
        mother_name = self.mother_name_text_copy.text
        mother_dob = self.date_picker_2.date
        mother_mbl_no_text = self.mother_mbl_no_text.text
        mother_mbl_no = int(mother_mbl_no_text) if mother_mbl_no_text.strip().isdigit() else None
        mother_profession = self.mother_profession_text.text
        mother_address = self.mother_address_text.text

        # Spouse details
        spouse_name = self.spouse_name_text.text
        spouse_mob = self.date_picker_3.date
        spouse_mbl_no_text = self.spouse_mbl_no_text.text
        spouse_mbl_no = int(spouse_mbl_no_text) if spouse_mbl_no_text.strip().isdigit() else None
        spouse_profession = self.drop_down_1.selected_value
        spouse_company = self.spouse_companyname_text.text
        anual_earning = self.annual_earning_text.text

        # Related person details
        person_relation = self.related_person_text.text
        related_dob = self.date_picker_3_copy.date
        related_name = self.name_text_copy.text
        related_mob_text = self.mbl_no_text_copy.text
        related_mob = int(related_mob_text) if related_mob_text.strip().isdigit() else None
        related_profession = self.profession_text_copy.text

        return {
            'father_name': father_name,
            'father_dob': father_dob,
            'father_mbl_no': father_mbl_no,
            'father_profession': father_profession,
            'father_address': father_address,

            'mother_name': mother_name,
            'mother_dob': mother_dob,
            'mother_mbl_no': mother_mbl_no,
            'mother_profession': mother_profession,
            'mother_address': mother_address,

            'spouse_name': spouse_name,
            'spouse_mob': spouse_mob,
            'spouse_mbl_no': spouse_mbl_no,
            'spouse_profession': spouse_profession,
            'spouse_company': spouse_company,
            'annual_earning': anual_earning,

            'related_person_relation': person_relation,
            'related_person_dob': related_dob,
            'related_person_name': related_name,
            'related_person_mob': related_mob,
            'related_person_profession': related_profession,
            'another_person': self.selected_radio_button  
        }

    def button_submit_click(self, **event_args):
     details = self.collect_details()
     if details:
        # Extracting details from the form
        father_name = details.get('father_name', '')
        father_dob = details.get('father_dob', '')
        father_mbl_no = details.get('father_mbl_no', '')
        father_profession = details.get('father_profession', '')
        father_address = details.get('father_address', '')
        another_person = details.get('another_person', '')

        # Checking if the user already has data in the table
        existing_row = app_tables.fin_guarantor_details.get(customer_id=self.userId)

        try:
            # If there's no existing data, add a new row
            if existing_row is None:
                new_row = app_tables.fin_guarantor_details.add_row(
                    customer_id=self.userId,
                    guarantor_name=father_name,
                    guarantor_date_of_birth=father_dob,
                    guarantor_mobile_no=father_mbl_no,
                    guarantor_profession=father_profession,
                    guarantor_address=father_address,
                    another_person=another_person
                )
            else:
                # If there's existing data, update it
                existing_row.update(
                    guarantor_name=father_name,
                    guarantor_date_of_birth=father_dob,
                    guarantor_mobile_no=father_mbl_no,
                    guarantor_profession=father_profession,
                    guarantor_address=father_address,
                    another_person=another_person
                )
        except Exception as e:
            Notification(f"Failed to submit form: {e}").show()
            return

        # Validations...
        errors = []
        if not re.match(r'^[A-Za-z\s]+$', father_name):
            errors.append("Enter a valid full name!")
        if not father_dob or father_dob > datetime.now().date():
            errors.append("Enter a valid date of birth!")
        if (datetime.now().date() - father_dob).days < 365 * 18:
            errors.append("You must be at least 18 years old!")
        if not re.match(r'^\d{10}$', str(father_mbl_no)):
            errors.append("Enter a valid mobile no!")

        if errors:
            Notification("\n".join(errors)).show()
        else:
            anvil.server.call('add_lendor_father_details', 
                              another_person, father_name, father_dob, 
                              father_mbl_no, father_profession, 
                              father_address, self.userId)
            open_form('lendor_registration_form.lender_registration_form_4_bank_form_1', 
                      user_id=self.userId)

    def button_submit_copy_click(self, **event_args):
     details = self.collect_details()
     if details:
        mother_name = details.get('mother_name', '')
        mother_dob = details.get('mother_dob', '')
        mother_mbl_no = details.get('mother_mbl_no', '')
        mother_profession = details.get('mother_profession', '')
        mother_address = details.get('mother_address', '')
        another_person = details.get('another_person', '')
    
     existing_row = app_tables.fin_guarantor_details.get(customer_id=self.userId)
    
     if existing_row is None:
        try:
            new_row = app_tables.fin_guarantor_details.add_row(
                customer_id=self.userId,
                guarantor_name=details.get('mother_name', ''),
                guarantor_date_of_birth=details.get('mother_dob', ''),
                guarantor_mobile_no=details.get('mother_mbl_no', ''),
                guarantor_profession=details.get('mother_profession', ''),
                guarantor_address=details.get('mother_address', ''),
                another_person=details.get('another_person', '')
            )
        except Exception as e:
            Notification(f"Failed to submit form: {e}").show()
            return
     else:
        existing_row['guarantor_name'] = details.get('mother_name', '')
        existing_row['guarantor_date_of_birth'] = details.get('mother_dob', '')
        existing_row['guarantor_mobile_no'] = details.get('mother_mbl_no', '')
        existing_row['guarantor_profession'] = details.get('mother_profession', '')
        existing_row['guarantor_address'] = details.get('mother_address', '')
        existing_row['another_person'] = details.get('another_person', '')
        
        try:
            existing_row.update()
        except Exception as e:
            Notification(f"Failed to update form: {e}").show()
            return
    
     # Validations...
     errors = []
     if not re.match(r'^[A-Za-z\s]+$', details.get('mother_name', '')):
        errors.append("Enter a valid full name!")
     if not details.get('mother_dob', '') or details.get('mother_dob', '') > datetime.now().date():
        errors.append("Enter a valid date of birth!")
     if (datetime.now().date() - details.get('mother_dob', '')).days < 365 * 18:
        errors.append("You must be at least 18 years old!")
     if not re.match(r'^\d{10}$', str(details.get('mother_mbl_no', ''))):
        errors.append("Enter a valid mobile no!")

     if errors:
        Notification("\n".join(errors)).show()
     else:
        anvil.server.call('add_lendor_mother_details', 
                              another_person, mother_name, mother_dob, 
                              mother_mbl_no, mother_profession, 
                              mother_address, self.userId)
        open_form('lendor_registration_form.lender_registration_form_4_bank_form_1', user_id=self.userId)

    def button_submit_copy_2_click(self, **event_args):
     details = self.collect_details()
     if details:
        spouse_name = details.get('spouse_name', '')
        spouse_mob = details.get('spouse_mob', '')
        spouse_mbl_no = details.get('spouse_mbl_no', '')
        spouse_profession = details.get('spouse_profession', '')
        spouse_company = details.get('spouse_company', '')
        annual_earning = details.get('annual_earning', '')
        another_person = details.get('another_person', '')
       
     existing_row = app_tables.fin_guarantor_details.get(customer_id=self.userId)
    
     if existing_row is None:
        try:
            new_row = app_tables.fin_guarantor_details.add_row(
                customer_id=self.userId,
                guarantor_name=details.get('spouse_name', ''),
                guarantor_marriage_date=details.get('spouse_mob', ''),
                guarantor_mobile_no=details.get('spouse_mbl_no', ''),
                guarantor_profession=details.get('spouse_profession', ''),
                guarantor_company_name=details.get('spouse_company', ''),
                guarantor_annual_earning=details.get('annual_earning', ''),
                another_person=details.get('another_person', '')
            )
        except Exception as e:
            Notification(f"Failed to submit form: {e}").show()
            return
     else:
        existing_row['guarantor_name'] = details.get('spouse_name', '')
        existing_row['guarantor_marriage_date'] = details.get('spouse_mob', '')
        existing_row['guarantor_mobile_no'] = details.get('spouse_mbl_no', '')
        existing_row['guarantor_profession'] = details.get('spouse_profession', '')
        existing_row['guarantor_company_name'] = details.get('spouse_company', '')
        existing_row['guarantor_annual_earning'] = details.get('annual_earning', '')
        existing_row['another_person'] = details.get('another_person', '')
        
        try:
            existing_row.update()
        except Exception as e:
            Notification(f"Failed to update form: {e}").show()
            return
    
     # Validations...
     errors = []
     if not re.match(r'^[A-Za-z\s]+$', details.get('spouse_name', '')):
        errors.append("Enter a valid full name!")
     if details.get('spouse_mob', '') > datetime.now().date():
        errors.append("Enter a valid date of marriage!")
     if not re.match(r'^\d{10}$', str(details.get('spouse_mbl_no', ''))):
        errors.append("Enter a valid mobile no!")

     if errors:
        Notification("\n".join(errors)).show()
     else:
         anvil.server.call('add_lendor_spouse_details', 
                              another_person, spouse_name, spouse_mob, 
                              spouse_mbl_no, spouse_profession, 
                              spouse_company, annual_earning, self.userId)
         open_form('lendor_registration_form.lender_registration_form_4_bank_form_1', user_id=self.userId)

    def button_submit_copy_3_click(self, **event_args):
     details = self.collect_details()
     if details:
        related_person_name = details.get('related_person_name', '')
        related_person_dob = details.get('related_person_dob', '')
        related_person_mob = details.get('related_person_mob', '')
        related_person_profession = details.get('related_person_profession', '')
        related_person_relation = details.get('related_person_relation', '')
        another_person = details.get('another_person', '')
    
     existing_row = app_tables.fin_guarantor_details.get(customer_id=self.userId)
    
     if existing_row is None:
        try:
            new_row = app_tables.fin_guarantor_details.add_row(
                customer_id=self.userId,
                guarantor_name=details.get('related_person_name', ''),
                guarantor_date_of_birth=details.get('related_person_dob', ''),
                guarantor_mobile_no=details.get('related_person_mob', ''),
                guarantor_profession=details.get('related_person_profession', ''),
                guarantor_person_relation=details.get('related_person_relation', ''),
                another_person=details.get('another_person', '')
            )
        except Exception as e:
            Notification(f"Failed to submit form: {e}").show()
            return
     else:
        existing_row['guarantor_name'] = details.get('related_person_name', '')
        existing_row['guarantor_date_of_birth'] = details.get('related_person_dob', '')
        existing_row['guarantor_mobile_no'] = details.get('related_person_mob', '')
        existing_row['guarantor_profession'] = details.get('related_person_profession', '')
        existing_row['guarantor_person_relation'] = details.get('related_person_relation', '')
        existing_row['another_person'] = details.get('another_person', '')
        
        try:
            existing_row.update()
        except Exception as e:
            Notification(f"Failed to update form: {e}").show()
            return
    
     # Validations...
     errors = []
     if not re.match(r'^[A-Za-z\s]+$', details.get('related_person_name', '')):
        errors.append("Enter a valid full name!")
     if not details.get('related_person_dob', '') or details.get('related_person_dob', '') > datetime.now().date():
        errors.append("Enter a valid date of birth!")
     if (datetime.now().date() - details.get('related_person_dob', '')).days < 365 * 18:
        errors.append("You must be at least 18 years old!")
     if not re.match(r'^\d{10}$', str(details.get('related_person_mob', ''))):
        errors.append("Enter a valid mobile no!")

     if errors:
        Notification("\n".join(errors)).show()
     else:
       another_person, related_person_name, related_person_dob, related_person_mob, related_person_profession, related_person_relation,user_id
       anvil.server.call('add_lendor_spouse_details', 
                              another_person, related_person_name, related_person_dob, 
                              related_person_mob, related_person_profession, 
                              related_person_relation, self.userId) 
       open_form('lendor_registration_form.lender_registration_form_4_bank_form_1', user_id=self.userId)

     
    # def button_submit_click(self, **event_args):
    
    #    existing_row = app_tables.fin_guarantor_details.get(customer_id=self.userId)
    
    #    if existing_row is None:
    #       try:
    #          new_row = app_tables.fin_guarantor_details.add_row(
    #             customer_id=self.userId,
    #             guarantor_name=details['father_name'],
    #             guarantor_date_of_birth=details['father_dob'],
    #             guarantor_mobile_no=details['father_mbl_no'],
    #             guarantor_profession=details['father_profession'],
    #             guarantor_address=details['father_address'],
    #             another_person=details['another_person']
    #         )
    #       except Exception as e:
    #          Notification(f"Failed to submit form: {e}").show()
    #          return
    #    else:
    #      existing_row['guarantor_name'] = details['father_name']
    #      existing_row['guarantor_date_of_birth'] = details['father_dob']
    #      existing_row['guarantor_mobile_no'] = details['father_mbl_no']
    #      existing_row['guarantor_profession'] = details['father_profession']
    #      existing_row['guarantor_address'] = details['father_address']
    #      existing_row['another_person'] = details['another_person']
        
    #      try:
    #          existing_row.update()
    #      except Exception as e:
    #          Notification(f"Failed to update form: {e}").show()
    #          return
    
    #    # Validations...
    #    errors = []
    #    if not re.match(r'^[A-Za-z\s]+$', details['father_name']):
    #      errors.append("Enter a valid full name!")
    #    if not details['father_dob'] or details['father_dob'] > datetime.now().date():
    #      errors.append("Enter a valid date of birth!")
    #    if datetime.now().date() - details['father_dob'] < timedelta(days=365 * 18):
    #      errors.append("You must be at least 18 years old!")
    #    if not re.match(r'^\d{10}$', str(details['father_mbl_no'])):
    #      errors.append("Enter a valid mobile no!")

    #    if errors:
    #      Notification("\n".join(errors)).show()
    #    else:
    #      anvil.server.call('add_lendor_father_details',another_person,father_name,father_dob,father_mbl_no,father_profession,father_address,user_id)
    #      open_form('lendor_registration_form.lender_registration_form_4_bank_form_1', user_id=self.userId)

    # def button_submit_copy_click(self, **event_args):
    #    details = self.collect_details()
    
    #    existing_row = app_tables.fin_guarantor_details.get(customer_id=self.userId)
    
    #    if existing_row is None:
    #       try:
    #          new_row = app_tables.fin_guarantor_details.add_row(
    #             customer_id=self.userId,
    #             guarantor_name=details['mother_name'],
    #             guarantor_date_of_birth=details['mother_dob'],
    #             guarantor_mobile_no=details['mother_mbl_no'],
    #             guarantor_profession=details['mother_profession'],
    #             guarantor_address=details['mother_address'],
    #             another_person=details['another_person']
    #         )
    #       except Exception as e:
    #          Notification(f"Failed to submit form: {e}").show()
    #          return
    #    else:
    #      existing_row['guarantor_name'] = details['mother_name']
    #      existing_row['guarantor_date_of_birth'] = details['mother_dob']
    #      existing_row['guarantor_mobile_no'] = details['mother_mbl_no']
    #      existing_row['guarantor_profession'] = details['mother_profession']
    #      existing_row['guarantor_address'] = details['mother_address']
    #      existing_row['another_person'] = details['another_person']
        
    #      try:
    #          existing_row.update()
    #      except Exception as e:
    #          Notification(f"Failed to update form: {e}").show()
    #          return
    
    #    # Validations...
    #    errors = []
    #    if not re.match(r'^[A-Za-z\s]+$', details['mother_name']):
    #      errors.append("Enter a valid full name!")
    #    if not details['mother_dob'] or details['mother_dob'] > datetime.now().date():
    #      errors.append("Enter a valid date of birth!")
    #    if datetime.now().date() - details['mother_dob'] < timedelta(days=365 * 18):
    #      errors.append("You must be at least 18 years old!")
    #    if not re.match(r'^\d{10}$', str(details['mother_mbl_no'])):
    #      errors.append("Enter a valid mobile no!")

    #    if errors:
    #      Notification("\n".join(errors)).show()
    #    else:
         
    #      open_form('lendor_registration_form.lender_registration_form_4_bank_form_1', user_id=self.userId)

    # def button_submit_copy_2_click(self, **event_args):
    #    details = self.collect_details()
    
    #    existing_row = app_tables.fin_guarantor_details.get(customer_id=self.userId)
    
    #    if existing_row is None:
    #       try:
    #          new_row = app_tables.fin_guarantor_details.add_row(
    #             customer_id=self.userId,
    #             guarantor_name=details['spouse_name'],
    #             guarantor_marriage_date=details['spouse_mob'],
    #             guarantor_mobile_no=details['spouse_mbl_no'],
    #             guarantor_profession=details['spouse_profession'],
    #             guarantor_company_name=details['spouse_company'],
    #             guarantor_annual_earning=details['annual_earning'],
    #             another_person=details['another_person']
    #         )
    #       except Exception as e:
    #          Notification(f"Failed to submit form: {e}").show()
    #          return
    #    else:
    #      existing_row['guarantor_name'] = details['spouse_name']
    #      existing_row['guarantor_marriage_date'] = details['spouse_mob']
    #      existing_row['guarantor_mobile_no'] = details['spouse_mbl_no']
    #      existing_row['guarantor_profession'] = details['spouse_profession']
    #      existing_row['guarantor_company_name'] = details['spouse_company']
    #      existing_row['guarantor_annual_earning'] = details['annual_earning']
    #      existing_row['another_person'] = details['another_person']
        
    #      try:
    #          existing_row.update()
    #      except Exception as e:
    #          Notification(f"Failed to update form: {e}").show()
    #          return
    
    #    # Validations...
    #    errors = []
    #    if not re.match(r'^[A-Za-z\s]+$', details['spouse_name']):
    #      errors.append("Enter a valid full name!")
    #    if details['spouse_mob'] > datetime.now().date():
    #      errors.append("Enter a valid date of marriage!")
    #    if not re.match(r'^\d{10}$', str(details['spouse_mbl_no'])):
    #      errors.append("Enter a valid mobile no!")

    #    if errors:
    #      Notification("\n".join(errors)).show()
    #    else:
    #      open_form('lendor_registration_form.lender_registration_form_4_bank_form_1', user_id=self.userId)

    # def button_submit_copy_3_click(self, **event_args):
    #    details = self.collect_details()
    
    #    existing_row = app_tables.fin_guarantor_details.get(customer_id=self.userId)
    
    #    if existing_row is None:
    #       try:
    #          new_row = app_tables.fin_guarantor_details.add_row(
    #             customer_id=self.userId,
    #             guarantor_name=details['related_person_name'],
    #             guarantor_date_of_birth=details['related_person_dob'],
    #             guarantor_mobile_no=details['related_person_mob'],
    #             guarantor_profession=details['related_person_profession'],
    #             guarantor_person_relation= details['related_person_relation'],
    #             another_person=details['another_person']
    #         )
    #       except Exception as e:
    #          Notification(f"Failed to submit form: {e}").show()
    #          return
    #    else:
    #      existing_row['guarantor_name'] = details['related_person_name']
    #      existing_row['guarantor_date_of_birth'] = details['related_person_dob']
    #      existing_row['guarantor_mobile_no'] = details['related_person_mob']
    #      existing_row['guarantor_profession'] = details['related_person_profession']
    #      existing_row['guarantor_person_relation'] = details['related_person_relation']
    #      existing_row['another_person'] = details['another_person']
        
    #      try:
    #          existing_row.update()
    #      except Exception as e:
    #          Notification(f"Failed to update form: {e}").show()
    #          return
    
    #    # Validations...
    #    errors = []
    #    if not re.match(r'^[A-Za-z\s]+$', details['related_person_name']):
    #      errors.append("Enter a valid full name!")
    #    if not details['related_person_dob'] or details['related_person_dob'] > datetime.now().date():
    #      errors.append("Enter a valid date of birth!")
    #    if datetime.now().date() - details['related_person_dob'] < timedelta(days=365 * 18):
    #      errors.append("You must be at least 18 years old!")
    #    if not re.match(r'^\d{10}$', str(details['related_person_mob'])):
    #      errors.append("Enter a valid mobile no!")

    #    if errors:
    #      Notification("\n".join(errors)).show()
    #    else:
    #      open_form('lendor_registration_form.lender_registration_form_4_bank_form_1', user_id=self.userId)

    def prev_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor_registration_form.lender_registration_form_3_marital_details', user_id=self.userId)

    def prev_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor_registration_form.lender_registration_form_3_marital_details', user_id=self.userId)

    def prev_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor_registration_form.lender_registration_form_3_marital_details', user_id=self.userId)

    def prev_4_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor_registration_form.lender_registration_form_3_marital_details', user_id=self.userId)

 