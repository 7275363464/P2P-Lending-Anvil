from ._anvil_designer import forgot_passwordTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class forgot_password(forgot_passwordTemplate):
    def __init__(self, email, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.role = "no-scroll"
        self.text_box_1.text = email

        # Initially hide the text in password fields
        self.text_box_2.hide_text = True
        self.text_box_2_copy.hide_text = True

        # Set the initial icon (closed eye)
        self.eye_icon_1.source = '_/theme/eye_closed.png'
        self.eye_icon_2.source = '_/theme/eye_closed.png'

    def eye_icon_1_click(self, **event_args):
        """This method is called when the eye icon next to text_box_2 is clicked"""
        if self.text_box_2.hide_text:
            self.text_box_2.hide_text = False  # Show the password
            self.eye_icon_1.source = '_/theme/eye_open.png'  # Change to open eye icon
        else:
            self.text_box_2.hide_text = True  # Hide the password
            self.eye_icon_1.source = '_/theme/eye_closed.png'  # Change to closed eye icon

    def eye_icon_2_click(self, **event_args):
        """This method is called when the eye icon next to text_box_2_copy is clicked"""
        if self.text_box_2_copy.hide_text:
            self.text_box_2_copy.hide_text = False  # Show the password
            self.eye_icon_2.source = '_/theme/eye_open.png'  # Change to open eye icon
        else:
            self.text_box_2_copy.hide_text = True  # Hide the password
            self.eye_icon_2.source = '_/theme/eye_closed.png'  # Change to closed eye icon

    # def validate_password(self):
    #     password = self.text_box_2.text.strip()
    #     retype_password = self.text_box_2_copy.text.strip()

    #     error_messages = []

    #     # Validate password length
    #     if len(password) < 8:
    #         error_messages.append('Password must be at least 8 characters long.')

    #     # Validate matching passwords
    #     if password != retype_password:
    #         error_messages.append('Passwords do not match.')

    #     if error_messages:
    #         self.error_label.text = ' '.join(error_messages)
    #         self.error_label.foreground = 'red'
    #         self.error_label.visible = True
    #     else:
    #         self.error_label.visible = False

    def validate_password(self):
        password = self.text_box_2.text.strip()
        retype_password = self.text_box_2_copy.text.strip()
        # Clear previous error messages
        self.password_error_label.text = ''
        self.retype_password_error_label.text = ''
        self.password_error_label.visible = False
        self.retype_password_error_label.visible = False
        
        # Validate password
        if not password:
            self.password_error_label.text = "Password cannot be empty."
            self.password_error_label.visible = True
        elif len(password) < 8:
            self.password_error_label.text = "Password must be at least 8 characters long."
            self.password_error_label.visible = True
        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=-])[A-Za-z\d!@#$%^&*()_+=-]+$', password):
            self.password_error_label.text = "Password must include (a-z), (A-Z), (0-9), and (!@#$%^&*()_+=-)."
            self.password_error_label.visible = True
        else:
            self.password_error_label.text = ""
            self.password_error_label.visible = False
        
        # Validate matching passwords
        if password != retype_password:
            self.retype_password_error_label.text = 'Passwords do not match.'
            # self.retype_password_error_label.visible = True
        else:
            self.retype_password_error_label.text = ""
            self.retype_password_error_label.visible = False
    

  
    def text_box_2_change(self, **event_args):
        """This method is called when the text in text_box_2 changes"""
        
        self.error_label.visible = False
        self.error_label.visible = True
        self.password_error_label.visible = False
        self.validate_password()

    def text_box_2_copy_change(self, **event_args):
        """This method is called when the text in text_box_2_copy changes"""
        
        self.error_label.visible = False
        self.error_label.visible = False
        self.password_error_label.visible = True
        self.validate_password()

    def button_1_click(self, **event_args):
        password = self.text_box_2.text.strip()
        retype_password = self.text_box_2_copy.text.strip()
        email = self.text_box_1.text.strip()

        if password != retype_password:
            self.retype_password_error_label.text = 'Passwords do not match. Please re-enter.'
            self.retype_password_error_label.foreground = 'red'
            self.retype_password_error_label.visible = True
            return

        user = app_tables.users.get(email=email)
        if user:
            hashed_password = anvil.server.call('hash_password_2', password)
            user['password_hash'] = hashed_password
            self.retype_password_error_label.text = 'Password updated successfully.'
            self.retype_password_error_label.foreground = 'green'
            open_form('bank_users.main_form.signin_page')
        else:
            self.retype_password_error_label.text = 'User not found.'
            self.retype_password_error_label.foreground = 'red'
        
        self.retype_password_error_label.visible = True

    def send_otp_click(self, **event_args):
        email = self.text_box_1.text.strip()
        if not email:
            alert("Please fill the email")
            return

        self.otp = anvil.server.call('send_email_otp', email)
        if self.otp:
            alert(f"OTP has been sent to {email}")
            self.show_otp_input()
        else:
            self.error_label.text = 'Failed to send OTP. Please try again later.'
            self.error_label.foreground = 'red'
            self.error_label.visible = True

    def show_otp_input(self):
        self.text_box_otp.visible = True
        self.verify_otp_button.visible = True
        self.send_otp.text = "Resend"  # Change text of send_otp link
        self.send_otp.visible = True

    def verify_otp_button_click(self, **event_args):
        entered_otp = self.text_box_otp.text.strip()
        if str(self.otp) == entered_otp:
            self.error_label.text = 'OTP verified successfully'
            self.error_label.foreground = 'green'
            self.error_label.visible = True
            
            # Update email verified status in user table
            email = self.text_box_1.text.strip()
            anvil.server.call('update_user_status', email, email_verified=True)

            self.eye_icon_1.visible = True
            self.eye_icon_2.visible = True
            self.label_5.visible = True
            self.label_5_copy.visible = True
            self.text_box_2.visible = True
            self.text_box_2_copy.visible = True
            self.send_otp.visible = False
            self.text_box_otp.visible = False
            self.verify_otp_button.visible = False
            self.button_1.visible = True
        else:
            self.error_label.text = 'Invalid OTP. Please try again.'
            self.error_label.foreground = 'red'
            self.error_label.visible = True
            self.send_otp.visible = True

    def label_2_show(self, **event_args):
        """This method is called when the Label is shown on the screen"""
        self.text_box_2.hide_text = True






# from ._anvil_designer import forgot_passwordTemplate
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables


# class forgot_password(forgot_passwordTemplate):
#   def __init__(self, email, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)
#     self.role = "no-scroll"
#     self.text_box_1.text = email

#     # Initially hide the text in password fields
#     self.text_box_2.hide_text = True
#     self.text_box_2_copy.hide_text = True

#     # Set the initial icon (closed eye)
#     self.eye_icon_1.source = '_/theme/eye_closed.png'  # Adjust the path as necessary
#     self.eye_icon_2.source = '_/theme/eye_closed.png'  # Adjust the path as necessary

#   def button_1_click(self, **event_args):
#     password = self.text_box_2.text.strip()
#     retype_password = self.text_box_2_copy.text.strip()
#     email = self.text_box_1.text.strip()

#     if password != retype_password:
#       self.error_label.text = 'Passwords do not match. Please re-enter.'
#       self.error_label.foreground = 'red'
#       self.error_label.visible = True
#       return

#     user = app_tables.users.get(email=email)
#     if user:
#       hashed_password = anvil.server.call('hash_password_2', password)
#       user['password_hash'] = hashed_password
#       self.error_label.text = 'Password updated successfully.'
#       self.error_label.foreground = 'green'
#       open_form('bank_users.main_form.signin_page')
#     else:
#       self.error_label.text = 'User not found.'
#       self.error_label.foreground = 'red'
    
#     self.error_label.visible = True

#   # def check_box_1_change(self, **event_args):
#   #   self.password_visible = self.check_box_1.checked
#   #   if self.password_visible:
#   #     self.text_box_2.hide_text = False  # Show decrypted password
#   #     self.text_box_2_copy.hide_text = False
#   #   else:
#   #     self.text_box_2.hide_text = True
#   #     self.text_box_2_copy.hide_text = True

#   def send_otp_click(self, **event_args):
#     email = self.text_box_1.text.strip()
#     if not email:
#       alert("Please fill the email")
#       return

#     self.otp = anvil.server.call('send_email_otp', email)
#     if self.otp:
#       alert(f"OTP has been sent to {email}")
#       self.show_otp_input()
#     else:
#       self.error_label.text = 'Failed to send OTP. Please try again later.'
#       self.error_label.foreground = 'red'
#       self.error_label.visible = True

#   def show_otp_input(self):
#     self.text_box_otp.visible = True
#     self.verify_otp_button.visible = True
#     self.send_otp.text = "Resend"  # Change text of send_otp link
#     self.send_otp.visible = True

#   def verify_otp_button_click(self, **event_args):
#     entered_otp = self.text_box_otp.text.strip()
#     if str(self.otp) == entered_otp:
#       self.error_label.text = 'OTP verified successfully'
#       self.error_label.foreground = 'green'
#       self.error_label.visible = True
      
#       # Update email verified status in user table
#       email = self.text_box_1.text.strip()
#       anvil.server.call('update_user_status', email, email_verified=True)

#       self.eye_icon_1.visible = True
#       self.eye_icon_2.visible = True
#       self.label_5.visible = True
#       self.label_5_copy.visible = True
#       self.text_box_2.visible = True
#       self.text_box_2_copy.visible = True
#       # self.check_box_1.visible = True
#       self.send_otp.visible = False
#       self.text_box_otp.visible = False
#       self.verify_otp_button.visible = False
#       self.button_1.visible = True
#     else:
#       self.retype_password_error_label.text = 'Invalid OTP. Please try again.'
#       self.retype_password_error_label.foreground = 'red'
#       self.retype_password_error_label.visible = True
#       self.send_otp.visible = True

#   def label_2_show(self, **event_args):
#     """This method is called when the Label is shown on the screen"""
#     self.text_box_2.hide_text = True

#   def eye_icon_1_click(self, **event_args):
#     """This method is called when the eye icon next to text_box_2 is clicked"""
#     if self.text_box_2.hide_text:
#       self.text_box_2.hide_text = False  # Show the password
#       self.eye_icon_1.source = '_/theme/eye_open.png'  # Change to open eye icon
#     else:
#       self.text_box_2.hide_text = True  # Hide the password
#       self.eye_icon_1.source = '_/theme/eye_closed.png'  # Change to closed eye icon

#   def eye_icon_2_click(self, **event_args):
#     """This method is called when the eye icon next to text_box_2_copy is clicked"""
#     if self.text_box_2_copy.hide_text:
#       self.text_box_2_copy.hide_text = False  # Show the password
#       self.eye_icon_2.source = '_/theme/eye_open.png'  # Change to open eye icon
#     else:
#       self.text_box_2_copy.hide_text = True  # Hide the password
#       self.eye_icon_2.source = '_/theme/eye_closed.png'  # Change to closed eye icon

